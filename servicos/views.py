from django.shortcuts import render
from planos.models import Cobertura

def servicos(request):
    exibir_coberturas = {
        'servicos': Cobertura.objects.filter(status=True)
    }
    return render(request,
                  'servicos/index.html',
                  exibir_coberturas)

    
