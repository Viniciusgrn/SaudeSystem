import csv
import io

import pandas as pd
import datetime                                
from django.utils.timezone import utc
from audioop import reverse
from typing import Container
from wsgiref.simple_server import server_version
from django.http import JsonResponse, HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import ProtectedError
from datetime import date, timedelta
from django.utils import timezone
from django.db import connection
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.core.serializers import serialize
import json
from django.forms.models import model_to_dict

from .models import Importar, Paciente, UnidadeSolicitante, UnidadeExecutante, Procedimento, Unificacao, VagaOfertada, Permuta, UserUnidade, HistoricoImportacao
from relatorios.models import DicionarioDeProcedimentos
from unidadeDemanda.models import UnidadeDemanda
from estabelecimentos.models import Estabelecimento
from esus.models import Ta_Cidadao

from django.urls import reverse_lazy

from .forms import PermutarForm
from braces.views import GroupRequiredMixin
from django import forms


# Create your views here

################## Create ################
class PacienteCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter", u"administrativo"]
    model = Paciente
    fields = ['cns', 'estabelecimento','numeroProntuario', 'nome', 'dataNascimento', 'sexo', 'cpf', 'telefonePrincipal', 'telefoneRecado', 'nomeResponsavel', "nomePai", "nomeDaMae", "nomeSocial","rg","orgaoEmissor","estadoEmissor","dataEmissao","racaCor","tipoSanguineo"]
    template_name = 'cadastros/formPaciente.html'
    success_url = reverse_lazy('listar-paciente')
    
    def get_context_data(self, **kwargs):
        context = super(PacienteCreate, self).get_context_data(**kwargs) # get the default context data        
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(self.request,"Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            context['userUnidade'] = False
        else:
            context['userUnidade'] = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.pk
            context['tituloform'] = "Editar Paciente"
        return context
        
    def form_valid(self, form):
        #verifica se o usuário é do callcenter
        if (self.request.user.groups.filter(name = "callcenter").exists()):
            #obtem altura e peso do form e converte para float concatenando
            altura = float(str(self.request.POST.get('alturaMetros')) + "." + str(self.request.POST.get('alturaCentimetros')))
            peso = float(str(self.request.POST.get('pesoKg')) + "." + str(self.request.POST.get('pesoGrama')))            
            try:
                #instancia altura e peso caso sejam maior do que 0.0
                if(altura is not None and altura >= 0.0 and peso is not None and peso >= 0.0):
                    #insere no form em formato string
                    form.instance.altura = str(self.request.POST.get('alturaMetros')) + "." + str(self.request.POST.get('alturaCentimetros'))
                    form.instance.peso = str(self.request.POST.get('pesoKg')) + "." + str(self.request.POST.get('pesoGrama'))
                else:
                    raise ValueError("Verifique se o peso ou altura foram preenchidos.")
            except ValueError as e:
                messages.error(self.request, e)
                return super().form_invalid(form)
        else:
            #usuarios que não são do callcenter
            try:
                #logica para altura
                altura = float(str(self.request.POST.get('alturaMetros')) + "." + str(self.request.POST.get('alturaCentimetros')))
                if(altura is not None and altura >= 0.24):
                    form.instance.altura = str(self.request.POST.get('alturaMetros')) + "." + str(self.request.POST.get('alturaCentimetros'))
                else:                
                    raise ValueError("Preencha a altura corretamente.")
            except TypeError as e:
                messages.error(self.request, e)
                return super().form_invalid(form)
            
            except ValueError as e:
                messages.error(self.request, e)
                return super().form_invalid(form)

            try:
                #logica para peso
                peso = float(str(self.request.POST.get('pesoKg')) + "." + str(self.request.POST.get('pesoGrama')))
                if(peso is not None and peso >= 0.212):
                    form.instance.peso = str(self.request.POST.get('pesoKg')) + "." + str(self.request.POST.get('pesoGrama'))
                else:                
                    raise ValueError("Preencha o peso corretamente.")
            except ValueError as e:
                messages.error(self.request, e)
                return super().form_invalid(form)
        
        #dados do usuário que cadastrou
        form.instance.createdBy_user = self.request.user
        form.instance.updatedBy_user = self.request.user
        
        #vincula paciente a unidade de saúde
        if 'estabelecimento' not in self.request.POST:
            form.instance.estabelecimento = Estabelecimento.objects.get(pk=UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.pk)            
        else:
            form.instance.estabelecimento = Estabelecimento.objects.get(pk=self.request.POST.get('estabelecimento'))
        
        messages.success(self.request, "Paciente cadastrado com sucesso!")
        url = super().form_valid(form)
        return url
        

class UnidadeSolicitanteCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = UnidadeSolicitante
    fields = ['cnes', 'nome', 'tipo']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-unidsol')

#essa função vai ser descontinuada
class UnidadeExecutanteCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = UnidadeExecutante
    fields = ['cnes', 'nome']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-unidexec')


class ProcedimentoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Procedimento
    fields = ['nome']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-procedimento')


class VagaOfertadaCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter", u"administrativo"]
    model = VagaOfertada
    fields = ['paciente', 'data_vagaOfertada', 'hora_vagaOfertada', 'tipo', 'procedimento', 'unidadeExecutante', 'codSolicitacao', 'motivo']
    template_name = 'cadastros/CadVagOf.html'
    success_url = reverse_lazy('listar-vagaofertada')
    
    def post(self, request, *args, **kwargs):
        try:
            # Malote.objects.values('id').get_or_create(created_at__contains=date.today())[0]['id']
            #verificar o id do malote e também da unidade
            unidadeSolicitante = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante
            paciente_id = self.request.POST.get('paciente')
            unidadeExecutante_id = self.request.POST.get('unidadeExecutante')
            procedimento_id = self.request.POST.get('procedimento')
            
            paciente = Paciente.objects.filter(pk=paciente_id).first()
            unidadeExecutante = UnidadeExecutante.objects.filter(pk=unidadeExecutante_id).first()
            procedimento = Procedimento.objects.filter(pk=procedimento_id).first()
            
            # raise Exception(procedimento_id)
            vagaOfertada = VagaOfertada.objects.create(
                paciente = paciente,
                data_vagaOfertada = self.request.POST.get('data_vagaOfertada'),
                hora_vagaOfertada = self.request.POST.get('hora_vagaOfertada'),
                tipo = self.request.POST.get('tipo'),
                codSolicitacao = self.request.POST.get('codSolicitacao'),
                unidadeExecutante = unidadeExecutante,
                unidadeSolicitante = unidadeSolicitante,
                procedimento = procedimento,
                motivo = self.request.POST.get('motivo'),
                createdBy_user_id = self.request.user.pk
            )
            
            messages.success(self.request, 'Vaga salva com sucesso!')
            return redirect(reverse("listar-vagaofertada", kwargs={}))
        except Exception as e:
            print(f"Ocorreu um erro ao salvar os dados: {e}")            
            # messages.error(self.request, 'Erro ao salvar a vaga. Verifique se preencheu corretamente todos os campos!')
            return redirect('listar-vagaofertada')
        
    
    def get_context_data(self, **kwargs):
        context = super(VagaOfertadaCreate, self).get_context_data(**kwargs) # get the default context data
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(self.request,"Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            context['userUnidade'] = False
        else:
            if (self.request.user.groups.filter(name = "enfermeiros").exists() or self.request.user.groups.filter(name = "administrator").exists()):
                context['opcaoRisco'] = True
            else: 
                context['opcaoRisco'] = False
            context['userUnidade'] = True            

        return context

    # def form_valid(self, form):
    #     form.instance.createdBy_user = self.request.user
    #     form.instance.unidadeSolicitante_id = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.id
    #     url = super().form_valid(form)
    #     return url


class PermutaCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = Permuta
    fields = ["nomePacienteAgendado", "nomePacienteOfertado", "data_vagaOfertada", "hora_vagaOfertada", "procedimento",
              "unidadeExecutante", "motivo"]
    template_name = "cadastros/CadVagOf.html"
    success_url = reverse_lazy('listar-permuta')

class UnificacaoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url=reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Unificacao
    fields = ['cns', 'nome', 'dataNascimento', 'telefone', 'altura','peso']

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user

        url = super().form_valid(form)
        return url


################## UpDate ################
class PacienteUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter", u"administrativo"]
    model = Paciente
    fields = ['cns', 'estabelecimento','numeroProntuario', 'nome', 'dataNascimento', 'sexo', 'cpf', 'telefonePrincipal', 'telefoneRecado', 'nomeResponsavel', "nomePai", "nomeDaMae", "nomeSocial","rg","orgaoEmissor","estadoEmissor","dataEmissao","racaCor","tipoSanguineo"]
    template_name = 'cadastros/formPaciente.html'
    success_url = reverse_lazy('listar-paciente')
    
    
    def get_context_data(self, **kwargs):
        context = super(PacienteUpdate, self).get_context_data(**kwargs)
        #pegando o paciente
        paciente = self.get_object()

        # Pegando os campos altura e peso do paciente
        alturaStr = paciente.altura
        pesoStr = paciente.peso
        
        # Convertendo para números
        altura = float(alturaStr)
        peso = float(pesoStr)
        
        # Dividindo o peso em kg e gramas
        pesoKg = int(peso)
        pesoGramas = int((peso - pesoKg) * 1000)
        # Dividindo a altura em metros e centímetros
        alturaMetros = int(altura)
        alturaCentimetros = int((altura - alturaMetros) * 100)
        
        context['pesoKg'] = pesoKg
        context['pesoGramas'] = pesoGramas
        context['alturaMetros'] = alturaMetros        
        context['alturaCentimetros'] = alturaCentimetros
        
        return context
        
    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url


class UnidadeSolicitanteUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = UnidadeSolicitante
    fields = ['cnes', 'nome','tipo','isActive','isVisible']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-unidsol')


class UnidadeExecutanteUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = UnidadeExecutante
    fields = ['cnes', 'nome', 'isVisible']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-unidexec')


class ProcedimentoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Procedimento
    fields = ['nome']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-procedimento')


class VagaOfertadaUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter", u"administrativo", u"medicos"]
    model = VagaOfertada
    fields = ['paciente', 'data_vagaOfertada', 'hora_vagaOfertada', 'tipo', 'procedimento', 'unidadeExecutante',
              'codSolicitacao', 'motivo']
    template_name = 'cadastros/CadVagOf.html'
    success_url = reverse_lazy('listar-vagaofertada')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url

class PermutaUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]

    def get(self, request, *args, **kwargs):
        form = PermutarForm()
        vagaOfertada = get_object_or_404(VagaOfertada, pk=kwargs['id'])
        pacientes = Paciente.objects.all().filter(isVisible=True).order_by('created_at').reverse()

        
        return render(request, 'cadastros/showPermuta.html',
                      {'vagaOfertada': vagaOfertada, "pacientes": pacientes, "form": form})



class UnificacaoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url=reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Unificacao
    fields = ['cns', 'nome', 'dataNascimento', 'telefone', 'altura','peso']

    def form_valid(self, form):
        form.instance.updatedBy_user = self.request.user        
        url = super().form_valid(form)
        return url


################## Delete ################
class PacienteDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Paciente
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-paciente')

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL. If the object is protected, send an error message.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()

        try:
            self.object.delete()
        except ProtectedError:
            messages.add_message(request, messages.WARNING, "Não foi possível deletar! Existem vagas ou permutas vinculadas ao cadastro desse paciente.")
            return HttpResponseRedirect(success_url)
        
        return HttpResponseRedirect(success_url)


class UnidadeSolicitanteDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = UnidadeSolicitante
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-unidsol')


class UnidadeExecutanteDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = UnidadeExecutante
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-unidexec')


class ProcedimentoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Procedimento
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-procedimento')

class VagaOfertadaDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter", u"administrativo"]
    model = VagaOfertada
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-vagaofertada')

class ImportarDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Importar
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-importar')

class PermutaConcluidaDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Permuta
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-permutas-concluidas')

class UnificacaoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Unificacao
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-unificacao')

################## List ################
class PacienteList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    # paginate_by = 10
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter", u"administrativo"]
    model = Paciente
    template_name = 'cadastros/listas/paciente.html'
    success_url = reverse_lazy('listar-paciente')
    paginate_by = 8

    def get_context_data(self, **kwargs):
        estabelecimento_id = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.pk
        context = super(PacienteList, self).get_context_data(**kwargs) # get the default context data  
        context['pacientes'] = Paciente.objects.filter(estabelecimento=estabelecimento_id)
        return context

    def get_queryset(self):
        
        txt_pesquisa = self.request.GET.get('s')
        if txt_pesquisa: 
            pacientes = Paciente.objects.filter(
            Q(cns__icontains = txt_pesquisa) | 
            Q(cpf__icontains = txt_pesquisa) | 
            Q(rg__icontains = txt_pesquisa) | 
            Q(numeroProntuario__icontains = txt_pesquisa) | 
            Q(nome__icontains = txt_pesquisa) | 
            Q(dataNascimento__icontains = txt_pesquisa) | 
            Q(telefonePrincipal__icontains=txt_pesquisa) |
            Q(celularPrincipal__icontains=txt_pesquisa) |
            Q(nomeDaMae__icontains=txt_pesquisa) |
            Q(nomePai__icontains=txt_pesquisa) |
            Q(nomeResponsavel__icontains=txt_pesquisa)
            ).filter(isVisible=True).order_by('id').reverse()       
        else:
            pacientes = Paciente.objects.filter(isVisible=True).order_by('id').reverse()
        
        return pacientes

class UnidadeSolicitanteList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    # paginate_by = 10
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = UnidadeSolicitante
    template_name = 'cadastros/listas/unidsol.html'

class UnidadeExecutanteList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    # paginate_by = 10
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = UnidadeExecutante
    template_name = 'cadastros/listas/unidexec.html'
    success_url = reverse_lazy('index')

class ProcedimentoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    # paginate_by = 10
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = Procedimento
    template_name = 'cadastros/listas/procedimento.html'
    success_url = reverse_lazy('index')

class VagaOfertadaList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter", u"administrativo"]
    model = VagaOfertada
    template_name = 'cadastros/listas/ListVagOf.html'
    success_url = reverse_lazy('index')    

    def get_queryset(self):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(self.request,"Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return  reverse_lazy('index')

        ##verificar se o usuário é admin ou callcenter
        if (self.request.user.groups.filter(name = "callcenter").exists() or self.request.user.groups.filter(name = "administrator").exists()):
            queryset = VagaOfertada.objects.all()
            return queryset

        user = UserUnidade.objects.filter(user=self.request.user)        
        unidadeSolicitante = user[0].unidadeSolicitante
        if (self.request.user.groups.filter(name="administrativo").exists()):
            queryset = VagaOfertada.objects.filter(unidadeSolicitante_id=unidadeSolicitante.id)
            return queryset

# class ImportarList(GroupRequiredMixin, LoginRequiredMixin, ListView):
#     # paginate_by = 10
#     login_url = reverse_lazy('userLogin')
#     group_required = [u"administrator", u"callcenter", u"administrativo"]
#     model = Importar
#     template_name = 'cadastros/listas/Listimportar.html'
#     success_url = reverse_lazy('index')
    

class ImportarList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = Importar
    template_name = 'cadastros/listas/Listimportar.html'
    success_url = reverse_lazy('index')
    paginate_by = 7

    # def get_paginate_by(self, queryset):
    #     return self.request.GET.get('paginate_by', self.paginate_by)
    def get_queryset(self):
        s = self.request.GET.get('s')
        if s:            
            qs = Importar.objects.filter(Q(data_solicitacao__icontains=s) | Q(descricao__icontains=s) | Q(cns__icontains=s) | Q(posicao__icontains=s)).order_by('posicao')
        else:
            qs = Importar.objects.all().order_by('posicao')
        return qs

    def get_context_data(self, **kwargs):
        context = super(ImportarList, self).get_context_data(**kwargs)
        group = self.request.user.groups.all()
        context['group'] = group
        return context

    # def get(self, request):
    #     fila = Importar.objects.raw('select * from cadastros_importar')
    #     return render(request, 'cadastros/listas/Listimportar.html', {'fila': fila})


class PermutaList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]


    # model = Permuta
    # template_name ='cadastros/listas/listarPermutas.html'
    # success_url = reverse_lazy('listar_permutas', {"vagas": vagas})
    def get(self, request):
        vagas = VagaOfertada.objects.all()
        return render(request, 'cadastros/listas/listarPermutas.html', {'vagas': vagas})

class PermutaConcluidaList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = Permuta
    paginate_by = 7
    template_name = 'cadastros/listas/listarPermutasConcluidas.html'

    # success_url = reverse_lazy('listar_permutas', {"vagas": vagas})
    # def get(self, request):
        # permutas = Permuta.objects.all()
        # permutas = Permuta.objects.filter(created_at__lte=__range(datetime.datetime.now(), now()+timedelta(days=-30))
        # permutas = Permuta.objects.filter(created_at__range=[datetime.datetime.now()+timedelta(days=-30), datetime.datetime.now()])
        # raise Exception(Permuta.objects.all())
        # return render(request, 'cadastros/listas/listarPermutasConcluidas.html', {'permutas': permutas})

    # @login_required(login_url='userLogin')

    def get_queryset(self):
        
        txt_search = self.request.GET.get('search')
        if txt_search: 
            permutas = Permuta.objects.filter(Q(nomePacienteOfertado__nome__icontains = txt_search) |Q(nomePacienteAgendado__nome__icontains = txt_search) |Q(nomePacienteOfertado__cns__icontains = txt_search) | Q(nomePacienteAgendado__cns__icontains = txt_search) | Q(procedimento__nome__icontains = txt_search) | Q(motivo__icontains = txt_search)| Q(createdBy_user__username__icontains = txt_search)).order_by('created_at')[::-1]
       
        else:
           permutas = Permuta.objects.filter(created_at__range=[datetime.datetime.now()+timedelta(days=-30), datetime.datetime.now()]).order_by('-created_at')
        
        return permutas

# def permutaList(request):
#     vagas = VagaOfertada.objects.all()
#     return render(request, 'cadastros/listas/listarPermutas.html', { 'vagas': vagas })


class UnificacaoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]

    # model = Permuta
    # template_name ='cadastros/listas/listarPermutas.html'
    # success_url = reverse_lazy('listar_permutas', {"vagas": vagas})
    def get(self, request):
        unificacaoPendente = Unificacao.objects.filter(status = 0)
        unificacaoRealizada = Unificacao.objects.filter(status = 1)
        return render(request, 'cadastros/listas/listarUnificacao.html', {'unificacaoPendente': unificacaoPendente, 'unificacaoRealizada': unificacaoRealizada})

