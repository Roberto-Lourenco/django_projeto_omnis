from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from .forms import (
    AlterarSenhaForm,
    LoginForm,
    PessoaFisicaEditForm,
    PessoaFisicaForm,
    PessoaJuridicaEditForm, 
    PessoaJuridicaForm,
    EnderecoForm,
    FuncionarioForm,
    ClienteForm,
    CustomPasswordResetForm
)
from django.contrib.auth.views import PasswordResetView
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
from .models import PessoaFisica, PessoaJuridica, Endereco, Funcionario, Cliente

#==========Login==========#
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            remember_me = request.POST.get('remember_me')
            if remember_me:
                request.session.set_expiry(60 * 60 * 24 * 30) # 30 dias
            else:
                request.session.set_expiry(0)
            messages.success(request, 'Login realizado com sucesso!')
            return redirect('usuarios:perfil')
            
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})



#==========Logout==========#
def logout_view(request):
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('home')  # Altere 'home' se o nome da sua URL principal for outro




#=======Recuperar senha=======#
    
class CustomPasswordResetView(PasswordResetView):
    template_name = 'usuarios/password_reset.html'
    email_template_name = 'usuarios/password_reset_email.html'
    subject_template_name = 'usuarios/password_reset_subject.txt'
    html_email_template_name = 'usuarios/password_reset_email.html'
    form_class = CustomPasswordResetForm



#==========Cadastro==========#
def redirecionar_cadastro(request):
    return render(request, 'usuarios/redirecionar_cadastro.html')

#=======Cadastro Pesoa Física=======#
def cadastro_pf(request):
    if request.method == 'POST':
        form = PessoaFisicaForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro PF realizado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = PessoaFisicaForm()
    return render(request, 'usuarios/cadastro_pf.html', {'form': form})

#=======Cadastro Pesoa Jurídica=======#
def cadastro_pj(request):
    if request.method == 'POST':
        form = PessoaJuridicaForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro PJ realizado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = PessoaJuridicaForm()
    return render(request, 'usuarios/cadastro_pj.html', {'form': form})


#==========Perfil==========#
@login_required(login_url='usuarios:login')
def perfil(request):
    perfil = None
    tipo_perfil = None
    try:
        perfil = request.user.pessoafisica
        tipo_perfil = 'pf'
    except PessoaFisica.DoesNotExist:
        try:
            perfil = request.user.pessoajuridica
            tipo_perfil = 'pj'
        except PessoaJuridica.DoesNotExist:
            perfil = request.user
            tipo_perfil = 'user'  # ou None

    enderecos = Endereco.objects.filter(usuario=request.user)
    return render(request, 'usuarios/perfil.html', {
        'perfil': perfil,
        'tipo_perfil': tipo_perfil,
        'enderecos': enderecos,
    })


#=======Perfil - adicionar endereço=======#
@login_required(login_url='usuarios:login')
def adicionar_endereco(request):
    if request.method == 'POST':
        form = EnderecoForm(request.POST, usuario=request.user)
        if form.is_valid():
            form.save() 
            messages.success(request, 'Endereço adicionado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = EnderecoForm(usuario=request.user)
    return render(request, 'usuarios/endereco_form.html', {'form': form})


#=======Perfil - editar perfil=======#
@login_required(login_url='usuarios:login')
def editar_perfil(request):
    user = request.user
    if hasattr(user, 'pessoafisica'):
        form = PessoaFisicaEditForm(instance=user.pessoafisica)
    elif hasattr(user, 'pessoajuridica'):
        form = PessoaJuridicaEditForm(instance=user.pessoajuridica)
    else:
        form = None
    try:
        instance = user.pessoafisica
        form_class = PessoaFisicaEditForm
    except PessoaFisica.DoesNotExist:
        try:
            instance = user.pessoajuridica
            form_class = PessoaJuridicaEditForm
        except PessoaJuridica.DoesNotExist:
            messages.error(request, "Tipo de usuário inválido.")
            return redirect('usuarios:perfil')

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        senha_form = AlterarSenhaForm(request.POST, user=user)

        if form.is_valid() and senha_form.is_valid():
            form.save()
            senha_form.save()

            # Atualiza a sessão para evitar logout após troca de senha
            update_session_auth_hash(request, user)

            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('usuarios:perfil')

    else:
        form = form_class(instance=instance)
        senha_form = AlterarSenhaForm(user=user)

    return render(request, 'usuarios/editar_perfil.html', {
        'form': form,
        'senha_form': senha_form
    })




@login_required
def atualizar_dado_ajax(request):
    if request.method == "POST":
        data = json.loads(request.body)
        campo = data.get("campo")
        valor = data.get("valor")
        perfil = request.user.perfil

        if hasattr(perfil, campo):
            setattr(perfil, campo, valor)
            perfil.save()
            return JsonResponse({"status": "ok"})
        return JsonResponse({"status": "erro", "mensagem": "Campo inválido"})

    return JsonResponse({"status": "erro", "mensagem": "Método não permitido"})

@login_required
def upload_foto_ajax(request):
    if request.method == "POST" and request.FILES.get("foto"):
        perfil = request.user.perfil
        perfil.foto = request.FILES["foto"]
        perfil.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "erro", "mensagem": "Nenhuma imagem enviada"})



