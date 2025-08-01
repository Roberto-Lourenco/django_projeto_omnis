from django.urls import path
from .views import resultado_cotacao, gerar_pdf_cotacao

urlpatterns = [
    path('', resultado_cotacao, name='resultado_cotacao'),
    path('cotacao/<int:cotacao_id>/pdf/', gerar_pdf_cotacao, name='gerar_pdf_cotacao'),
]