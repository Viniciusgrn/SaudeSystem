from django.contrib import messages
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User, Group
from django.views.generic import TemplateView, UpdateView
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import Perfil, Profile
from .forms import UsuarioForm
from django.urls import reverse_lazy
import random, string

# Create your views here.
    #with templateView and OO
class LoginView(TemplateView):
    template_name = 'auth/login.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["titulo"] = 'Login'
        context["botao"] = 'Entrar'

        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            django_login(request, user)
            return redirect('index')
        
        message = 'Credenciais inválidas'
        return render(request, 'auth/login.html', {'message': message})

  


class PerfilUpdate(UpdateView):
    template_name = 'auth/form1.html'
    model = Profile
    fields = ['cns', 'cpf', 'nome','sexo','dataNascimento','cargo','altura','peso','nomeDaMae','nomeDoPai','comment','telefone1','celular1','allowMessage']
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Profile, user=self.request.user)
        return self.object



class PasswordsChangeView(PasswordChangeView):
    from_class = PasswordChangeForm
    success_url = reverse_lazy('changedonePassword')

    # messages.add_message(request, messages.WARNING, "Não foi possível deletar! Existem vagas ou permutas vinculadas ao cadastro desse paciente.")
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        context["titulo"] = 'Mudar senha'
        context["botao"] = 'Salvar'

        return context

class PasswordsChangeDoneView(PasswordChangeDoneView):
    template_name = 'auth/success_change.html'


class UsuarioCreate(CreateView):
    template_name = 'auth/form.html'
    form_class = UsuarioForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        grupo = get_object_or_404(Group, name="paciente")
        form.instance.username = form.instance.email
        
        url = super().form_valid(form)        
        self.object.groups.add(grupo)
        self.object.save()

        Profile.objects.create(user=self.object )
        
        return url

    def  get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['titulo'] = "Criar uma conta"
        context['botao'] = 'Cadastrar'

        return context


    

# with templateView and OO
# class LogoutView(TemplateView):
#     template_name = 'auth/login.html'
    
#     def get(self, request, *args, **kwargs):
#         django_logout(request)
#         return redirect('index')

# with view and OO
# class LoginView(View):
#     template_name = 'auth/login.html'
#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(username=username, password=password)

#         if user:
#             django_login(request, user)
#             return redirect('index')
        
#         message = 'Credenciais inválidas'
#         return render(request, self.template_name, {'message': message})

# without view and OO
# class LogoutView(View):
#     def get(self, request, *args, **kwargs):
#         django_logout(request)
#         return redirect('index')

# without OO
# def login(request: HttpRequest):
#     if request.method == "GET":
#         return render(request, "authUser/templates/auth/login.html")

#     username = request.POST.get("username")
#     password = request.POST.get("password")

#     user = authenticate(username=username, password=password)

#     if user:
#         django_login(request, user)
#         #next_param = request.GET.get('next')
#         #if next_param:#
#         return redirect('index')
    
#     message = "Credenciais inválidas"
#     return render(request, 'authUser/templates/auth/login.html', {'message': message})


# without OO
# def logout(request: HttpRequest):
#     django_logout(request)
#     return redirect('userLogin')