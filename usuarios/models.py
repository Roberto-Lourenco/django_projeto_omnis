from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from localflavor.br.models import BRCPFField, BRCNPJField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.utils import timezone


# User manager para modificar o auth do django
class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('nome_completo', 'Admin')
        extra_fields.setdefault('telefone', '+21999999999')
        return self.create_user(email, password, **extra_fields)


# Classe abstrata de Usuarios
class Usuario(AbstractBaseUser, PermissionsMixin):
    GENERO_CHOICES = [
    ('M', 'Masculino'),
    ('F', 'Feminino'),
]
    TIPO_USUARIO_CHOICES = [
    ('cliente', 'Cliente'),
    ('usuario', 'Usuário'),
]
    email = models.EmailField('Email', unique=True)
    nome_completo = models.CharField('Nome Completo', max_length=150)
    genero = models.CharField(
        'Gênero',
        max_length=3,
        choices=GENERO_CHOICES,
        help_text='Selecione seu gênero.'
    )
    
    # Formtação dos campos do telefone usando o modulo PhoneNumberField
    telefone = PhoneNumberField(
        'Telefone',
        region='BR',
        error_messages={
            'invalid': 'Digite um número de telefone válido. Exemplo: (11) 2345-6789.'
        } 
            )
    tipo_usuario = models.CharField(
        'Tipo de Usuário',
        max_length=10,
        choices=TIPO_USUARIO_CHOICES,
        default='usuario'
    )
    
    # Caso o usuario exclua a conta, será aqui será alterado para inativo
    is_active = models.BooleanField('Ativo', default=True)
    is_staff = models.BooleanField('Equipe', default=False)
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome_completo', 'telefone']
    
    objects = UsuarioManager()
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['nome_completo']
    
    def __str__(self):
        return f"{self.nome_completo} ({self.email})"

    def nome_capitalize(self):
        
        partes = self.nome_completo.strip().split()
    
        if len(partes) >= 2 and len(partes[1]) <= 2:
            return " ".join(p.title() for p in partes[:3])
        else:
            return " ".join(p.title() for p in partes[:2])
        
    def tipo_capitalize(self):
        tipousuario = self.tipo_usuario.capitalize()
        
        if self.genero == "F" and tipousuario == "Usuario":
            tipousuario = "Usuária"
        elif tipousuario == "Usuario":
            tipousuario = "Usuário"
        return tipousuario




# Classe Usuario PF
class PessoaFisica(Usuario):
    cpf = BRCPFField(
        'CPF', 
        unique=True,
    )
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    nome_mae = models.CharField(verbose_name='Nome da Mãe', max_length=250, blank=True)
    
    class Meta:
        verbose_name = 'Pessoa Física'
        verbose_name_plural = 'Pessoas Físicas'
    
    # Verificar se o usuário é maior de idade
    def clean(self):
        super().clean()
        if not self.data_nascimento:
            raise ValidationError({'data_nascimento': 'Data de nascimento é obrigatória.'})
    
        hoje = timezone.now().date()
        nascimento = self.data_nascimento

        idade = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))

        if idade < 18:
            raise ValidationError({'data_nascimento': 'O usuário deve ter pelo menos 18 anos.'})
    
        def __str__(self):
            return f"{self.nome_completo} (CPF: {self.cpf})"


# Classe Usuario PJ
class PessoaJuridica(Usuario):
    cnpj = BRCNPJField('CNPJ', unique=True)
    razao_social = models.CharField('Razão Social', max_length=150)
    nome_fantasia = models.CharField('Nome Fantasia', max_length=150)
    inscricao_estadual = models.CharField('Inscrição Estadual', max_length=20, blank=True)
    
    class Meta:
        verbose_name = 'Pessoa Jurídica'
        verbose_name_plural = 'Pessoas Jurídicas'
    
    def __str__(self):
        return f"{self.nome_fantasia} (CNPJ: {self.cnpj})"

# Endereço (Se relaciona com o usuario)
class Endereco(models.Model):
    cep = models.CharField('CEP', max_length=9, validators=[RegexValidator(r'^\d{5}-\d{3}$', 'Formato: 00000-000')])
    logradouro = models.CharField('Logradouro', max_length=100)
    numero = models.CharField('Número', max_length=10)
    complemento = models.CharField('Complemento', max_length=50, blank=True)
    bairro = models.CharField('Bairro', max_length=50)
    cidade = models.CharField('Cidade', max_length=50)
    estado = models.CharField('Estado', max_length=2)
    
    # Define se esse será o endereço principal do usuário
    principal = models.BooleanField('Principal', default=False)
    
    # Relação direta com o modelo Usuario
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='enderecos')

    class Meta:
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'principal'],
                condition=models.Q(principal=True),
                name='unique_endereco_principal'
            )
        ]
        
    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado}"


#========== FUNCIONARIOS ==========#
class Funcionario(models.Model):
    CARGO_CHOICES = [
        ('CORRETOR', 'Corretor'),
        ('ATENDENTE', 'Atendente'),
        ('ANALISTA', 'Analista de Sinistros'),
        ('GERENTE', 'Gerente'),
    ]
    
    DEPARTAMENTOS = [
        ('COMUNICACAO','Comunicação'),
        ('VENDAS','Vendas'),
        ('TI','Tecnlogia'),
    ]
    
    # Funcionario será cadastrado apenas como PF
    usuario = models.OneToOneField(PessoaFisica, on_delete=models.CASCADE, related_name='funcionario')
    
    # Matrícula para crachá (TESE)
    matricula = models.AutoField(primary_key=True)
    cargo = models.CharField('Cargo', max_length=20, choices=CARGO_CHOICES)
    
    # Data de emissão para calculos CLT
    data_admissao = models.DateField('Data de Admissão')
    
    departamento = models.CharField('Departamento', max_length=50, choices=DEPARTAMENTOS)
    
    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
        ordering = ['usuario__nome_completo']
        indexes = [
            models.Index(fields=['matricula']),
            models.Index(fields=['departamento']),
        ]
    
    def __str__(self):
        return f"{self.usuario.nome_completo} - {self.get_cargo_display()} - {self.get_departamento_display()}"


#========== METADADOS ==========#
class Cliente(models.Model):
    TIPO_CLIENTE = [
        ('POTENCIAL', 'Potencial'),
        ('ATIVO', 'Ativo'),
        ('INATIVO', 'Inativo'),
        ('BLOQUEADO', 'Bloqueado'),
    ]
    
    # Relação genérica para funcionar com PessoaFisica ou PessoaJuridica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    usuario = GenericForeignKey('content_type', 'object_id')
    
    tipo = models.CharField('Tipo de Cliente', max_length=20, choices=TIPO_CLIENTE, default='POTENCIAL')
    data_cadastro = models.DateTimeField('Data de Cadastro', auto_now_add=True)
    indicado_por = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='indicacoes')
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        indexes = [
            models.Index(fields=['content_type', 'object_id']),
        ]
    
    def clean(self):
        if self.indicado_por and self.indicado_por.id == self.id:
            raise ValidationError({'indicado_por': 'Um cliente não pode ser indicado por ele mesmo.'})
    
    def __str__(self):
        return f"{self.usuario.nome_completo} - {self.get_tipo_display()}"