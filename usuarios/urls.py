from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from .views import CustomPasswordResetView

app_name = 'usuarios'

urlpatterns = [
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Cadastro (PF/PJ)
    path('cadastrar/', views.redirecionar_cadastro, name='redirecionar_cadastro'),
    path('cadastrar/pf/', views.cadastro_pf, name='cadastro_pf'),
    path('cadastrar/pj/', views.cadastro_pj, name='cadastro_pj'),
    
    # Recuperação de senha
    path('recuperar-senha/', CustomPasswordResetView.as_view(), name='recuperar_senha'),

    
    path('recuperar-senha/enviado/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='usuarios/password_reset_done.html'
         ),
         name='password_reset_done'),
    
    path('recuperar-senha/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='usuarios/password_reset_confirm.html',
             success_url=reverse_lazy('usuarios:password_reset_complete')
         ),
         name='password_reset_confirm'),
    
    path('recuperar-senha/concluido/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='usuarios/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    
    # Área do usuário 
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path("perfil/atualizar/", views.atualizar_dado_ajax, name="atualizar_dado_ajax"),
    path("perfil/upload-foto/", views.upload_foto_ajax, name="upload_foto_ajax"),

    path('perfil/endereco/', views.adicionar_endereco, name='adicionar_endereco'),
    path('perfil/endereco/editar/<int:pk>/', views.editar_endereco, name='editar_endereco'),
    path('perfil/endereco/deletar/<int:pk>/', views.DeletarEndereco.as_view(), name='deletar_endereco'),
    
    # Área administrativa 
    path('admin/funcionarios/', views.lista_funcionarios, name='lista_funcionarios'),
    path('admin/funcionarios/novo/', views.criar_funcionario, name='criar_funcionario'),
    path('admin/funcionarios/editar/<int:pk>/', views.editar_funcionario, name='editar_funcionario'),
    
    # Administração de clientes
    path('admin/clientes/', views.lista_clientes, name='lista_clientes'),
    path('admin/clientes/novo/', views.criar_cliente, name='criar_cliente'),
    path('admin/clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
]