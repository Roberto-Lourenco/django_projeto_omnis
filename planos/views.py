from django.shortcuts import render

def planos(request):
    return render(request, 'planos/index.html')
