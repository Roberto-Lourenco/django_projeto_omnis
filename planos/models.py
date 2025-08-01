from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

#==========CLASSE COBERTURA==========#
class Cobertura(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da cobertura")
    desc = models.TextField(max_length=500, verbose_name="Descrição da cobertura")
    valor_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor padrão",
        null=True,
        blank=True
    )
    
    # Icone para adicionar a página ao exibir no html (Será apenas o código do icone para usar no FontAwesome)
    icone = models.CharField(
        max_length=100,
        verbose_name="Código do ícone (FontAwesome)",
        help_text='Exemplos válidos: fas fa-car, far fa-address-card, fab fa-whatsapp',
        default='fas fa-shield-alt',
        blank=True
    )
    
    # STATUS DA COBERTURA
    status = models.BooleanField(default=True,
                                 verbose_name="Ativada",
                                 help_text="Desmarque para desativar esta cobertura")
    
    # Datas
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    
    class Meta:
        verbose_name = "Cobertura"
        verbose_name_plural = "Coberturas"
        ordering = ['nome']
        
        
    def __str__(self):
        return self.nome


#==========CLASSE PLANOS==========#
class Plano(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Plano")
    preco_base = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Preço Base",
        validators=[MinValueValidator(0)]
    )
    desc = models.TextField(max_length=500, verbose_name="Descrição")
    
    # RELAÇÃO  PLANO X VEICULO
    is_padrao = models.BooleanField(
    default=False,
    verbose_name="Plano padrão",
    help_text="Marcar se este plano deve ser oferecido quando não houver veículo específico"
    )
    
    # RELAÇÃO COBERTURA X PLANO
    coberturas = models.ManyToManyField(
        Cobertura,
        verbose_name="Coberturas incluídas",
        blank=True,
        related_name="planos"
    )
     
    franquia = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Franquia",
        null=True,
        blank=True
    )
    
    limite_indenizacao = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Limite de Indenização",
        null=True,
        blank=True
    )
    
    status = models.BooleanField(default=True, verbose_name="Ativado")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    
    
    class Meta:
        verbose_name = "Plano"
        verbose_name_plural = "Planos"
        ordering = ['preco_base']

    
    def __str__(self):
        return self.nome
    
    # EXIBIR COBERTURAS INCLUSAS NA SEÇÃO PLANOS DO ADMIN
    def coberturas_incluidas(self):
        return ", ".join([c.nome for c in self.coberturas.all()])
    coberturas_incluidas.short_description = "Coberturas Incluídas"
    
    


#==========CLASSE MARCA==========#
    # Criado separadamente de veiculos para utilizar como Choice na criação do veículo.
class Marca(models.Model):
    nome = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.nome
    
#==========CLASSE VEICULOS==========#
class Veiculo(models.Model):
    CATEGORIAS = [
        ('POPULAR', 'Popular'),
        ('MEDIO', 'Médio'),
        ('LUXO', 'Luxo')
    ]
    
    TRANSMISSOES = [
        ('AUTOMATICO', 'Automático'),
        ('MANUAL', 'Manual'),
        ('SEMI_AUTOMATICO', 'Semi-Automático')
    ]
    
    # Informações básicas
    # Exibe a classe marca em forma de select
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    modelo = models.CharField(max_length=50)
    ano = models.PositiveIntegerField()
    categoria = models.CharField(max_length=10, choices=CATEGORIAS)
    
    # Detalhes técnicos
    versao = models.CharField(max_length=100)
    transmissao = models.CharField(max_length=15, choices=TRANSMISSOES)
    valor_fipe = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Relacionamentos
    planos = models.ManyToManyField('Plano', blank=True, related_name='veiculos')
    
    # Datas
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
        unique_together = ['marca', 'modelo', 'ano', 'versao']

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.versao} ({self.ano}) - {self.get_categoria_display()}"
    
    @classmethod
    def get_planos_padrao(cls):
        """Retorna planos padrão para quando não há veículo específico"""
        return Plano.objects.filter(
        is_padrao=True,
        status=True 
        ).order_by('preco_base') 



    # CALCULO DE VALOR BASE (INCREMENTO DE ACORDO COM A CATEGORIA DO VEICULO)
    @property
    def valor_seguro_base(self):
        if self.categoria == 'POPULAR':
            return self.valor_fipe * Decimal('0.03')  # 3% do FIPE
        elif self.categoria == 'MEDIO':
            return self.valor_fipe * Decimal('0.04')
        else:
            # CATEGORIA LUXO
            return self.valor_fipe * Decimal('0.06')

