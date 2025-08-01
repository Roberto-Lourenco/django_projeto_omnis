from django.http import HttpResponse
from django.shortcuts import render
from usuarios.email_sender import enviar_email

def envio_apolice(request):
    usuario = request.user

    contexto = {
        'usuario': usuario,
        'plano': 'Premium',
        'coberturas': [
            'Assistência na Estrada',
            'Proteção Abrangente',
            'Substituição de Chave',
        ],
        'numero_apolice': '12345678-OMNIS',
    }

    enviar_email(
        assunto='Sua nova Apólice Omnis',
        template_html='contratos/emails/email_apolice.html',
        contexto=contexto,
        destinatario=usuario.email
    )
    return HttpResponse(f'Email enviado com sucesso para {usuario.email}, Nome: {usuario.nome_completo}')