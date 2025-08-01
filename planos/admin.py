from django.contrib import admin
from .models import Plano, Cobertura, Veiculo, Marca


class CoberturaInline(admin.TabularInline):
    model = Plano.coberturas.through
    extra = 1
    verbose_name = "Cobertura incluída"
    verbose_name_plural = "Coberturas incluídas"
    
@admin.register(Plano)
class PlanoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'preco_base', 'is_padrao', 'status', 'coberturas_incluidas')
    list_editable = ('is_padrao', 'status')
    list_filter = ('is_padrao', 'status', 'coberturas')
    search_fields = ('nome', 'descricao')
    filter_horizontal = ('coberturas',) 
    inlines = [CoberturaInline]
    
    fieldsets = (
        (None, {
            'fields': ('nome', 'preco_base', 'is_padrao', 'status')
        }),
        ('Detalhes', {
            'fields': ('desc', 'franquia', 'limite_indenizacao'),
            'classes': ('collapse',)
        }),
        ('Coberturas', {
            'fields': ('coberturas',),
        }),
    )

@admin.register(Cobertura)
class CoberturaAdmin(admin.ModelAdmin):
    list_display = ('nome','valor_base','icone', 'status',)
    list_editable = ('status',)
    list_filter = (('planos',admin.RelatedOnlyFieldListFilter),
                   'status','valor_base','data_criacao')
    

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    search_fields = ('nome',)
    list_display = ('nome', 'qtd_veiculos')
    
    # Exibe os veiculos vinculados a Marca
    def qtd_veiculos(self, obj):
        return obj.veiculo_set.count() 
    
@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'ano', 'versao', 'categoria', 'valor_fipe')
    list_filter = ('categoria', 'marca', 'ano')
    search_fields = ('marca__nome', 'modelo', 'versao')
    
    # Para facilitar seleção dos planos
    filter_horizontal = ('planos',)
    

    
