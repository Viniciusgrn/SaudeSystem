from email.headerregistry import Group
from django.shortcuts import render
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Gestantes
from .forms import GestantesForm
# from .forms import EquipamentoForm
from cadastros.models import UnidadeSolicitante
from django.db.models import Q
from django import forms

class GestanteCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    template_name = "gestantes/form.html"
    group_required = [u"administrator"]
    model = Gestantes
    fields = ['nome', 'dataNascimento', 'telefoneParaContato', 'etapaGestacao', 'cns', 'cross',  'statusProcesso', 'unidade', 'dataInicioPrenatal', 'gestaoGemelar', 'dum', 'idadeGestacionalUltrassom',
              'idadeGestacional', 'ddp', 'trimestre', 'observacaoUnidade', 'dataSolicitacaoUsObstetrico', 'dataAgendada', 'codigoSolicitacao', 'observacaoSMS']
    success_url = reverse_lazy('list-gestantes')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url


class GestanteList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    template_name = "gestantes/list-gestantes.html"
    model = Gestantes
    success_url = reverse_lazy('list-gestantes')


class GestanteUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    template_name = "gestantes/form.html"
    group_required = [u"administrator"]
    model = Gestantes
    fields = ['nome', 'dataNascimento', 'telefoneParaContato', 'cns', 'cross', 'etapaGestacao', 'statusProcesso', 'unidade', 'dataInicioPrenatal', 'gestaoGemelar', 'dum',
              'idadeGestacional', 'idadeGestacionalUltrassom', 'ddp', 'trimestre', 'observacaoUnidade', 'dataSolicitacaoUsObstetrico', 'dataAgendada', 'codigoSolicitacao', 'observacaoSMS']
    success_url = reverse_lazy('list-gestantes')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url

class GestanteDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Gestantes
    template_name = "gestantes/form-excluir.html"
    success_url = reverse_lazy('list-gestantes')


