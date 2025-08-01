from django.contrib import admin
from django.urls import path, include
from contratos import views as contrato

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Apps principais
    path('', include('home.urls')),
    path('contato/', include('contato.urls')),
    path('servicos/', include('servicos.urls')),
    path('resultado/', include('resultadoCotacao.urls')),
    path('planos/', include('planos.urls')),
    path('usuarios/', include('usuarios.urls', namespace='usuarios')),
    path('enviar_apolice/', contrato.envio_apolice, name='enviar_apolice'),
]
