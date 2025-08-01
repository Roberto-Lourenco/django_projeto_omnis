from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def enviar_email(assunto, template_html, contexto, destinatario):
    """
    :param assunto: Assunto do e-mail
    :param template_html: Caminho do template HTML (ex: 'usuarios/email_apolice.html')
    :param contexto: Dicionário com dados para o template
    :param destinatario: E-mail do destinatário (string ou lista)
    """
    
    html_content = render_to_string(template_html, contexto)
    text_content = strip_tags(html_content)
    
    if isinstance(destinatario, str):
        destinatario = [destinatario]

    email = EmailMultiAlternatives(
        subject=assunto,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=destinatario
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