################## Refatorar ################

@login_required(login_url='userLogin')
def showPermuta(request, id):
    form = PermutarForm()
    vagaOfertada = get_object_or_404(VagaOfertada, pk=id)
    pacientes = Paciente.objects.all()
    return render(request, 'cadastros/showPermuta.html',
                  {'vagaOfertada': vagaOfertada, "pacientes": pacientes, "form": form})


@transaction.atomic
def permutaStore(request: HttpRequest):
    with transaction.atomic():
        if request.method == 'POST':
            vaga = VagaOfertada.objects.get(pk=request.POST.get('vaga'))
            Permuta.objects.create(
                data_vagaOfertada=request.POST.get('data_vagaOfertada'),
                hora_vagaOfertada=request.POST.get('hora_vagaOfertada'),
                procedimento=Procedimento.objects.get(id=request.POST.get('procedimento')),                
                unidadeExecutante=UnidadeExecutante.objects.get(id=request.POST.get('unidadeExecutante')),
                unidadeSolicitante = vaga.unidadeSolicitante,
                motivo=request.POST.get('motivo'),
                nomePacienteAgendado_id=request.POST.get('nomePacienteAgendado'),
                codSolicitacaoPacienteOfertado=request.POST.get('codSolicitacaoPacienteOfertado'),
                nomePacienteOfertado_id=request.POST.get('nomePacienteOfertado'),
                createdBy_user_id=request.user.id,                
            )

            vaga.status = True
            vaga.save()
            # vagaStatus = vagaDestroy(request, vaga)
            messages.success(request, "Permuta efetuada!")            
            return redirect('listar_permutas')
    return redirect('index')

