
from django.shortcuts import get_object_or_404, render, redirect
from .models import Cotacao
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa



def gerar_pdf_cotacao(request, cotacao_id):
    cotacao = get_object_or_404(Cotacao, id=cotacao_id)

    template_path = 'resultadoCotacao/pdf_cotacao.html'
    context = {'cotacao': cotacao}
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="cotacao_{cotacao.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Erro ao gerar PDF', status=500)
    return response




def resultado_cotacao(request):
    cotacao_id = request.session.get('cotacao_id')
    
    if not cotacao_id:
        return redirect('home')
    
    try:
        cotacao = Cotacao.objects.get(id=cotacao_id)
        primeiro_nome = cotacao.nome.split()[0].capitalize() if cotacao.nome else ''
        
        veiculo = cotacao.veiculo
        
        planos = []
        if veiculo:
            planos = veiculo.planos.filter(status=True)
            if not planos.exists():
                from planos.models import Plano
                planos = Plano.objects.filter(is_padrao=True, status=True)
        
        planos_com_valor = []
        for plano in planos:
            valor_calculado = veiculo.valor_seguro_base + plano.preco_base if veiculo else plano.preco_base
            planos_com_valor.append({
                'nome': plano.nome,
                'preco_base': plano.preco_base,
                'valor_calculado': valor_calculado,
                'descricao': plano.desc,
            })
        
        return render(request, 'resultadoCotacao/index.html', {
            'cotacao': cotacao,
            'primeiro_nome': primeiro_nome,
            'planos_com_valor': planos_com_valor
        })
    except Cotacao.DoesNotExist:
        return redirect('home')
