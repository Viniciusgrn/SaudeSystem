from email.headerregistry import Group
from django.shortcuts import render
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Equipamento, Marca
# from .forms import EquipamentoForm
from cadastros.models import UnidadeSolicitante
from django.db.models import Q

############################### Equipamento #######################################

class EquipamentosList(GroupRequiredMixin ,LoginRequiredMixin ,ListView):
    login_url = reverse_lazy('userLogin')
    template_name = 'equipamentos/list-equipamentos.html'
    group_required = [u'Administrator', u"support"]
    model = Equipamento
    success_url = reverse_lazy('list-equipamentos')

    def get_context_data(self, **kwargs):
        context = super(EquipamentosList, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['computadoresTotal'] = Equipamento.objects.filter(equipamento='Computador').filter(status=1).count()
            context['impressorasTotal'] = Equipamento.objects.filter(equipamento='Impressora').filter(status=1).count()
            context['monitorTotal'] = Equipamento.objects.filter(equipamento='Monitor').filter(status=1).count()
            context['tabletsTotal'] = Equipamento.objects.filter(equipamento='Tablet').filter(status=1).count()
            context['depreciadosTotal'] = Equipamento.objects.filter(status=2).count()
            context['outrosTotal'] = Equipamento.objects.filter(equipamento='Outros').filter(status=1).count()
            context['equipamentos'] = Equipamento.objects.all()            
            return context
             

    # def get_queryset(self):

    #     txt_search = self.request.GET.get('search')
    #     if txt_search: 
    #         unidade = UnidadeSolicitante.objects.get(nome = txt_search)
    #         equipamento = Equipamento.objects.filter(Q(unidade__id__icontains=unidade.id))
            
    #     else:
    #        equipamento = Equipamento.objects.all()

    #     return equipamento


class EquipamentoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    template_name = 'equipamentos/form.html'
    group_required = [u'Administrator', u"support"]
    model = Equipamento
    fields = ['unidade', 'localidade', 'patrimonio', 'adesivo', 'equipamento', 'marca', 'modelo',  'alugadoPor', 'observacao', 'status']
    success_url = reverse_lazy('list-equipamentos')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url

class EquipamentoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Equipamento
    fields = ['unidade', 'localidade', 'patrimonio', 'adesivo', 'equipamento', 'marca', 'modelo',  'alugadoPor', 'observacao', 'status']
    template_name = 'equipamentos/form.html'
    success_url = reverse_lazy('list-equipamentos')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url
############################### Marca #######################################


class MarcaList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = 'equipamentos/list-marcas.html'
    group_required = [u'Administrator', u"support"]
    model = Marca
    success_url = reverse_lazy('list-marcas')

class MarcaCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    template_name = 'equipamentos/form.html'
    group_required = [u'Administrator', u"support"]
    fields = ['marca', 'descricao', 'observacao']
    model = Marca
    success_url = reverse_lazy('list-marcas')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user

        url = super().form_valid(form)
        return url


class MarcaUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u'Administrator', u"support"]
    model = Marca
    fields = ['marca', 'descricao', 'observacao','status']
    template_name = 'equipamentos/form.html'
    success_url = reverse_lazy('list-marcas')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url