@transaction.atomic
def vagaOfertadaStatusTrue(request: HttpRequest, id):
    with transaction.atomic():
        vagaOfertada = get_object_or_404(VagaOfertada, pk=id)
        vagaOfertada.status = True
        # vigente a partir de 06/09/2023 15:48
        # vagaOfertada.createdBy_user_id = request.user.id
        vagaOfertada.save()
        messages.success(request, "Permuta removida da lista!")
        return redirect('listar_permutas')

@transaction.atomic
def vagaDestroy(request, vaga):
    with transaction.atomic():
        if request.method == 'POST':
            vaga.delete()
            return True
        return False

# usado na permuta
def buscaDadosPacienteAjax(request):
    if request.is_ajax():
        if request.method == 'POST':
            if 'cns'  in request.POST:
                if Paciente.objects.filter(cns=request.POST['cns']).exists():
                    paciente = Paciente.objects.get(cns=request.POST['cns'])
                    return JsonResponse(model_to_dict(paciente), safe=False)
            elif 'nomePaciente' in request.POST:
                if Paciente.objects.filter(nome=request.POST['nomePaciente']).exists():
                    paciente = Paciente.objects.filter(nome=request.POST['nomePaciente']).first()
                    return JsonResponse(model_to_dict(paciente), safe=False)
        return JsonResponse("Ops! Você não tem permissão. Não é POST", safe=False)
    return JsonResponse("Ops! Você não tem permissão. Não é Ajax", safe=False)

