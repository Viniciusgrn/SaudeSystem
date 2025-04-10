from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpRequest
from django.db import transaction
from .models import ClassificacaoRisco
from cadastros.models import Paciente, UserUnidade
from braces.views import GroupRequiredMixin
from cadastros.forms import PermutarForm
import os

# Create your views here.
class ClassificacaoRiscoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter", u"administrativo"]
    model = ClassificacaoRisco
    fields = ['paciente', 'procedimento', 'unidadeExecutante', 'codSolicitacao', 'file']
    template_name = 'classificacaoDeRisco/form.html'
    success_url = reverse_lazy('listar_classificacaoRisco')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        form.instance.unidadeSolicitante_id = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.id
        url = super().form_valid(form)
        return url

class ClassificacaoRiscoPendenteList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter", u"enfermeiros", u"medicos"]
    model = ClassificacaoRisco
    template_name = 'classificacaoDeRisco/ListClassificacaoRisco.html'
    success_url = reverse_lazy('index')

    def get_queryset(self):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(self.request,
                             "Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return reverse_lazy('index')


        ##verificar se o usuário é admin ou callcenter
        if (self.request.user.groups.filter(name="callcenter").exists() or
                self.request.user.groups.filter(name="administrator").exists() or
                self.request.user.groups.filter(name="medicos").exists()):
            queryset = ClassificacaoRisco.objects.filter(status=1).order_by('-pk')
            return queryset


        if (self.request.user.groups.filter(name="enfermeiros").exists()):
            user = UserUnidade.objects.filter(user=self.request.user)
            unidadeSolicitante = user[0].unidadeSolicitante
            queryset = ClassificacaoRisco.objects.filter(unidadeSolicitante_id=unidadeSolicitante.id, status=1)
            return queryset

    # def get_context_data(self, **kwargs):
    #     filter = VagaOfertadaFilter()
    #     context = super(ListView, self).get_context_data(**kwargs)
    #     context['filter'].append(filter)
    #     return context

class AnalisarRiscoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter", u"medicos"]
    model = ClassificacaoRisco
    template_name = 'classificacaoDeRisco/ListClassificacaoRisco.html'
    success_url = reverse_lazy('listar_classificacaoRisco')

    def get(self, request, *args, **kwargs):
        form = PermutarForm()
        classificacaoRisco = get_object_or_404(ClassificacaoRisco, pk=kwargs['id'])
        pacientes = Paciente.objects.all()
        return render(request, 'classificacaoDeRisco/showClassificacaoRisco.html',
                      {'classificacaoRisco': classificacaoRisco, "pacientes": pacientes, "form": form})

    def post(self, request, *args, **kwargs):
        form = PermutarForm()
        classificacaoRisco = get_object_or_404(ClassificacaoRisco, pk=kwargs['id'])
        classificacaoRisco.status = request.POST.get('status')
        classificacaoRisco.comment = request.POST.get('comment')

        #remove o arquivo após a análise do médico
        if (os.path.exists("uploads/" + request.POST.get('file'))):
            os.remove("uploads/" + request.POST.get('file'))
        else:
            print("Arquivo não existe.")
        #fim remove arquivo
        classificacaoRisco.save()
        return redirect('listar_classificacaoRisco')

@transaction.atomic
def classificacaoRiscoStatusTrue(request: HttpRequest, id):
    with transaction.atomic():
        classificacaoRisco = get_object_or_404(ClassificacaoRisco, pk=id)
        classificacaoRisco.status = 2
        classificacaoRisco.createdBy_user_id = request.user.id
        classificacaoRisco.save()
        messages.success(request, "Pedido aceito com sucesso!")
        return reverse_lazy('listar_classificacaoRisco')

