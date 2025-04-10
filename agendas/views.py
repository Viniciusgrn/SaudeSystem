from email.headerregistry import Group
from django.shortcuts import render
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Agenda
from django.db.models import Q


class AgendaList(GroupRequiredMixin, LoginRequiredMixin ,ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"regulacao"]
    template_name = "agendas/list-agendas.html"
    model = Agenda
    success_url = reverse_lazy('list-agenda')

class AgendaCreate(GroupRequiredMixin, LoginRequiredMixin ,CreateView):
    login_url = reverse_lazy('userLogin')
    template_name = "agendas/form.html"
    model = Agenda
    group_required = [u"administrator", u"regulacao"]
    fields = ['dataAgendamento', 'horarioAgendamento', 'procedimento', 'quantidade', 'tipoConsulta']
    success_url = reverse_lazy('list-agenda')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url

class AgendaUpdate(GroupRequiredMixin, LoginRequiredMixin ,UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"regulacao"]
    template_name = "agendas/form.html"
    model = Agenda
    fields = ['dataAgendamento', 'horarioAgendamento', 'procedimento', 'quantidade', 'tipoConsulta']
    success_url = reverse_lazy('list-agenda')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url

class AgendaDelete(GroupRequiredMixin, LoginRequiredMixin ,DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Agenda
    template_name = "agendas/form-excluir.html"
    success_url = reverse_lazy('list-agenda')


