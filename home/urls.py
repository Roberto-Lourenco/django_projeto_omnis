from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Página principal
    path('', views.home, name='home'),
    # Endpoints AJAX para os selects dinâmicos
    path('get-modelos/', views.get_modelos, name='get_modelos'),
    path('get-anos/', views.get_anos, name='get_anos'),
    path('get-versoes/', views.get_versoes, name='get_versoes'),
    # Validação de CEP
    path('validar-cep/', views.validar_cep, name='validar_cep'),
]