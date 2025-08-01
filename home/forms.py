from django import forms
from django.core.exceptions import ValidationError
from planos.models import Marca, Veiculo
from .models import Cotacao
import re
from datetime import date

class CotacaoForm(forms.ModelForm):
    class Meta:
        model = Cotacao
        fields = '__all__'
    # Dados pessoais
    nome = forms.CharField(
        label='Nome Completo',
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Nome Completo',
            'class': 'form-control'
        })
    )
    
    cpf = forms.CharField(
        label='CPF',
        max_length=14,
        widget=forms.TextInput(attrs={
            'placeholder': 'CPF',
            'class': 'form-control'
        })
    )
    
    data_nascimento = forms.DateField(
        label='Data de Nascimento',
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
            'min': '1910-01-01',
            'max': '2007-01-01'
        })
    )
    
    telefone = forms.CharField(
        label='Telefone',
        max_length=15,
        min_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Telefone',
            'class': 'form-control'
        })
    )
    
    # CEP
    cep = forms.CharField(
        label='CEP',
        max_length=9,
        widget=forms.TextInput(attrs={
            'placeholder': 'CEP',
            'class': 'form-control'
        })
    )
    # ENDEREÇO ESCONDIDO NO HTML
    logradouro = forms.CharField(required=False, widget=forms.HiddenInput())
    bairro = forms.CharField(required=False, widget=forms.HiddenInput())
    cidade = forms.CharField(required=False, widget=forms.HiddenInput())
    uf = forms.CharField(required=False, widget=forms.HiddenInput())
    
    # Dados do veículo
    marca_veiculo = forms.ChoiceField(
        label='Marca',
        choices=[],  
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_marca',
            'required': 'required'
        })
    )

    modelo_veiculo = forms.ChoiceField(
        label='Modelo',
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_modelo',
            'required': 'required'
        })
    )
    
    ano_veiculo = forms.CharField(  
    label='Ano',
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'id_ano',
        'required': 'required',
        'readonly': 'readonly'
    })
    )

    versao_veiculo = forms.ChoiceField(
        label='Versão',
        choices=[],
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_versao',
            'required': 'required'
        })
    )
    
    termos_aceitos = forms.BooleanField(
        label='Li e concordo com os termos',
        widget=forms.CheckboxInput(attrs={'required': 'required'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Para cada campo dinâmico, se existir no data, adiciona como opção válida
        dynamic_fields = ['marca_veiculo', 'modelo_veiculo', 'versao_veiculo']
        for field in dynamic_fields:
            if field in self.data:
                self.fields[field].choices = [
                    (self.data[field], self.data[field])
                    ]
            elif self.instance.pk:
                value = getattr(self.instance, field)
                if value:
                    self.fields[field].choices = [(value, value)]

    
    def clean_cpf(self):
        cpf = self.cleaned_data['cpf']
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        if len(cpf) != 11:
            raise ValidationError('CPF deve conter 11 dígitos')
        
        # Validação do CPF (algoritmo)
        # ... (implemente a mesma validação que está no seu JS)
        
        return cpf
    
    def clean_data_nascimento(self):
        data = self.cleaned_data['data_nascimento']
        idade = (date.today() - data).days // 365
        
        if idade < 18:
            raise ValidationError('Você deve ter pelo menos 18 anos para fazer uma cotação')
        
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        marca = cleaned_data.get('marca_veiculo')
        modelo = cleaned_data.get('modelo_veiculo')
        ano = cleaned_data.get('ano_veiculo')
        versao = cleaned_data.get('versao_veiculo') 

        if marca and modelo and ano and versao: 
            try:
                marca_obj = Marca.objects.get(nome__iexact=marca)
                veiculo = Veiculo.objects.get(
                    marca=marca_obj,
                    modelo__iexact=modelo,
                    ano=ano,
                    versao__iexact=versao  
                )
            except Marca.DoesNotExist:
                raise ValidationError('Marca não encontrada em nossa base de dados')
            except Veiculo.DoesNotExist:
                raise ValidationError('Veículo não encontrado em nossa base de dados')
    
        return cleaned_data