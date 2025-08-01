from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import Cotacao

class IdadeFilter(admin.SimpleListFilter):
    title = 'Faixa etária'
    parameter_name = 'idade'

    def lookups(self, request, model_admin):
        return (
            ('18-25', '18 a 25 anos'),
            ('26-35', '26 a 35 anos'),
            ('36-50', '36 a 50 anos'),
            ('50+', 'Mais de 50 anos'),
        )

    def queryset(self, request, queryset):
        today = timezone.now().date()
        if self.value() == '18-25':
            return queryset.filter(
                data_nascimento__lte=today - timedelta(days=365*18),
                data_nascimento__gte=today - timedelta(days=365*25)
            )
        elif self.value() == '26-35':
            return queryset.filter(
                data_nascimento__lte=today - timedelta(days=365*26),
                data_nascimento__gte=today - timedelta(days=365*35)
            )
        elif self.value() == '36-50':
            return queryset.filter(
                data_nascimento__lte=today - timedelta(days=365*36),
                data_nascimento__gte=today - timedelta(days=365*50)
            )
        elif self.value() == '50+':
            return queryset.filter(
                data_nascimento__lte=today - timedelta(days=365*50)
            )
        return queryset

@admin.register(Cotacao)
class CotacaoAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'data_nascimento_formatada',  
        'cidade', 
        'uf',
        'marca_veiculo',
        'modelo_veiculo',
    )
    
    list_filter = (
        'marca_veiculo',
        'modelo_veiculo',
        'uf',
        'criado_em',
        IdadeFilter
    )
    
    search_fields = ('nome', 'data_nascimento_formatada','uf','marca_veiculo','modelo_veiculo')

    def data_nascimento_formatada(self, obj):
        return obj.data_nascimento.strftime('%d/%m/%Y')
    data_nascimento_formatada.short_description = 'Data de Nascimento'

    def planos_sugeridos_display(self, obj):
        return ", ".join([plano.nome for plano in obj.planos_sugeridos.all()])
    planos_sugeridos_display.short_description = 'Planos Sugeridos'