def buscaCartaoSusAjax(request):
    if request.is_ajax():
        if request.method == 'POST':
            paciente = Paciente.objects.get(pk=request.POST['id'])
            cartaoSus = paciente.cns
            return JsonResponse({'nome' : paciente.nome, 'cartaoSus': cartaoSus}, safe=False)
        return JsonResponse("Ops! Você não tem permissão", safe=False)
    return JsonResponse("Ops! Você não tem permissão", safe=False)

def verificaCnsAjax(request):    
    if request.is_ajax():        
        if request.method == 'POST':
            print(Paciente.objects.filter(cns=request.POST['cns']))
            if Paciente.objects.filter(cns=request.POST['cns']).exists():
                paciente = Paciente.objects.get(cns=request.POST['cns'])
                return JsonResponse({'paciente': paciente.nome,  'status': True}, safe=False)
            else:                                
                return JsonResponse({'status': False}, safe=False)
        return JsonResponse("Ops! Você não tem permissão", safe=False)
    return JsonResponse("Ops! Você não tem permissão", safe=False)

    # if request.method == 'POST':
    #     paciente = Paciente.objects.get(pk=id)
    #     cartaoSus = paciente.cns
    #     return JsonResponse({'data': cartaoSus})


def historicoFilaEsperaAjax(request):
    ##teste grafico fila
    historico = HistoricoImportacao.objects.values('dataDoArquivo', 'tipoFila','totalFila').order_by('dataDoArquivo').filter(created_at__range=[datetime.datetime.now()+timedelta(days=-90), datetime.datetime.now()]).distinct()    
    
    filaEspera = []
    for item in historico:
        if(item['totalFila']):
            if(item['tipoFila'] == 2):                
                data = {
                    'dataArquivo': item['dataDoArquivo'].strftime("%d/%m/%Y"), #item
                    'total': item['totalFila'],
                }
                filaEspera.append(data)

    # return JsonResponse({'filaEspera':filaEspera, 'filaRegulada': filaRegulada}, safe=False)
    return JsonResponse(filaEspera,  safe=False)

