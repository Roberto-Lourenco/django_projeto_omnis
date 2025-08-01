from django.db import models

from planos.models import Marca, Plano, Veiculo

# Create your models here.

#==========CLASSE COTAÇÃO==========#
class Cotacao(models.Model):
    ESTADOS = [
        ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'),
        ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), 
        ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), 
        ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
        ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins'),
    ]

    # Dados pessoais
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=15)
    
    # Endereço (preenchido via CEP)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=50, blank=True)
    cidade = models.CharField(max_length=50, blank=True)
    uf = models.CharField(max_length=2, choices=ESTADOS, blank=True)
    
    # Dados do veículo
    marca_veiculo = models.CharField(max_length=50)
    modelo_veiculo = models.CharField(max_length=50)
    ano_veiculo = models.PositiveIntegerField()
    versao_veiculo = models.CharField(max_length=100, blank=True)
    
    
    # Termos
    termos_aceitos = models.BooleanField(default=False)
    
    # Datas
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    
    # Relacionamentos
    veiculo = models.ForeignKey(Veiculo, on_delete=models.SET_NULL, null=True, blank=True)
    planos_sugeridos = models.ManyToManyField(Plano, blank=True)
    
    class Meta:
        verbose_name = 'Cotação anônima'
        verbose_name_plural = 'Cotações anônimas'
        ordering = ['-criado_em']
    
    def __str__(self):
        return f"Cotação #{self.id} - {self.nome}"
    
    def save(self, *args, **kwargs):
        if not self.veiculo:
            try:
                marca_obj = Marca.objects.get(nome__iexact=self.marca_veiculo)
                self.veiculo = Veiculo.objects.get(
                    marca=marca_obj,
                    modelo__iexact=self.modelo_veiculo,
                    ano=self.ano_veiculo,
                    versao__iexact=self.versao_veiculo
                )
            except (Marca.DoesNotExist, Veiculo.DoesNotExist):
                pass
        
        super().save(*args, **kwargs)
        
        if self.veiculo and not self.planos_sugeridos.exists():
            self.planos_sugeridos.set(self.veiculo.planos.all())
