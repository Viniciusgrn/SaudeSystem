from email.headerregistry import Group
from typing import Any, Dict
from django.db import models
from django.shortcuts import render, redirect
from braces.views import GroupRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse, resolve, ResolverMatch
from .models import Malote, MaloteSaida, MaloteLog, Guia
from django.contrib.auth.models import User, Group
from cadastros.models import UserUnidade, UnidadeSolicitante, Paciente
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import pandas as pd
from django.contrib import messages
from relatorios.models import DicionarioDeProcedimentos
import datetime
from django.utils.timezone import utc
from datetime import *
from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from .forms import ScannerForm
from django.shortcuts import redirect
  
    

##################################################### LIST ###########################################################################

#Lista de unidades
class MaloteUnidadesList(GroupRequiredMixin,  LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/list-unidades.html"
    model = Malote
    group_required = [u"administrator", u"malote"]
    # permission_required = ("malote.view_malote")
    success_url = reverse_lazy('list-maloteUnidades')

    #Traz as unidades que possuem malotes, quantos malotes possui e data da ultima inserção
    def get_context_data(self, **kwargs):
        context = super(MaloteUnidadesList, self).get_context_data(**kwargs)
        unidades = Malote.objects.raw("SELECT u.id, m.unidadeSolicitante_id, m.id, u.nome, m.created_at AS ultimaInsercao, (SELECT COUNT(m.etapa) from malotes_malote m WHERE u.id=m.unidadeSolicitante_id and m.etapa=1) AS Recebidos, (SELECT COUNT(m.etapa) from malotes_malote m WHERE u.id=m.unidadeSolicitante_id and m.etapa=3) AS aguardandoEncaminhamento,COUNT(m.unidadeSolicitante_id) AS quantidade FROM cadastros_unidadesolicitante u INNER JOIN malotes_malote m ON  u.id=m.unidadeSolicitante_id GROUP BY u.nome")
        context['unidades'] = unidades
        return context

class MaloteUnidadesEntrada(GroupRequiredMixin,  LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/list-unidades.html"
    model = Malote
    group_required = [u"administrator", u"malote"]
    # permission_required = ("malote.view_malote")
    success_url = reverse_lazy('list-maloteUnidades')

    #Traz as unidades que possuem malotes, quantos malotes possui e data da ultima inserção
    def get_context_data(self, **kwargs):
        context = super(MaloteUnidadesList, self).get_context_data(**kwargs)
        unidades = Malote.objects.raw("SELECT u.id, m.unidadeSolicitante_id, m.id, u.nome, m.created_at AS ultimaInsercao, (SELECT COUNT(m.etapa) from malotes_malote m WHERE u.id=m.unidadeSolicitante_id and m.etapa=1) AS Recebidos, (SELECT COUNT(m.etapa) from malotes_malote m WHERE u.id=m.unidadeSolicitante_id and m.etapa=3) AS aguardandoEncaminhamento,COUNT(m.unidadeSolicitante_id) AS quantidade FROM cadastros_unidadesolicitante u INNER JOIN malotes_malote m ON  u.id=m.unidadeSolicitante_id GROUP BY u.nome")
        context['unidades'] = unidades
        return context

#Lista de malotes para as regulção
class MaloteListRegulacao(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/list-malotesRegulacao.html"
    model = Malote
    group_required = [u"administrator", u"malote"]
    success_url = reverse_lazy('list-malotes-all')

    def get_queryset(self):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(self.request,"Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return  reverse_lazy('index')

        #verificar se o usuário é admin ou malote e filtra os dados pela unidade referente no url ou caso não tenha id na url traz todos os objetos
        pk = self.kwargs.get('pk')
        if (self.request.user.groups.filter(name = "malote").exists() or self.request.user.groups.filter(name = "administrator").exists()):
            if Malote.objects.filter(unidadeSolicitante_id= pk):
                 queryset = Malote.objects.filter(unidadeSolicitante_id=pk)
                 return queryset
            else:
                queryset = Malote.objects.all()
                return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Envia o id da unidade que esta sendo acessada
        pk = self.kwargs.get('pk')
        context["unidadePk"] = pk

        #Envia o contexto com o nome da unidade 
        filtroUnidade = UnidadeSolicitante.objects.filter(id=pk).values('nome')
        if pk != None:
            nomeUnidade = filtroUnidade[0].get('nome')
            context['nomeUnidade'] = nomeUnidade + ' - Malotes'
        else:
            context['nomeUnidade'] = 'Todos os malotes'
        #Envia o contexto com a ultima atualização de um user com grupo malote no sistema
        groups = User.objects.filter(groups__name='malote').values_list('id')
        ultimaatualizacao = Malote.objects.filter(unidadeSolicitante_id=pk).values().filter(updatedBy_user_id__in=groups).exclude(Q(updatedBy_user_id__isnull=True) | Q(updatedBy_user_id__exact=0)).order_by('updated_at').last()  
        if ultimaatualizacao != None:
            ultimaatualizacao = ultimaatualizacao.get('updated_at')
            horarioUltimaAtualizacao = ultimaatualizacao.__format__("%d/%m/%Y")
            context["horarioUltimaAtualizacao"] = horarioUltimaAtualizacao
            return context
        else: 
            semRegistro = 'Sem registros'
            context["horarioUltimaAtualizacao"] = semRegistro
            return context

    
 # Lista de malotes para os cirurgia
class MaloteListCirurgia(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/list-malotesCirurgia.html"
    model = Malote
    group_required = [u"administrator", u"cirurgia"]
    success_url = reverse_lazy('list-malotes-all')

    def get_queryset(self):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(self.request,"Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return  reverse_lazy('index')

        #verificar se o usuário é admin ou malote e filtra os dados pela unidade referente no url ou caso não tenha id na url traz todos os objetos
        pk = self.kwargs.get('pk')
        if (self.request.user.groups.filter(name="cirurgia").exists() or self.request.user.groups.filter(name="administrator").exists()):
            if Malote.objects.filter(unidadeSolicitante_id= pk):
                 queryset = Malote.objects.filter(unidadeSolicitante_id=pk)
                 return queryset
            else:
                queryset = Malote.objects.all()
                return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        groups = User.objects.filter(groups__name='malote').values_list('id')
        ultimaatualizacao = Malote.objects.filter(unidadeSolicitante_id=pk).values().filter(updatedBy_user_id__in=groups).exclude(Q(updatedBy_user_id__isnull=True) | Q(updatedBy_user_id__exact=0)).order_by('updated_at').last()
        if ultimaatualizacao != None:
            ultimaatualizacao = ultimaatualizacao.get('updated_at')
            horarioUltimaAtualizacao = ultimaatualizacao.__format__("%d/%m/%Y")
            context["horarioUltimaAtualizacao"] = horarioUltimaAtualizacao
            return context
        else: 
            semRegistro = 'Sem registros'
            context["horarioUltimaAtualizacao"] = semRegistro
            return context



 # Lista de malotes para os médicos
class MaloteListMedico(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/list-malotesMedico.html"
    model = Malote
    group_required = [u"administrator", u"medicos"] 
    success_url = reverse_lazy('list-malotes-all')

    def get_queryset(self):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(self.request,"Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return  reverse_lazy('index')

        #verificar se o usuário é admin ou malote e filtra os dados pela unidade referente no url ou caso não tenha id na url traz todos os objetos
        pk = self.kwargs.get('pk')
        if (self.request.user.groups.filter(name="medicos").exists() or self.request.user.groups.filter(name="administrator").exists()):
            if Malote.objects.filter(unidadeSolicitante_id= pk):
                 queryset = Malote.objects.filter(unidadeSolicitante_id=pk)
                 return queryset
            else:
                queryset = Malote.objects.all()
                return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        groups = User.objects.filter(groups__name='malote').values_list('id')
        ultimaatualizacao = Malote.objects.filter(unidadeSolicitante_id=pk).values().filter(updatedBy_user_id__in=groups).exclude(Q(updatedBy_user_id__isnull=True) | Q(updatedBy_user_id__exact=0)).order_by('updated_at').last()
        if ultimaatualizacao != None:
            ultimaatualizacao = ultimaatualizacao.get('updated_at')
            horarioUltimaAtualizacao = ultimaatualizacao.__format__("%d/%m/%Y")
            context["horarioUltimaAtualizacao"] = horarioUltimaAtualizacao
            return context
        else: 
            semRegistro = 'Sem registros'
            context["horarioUltimaAtualizacao"] = semRegistro
            return context


 # Lista de malotes para ame
class MaloteListAme(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/list-malotesAme.html"
    model = Malote
    group_required = [u"administrator", u"ame"] 
    success_url = reverse_lazy('list-malotes-all')

    def get_queryset(self):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(
                self.request, "Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return reverse_lazy('index')

        # verificar se o usuário é admin ou malote e filtra os dados pela unidade referente no url ou caso não tenha id na url traz todos os objetos
        pk = self.kwargs.get('pk')
        if (self.request.user.groups.filter(name="ame").exists() or self.request.user.groups.filter(name="administrator").exists()):
            if Malote.objects.filter(unidadeSolicitante_id=pk):
                queryset = Malote.objects.filter(unidadeSolicitante_id=pk)
                return queryset
            else:
                queryset = Malote.objects.all()
                return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        groups = User.objects.filter(groups__name='malote').values_list('id')
        ultimaatualizacao = Malote.objects.filter(unidadeSolicitante_id=pk).values().filter(updatedBy_user_id__in=groups).exclude(
            Q(updatedBy_user_id__isnull=True) | Q(updatedBy_user_id__exact=0)).order_by('updated_at').last()
        if ultimaatualizacao != None:
            ultimaatualizacao = ultimaatualizacao.get('updated_at')
            horarioUltimaAtualizacao = ultimaatualizacao.__format__("%d/%m/%Y")
            context["horarioUltimaAtualizacao"] = horarioUltimaAtualizacao
            return context
        else:
            semRegistro = 'Sem registros'
            context["horarioUltimaAtualizacao"] = semRegistro
            return context



 # Lista de malotes para Hospital De Olhos
class MaloteListHospitalDeOlhos(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/list-malotesHospitalDeOlhos.html"
    model = Malote
    group_required = [u"administrator", u"hospitalDeOlhos"] 
    success_url = reverse_lazy('list-malotes-all')

    def get_queryset(self):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(
                self.request, "Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return reverse_lazy('index')

        # verificar se o usuário é admin ou malote e filtra os dados pela unidade referente no url ou caso não tenha id na url traz todos os objetos
        pk = self.kwargs.get('pk')
        if (self.request.user.groups.filter(name="hospitalDeOlhos").exists() or self.request.user.groups.filter(name="administrator").exists()):
            if Malote.objects.filter(unidadeSolicitante_id=pk):
                queryset = Malote.objects.filter(unidadeSolicitante_id=pk)
                return queryset
            else:
                queryset = Malote.objects.all()
                return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        groups = User.objects.filter(groups__name='malote').values_list('id')
        ultimaatualizacao = Malote.objects.filter(unidadeSolicitante_id=pk).values().filter(updatedBy_user_id__in=groups).exclude(
            Q(updatedBy_user_id__isnull=True) | Q(updatedBy_user_id__exact=0)).order_by('updated_at').last()
        if ultimaatualizacao != None:
            ultimaatualizacao = ultimaatualizacao.get('updated_at')
            horarioUltimaAtualizacao = ultimaatualizacao.__format__("%d/%m/%Y")
            context["horarioUltimaAtualizacao"] = horarioUltimaAtualizacao
            return context
        else:
            semRegistro = 'Sem registros'
            context["horarioUltimaAtualizacao"] = semRegistro
            return context

 # Lista de malotes para biópsia
class MaloteListBiopsia(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/list-malotesBiopsia.html"
    model = Malote
    group_required = [u"administrator", u"biopsia"] 
    success_url = reverse_lazy('list-malotes-all')

    def get_queryset(self):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(
                self.request, "Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return reverse_lazy('index')

        # verificar se o usuário é admin ou malote e filtra os dados pela unidade referente no url ou caso não tenha id na url traz todos os objetos
        pk = self.kwargs.get('pk')
        if (self.request.user.groups.filter(name="biopsia").exists() or self.request.user.groups.filter(name="administrator").exists()):
            if Malote.objects.filter(unidadeSolicitante_id=pk):
                queryset = Malote.objects.filter(unidadeSolicitante_id=pk)
                return queryset
            else:
                queryset = Malote.objects.all()
                return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        groups = User.objects.filter(groups__name='malote').values_list('id')
        ultimaatualizacao = Malote.objects.filter(unidadeSolicitante_id=pk).values().filter(updatedBy_user_id__in=groups).exclude(
            Q(updatedBy_user_id__isnull=True) | Q(updatedBy_user_id__exact=0)).order_by('updated_at').last()
        if ultimaatualizacao != None:
            ultimaatualizacao = ultimaatualizacao.get('updated_at')
            horarioUltimaAtualizacao = ultimaatualizacao.__format__("%d/%m/%Y")
            context["horarioUltimaAtualizacao"] = horarioUltimaAtualizacao
            return context
        else:
            semRegistro = 'Sem registros'
            context["horarioUltimaAtualizacao"] = semRegistro
            return context


 # Lista de malotes para Alta Complexidade
class MaloteListAltaComplexidade(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/list-malotesAltaComplexidade.html"
    model = Malote
    group_required = [u"administrator", u"altaComplexidade"]
    success_url = reverse_lazy('list-malotes-all')

    def get_queryset(self):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(
                self.request, "Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return reverse_lazy('index')

        # verificar se o usuário é admin ou malote e filtra os dados pela unidade referente no url ou caso não tenha id na url traz todos os objetos
        pk = self.kwargs.get('pk')
        if (self.request.user.groups.filter(name="altaComplexidade").exists() or self.request.user.groups.filter(name="administrator").exists()):
            if Malote.objects.filter(unidadeSolicitante_id=pk):
                queryset = Malote.objects.filter(unidadeSolicitante_id=pk)
                return queryset
            else:
                queryset = Malote.objects.all()
                return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        groups = User.objects.filter(groups__name='malote').values_list('id')
        ultimaatualizacao = Malote.objects.filter(unidadeSolicitante_id=pk).values().filter(updatedBy_user_id__in=groups).exclude(
            Q(updatedBy_user_id__isnull=True) | Q(updatedBy_user_id__exact=0)).order_by('updated_at').last()
        if ultimaatualizacao != None:
            ultimaatualizacao = ultimaatualizacao.get('updated_at')
            horarioUltimaAtualizacao = ultimaatualizacao.__format__("%d/%m/%Y")
            context["horarioUltimaAtualizacao"] = horarioUltimaAtualizacao
            return context
        else:
            semRegistro = 'Sem registros'
            context["horarioUltimaAtualizacao"] = semRegistro
            return context
        
 # Lista de malotes para BERA


class MaloteListBERA(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/list-malotesBera.html"
    model = Malote
    group_required = [u"administrator", u"bera"]
    success_url = reverse_lazy('list-malotes-all')

    def get_queryset(self):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(
                self.request, "Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return reverse_lazy('index')

        # verificar se o usuário é admin ou malote e filtra os dados pela unidade referente no url ou caso não tenha id na url traz todos os objetos
        pk = self.kwargs.get('pk')
        if (self.request.user.groups.filter(name="bera").exists() or self.request.user.groups.filter(name="administrator").exists()):
            if Malote.objects.filter(unidadeSolicitante_id=pk):
                queryset = Malote.objects.filter(unidadeSolicitante_id=pk)
                return queryset
            else:
                queryset = Malote.objects.all()
                return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        groups = User.objects.filter(groups__name='malote').values_list('id')
        ultimaatualizacao = Malote.objects.filter(unidadeSolicitante_id=pk).values().filter(updatedBy_user_id__in=groups).exclude(
            Q(updatedBy_user_id__isnull=True) | Q(updatedBy_user_id__exact=0)).order_by('updated_at').last()
        if ultimaatualizacao != None:
            ultimaatualizacao = ultimaatualizacao.get('updated_at')
            horarioUltimaAtualizacao = ultimaatualizacao.__format__("%d/%m/%Y")
            context["horarioUltimaAtualizacao"] = horarioUltimaAtualizacao
            return context
        else:
            semRegistro = 'Sem registros'
            context["horarioUltimaAtualizacao"] = semRegistro
            return context


#Lista de malotes para as unidades
class MaloteListUnidade(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/list-malotesUnidade.html"
    model = Malote
    group_required = [u"administrativo", u"administrator"]


    def get_queryset(self):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(self.request,"Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return  reverse_lazy('index')

        #Filtra os dados referente a unidade do usuário 
        user = UserUnidade.objects.filter(user=self.request.user)        
        unidadeSolicitante = user[0].unidadeSolicitante
        if (self.request.user.groups.filter(name="administrativo").exists()):
            queryset = Malote.objects.filter(unidadeSolicitante_id=unidadeSolicitante.id)
            return queryset

    ####### Ultima atualização
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = UserUnidade.objects.filter(user=self.request.user)        
        unidadeSolicitante = user[0].unidadeSolicitante
        pk = unidadeSolicitante.id
        #Fazer lista de usuario com grupo malote
        groups = User.objects.filter(groups__name='malote').values_list('id')
        # ultimaatualizacao = Malote.objects.filter(unidadeSolicitante_id=pk).values().filter(Q(updatedBy_user_id=groups[0]) | Q(updatedBy_user_id=groups[1]) | Q(updatedBy_user_id=groups[2])).exclude(Q(updatedBy_user_id__isnull=True) | Q(updatedBy_user_id__exact=0)).order_by('updated_at').last()
        ultimaatualizacao = Malote.objects.filter(unidadeSolicitante_id=pk).values().filter(updatedBy_user_id__in=groups).exclude(Q(updatedBy_user_id__isnull=True) | Q(updatedBy_user_id__exact=0)).order_by('updated_at').last()
        # raise Exception(ultimaatualizacao)
        if ultimaatualizacao != None:
            ultimaatualizacao = ultimaatualizacao.get('updated_at')
            horarioUltimaAtualizacao = ultimaatualizacao.__format__("%d/%m/%Y")
            # raise Exception(horarioUltimaAtualizacao)
            context["horarioUltimaAtualizacao"] = horarioUltimaAtualizacao
            return context
        else: 
            semRegistro = 'Sem registros'
            context["horarioUltimaAtualizacao"] = semRegistro
            return context
        

#Consulta(Pesquisa)
class MaloteConsulta(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/consulta.html"
    model = Malote
    group_required = [u"administrativo", u"administrator"]

    def get_queryset(self):
        
        txt_pesquisa = self.request.GET.get('s')
        if txt_pesquisa: 
            malote = Malote.objects.filter(Q(sus__icontains=txt_pesquisa) | Q(nome__icontains=txt_pesquisa) | Q(dataNascimento__icontains=txt_pesquisa) | Q(etapa__icontains=txt_pesquisa))
       
        else:
            malote = Malote.objects.all()
        
        return malote


# class Malotesaidalist(GroupRequiredMixin, LoginRequiredMixin, ListView):
#     login_url = reverse_lazy('userLogin')
#     template_name = "malotes/list-malotesSaidaRegulacao.html"
#     model = MaloteSaida
#     group_required = [u"administrator", u"malote"]

class MaloteUnidadesSaidaList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesSaida/list-unidadesSaida.html"
    model = Malote
    group_required = [u"administrator", u"malote"]
    success_url = reverse_lazy('list-maloteUnidades')

    # Traz as unidades que possuem malotes, quantos malotes possui e data da ultima inserção
    def get_context_data(self, **kwargs):
        context = super(MaloteUnidadesSaidaList, self).get_context_data(**kwargs)
        unidades = MaloteSaida.objects.raw("SELECT u.id, u.nome, ms.unidadeSolicitante_id, (SELECT COUNT(ms.agendado)from malotes_malotesaida ms WHERE u.id = ms.unidadeSolicitante_id and ms.agendado = 0)  aguardandoAgendamento FROM malotes_malotesaida ms INNER JOIN malotes_malote me ON ms.malote_id=me.id INNER JOIN cadastros_unidadesolicitante u ON u.id=ms.unidadeSolicitante_id GROUP BY u.nome;")
        context['unidades'] = unidades
        return context


class MaloteSaidalistRegulacao(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesSaida/list-malotesSaidaRegulacao.html"
    model = MaloteSaida
    group_required = [u"administrator", u"malote"]

    def get_queryset(self, **kwargs):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(self.request,"Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return  reverse_lazy('index')
        
        idUnidade = self.kwargs.get('pk')
        #verificar se o usuário é admin ou malote e filtra os dados pela unidade referente no url ou caso não tenha id na url traz todos os objetos
        if (self.request.user.groups.filter(name="malote").exists() or self.request.user.groups.filter(name="administrator").exists()):
            if idUnidade != None:
                queryset = MaloteSaida.objects.raw(
                    "SELECT  ms.id as maloteId, me.nome,me.dataNascimento,me.sus,me.classificacao,me.etapa,me.statusProcesso,me.justificativa,ms.*, ue.nome as localAgendamento FROM malotes_malotesaida ms INNER JOIN malotes_malote me ON ms.malote_id = me.id INNER JOIN cadastros_unidadesolicitante us ON ms.unidadeSolicitante_id = us.id LEFT JOIN cadastros_unidadeexecutante ue ON ms.unidadeExecutante_id = ue.id WHERE us.id = %s;", [idUnidade])
                return queryset
            else:
                queryset = MaloteSaida.objects.raw("SELECT  ms.id as maloteId, me.nome,me.dataNascimento,me.sus,me.classificacao,me.etapa,me.statusProcesso,me.justificativa,ms.*, ue.nome as localAgendamento FROM malotes_malotesaida ms INNER JOIN malotes_malote me ON ms.malote_id = me.id INNER JOIN cadastros_unidadesolicitante us ON ms.unidadeSolicitante_id = us.id LEFT JOIN cadastros_unidadeexecutante ue ON ms.unidadeExecutante_id = ue.id;")
                return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Envia o id da unidade que esta sendo acessada
        pk = self.kwargs.get('pk')
        context["unidadePk"] = pk

        #Envia o contexto com o nome da unidade 
        filtroUnidade = UnidadeSolicitante.objects.filter(id=pk).values('nome')
        if pk != None:
            nomeUnidade = filtroUnidade[0].get('nome')
            context['nomeUnidade'] = nomeUnidade + ' - Malotes'
        else:
            context['nomeUnidade'] = 'Todos os malotes'
        return context
    

class MaloteSaidaListUnidade(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesSaida/list-maloteSaidaUnidade.html"
    model = MaloteSaida
    group_required = [u"administrativo", u"administrator"]

    def get_queryset(self):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(
                self.request, "Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return reverse_lazy('index')

        # Filtra os dados referente a unidade do usuário
        user = UserUnidade.objects.filter(user=self.request.user)
        unidadeSolicitante = user[0].unidadeSolicitante
        if (self.request.user.groups.filter(name="administrativo").exists()):
        # raise Exception(unidadeSolicitante)
            queryset = MaloteSaida.objects.raw(
                "SELECT ms.id as maloteId, me.*,ms.*, ue.nome as localAgendamento FROM malotes_malotesaida ms INNER JOIN malotes_malote me ON ms.malote_id = me.id INNER JOIN cadastros_unidadesolicitante us ON me.unidadeSolicitante_id = us.id LEFT JOIN cadastros_unidadeexecutante ue ON ms.unidadeExecutante_id = ue.id WHERE us.id = %s;", [unidadeSolicitante.id])
            return queryset

##################################################### CREATE ###########################################################################


class MaloteCreateRegulcao(GroupRequiredMixin, LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/formRegulacao.html"
    model = Malote
    group_required = [u"administrator", u"malote"]
    fields = ['nome', 'dataNascimento', 'procedimento', 'unidadeSolicitante', 'tipo', 'classificacao',
              'cross', 'sus', 'sigtap', 'cid', 'statusProcesso', 'justificativa', 'observacaoRegulacao']
    ####### Voltar para a página referente a unidade ######
    def form_valid(self, form):
        unidade = form.cleaned_data['unidadeSolicitante']
        success_url = reverse_lazy('list-malotes-regulacao', pk=unidade.id)
        return success_url

    # def get_queryset(self):
    #     procedimento = DicionarioDeProcedimentos.objects.get('nomenclatura')
    #     return procedimento

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        if form.instance.statusProcesso == 7:
            form.instance.statusTempo = datetime.now()
            form.instance.statusUser = self.request.user
        form.instance.etapa = 1 #####VER COM A JULIA, se ela coloca vai direto pra 2? !!!!!!
        url = super().form_valid(form)
        return url


class MaloteCreateUnidade(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/formUnidade.html"
    model = Malote
    group_required = [u"administrator", u"administrativo"]
    fields = ['nome', 'dataNascimento', 'procedimento', 'tipo',
              'classificacao', 'cross', 'sus', 'cid', 'observacaoUnidade']
    success_url = reverse_lazy('list-malotes-unidade')


    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        form.instance.unidadeSolicitante_id = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.id
        form.instance.etapa = 1
        url = super().form_valid(form)
        return url


class MaloteSaidaCreate(GroupRequiredMixin,LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesSaida/formCreateRegulacaoSaida.html"
    model = MaloteSaida
    group_required = [u'administrator', u'malote']
    fields = ['malote', 'agendamentoData', 'unidadeExecutante', 'procedimento', 'unidadeSolicitante']
    
    def form_valid(self, form):
        self.form = form
        malote = self.form.cleaned_data['malote'] 
        if malote.unidadeSolicitante_id == 47: # Id 47 se refere ao AME
            unidadeSolicitante = self.form.cleaned_data['unidadeSolicitante'].pk
        else:
            unidadeSolicitante = malote.unidadeSolicitante_id
            form.instance.unidadeSolicitante_id = unidadeSolicitante
        unidadeSolicitante = int(unidadeSolicitante)
        # raise Exception(unidadeSolicitante)
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url(unidadeSolicitante)) 


    def get_success_url(self, unidadeSolicitante):
        success_url = reverse_lazy('list-malotesSaida-regulacao', kwargs={"pk": unidadeSolicitante})
        return success_url


##################################################### UPDATE ###########################################################################

class MaloteUpdateRegulcao(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/formRegulacao.html"
    model = Malote
    group_required = [u"administrator", u"malote"]
    fields = ['nome', 'dataNascimento', 'procedimento', 'tipo', 'classificacao', 'cross', 'sus', 'cid', 'sigtap','statusProcesso', 'justificativa', 'observacaoRegulacao', 'etapa']
    ####### Voltar para a página referente a unidade ######
    def form_valid(self, form):
        unidade = form.cleaned_data['unidadeSolicitante']
        success_url = reverse_lazy('list-malotes-regulacao', pk=unidade.id)
        return success_url

    def form_valid(self, form):
        form.instance.updatedBy_user = self.request.user
        if form.instance.statusProcesso == 7:
            form.instance.statusData = datetime.now()
            form.instance.statusUser = self.request.user
        # if (form.instance.etapa == 2 and self.request.user.groups.filter(name="administrativo").exists()):
        #     form.instance.etapa = 3
        url = super().form_valid(form)
        return url    
    
class MaloteUpdateMedico(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/formMedico.html"
    model = Malote
    group_required = [u"administrator", u"medicos"]
    fields = ['nome', 'dataNascimento', 'tipo', 'observacaoMedico', 'classificacao', 'sigtap', 'sus', 'cid', 'etapa'] 
    success_url = reverse_lazy('list-malotes-medico')

    def form_valid(self, form):
        form.instance.updatedBy_user = self.request.user
        form.instance.medicoRegulador = self.request.user
        form.instance.etapa = 3
        url = super().form_valid(form)
        return url    
    

class MaloteUpdateAdmin(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/formRegulacao.html"
    model = Malote
    group_required = [u"administrator"]
    fields = ['nome', 'dataNascimento', 'procedimento', 'tipo', 'classificacao', 'cross',
              'sus', 'cid', 'sigtap', 'statusProcesso', 'justificativa', 'observacaoRegulacao','etapa']
    ####### Voltar para a página referente a unidade ######
    def form_valid(self, form):
        unidade = form.cleaned_data['unidadeSolicitante']
        success_url = reverse_lazy('list-malotes-regulacao', pk=unidade.id)
        return success_url

    def form_valid(self, form):
        form.instance.updatedBy_user = self.request.user
        form.instance.updated_at = datetime.now()
        url = super().form_valid(form)
        return url
    

class MaloteUpdateDevolucao(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/formDevolucao.html"
    model = Malote
    group_required = [u"administrator", u"bera", u"altaComplexidade", u"biopsia", u"hospitalDeOlhos", u"ame", u"cirurgia"]
    fields = ['observacaoPrestadores']
    def get_success_url(self):
        if self.request.user.groups.filter(name="bera").exists():
            success_url = reverse_lazy('list-malotes-Bera')
            return success_url
        elif self.request.user.groups.filter(name="altaComplexidade").exists():
            success_url = reverse_lazy('list-malotes-AltaComplexidade')
            return success_url
        elif self.request.user.groups.filter(name="cirurgia").exists():
            success_url = reverse_lazy('list-malotes-Cirurgia')
            return success_url
        elif self.request.user.groups.filter(name="biopsia").exists():
            success_url = reverse_lazy('list-malotes-Biopsia')
            return success_url
        elif self.request.user.groups.filter(name="hospitalDeOlhos").exists():
            success_url = reverse_lazy('list-malotes-HospitalDeOlhos')
            return success_url
        elif self.request.user.groups.filter(name="ame").exists():
            success_url = reverse_lazy('list-malotes-Ame')
            return success_url
        else:
            success_url = reverse_lazy('list-maloteUnidadesSaida')   
            return success_url

    def form_valid(self, form):
        form.instance.updatedBy_user = self.request.user
        form.instance.updated_at = datetime.now()
        form.instance.etapa = 3
        maloteid = self.kwargs.get('pk')
        observacao = self.request.POST.get('observacaoPrestadores')
        acao = 'Malote devolvido para etapa 3'
        maloteLog(maloteid, acao, self.request.user.pk, observacao)
        url = super().form_valid(form)
        return url

class MaloteSaidaUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesSaida/formRegulacaoSaida.html"
    model = MaloteSaida
    group_required = [u'administrator',u'malote']
    fields = ['agendamentoData', 'procedimento',
              'unidadeExecutante', 'procedimento', 'unidadeSolicitante']
    ####### Voltar para a página referente a unidade ###### 
    def get_success_url(self):
        unidade = self.request.POST.get('unidadeSolicitante')
        success_url = reverse_lazy('list-malotesSaida-regulacao', kwargs={"pk": unidade})
        return success_url

    def form_valid(self, form):
        form.instance.updatedBy_user = self.request.user
        form.instance.updated_at = datetime.now()
        form.instance.dataEncaminhado = datetime.now()
        form.instance.agendado = 1
        url = super().form_valid(form)
        return url

    #por nome e nascimento no forms e fazer botao para retornar encaminhamento errado para julia
    def get_context_data(self, **kwargs):
        maloteSaidaId = self.kwargs.get('pk')
        context = super(MaloteSaidaUpdate, self).get_context_data(**kwargs)
        pacientes = Malote.objects.raw("Select me.id, ms.id, me.nome, me.dataNascimento from malotes_malote me inner join malotes_malotesaida ms on me.id = ms.malote_id where ms.malote_id=%s;", [maloteSaidaId])
        context['pacientes'] = pacientes
        return context

##################################################### DELETE ###########################################################################

class MaloteDeleteAdmin(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    model = Malote
    group_required = [u"administrator"]
    template_name = "malotesEntrada/form-excluir.html"
    success_url = reverse_lazy('list-malotes-all')

    # def gerarLog(self, *args, **kwargs ):
    #     id_malote = self.kwargs.get("pk")
    #     print("###############################################################################################")
    #     print(id_malote)
    #     print("###############################################################################################")
    #     maloteLog()


# class Malotesaidadelete():
#     login_url = reverse_lazy('userLogin')
#     model = MaloteSaida
#     group_required = [u"administrator"]
#     template_name = "malotes/form-excluir.html"
#     success_url = reverse_lazy("list-malote-saída")


#################################################### Funções ###########################################################################

def maloteLog(malotes,acao,usuarioId, observacao = None):
    # arrayMalotesLog = []
    idUsuario = usuarioId
    idUsuario = int(idUsuario)
    # objMalote = MaloteLog(
    #     malote_id=malotes,
    #     acao = acao,
    #     createdBy_user_id = usuarioId,
    #     observacao = observacao,
    # )
    # arrayMalotesLog.append(objMalote)
    if observacao == None:
        MaloteLog.objects.create(
            malote_id=malotes,
            acao=acao,
            createdBy_user_id=idUsuario,
        )
    else:
        MaloteLog.objects.create(
            malote_id=malotes,
            acao=acao,
            createdBy_user_id=idUsuario,
            observacao=observacao,
        )


def maloteCreateSaida(malotesId, etapa, idUsuario, unidadeSolicitante):
    arrayMalotesSaida = []
    arrayMalotesEntrada = []
    # Se a etapa for 10 o malote ira para o malote de saída
    for maloteId in malotesId:
        procedimento = Malote.objects.filter(pk=maloteId).values('procedimento_id')
        # Será criado um objeto do malote de entrada no malote de saída utilizando seu ID
        objSaida = MaloteSaida(
            malote_id=maloteId,
            createdBy_user_id = idUsuario,
            unidadeSolicitante_id = unidadeSolicitante, 
            procedimento_id = procedimento,
        )
        # Os malotes de saida criados serão armazenados no array
        arrayMalotesSaida.append(objSaida)

        # Os malotes de entrada selecionados terão sua etapa alterada para "Malote de saída", armazenando o uptaded_by_user.
        objEntrada = Malote(
            pk=maloteId,
            etapa=etapa,
            statusProcesso=7,
            updatedBy_user_id=idUsuario,
        )
        # Os malotes de entrada serão adicionados ao array demalotes de entrada
        arrayMalotesEntrada.append(objEntrada)
    MaloteSaida.objects.bulk_create(arrayMalotesSaida)
    Malote.objects.bulk_update(arrayMalotesEntrada, ['etapa','statusProcesso', 'updatedBy_user_id'])

def maloteUpdateEtapaUmRegulacao(request):
    malotesId = request.POST.getlist("malotesSelecionados")
    etapa = request.POST.get("etapa")
    unidadePk = request.POST.get("unidadePk")
    idUsuario = request.user.pk
    idUsuario = int(idUsuario)
    # raise Exception(idUsuario)
    arrayMalotesEntrada = []
    if etapa == '10':
        maloteCreateSaida(malotesId, etapa, idUsuario, unidadePk)
    else:
        for maloteId in malotesId:
            obj = Malote(
                pk=maloteId,
                statusProcesso=7,
                etapa=etapa,
                statusData=datetime.now(),
                statusUser_id=idUsuario,
                updatedBy_user_id=idUsuario,
            )
            arrayMalotesEntrada.append(obj)
        # Se a etapa for 10(Para o malote de saída) os dois arrays criados serão utilizados para criar entradas no malote de saída e atualizar as existentes no malote de entrada
        Malote.objects.bulk_update(arrayMalotesEntrada, ['etapa', 'statusProcesso', 'statusData', 'statusUser_id', 'updatedBy_user_id'])
    if unidadePk != 'None':
        return HttpResponseRedirect(reverse('list-malotes-regulacao', args=[unidadePk]))
    else:
        return HttpResponseRedirect(reverse('list-malotes-all'))

def maloteUpdateEtapaTresRegulacao(request):
    malotesId = request.POST.getlist("malotesSelecionados")
    etapa = request.POST.get("etapa")
    unidadePk = request.POST.get("unidadePk")
    idUsuario = request.user.pk
    idUsuario = int(idUsuario)
    arrayMalotes = []
    for maloteId in malotesId:
        #Faz o queryset
        querysetScanner = Malote.objects.filter(id=maloteId).values('scanner')
        #Pega o id no array do querry set para enviar ao objeto
        statusScanner = querysetScanner[0]['scanner']
        if statusScanner == True:
            obj = Malote(
                pk=maloteId,
                etapa=etapa,
                updatedBy_user_id=idUsuario
            )
            arrayMalotes.append(obj)
        else: 
            messages.error(request, "Não foi possivel encaminhar, um ou mais malotes ainda não foram scanneados.")
            if unidadePk != 'None':
                return HttpResponseRedirect(reverse('list-malotes-regulacao', args=[unidadePk]))
            else:
                return HttpResponseRedirect(reverse('list-malotes-all'))
        # raise Exception(unidadePk)
    Malote.objects.bulk_update(arrayMalotes, ['etapa', 'updatedBy_user_id'])
    if unidadePk != 'None':
        return HttpResponseRedirect(reverse('list-malotes-regulacao', args=[unidadePk]))
    else:
        return HttpResponseRedirect(reverse('list-malotes-all'))

#Não utilizado, atualmente medico não seleciona varios, atualização ja ocorre no update
def maloteUpdateEtapaMedico(request):
    malotesId = request.POST.getlist("malotesSelecionados")
    etapa = request.POST.get("etapa")
    idUsuario = request.user.pk
    idUsuario = int(idUsuario)
    arrayMalotes = []
    for maloteId in malotesId:
      obj = Malote(
          pk=maloteId,
          etapa = 3,
          updatedBy_user_id=idUsuario,
          medicoRegulador_id=idUsuario
      )
      arrayMalotes.append(obj)

    # raise Exception(unidadePk)
    Malote.objects.bulk_update(arrayMalotes, ['etapa', 'updatedBy_user_id','medicoRegulador_id'])
    return HttpResponseRedirect(reverse('list-malotes-medico'))

def maloteUpdateScanner(request):
    maloteId = request.POST.get("id")
    idUsuario = request.user.pk
    querysetScanner = Malote.objects.filter(id=maloteId).values('scanner')
    statusScanner = querysetScanner[0]['scanner']
    # raise Exception(statusScanner)

    if statusScanner == False:
        obj = Malote.objects.get(pk=maloteId)
        obj.scanner = True
        obj.dataScanner = datetime.now()
        obj.updatedBy_user_id = idUsuario
        obj.save()
    elif statusScanner == True:
        obj = Malote.objects.get(pk=maloteId)
        obj.scanner = False
        obj.dataScanner = datetime.now()
        obj.updatedBy_user_id = idUsuario
        obj.save()

    querysetCheckbox = Malote.objects.filter(id=maloteId).values('scanner')
    statusCheckbox = querysetCheckbox[0]['scanner']

    return JsonResponse({'id': maloteId, 'status': statusCheckbox}, safe=False)



def maloteUpdateRecebidoPelaUnidade(request):
    maloteId = request.POST.get("id")
    idUsuario = request.user.pk
    idUsuario = int(idUsuario)
    querysetRecebido = MaloteSaida.objects.filter(id=maloteId).values('recebidoPelaUnidade')
    statusRecebido = querysetRecebido[0]['recebidoPelaUnidade']
    # raise Exception(idUsuario)

    if statusRecebido == False:
        obj = MaloteSaida.objects.get(pk=maloteId)
        obj.recebidoPelaUnidade = True
        obj.recebido_at = datetime.now()
        obj.recebidoBy_user_id = idUsuario
        obj.updatedBy_user_id = idUsuario
        obj.save()
    elif statusRecebido == True:
        obj = MaloteSaida.objects.get(pk=maloteId)
        obj.recebidoPelaUnidade = False
        obj.recebido_at = datetime.now()
        obj.updatedBy_user_id = idUsuario
        obj.save()

    querysetCheckbox = MaloteSaida.objects.filter(id=maloteId).values('recebidoPelaUnidade')
    statusCheckbox = querysetCheckbox[0]['recebidoPelaUnidade']

    return JsonResponse({'id': maloteId, 'status': statusCheckbox}, safe=False)



def maloteUpdateAme(request):
    malotesId = request.POST.getlist("malotesSelecionados")
    etapa = request.POST.get("etapa")
    unidadePk = request.POST.get("unidadePk")
    idUsuario = request.user.pk
    idUsuario = int(idUsuario)
    arrayMalotes = []
    if etapa == '10':
        maloteCreateSaida(malotesId, etapa, idUsuario, unidadePk)
    else:
        for maloteId in malotesId:
            obj = Malote(
                pk=maloteId,
                etapa=etapa,
                updatedBy_user_id=idUsuario
            )
            arrayMalotes.append(obj)
            # raise Exception(unidadePk)
        Malote.objects.bulk_update(arrayMalotes, ['etapa', 'updatedBy_user_id'])
    return HttpResponseRedirect(reverse('list-malotes-Ame'))

def maloteUpdateBiopsia(request):
    malotesId = request.POST.getlist("malotesSelecionados")
    etapa = request.POST.get("etapa")
    unidadePk = request.POST.get("unidadePk")
    idUsuario = request.user.pk
    idUsuario = int(idUsuario)
    arrayMalotes = []
    if etapa == '10':
        maloteCreateSaida(malotesId, etapa, idUsuario, unidadePk)
    else:
        for maloteId in malotesId:
            obj = Malote(
                pk=maloteId,
                etapa=etapa,
                updatedBy_user_id=idUsuario
            )
        arrayMalotes.append(obj)
        Malote.objects.bulk_update(arrayMalotes, ['etapa', 'updatedBy_user_id'])
    return HttpResponseRedirect(reverse('list-malotes-Biopsia'))



def maloteUpdateHospitalDeOlhos(request):
    malotesId = request.POST.getlist("malotesSelecionados")
    etapa = request.POST.get("etapa")
    unidadePk = request.POST.get("unidadePk")
    idUsuario = request.user.pk
    idUsuario = int(idUsuario)
    arrayMalotes = []
    if etapa == '10':
        maloteCreateSaida(malotesId, etapa, idUsuario, unidadePk)
    else:
        for maloteId in malotesId:
            obj = Malote(
                pk=maloteId,
                etapa=etapa,
                updatedBy_user_id=idUsuario
            )
            arrayMalotes.append(obj)
        Malote.objects.bulk_update(arrayMalotes, ['etapa', 'updatedBy_user_id'])
    return HttpResponseRedirect(reverse('list-malotes-HospitalDeOlhos'))




def maloteUpdateCirurgia(request):
    malotesId = request.POST.getlist("malotesSelecionados")
    etapa = request.POST.get("etapa")
    unidadePk = request.POST.get("unidadePk")
    idUsuario = request.user.pk
    idUsuario = int(idUsuario)
    arrayMalotes = []
    if etapa == '10':
        maloteCreateSaida(malotesId, etapa, idUsuario, unidadePk)
    else:
        for maloteId in malotesId:
            obj = Malote(
                pk=maloteId,
                etapa=etapa,
                updatedBy_user_id=idUsuario
            )
            arrayMalotes.append(obj)
            # raise Exception(unidadePk)
        Malote.objects.bulk_update(arrayMalotes, ['etapa', 'updatedBy_user_id'])
    return HttpResponseRedirect(reverse('list-malotes-Cirurgia'))


def maloteUpdateAltaComplexidade(request):
    malotesId = request.POST.getlist("malotesSelecionados")
    etapa = request.POST.get("etapa")
    unidadePk = request.POST.get("unidadePk")
    idUsuario = request.user.pk
    idUsuario = int(idUsuario)
    arrayMalotes = []
    if etapa == '10':
        maloteCreateSaida(malotesId, etapa, idUsuario, unidadePk)
    else:
        for maloteId in malotesId:
            obj = Malote(
                pk=maloteId,
                etapa=etapa,
                updatedBy_user_id=idUsuario
            )
            arrayMalotes.append(obj)
        Malote.objects.bulk_update(arrayMalotes, ['etapa', 'updatedBy_user_id'])
    return HttpResponseRedirect(reverse('list-malotes-AltaComplexidade'))


################################################
######### CRUD MALOTE SIMPLIFICADO #############
################################################

class UnidadeList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/unidadeList.html"
    model = Malote
    group_required = [u"administrativo", u"administrator"]

    def get_queryset(self):
        #verifica se o usuário esta em uma unidade
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(self.request,"Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return reverse_lazy('index')
        #Filtra os dados referente a unidade do usuário 
        user = UserUnidade.objects.filter(user=self.request.user)        
        unidadeOrigem = user[0].unidadeSolicitante
        
        # queryset = Malote.objects.filter(unidadeOrigem_id=unidadeOrigem.id).order_by("-created_at") & Malote.objects.filter(unidadeDestino_id=unidadeOrigem.id).order_by("-created_at")
        # queryset = Malote.objects.raw("select * from malotes_malote where unidadeOrigem_id=34 and unidadeDestino_id=1")
        queryset = Malote.objects.filter(unidadeDestino=unidadeOrigem.pk)
        # raise Exception(queryset)
        return queryset

    ## VERIFICAR 15/02/2024
    ####### Ultima atualização
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = UserUnidade.objects.filter(user=self.request.user)        
        unidadeSolicitante = user[0].unidadeSolicitante
        pk = unidadeSolicitante.id
        #Fazer lista de usuario com grupo malote
        groups = User.objects.filter(groups__name='malote').values_list('id')
        # ultimaatualizacao = Malote.objects.filter(unidadeSolicitante_id=pk).values().filter(Q(updatedBy_user_id=groups[0]) | Q(updatedBy_user_id=groups[1]) | Q(updatedBy_user_id=groups[2])).exclude(Q(updatedBy_user_id__isnull=True) | Q(updatedBy_user_id__exact=0)).order_by('updated_at').last()
        ultimaatualizacao = Guia.objects.filter(unidadeOrigem_id=pk).values().filter(updatedBy_user_id__in=groups).exclude(Q(updatedBy_user_id__isnull=True) | Q(updatedBy_user_id__exact=0)).order_by('updated_at').last()
        
               
        context['guias'] = Guia.objects.filter(unidadeOrigem_id=pk)
        context['malotesOrigem'] = Malote.objects.filter(unidadeOrigem_id=pk).order_by("-created_at")
        context['malotesDestino'] = Malote.objects.filter(unidadeDestino_id=pk).order_by("-created_at")
        context['totalPendentes'] = Malote.objects.filter(status=1).filter(unidadeOrigem=pk).count()
        context['totalEnviados'] = Malote.objects.filter(status=2).filter(unidadeOrigem=pk).count()
        context['totalRecebidos']= Malote.objects.filter(status=3).filter(unidadeDestino=pk).count()
        context['totalDevolvidos']= Malote.objects.filter(status=4).filter(unidadeDestino=pk).count()
        context['unidades'] = UnidadeSolicitante.objects.all()
        
        
        ##REVISAR ESTA VERIFICAÇÃO DE DATAS
        # raise Exception(ultimaatualizacao)
        if ultimaatualizacao != None:
            ultimaatualizacao = ultimaatualizacao.get('updated_at')
            horarioUltimaAtualizacao = ultimaatualizacao.__format__("%d/%m/%Y")
            # raise Exception(horarioUltimaAtualizacao)
            context["horarioUltimaAtualizacao"] = horarioUltimaAtualizacao
            return context
        else: 
            semRegistro = 'Sem registros'
            context["horarioUltimaAtualizacao"] = semRegistro
            return context
 
class UnidadeGuiaCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/formUnidadeCadastroMalote.html"
    model = Guia
    group_required = [u"administrator", u"administrativo"]
    fields = []    
    success_url = reverse_lazy('unidadeList')   

    def post(self, request, *args, **kwargs):
        try:
            # Malote.objects.values('id').get_or_create(created_at__contains=date.today())[0]['id']
            #verificar o id do malote e também da unidade
            unidadeOrigem = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante
            malote_id = Malote.objects.values('id').filter(unidadeOrigem=unidadeOrigem.id).filter(created_at__contains=date.today())
            
            
            if not malote_id:
                malote = Malote(
                    createdBy_user = self.request.user,
                    unidadeOrigem_id = unidadeOrigem.id
                )
                malote.save()
                
                guia = Guia.objects.create(
                    nome = self.request.POST.get('nome'),
                    unidadeOrigem_id = unidadeOrigem.id,
                    dataNascimento = self.request.POST.get('dataNascimento'),
                    sus = self.request.POST.get('sus'),
                    cross = self.request.POST.get('cross'),
                    procedimento_id = self.request.POST.get('procedimento'),
                    tipo = self.request.POST.get('tipo'),
                    classificacao = self.request.POST.get('classificacao'),
                    observacaoUnidade = self.request.POST.get('observacaoUnidade'),
                    createdBy_user_id = self.request.user.pk,
                    malote_id = malote.id,
                )
            else:
                guia = Guia(
                nome = self.request.POST.get('nome'),
                unidadeOrigem_id = unidadeOrigem.id,
                dataNascimento = self.request.POST.get('dataNascimento'),
                sus = self.request.POST.get('sus'),
                cross = self.request.POST.get('cross'),
                procedimento_id = self.request.POST.get('procedimento'),
                tipo = self.request.POST.get('tipo'),
                classificacao = self.request.POST.get('classificacao'),
                observacaoUnidade = self.request.POST.get('observacaoUnidade'),
                createdBy_user_id = self.request.user.pk,
                malote_id = malote_id,
                )
            
            guia.save()
            messages.success(self.request, 'Guia salva no malote com sucesso!')
        except:
            messages.error(self.request, 'Erro ao salvar a guia. Preencha todos os campos corretamente!')
        
        return redirect(reverse("unidadeList", kwargs={}))
    
    def get_context_data(self, **kwargs):
        context = super(UnidadeGuiaCreate, self).get_context_data(**kwargs)
        pacientes = Paciente.objects.all()
        procedimentos = DicionarioDeProcedimentos.objects.filter(isVisible=True)
        context['procedimentos'] = procedimentos
        context['pacientes'] = pacientes
        context['classificacoes'] = Guia.classificacao_choices
        context['tipos'] = Guia.tipo_choices
        return context

class MaloteUnidadesEntrada(GroupRequiredMixin,  LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/unidadesEntrada.html"
    model = Guia
    group_required = [u"administrator", u"malote"]
    # permission_required = ("malote.view_malote")
    success_url = reverse_lazy('unidadesEntrada')

    #Traz as unidades que possuem malotes, quantos malotes possui e data da ultima inserção
    def get_context_data(self, **kwargs):
        context = super(MaloteUnidadesEntrada, self).get_context_data(**kwargs)
        unidades = Guia.objects.raw("SELECT u.id, m.unidadeOrigem_id, m.id, u.nome, m.created_at AS ultimaInsercao, (SELECT COUNT(m.etapa) from malotes_guia m WHERE u.id=m.unidadeOrigem_id and m.etapa=1) AS Recebidos, (SELECT COUNT(m.etapa) from malotes_guia m WHERE u.id=m.unidadeOrigem_id and m.etapa=3) AS aguardandoEncaminhamento,COUNT(m.unidadeOrigem_id) AS quantidade FROM cadastros_unidadesolicitante u INNER JOIN malotes_guia m ON  u.id=m.unidadeOrigem_id GROUP BY u.nome")
        context['unidades'] = unidades
        return context

class MaloteUpdateUnidade(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    template_name = "malotesEntrada/formUnidadeCadastroMalote.html"
    model = Guia
    group_required = [u"administrator", u"administrativo"]
    fields = ['nome', 'dataNascimento', 'tipo', 'classificacao', 'cross', 'sus', 'observacaoUnidade']
    success_url = reverse_lazy('list-maloteUnidades')

    def get(self, request, *args, **kwargs):
        self.referer = request.META.get("HTTP_REFERER", "")
        guia_id = kwargs['pk']
        guia = Guia.objects.filter(pk=guia_id) 
        procedimentos = DicionarioDeProcedimentos.objects.filter(isVisible=1)
        classificacoes = Guia.classificacao_choices
        tipos = Guia.tipo_choices        
        return render(request, 'malotesEntrada/formUnidadeCadastroMalote.html', {"guia": guia, "procedimentos": procedimentos, "classificacoes": classificacoes, "tipos":tipos})

    def post(self, request, *args, **kwargs):
        try:
            guia = Guia.objects.filter(pk=kwargs['pk'])[0]
            # raise Exception(guia)
            guia.nome = self.request.POST.get('nome')
            guia.dataNascimento = self.request.POST.get('dataNascimento')
            guia.sus = self.request.POST.get('sus')
            guia.cross = self.request.POST.get('cross')
            guia.procedimento_id = self.request.POST.get('procedimento')
            guia.tipo = self.request.POST.get('tipo')
            guia.classificacao = self.request.POST.get('classificacao')
            guia.observacaoUnidade = self.request.POST.get('observacaoUnidade')
            guia.createdBy_user_id = self.request.user.pk
            # guia.save(update_fields=['nome', 'dataNascimento', 'sus', 'cross', 'procedimento', 'tipo', 'classificacao', 'observacaoUnidade', 'createdBy_user'])        
            guia.save()
            # raise Exception(guia)
            messages.success(self.request, 'Guia salva no malote com sucesso!')
        except:
            messages.error(self.request, 'Erro ao salvar a guia. Preencha todos os campos corretamente!')
            
        return redirect('unidadeList')
        
    def form_valid(self, form):
        form.instance.updatedBy_user = self.request.user
        url = super().form_valid(form)
        return url

def EnviarMaloteDestino(request):    
    # raise Exception(request.POST.get('unidadeDestino'))
    malote = Malote.objects.get(pk=request.POST.get('malote_id'))
    malote.unidadeDestino_id = request.POST.get('unidadeDestino') 
    malote.status = 2
    malote.dataEnvio = datetime.now()
    malote.sentBy_user_id = request.user.pk
    malote.save()
    return redirect('unidadeList')
    