def historicoFilaReguladaAjax(request):
    ##teste grafico fila
    historico = HistoricoImportacao.objects.values('dataDoArquivo', 'tipoFila','totalFila').order_by('dataDoArquivo').filter(created_at__range=[datetime.datetime.now()+timedelta(days=-90), datetime.datetime.now()]).distinct() 
    filaRegulada = []    
    for item in historico:
        if(item['totalFila']):
            if(item['tipoFila'] == 1):
                data = {
                    'dataArquivo': item['dataDoArquivo'].strftime("%d/%m/%Y"), #item
                    'total': item['totalFila'],
                }
                filaRegulada.append(data)

    # return JsonResponse({'filaEspera':filaEspera, 'filaRegulada': filaRegulada}, safe=False)
    return JsonResponse(filaRegulada,  safe=False)


def graficoUnidadesDiarioAjax(request):
    if request.is_ajax():
        if request.method == 'POST':
            historico = UnidadeDemanda.objects.values_list('unidade', 'total').filter(
                dataSolicitacao__startswith=datetime.datetime.strptime(request.POST['data'], "%d/%m/%Y").strftime('%Y-%m-%d')).distinct()
            filaRegulada = []
            for item in historico:
                data = {
                    'nomeUnidadeSolicitante': item[0],  # item
                    'totalChamado': item[1],
                }
                filaRegulada.append(data)
        
            # return JsonResponse({'filaEspera':filaEspera, 'filaRegulada': filaRegulada}, safe=False)
            return JsonResponse(filaRegulada,  safe=False)
        else:
            historico = Importar.objects.raw('WITH todas_unidades AS (SELECT DISTINCT nomeUnidadeSolicitante FROM cadastros_importar), chamados_por_unidade AS (SELECT nomeUnidadeSolicitante, COUNT(id) AS totalChamados FROM cadastros_importar WHERE data_solicitacao >= (SELECT DATE_SUB(date(MAX(data_solicitacao)), INTERVAL 0 DAY) FROM cadastros_importar) AND tipoFila = 2 GROUP BY nomeUnidadeSolicitante) SELECT  u.nomeUnidadeSolicitante, COALESCE(c.totalChamados, 0) AS totalChamado FROM todas_unidades u JOIN chamados_por_unidade c ON u.nomeUnidadeSolicitante = c.nomeUnidadeSolicitante ORDER BY u.nomeUnidadeSolicitante;')
            filaRegulada = []
            for item in historico:
                data = {
                    'nomeUnidadeSolicitante': item.nomeUnidadeSolicitante,
                    'totalChamado': item.totalChamados,
                }
                filaRegulada.append(data)
            # return JsonResponse({'filaEspera':filaEspera, 'filaRegulada': filaRegulada}, safe=False)
            return JsonResponse(filaRegulada,  safe=False)
    return JsonResponse("Ops! Você não tem permissão", safe=False)



    ##teste grafico fila
    # historico = Importar.objects.values('nomeUnidadeSolicitante').annotate(totalChamados=Count('nomeUnidadeSolicitante'))
    

