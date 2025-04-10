from email.headerregistry import Group
from django.shortcuts import render
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Profissional
# from .forms import EquipamentoForm
from cadastros.models import UnidadeSolicitante
from django.db.models import Q

class ProfissionalCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"regulacao"]
    template_name = "profissionais/form.html"
    model = Profissional
    fields = ['cpf', 'cns', 'nome', 'municipioAtuacao']
    success_url = reverse_lazy('list-profissionais')

    def form_valid(self, form):
        raise Exception('profissional create')
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url

class ProfissionalList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"regulacao"]
    template_name = "profissionais/list-profissionais.html"
    model = Profissional
    success_url = reverse_lazy('list-profissionais')

class ProfissionalUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"regulacao"]
    template_name = "profissionais/form.html"
    model = Profissional
    fields = ['nome', 'cns', 'cpf', 'programa', 'dataDeAdesao', 'municipioAtuacao', 'perfil', 'cnesEstabelecimento', 'nomeFantasiaEstabelecimento',
              'cbo', 'orgaoEmissor', 'uf', 'registroConselhoClasse', 'cnpjEmpregador', 'naturezaJuridica', 'atendimentoSus', 'cargaHorariaAmbulatorial', 'cargaHorariaHospitalar', 'cargaHorariaOutros', 'profissionalStatus', 'formaContratacaoEstabelecimento',
              'formaContratacaoEmpregador', 'detalhamentoFormaContratacao']
    success_url = reverse_lazy('list-profissionais')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url

class ProfissionalDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Profissional
    template_name = "profissionais/form-excluir.html"
    success_url = reverse_lazy('list-profissionais')