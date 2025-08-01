from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from .models import Usuario, PessoaFisica, PessoaJuridica, Endereco, Funcionario, Cliente
from localflavor.br.forms import BRCPFField, BRCNPJField
from django.contrib.contenttypes.models import ContentType
from phonenumbers import NumberParseException, parse, is_valid_number, format_number, PhoneNumberFormat
from django.template.loader import render_to_string
from .email_sender import enviar_email
from django.utils.timezone import now as django_now
from django.contrib.auth.views import PasswordResetView


#=======Pesoa Física=======#
class UsuarioCreationForm(forms.ModelForm):
    
    # Recebe a senha 2x (Confirmação por parte do usuario.)
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    class Meta:
        #Importa o model Usuario para usar como base (email, nome, tel)
        model = Usuario
        fields = ('email', 'nome_completo', 'telefone','genero')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não coincidem")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Editar e visualizar o usuario no painel admin
class UsuarioChangeForm(forms.ModelForm):
    # Criptografia a senha para privacidade do usuário
    password = ReadOnlyPasswordHashField()

    # Retorna os dados
    class Meta:
        model = Usuario
        fields = ('email', 'password', 'nome_completo', 'telefone', 'genero', 'is_active', 'is_staff', 'tipo_usuario')
    # Preserva a integridade da senha
    def clean_password(self):
        return self.initial["password"]
    
# Formulário para criação de PF
class PessoaFisicaForm(UsuarioCreationForm):
    cpf = BRCPFField(label='CPF')
    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    nome_mae = forms.CharField(label='Nome da Mãe', required=True)

    class Meta(UsuarioCreationForm.Meta):
        model = PessoaFisica
        fields = UsuarioCreationForm.Meta.fields + ('cpf', 'data_nascimento', 'nome_mae')

# Formulário para criação de PJ
class PessoaJuridicaForm(UsuarioCreationForm):
    cnpj = BRCNPJField(label='CNPJ')
    razao_social = forms.CharField(label='Razão Social', max_length=150)
    nome_fantasia = forms.CharField(label='Nome Fantasia', max_length=150)
    inscricao_estadual = forms.CharField(label='Inscrição Estadual', max_length=20, required=False)

    class Meta(UsuarioCreationForm.Meta):
        model = PessoaJuridica
        fields = UsuarioCreationForm.Meta.fields + (
            'cnpj', 'razao_social', 'nome_fantasia', 'inscricao_estadual'
        )

# Formulário para inserir o email
class EnderecoForm(forms.ModelForm):
    principal = forms.BooleanField(
        required=False,
        label="Endereço principal",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    class Meta:
        model = Endereco
        fields = [
            'cep', 'logradouro', 'numero', 'complemento',
            'bairro', 'cidade', 'estado', 'principal'
        ]
        widgets = {
            'cep': forms.TextInput(attrs={'data-mask': '00000-000'}),
        }

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        principal = cleaned_data.get('principal')

        if principal and self.usuario:
            if Endereco.objects.filter(usuario=self.usuario, principal=True).exclude(pk=self.instance.pk).exists():
                self.add_error('principal', 'Já existe um endereço principal para este usuário.')
        return cleaned_data

    def save(self, commit=True):
        endereco = super().save(commit=False)
        if self.usuario:
            endereco.usuario = self.usuario
        if commit:
            endereco.save()
        return endereco

    

# Formulário para criação de funcionário(herda do PF)
class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['usuario', 'matricula', 'cargo', 'data_admissao', 'departamento']
        widgets = {
            'data_admissao': forms.DateInput(attrs={'type': 'date'}),
            'usuario': forms.Select(attrs={'class': 'form-control'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra apenas pessoas físicas não vinculadas a funcionários
        self.fields['usuario'].queryset = PessoaFisica.objects.filter(
            funcionario__isnull=True
        )

# Formulario para exibição de Clientes
class ClienteForm(forms.ModelForm):
    tipo = forms.ChoiceField(choices=Cliente.TIPO_CLIENTE)
    indicado_por = forms.ModelChoiceField(
        queryset=Cliente.objects.none(),
        required=False
    )

    class Meta:
        model = Cliente
        fields = ['tipo', 'indicado_por']
        exclude = ['usuario', 'content_type', 'object_id']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            
            self.instance.content_type = ContentType.objects.get_for_model(self.user)
            self.instance.object_id = self.user.id
        
        if self.instance.pk:
            self.fields['indicado_por'].queryset = Cliente.objects.exclude(pk=self.instance.pk)
        else:
            self.fields['indicado_por'].queryset = Cliente.objects.all()


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                # Busca o email do usuario no banco de dados (Tá no try, se der erro vai acusar)
                user = Usuario.objects.get(email=email)
                
                # Valida os hashs da password(criptografa a password que o usuario enviou e compara os hashs)
                if not check_password(password, user.password):
                    raise ValidationError("E-mail ou senha incorretos")
                
                # Se o status da conta estiver como False
                if not user.is_active:
                    raise ValidationError("Esta conta está inativa. Entre em contato com o suporte")
                cleaned_data['user'] = user
                
                # Qualquer erro que der irá dar raise no Email e senha incorreto
            except Usuario.DoesNotExist:
                raise ValidationError("E-mail ou senha incorretos")
        
        # Útil par utilizar o .is_valid() depois
        return cleaned_data
    
class PessoaFisicaEditForm(forms.ModelForm):
    data_nascimento = forms.DateField(input_formats=['%d/%m/%Y'])
    telefone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '(99) 99999-9999'})
    )

    class Meta:
        model = PessoaFisica
        fields = ['nome_completo', 'email', 'data_nascimento', 'telefone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        telefone_valor = None
        if 'telefone' in self.initial:
            telefone_valor = self.initial['telefone']
        elif self.instance and getattr(self.instance, 'telefone', None):
            telefone_valor = self.instance.telefone

        if telefone_valor:
            
            # Se já for PhoneNumber, converte para string
            if not isinstance(telefone_valor, str):
                telefone_valor = str(telefone_valor)
            try:
                phone_obj = parse(telefone_valor, 'BR')
                if is_valid_number(phone_obj):
                    self.initial['telefone'] = format_number(phone_obj, PhoneNumberFormat.NATIONAL)
            except NumberParseException:
                self.initial['telefone'] = telefone_valor



class PessoaJuridicaEditForm(forms.ModelForm):
    telefone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '(21) 99999-9999'}),
    )

    class Meta:
        model = PessoaJuridica
        fields = ['nome_completo', 'email', 'nome_fantasia', 'telefone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        telefone_valor = None
        if 'telefone' in self.initial:
            telefone_valor = self.initial['telefone']
        elif self.instance and getattr(self.instance, 'telefone', None):
            telefone_valor = self.instance.telefone

        if telefone_valor:
            # Se já for PhoneNumber, converte para string
            if not isinstance(telefone_valor, str):
                telefone_valor = str(telefone_valor)

            try:
                phone_obj = parse(telefone_valor, 'BR')
                if is_valid_number(phone_obj):
                    self.initial['telefone'] = format_number(phone_obj, PhoneNumberFormat.NATIONAL)
            except NumberParseException:
                self.initial['telefone'] = telefone_valor



class AlterarSenhaForm(forms.Form):
    nova_senha = forms.CharField(
        label="Nova senha",
        widget=forms.PasswordInput,
        required=False,
        help_text="Deixe vazio para manter a senha atual."
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def save(self):
        senha = self.cleaned_data.get('nova_senha')
        if senha:
            self.user.set_password(senha)
            self.user.save()


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label="E-mail",
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Digite seu e-mail',
        })
    )


        

