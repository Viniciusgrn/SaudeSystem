from django.shortcuts import render
from email.headerregistry import Group

import contato
from .models import Contato
from django.urls import reverse_lazy
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.

class ContatoCreate(LoginRequiredMixin, CreateView):
        login_url = reverse_lazy('userLogin')
        fields = [ 'nomeCompleto', 'cargo', 'unidade', 'assunto', 'mensagem']
        model = Contato
        template_name = 'contatos/formcontato.html'
        success_url = reverse_lazy('contato-list')

        def form_valid(self, formcontato):
           formcontato.instance.createdBy_user = self.request.user        
           url = super().form_valid(formcontato)
           return url


class ContatoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
        login_url = reverse_lazy('userLogin')
        group_required = [u'administrativo']
        fields = [ 'nomeCompleto', 'cargo', 'unidade', 'assunto', 'mensagem']
        model = Contato
        template_name = 'contatos/formcontato.html'
        success_url = reverse_lazy('contato-list')


class ContatoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
        login_url = reverse_lazy('userLogin')
        group_required = [u'administrativo']
        model = Contato
        template_name = 'contatos/list-contato.html'
        success_url = reverse_lazy('contato-list')
        paginate_by = 7
        p = Paginator(Paginator.count, per_page=7)

        def start_index(self):
       
              if self.Paginator.count == 0:
                 return 0
              return (self.paginator.per_page * (self.number - 1)) + 1

       
        def get_queryset(self):
        
           txt_contato = self.request.GET.get('contato')
           if txt_contato: 
            contatos = Contato.objects.filter(Q(nomeCompleto__icontains = txt_contato) | Q(cargo__icontains = txt_contato) | Q(unidade__icontains = txt_contato) | Q(assunto__icontains=txt_contato) | Q(mensagem__icontains=txt_contato))
       
           else:
            contatos = Contato.objects.all()
        
           return contatos
       