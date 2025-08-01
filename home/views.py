from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests

from resultadoCotacao.models import Cotacao
from resultadoCotacao.forms import CotacaoForm
from planos.models import Marca, Veiculo

def home(request):
    if request.method == 'POST':
        form = CotacaoForm(request.POST)
        if form.is_valid():
            try:
                veiculo = Veiculo.objects.get(
                    marca__nome__iexact=form.cleaned_data['marca_veiculo'],
                    modelo__iexact=form.cleaned_data['modelo_veiculo'],
                    ano=form.cleaned_data['ano_veiculo'],
                    versao__iexact=form.cleaned_data['versao_veiculo']
                )
            except Veiculo.DoesNotExist:
                veiculo = None

            cotacao = form.save(commit=False)
            cotacao.veiculo = veiculo  # Associa o veículo encontrado
            cotacao.save()
            
            
            request.session['cotacao_id'] = cotacao.id
            return redirect('resultado_cotacao')
    else:
        form = CotacaoForm()
    
    return render(request, 'home/index.html', {
        'form': form,
        'marcas': Marca.objects.all().order_by('nome')
    })

def get_modelos(request):
    marca = request.GET.get('marca')
    modelos = []
    
    if marca:
        try:
            marca_obj = Marca.objects.get(nome__iexact=marca)
            modelos = Veiculo.objects.filter(
                marca=marca_obj
            ).values_list('modelo', flat=True).distinct().order_by('modelo')
        except Marca.DoesNotExist:
            pass
    
    return JsonResponse({'modelos': list(modelos)})

def get_anos(request):
    marca = request.GET.get('marca')
    modelo = request.GET.get('modelo')
    anos = []
    
    if marca and modelo:
        try:
            anos = Veiculo.objects.filter(
                marca__nome__iexact=marca,
                modelo__iexact=modelo
            ).values_list('ano', flat=True).distinct().order_by('-ano')
        except Veiculo.DoesNotExist:
            pass
    
    return JsonResponse({'anos': list(anos)})

def get_versoes(request):
    marca = request.GET.get('marca')
    modelo = request.GET.get('modelo')
    ano = request.GET.get('ano')
    versoes = []
    
    if marca and modelo and ano:
        try:
            versoes = Veiculo.objects.filter(
                marca__nome__iexact=marca,
                modelo__iexact=modelo,
                ano=ano
            ).values_list('versao', flat=True).distinct().order_by('versao')
        except Veiculo.DoesNotExist:
            pass
    
    return JsonResponse({'versoes': list(versoes)})

def validar_cep(request):
    cep = request.GET.get('cep', '').replace('-', '')
    
    if len(cep) != 8 or not cep.isdigit():
        return JsonResponse({'error': 'Formato de CEP inválido'}, status=400)
    
    try:
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        data = response.json()
        
        if 'erro' in data:
            return JsonResponse({'error': 'CEP não encontrado'}, status=404)
            
        return JsonResponse({
            'logradouro': data.get('logradouro', ''),
            'bairro': data.get('bairro', ''),
            'cidade': data.get('localidade', ''),
            'uf': data.get('uf', '')
        })
        
    except requests.RequestException:
        return JsonResponse({'error': 'Erro ao consultar CEP'}, status=500)
