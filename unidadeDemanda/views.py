from email.headerregistry import Group
from typing import List
from django.shortcuts import render
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import UnidadeDemanda
import datetime
from django.utils import timezone

class UnidadeDemandaCreate(GroupRequiredMixin,LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u'administrator']
    model = UnidadeDemanda
    fields = ['unidade', 'cnes', 'quantidade']
    template_name = 'unidadeDemanda/form.html'
    success_url = reverse_lazy('list-unidadeDemanda')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url
    

class UnidadeDemandaUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u'administrator']
    model = UnidadeDemanda
    fields = ['unidade', 'cnes', 'quantidade']
    template_name = 'unidadeDemanda/form.html'
    success_url = reverse_lazy('list-unidadeDemanda')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url
    

class UnidadeDemandaDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    model = UnidadeDemanda
    group_required = (u'Administrator')
    template_name = "unidadeDemanda/form-excluir.html"
    success_url = reverse_lazy('list-unidadeDemanda')


class UnidadeDemandaList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = (u'Administrator')
    model = UnidadeDemanda
    template_name = 'unidadeDemanda/list-unidadeDemanda.html'
    success_url = reverse_lazy('list-unidadeDemanda')