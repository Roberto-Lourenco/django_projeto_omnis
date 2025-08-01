from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, PessoaFisica, PessoaJuridica, Endereco, Funcionario, Cliente
from .forms import UsuarioCreationForm, UsuarioChangeForm

class UsuarioAdmin(BaseUserAdmin):
    form = UsuarioChangeForm
    add_form = UsuarioCreationForm

    list_display = ('email', 'nome_completo', 'telefone', 'genero', 'tipo_usuario', 'is_active', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'tipo_usuario', 'genero')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome_completo', 'telefone', 'genero', 'tipo_usuario')}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome_completo', 'telefone', 'genero', 'password1', 'password2'),
        }),
    )

    search_fields = ('email', 'nome_completo')
    ordering = ('nome_completo',)
    filter_horizontal = ('groups', 'user_permissions',)

@admin.register(PessoaFisica)
class PessoaFisicaAdmin(UsuarioAdmin):
    list_display = ('nome_completo', 'email', 'cpf', 'data_nascimento', 'data_cadastro')
    readonly_fields = UsuarioAdmin.readonly_fields + ('cpf','data_cadastro','last_login')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome_completo', 'telefone','genero',)}),
        ('Dados PF', {'fields': ('cpf', 'data_nascimento', 'nome_mae')}),
        ('Permissões', {
            'fields': ('tipo_usuario', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Datas Importantes', {'fields': ('last_login', 'data_cadastro')}),
    )
    
    add_fieldsets = UsuarioAdmin.add_fieldsets + (
        ('Dados PF', {'fields': ('cpf', 'data_nascimento', 'nome_completo')}),
    )

@admin.register(PessoaJuridica)
class PessoaJuridicaAdmin(UsuarioAdmin):
    list_display = ('nome_fantasia', 'email', 'cnpj', 'razao_social', 'data_cadastro')
    readonly_fields = UsuarioAdmin.readonly_fields + ('cnpj','data_cadastro','last_login')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('nome_completo', 'telefone','genero',)}),
        ('Dados PJ', {'fields': ('cnpj', 'razao_social', 'nome_fantasia', 'inscricao_estadual')}),
        ('Permissões', {
            'fields': ('tipo_usuario','is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Datas Importantes', {'fields': ('last_login', 'data_cadastro')}),
    )
    
    add_fieldsets = UsuarioAdmin.add_fieldsets + (
        ('Dados PJ', {'fields': ('cnpj', 'razao_social', 'nome_fantasia', 'inscricao_estadual')}),
    )

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'logradouro', 'numero', 'cidade', 'principal')
    list_filter = ('principal', 'estado')
    search_fields = ('usuario__nome_completo', 'logradouro', 'cep')

@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'matricula', 'cargo', 'departamento', 'data_admissao')
    list_filter = ('cargo', 'departamento')
    search_fields = ('usuario__nome_completo', 'matricula')
    raw_id_fields = ('usuario',)
    readonly_fields = ('matricula',)
    fieldsets = (
        ('Informações pessoais', {'fields': ('usuario',)}),
        ('Informações do funcionário', {'fields': ('matricula', 'cargo', 'departamento',)}),
        ('Datas Importantes', {'fields': ('data_admissao',)}),
    )


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    exclude = ('content_type', 'object_id')
    readonly_fields = ('usuario',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