################## Sincronizar Dicionário  Fila De Espera ################
@login_required(login_url='userLogin')
def sincronizarDicionarioFilaEspera(request):    
    try:
        cursor = connection.cursor()
        cursor.execute('CALL atualizarFila')           
        messages.success(request, 'Dicionário sincronizado com sucesso.')        
        return redirect(request.META.get('HTTP_REFERER'))
    except ProtectedError:
        messages.error(request, 'Não foi possível sincronizar. Tente novamente mais tarde.')       
        return redirect(request.META.get('HTTP_REFERER'))

def is_import(user):
    if user.groups.filter(name='administrator').exists():        
        return True
    elif user.groups.filter(name='importacao').exists():
        return True
    else:
        return False

################## Importar ################
@login_required(login_url='userLogin')
@user_passes_test(is_import, login_url='userLogin')
def importar(request):
    context = {
            'ultimaImportacaoSimples': HistoricoImportacao.objects.filter(tipoFila=2).order_by('-id')[0],
            'ultimaImportacaoRegulada': HistoricoImportacao.objects.filter(tipoFila=1).order_by('-id')[0],
        }
    
    if request.method == 'POST':
        if  len(request.FILES) != 0:
            myfile = request.FILES['myfile']
                 
            #Transforma o arquivo csv em dataframe
            df = pd.read_csv(myfile, error_bad_lines=False, delimiter=';')
            
           
            for row in df.values:
                #Verifica se é fila regulada, pelo dataframe, vendo as linhas da coluna 8(row[8]) são iguais a 1
                if row[8] == 1:
                    #Filtra no banco de dados de importar(cadastros_importar) os objetos que possuem tipo de fila = 1 e os deleta 
                    Importar.objects.filter(tipoFila=1).delete()
                    #Cria um array vazio
                    aux = [] 
                    sexo = ''
                    #Pesquisa pelas colunas do dataframe
                    for row in df.values:
                        #Verifica o sexo do usuário para o armazenar no banco como 0 ou 1
                        if row[21] == 'FEMININO': 
                            sexo=0 
                        else:
                            sexo=1
                        # Filtro de datas(Caso dê problema na formatação)
                        # dataEHora = datetime.datetime.strptime(row[9], "%d/%m/%Y %H:%M") # Formata data e hora
                        # data = datetime.datetime.strptime(row[17], "%d/%m/%Y") # Formata somente a data 
                        # Caso o código da classificação de risco seja maior ou igual a 3, o if é executado e o objeto é criado
                        if row[23] >= 1:
                            obj = Importar(
                                ##############Data Solicitação##################
                                # data_solicitacao=dataEHora,
                                data_solicitacao=row[9],
                                ##############Data Solicitação##################
                                descricao=row[11],
                                alias='',#alias do dicionario de procedimentos  será aqui
                                cns=row[19],
                                cod_class=row[23],
                                posicao=row[24],
                                codSigtap=row[14],
                                tipoFila=row[8],
                                cnesSolicitante=row[3],
                                nomeUnidadeSolicitante=row[4],
                                nomeUsuario=row[16],
                                ##############Data Nascimento##################
                                # nascimentoUsuario=data, 
                                nascimentoUsuario=row[17],
                                ##############Data Nascimento##################
                                maeUsuario=row[18],
                                cpfUsuario=row[20],
                                sexoUsuario=sexo,
                                codigoCid=row[28],
                                descricaoCid=row[29],
                                codigoSolicitacao=row[22],
                                codigoDoProcedimento=row[10],
                            )
                            row[17] = datetime.datetime.utcnow().replace(tzinfo=utc)
                            #Os adiciona em aux
                            aux.append(obj)  
                    #Adiciona varias informações no banco de dados
                    Importar.objects.bulk_create(aux)
                     #Cria um registro referente a importação feita no histórico de importações
            
                    HistoricoImportacao.objects.create(nomeArquivo = myfile,
                                                    dataDoArquivo=df.values[0][0], #data do arquivo sem formatar
                                                    #dataDoArquivo=datetime.datetime.strptime(df.values[0][0], "%d/%m/%Y %H:%M"),  #data do arquivo formatada
                                                    tipoFila = df.values[0][8],
                                                    totalFila = len(df.axes[0]),
                                                    createdBy_user_id = request.user.id,)
                    


                    messages.success(request, 'Importação da FILA REGULADA foi concluída com sucesso.')
                    #Termina o for
                    break    

                #Verifica se é fila simples, pelo dataframe, vendo as linhas da coluna 8(row[8]) são iguais a 2
                elif row[8] == 2:
                    #Filtra no banco de dados de importar(cadastros_importar) os objetos que possuem tipo de fila = 2 e os deleta
                    Importar.objects.filter(tipoFila=2).delete()
                    #Cria um array vazio
                    aux = []
                    sexo = ''

                    #Pesquisa pelas coludas do dataframe
                    for row in df.values:
                        #Verifica o sexo do usuário para o armazenar no banco como 0 ou 1
                        if row[21] == 'FEMININO': 
                            sexo=0 
                        else:
                            sexo=1
                        # Filtro de datas(Caso dê problema na formatação)                            
                        # dataEHora=datetime.datetime.strptime(row[9], "%d/%m/%Y %H:%M") # Formata data e hora
                        # data = datetime.datetime.strptime(row[17], "%d/%m/%Y") # Formata somente a data 
                        # Caso o código da classificação de risco seja maior ou igual a 3, o if é executado e o objeto é criado 
                        if row[23] >= 1:
                            obj = Importar(
                                ##############Data Solicitação##################
                                # data_solicitacao=dataEHora,
                                data_solicitacao=row[9],
                                ##############Data Solicitação##################
                                descricao=row[11],
                                alias='',  # alias do dicionario de procedimentos  será aqui
                                cns=row[19],
                                cod_class=row[23],
                                posicao=row[24],
                                codSigtap=row[14],
                                tipoFila=row[8],
                                cnesSolicitante=row[3],
                                nomeUnidadeSolicitante=row[4],
                                nomeUsuario=row[16],
                                ##############Data Nascimento##################
                                # nascimentoUsuario=data,
                                nascimentoUsuario=row[17],
                                ##############Data Nascimento##################
                                maeUsuario=row[18],
                                cpfUsuario=row[20],
                                sexoUsuario=sexo,
                                codigoCid=row[28],
                                descricaoCid=row[29],
                                codigoSolicitacao=row[22],
                                codigoDoProcedimento=row[10],
                            )
                            row[17]= datetime.datetime.utcnow().replace(tzinfo=utc)
                            #Os adiciona em aux
                            aux.append(obj)
                    #Adiciona varias informações no banco de dados
                    Importar.objects.bulk_create(aux)
                     #Cria um registro referente a importação feita no histórico de importações
            
                    HistoricoImportacao.objects.create(nomeArquivo = myfile,
                                            dataDoArquivo=df.values[0][0], #data do arquivo sem formatar
                                            #dataDoArquivo=datetime.datetime.strptime(df.values[0][0], "%d/%m/%Y %H:%M"),  #data do arquivo formatada
                                            tipoFila = df.values[0][8],
                                            totalFila = len(df.axes[0]),
                                            createdBy_user_id = request.user.id,)
                    
                    ##DEMANDA DIARIA
                    ##fazer um if para verificar se a data ja existe para aquela unidade
                    unidadesSolicitantes = Importar.objects.raw('SELECT s.id, s.nomeUnidadeSolicitante, s.data_solicitacao, s.cnesSolicitante, COUNT(s.id) as total FROM cadastros_importar s WHERE s.data_solicitacao >= (SELECT DATE_SUB(date(MAX(sub.data_solicitacao)), INTERVAL 0 DAY) FROM cadastros_importar sub) AND s.data_solicitacao  AND s.tipoFila = 2 GROUP BY s.nomeUnidadeSolicitante ORDER BY s.nomeUnidadeSolicitante')
                    unidades = []
                    for unidade in unidadesSolicitantes:
                        obj = UnidadeDemanda(                                                                        
                            unidade=unidade.nomeUnidadeSolicitante,
                            dataSolicitacao = unidade.data_solicitacao,
                            cnes = unidade.cnesSolicitante,
                            total = unidade.total,
                            createdBy_user_id = request.user.id,
                        )
                        unidades.append(obj)
                    UnidadeDemanda.objects.bulk_create(unidades)

                    messages.success(request, 'Importação da FILA DE ESPERA foi concluída com sucesso.')
                    #Termina o for
                    break         
            return render(request, "cadastros/importar.html", context)
        else:
            messages.error(request, 'Selecione um arquivo para importar.')
            return render(request, "cadastros/importar.html", context)
    
    return render(request, "cadastros/importar.html", context)


def pegaUser(request):
    return request.user


    