# ========== Área administrativa ========== #

#=======Funcionários=======#

#====Funcionários - Criar====#
@login_required
def criar_funcionario(request):
    if not request.user.is_staff:
        return redirect('usuarios:perfil')
    
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário cadastrado com sucesso!')
            return redirect('lista_funcionarios')
    else:
        form = FuncionarioForm()
    
    return render(request, 'usuarios/funcionario_form.html', {'form': form})

#====Funcionários - Listar====#
@login_required
def lista_funcionarios(request):
    if not request.user.is_staff:
        return redirect('usuarios:perfil')
    
    funcionarios = Funcionario.objects.select_related('usuario').all()
    return render(request, 'usuarios/lista_funcionarios.html', {
        'funcionarios': funcionarios
    })

#====Funcionários - Editar====# 
@login_required
def editar_funcionario(request, pk):
    if not request.user.is_staff:
        return redirect('usuarios:perfil')
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário atualizado com sucesso!')
            return redirect('lista_funcionarios')
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, 'usuarios/funcionario_form.html', {'form': form})

#=======Clientes=======#

#====Clientes - Criar====#
@login_required
def criar_cliente(request):
    if not request.user.is_staff:
        return redirect('perfil')
    
    if request.method == 'POST':
        form = ClienteForm(request.POST, user=request.user)  # Passa o usuário logado
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente registrado com sucesso!')
            return redirect('lista_clientes')
    else:
        form = ClienteForm(user=request.user)  # Passa o usuário logado
    
    return render(request, 'usuarios/cliente_form.html', {'form': form})

#====Clientes - Listar====#
@login_required
def lista_clientes(request):
    if not request.user.is_staff:
        return redirect('usuarios:perfil')
    
    clientes = Cliente.objects.select_related('usuario').all()
    return render(request, 'usuarios/lista_clientes.html', {
        'clientes': clientes
    })
    
#====Clientes - Editar====#
@login_required
def editar_cliente(request, pk):
    if not request.user.is_staff:
        return redirect('usuarios:perfil')
    
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'usuarios/cliente_form.html', {'form': form})
    
    

#=======Endereço=======#

#====Endereço - editar existente====#
@login_required(login_url='usuarios:login')
def editar_endereco(request, pk):
    endereco = get_object_or_404(Endereco, pk=pk, usuario=request.user)
    if request.method == 'POST':
        form = EnderecoForm(request.POST, instance=endereco)
        if form.is_valid():
            form.save()
            messages.success(request, 'Endereço atualizado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = EnderecoForm(instance=endereco)
    return render(request, 'usuarios/endereco_form.html', {'form': form, 'object':endereco})

#====Endereço - deletar existente====#
class DeletarEndereco(DeleteView):
    model = Endereco
    success_url = reverse_lazy('usuarios:perfil')
    template_name = 'usuarios/endereco_confirm_delete.html'
    
    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)



