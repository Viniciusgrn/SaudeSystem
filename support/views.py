from email.headerregistry import Group
from typing import List
from django.shortcuts import render
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Chamado, Tecnico
import datetime
from django.utils import timezone 
from datetime import timedelta
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from io import BytesIO
import pandas as pd

from cadastros.models import UserUnidade, UnidadeSolicitante, Importar
from equipamentos.models import Equipamento
from .forms import ChamadoForm

###Create
class ChamadoUnidadeCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    # group_required = [u'Administrator', u'administrativo', u"callcenter"]
    model = Chamado    
    fields = ['solicitante', 'assunto', 'ocorrencia']
    template_name = 'support/form.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        form.instance.unidade_id = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.id
        form.instance.dataAbertura = timezone.now()
        url = super().form_valid(form)
        messages.success(self.request, 'Seu chamado foi registrado e esta na fila de atendimento.')
        return url

class ChamadoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u'Administrator', u'support']
    model = Chamado
    form_class = ChamadoForm
    # fields = ['dataAbertura',  'unidade', 'solicitante', 'assunto', 'ocorrencia', 'tecnico', 'dataOperacao', 'dataResolucao', 'observacao', 'status']
    template_name = 'support/form.html'
    success_url = reverse_lazy('list-chamados')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user        
        url = super().form_valid(form)
        return url

class TecnicoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u'Administrator', u'support']
    model = Tecnico
    fields = ['nome', 'status', 'vinculo', 'observacao']
    template_name = 'support/form.html'
    success_url = reverse_lazy('list-tecnico')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url

###Update
class ChamadoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u'Administrator', u'support']
    model = Chamado
    form_class = ChamadoForm
    # fields = ['dataAbertura', 'unidade', 'solicitante','ocorrencia', 'tecnico', 'dataOperacao', 'dataResolucao', 'observacao', 'status']
    template_name = 'support/form.html'
    success_url = reverse_lazy('list-chamados')    

    def form_valid(self, form):
        form.instance.updatedBy_user = self.request.user
        url = super().form_valid(form)
        return url

class TecnicoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u'Administrator', u'support']
    model = Tecnico
    fields = ['nome', 'status', 'vinculo', 'observacao']
    template_name = 'support/form.html'
    success_url = reverse_lazy('list-tecnico')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url

###Delete
class ChamadoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    model = Chamado
    group_required = [u'Administrator', u'support']
    template_name = "support/form-excluir.html"
    success_url = reverse_lazy('list-chamados')

class TecnicoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    model = Tecnico
    group_required = [u'Administrator']
    template_name = "support/form-excluir.html"
    success_url = reverse_lazy('list-tecnico')

###List
class ChamadoUnidadeList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    model = Chamado
    template_name = 'support/list-chamados-unidade.html'
    success_url = reverse_lazy('index')    

    def get_queryset(self):
        if (not UserUnidade.objects.filter(user=self.request.user).exists()):
            messages.warning(self.request,"Seu usuário não esta vinculado a unidade. Entre em contato com o T.I da Secretaria de Saúde.")
            return  reverse_lazy('index')       

        user = UserUnidade.objects.filter(user=self.request.user)        
        unidadeSolicitante = user[0].unidadeSolicitante
        # if (self.request.user.groups.filter(name="administrativo").exists()):
        queryset = Chamado.objects.filter(unidade_id=unidadeSolicitante.id).order_by('dataAbertura').reverse()        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicione suas variáveis extras aqui
        if self.request.user.is_authenticated:
            unidade_id = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.id
            
            context['totalConcluidos'] = Chamado.objects.filter(unidade_id = unidade_id).filter(status=4).count()
            context['totalAbertos'] = Chamado.objects.filter(unidade_id = unidade_id).filter(status=1).count()
            
        return context

class ChamadoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u'Administrator', u'support']
    model = Chamado
    template_name = 'support/list-chamados.html'
    success_url = reverse_lazy('list-chamados')

    def get_queryset(self):
        # queryset = Chamado.objects.all().order_by('dataAbertura').reverse()
        queryset = Chamado.objects.filter(created_at__range=[datetime.datetime.now()+timedelta(days=-90), datetime.datetime.now()]).order_by('dataAbertura').reverse()
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicione suas variáveis extras aqui
        if self.request.user.is_authenticated:
            unidade_id = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.id
            context['unidade'] = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.nome
            context["colaboradores"] = UserUnidade.objects.filter(unidadeSolicitante_id=unidade_id)

            ############### chamados
            ## 7 dias
            # raise Exception(datetime.datetime.now()-timedelta(days=30))
            context['seteDiasAguardando'] = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=7), datetime.datetime.now()]).filter(status=1).count()
            # raise Exception(Chamado.objects.filter(created_at__range=['2023-03-01 00:00:00', '2023-04-11 00:00:00']).filter(status=1).count())
            context['seteDiasAndamento']  = Chamado.objects.filter(updated_at__range=[datetime.datetime.now()-timedelta(days=7), datetime.datetime.now()]).filter(status=3).count()
            context['seteDiasFechados']   = Chamado.objects.filter(updated_at__range=[datetime.datetime.now()-timedelta(days=7), datetime.datetime.now()]).filter(status=4).count()
            context['seteDiasTotal']      = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=7), datetime.datetime.now()]).count()

            ## 15 dias
            context['quinzeDiasAguardando'] = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=15), datetime.datetime.now()]).filter(status=1).count()
            context['quinzeDiasAndamento']  = Chamado.objects.filter(updated_at__range=[datetime.datetime.now()-timedelta(days=15), datetime.datetime.now()]).filter(status=3).count()
            context['quinzeDiasFechados']   = Chamado.objects.filter(updated_at__range=[datetime.datetime.now()-timedelta(days=15), datetime.datetime.now()]).filter(status=4).count()
            context['quinzeDiasTotal']      = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=15), datetime.datetime.now()]).count()

            ## 30 dias
            context['trintaDiasAguardando'] = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=30), datetime.datetime.now()]).filter(status=1).count()
            context['trintaDiasAndamento']  = Chamado.objects.filter(updated_at__range=[datetime.datetime.now()-timedelta(days=30), datetime.datetime.now()]).filter(status=3).count()
            context['trintaDiasFechados']   = Chamado.objects.filter(updated_at__range=[datetime.datetime.now()-timedelta(days=30), datetime.datetime.now()]).filter(status=4).count()
            context['trintaDiasTotal']      = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=30), datetime.datetime.now()]).count()

            ## total
            context['aguardandoHoje'] = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=1), datetime.datetime.now()]).filter(status=1).count()
            context['aguardandoTotal'] = Chamado.objects.filter(status=1).count()
            context['andamentoTotal']  = Chamado.objects.filter(status=3).count()
            context['fechadosTotal']   = Chamado.objects.filter(status=4).count()
            context['chamadosTotal']   = Chamado.objects.all().count()

            ############### equipamentos
            context['equipamentoTotal'] = Equipamento.objects.all().count()
            context['computadores'] = Equipamento.objects.filter(equipamento="Computador").count()
            context['monitores'] = Equipamento.objects.filter(equipamento="Monitor").count()
            context['impressoras'] = Equipamento.objects.filter(equipamento="Impressora").count()
            context['tablets'] = Equipamento.objects.filter(equipamento="Tablet").count()
            context['equipamentoUltimoCadastro'] = Equipamento.objects.last().updated_at


            ############### fila
            context['totalPessoasFila'] = Importar.objects.filter(alias__isnull=False).count()
            context['totalPessoasFilaSimples'] = Importar.objects.filter(tipoFila=2).filter(alias__isnull=False).count()
            context['totalPessoasFilaRegulada'] = Importar.objects.filter(tipoFila=1).filter(alias__isnull=False).count()

            ################### tecnicos
            # context['totalChamadosPorTecnico'] = Chamado.objects.raw('SELECT sc.id, sc.tecnico_id, COUNT(sc.id) AS "totalChamados" FROM support_chamado sc INNER JOIN auth_user au ON au.id = sc.createdBy_user_id WHERE sc.status <> 1 GROUP BY sc.tecnico_id order by sc.tecnico_id' )
            
            context['totalChamadosPorTecnico'] = Chamado.objects.raw('SELECT sc.id, st.nome, COUNT(sc.id) AS "totalChamados" FROM support_chamado sc INNER JOIN support_tecnico st ON st.id = sc.tecnico_id WHERE sc.status <> 1 and sc.isVisible = 1 and st.status = 1 GROUP BY sc.tecnico_id order by sc.tecnico_id' )
            context['totalChamadosPorTecnicoMensal'] = Chamado.objects.raw('SELECT sc.id, st.nome, COUNT(sc.id) AS "totalChamados" FROM support_chamado sc INNER JOIN support_tecnico st ON st.id = sc.tecnico_id WHERE sc.status <> 1 and sc.isVisible = 1 and st.status = 1 and DATE_SUB(CURDATE(),INTERVAL 30 DAY) <= sc.updated_at GROUP BY sc.tecnico_id order by sc.tecnico_id' )
            context['totalChamadosPorUnidade'] = Chamado.objects.raw('SELECT sc.id, sc.unidade_id, COUNT(sc.id) AS "totalChamados" FROM support_chamado sc WHERE sc.status <> 1 GROUP BY sc.unidade_id order by sc.unidade_id desc')

        return context
    
class TecnicoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u'Administrator', u'support']
    model = Tecnico
    template_name = 'support/list-tecnicos.html'
    success_url = reverse_lazy('list-tecnico')


class AnalyticsSupport(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u'Administrator']
    model = Chamado
    template_name = 'support/analyticsSupport.html'
    success_url = reverse_lazy('analyticsSupport')
    
    def get_context_data(self, **kwargs):
         context = super(AnalyticsSupport, self).get_context_data(**kwargs)
         if self.request.user.is_authenticated:
            unidade_id = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.id
            context['unidade'] = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.nome
            context["colaboradores"] = UserUnidade.objects.filter(unidadeSolicitante_id=unidade_id)

            ############### chamados
            ## 7 dias
            # raise Exception(datetime.datetime.now()-timedelta(days=30))
            context['seteDiasAguardando'] = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=7), datetime.datetime.now()]).filter(status=1).count()
            # raise Exception(Chamado.objects.filter(created_at__range=['2023-03-01 00:00:00', '2023-04-11 00:00:00']).filter(status=1).count())
            context['seteDiasAndamento']  = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=7), datetime.datetime.now()]).filter(status=3).count()
            context['seteDiasFechados']   = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=7), datetime.datetime.now()]).filter(status=4).count()
            context['seteDiasTotal']      = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=7), datetime.datetime.now()]).count()
            
            
            ## 15 dias
            context['quinzeDiasAguardando'] = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=15), datetime.datetime.now()]).filter(status=1).count()            
            context['quinzeDiasAndamento']  = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=15), datetime.datetime.now()]).filter(status=3).count()
            context['quinzeDiasFechados']   = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=15), datetime.datetime.now()]).filter(status=4).count()
            context['quinzeDiasTotal']      = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=15), datetime.datetime.now()]).count()
            
            ## 30 dias
            context['trintaDiasAguardando'] = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=30), datetime.datetime.now()]).filter(status=1).count()            
            context['trintaDiasAndamento']  = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=30), datetime.datetime.now()]).filter(status=3).count()
            context['trintaDiasFechados']   = Chamado.objects.filter(updated_at__range=[datetime.datetime.now()-timedelta(days=30), datetime.datetime.now()]).filter(status=4).count()
            context['trintaDiasTotal']      = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=30), datetime.datetime.now()]).count()
            
            ## total
            context['aguardandoTotal'] = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=200), datetime.datetime.now()]).filter(status=1).count()            
            context['andamentoTotal']  = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=200), datetime.datetime.now()]).filter(status=3).count()
            context['fechadosTotal']   = Chamado.objects.filter(created_at__range=[datetime.datetime.now()-timedelta(days=200), datetime.datetime.now()]).filter(status=4).count()
            context['chamadosTotal']   = Chamado.objects.all().count()
            
            ############### equipamentos
            context['equipamentoTotal'] = Equipamento.objects.all().count()
            context['computadores'] = Equipamento.objects.filter(equipamento="Computador").count()
            context['monitores'] = Equipamento.objects.filter(equipamento="Monitor").count()
            context['impressoras'] = Equipamento.objects.filter(equipamento="Impressora").count()
            context['tablets'] = Equipamento.objects.filter(equipamento="Tablet").count()            
            
            ############### fila
            context['totalPessoasFila'] = Importar.objects.filter(alias__isnull=False).count()
            context['totalPessoasFilaSimples'] = Importar.objects.filter(tipoFila=2).filter(alias__isnull=False).count()
            context['totalPessoasFilaRegulada'] = Importar.objects.filter(tipoFila=1).filter(alias__isnull=False).count()

            ################### tecnicos
            # context['totalChamadosPorTecnico'] = Chamado.objects.raw('SELECT sc.id, sc.tecnico_id, COUNT(sc.id) AS "totalChamados" FROM support_chamado sc INNER JOIN auth_user au ON au.id = sc.createdBy_user_id WHERE sc.status <> 1 GROUP BY sc.tecnico_id order by sc.tecnico_id' )
            context['totalChamadosPorTecnico'] = Chamado.objects.raw('SELECT sc.id, st.nome, COUNT(sc.id) AS "totalChamados" FROM support_chamado sc INNER JOIN support_tecnico st ON st.id = sc.tecnico_id WHERE sc.status <> 1 and isVisible = 1 GROUP BY sc.tecnico_id order by sc.tecnico_id' )
            context['totalChamadosPorUnidade'] = Chamado.objects.raw('SELECT sc.id, sc.unidade_id, COUNT(sc.id) AS "totalChamados" FROM support_chamado sc INNER JOIN auth_user au ON au.id = sc.createdBy_user_id WHERE sc.status <> 1 GROUP BY sc.unidade_id order by sc.unidade_id')
            
            
            #   raise Exception(UserUnidade.objects.filter(unidadeSolicitante_id=unidade_id))

            return context
         return context

def graficoTecnicosAjax(request):
    ##teste grafico fila
    # historico = Chamado.objects.values('dataDoArquivo', 'tipoFila','totalFila').order_by('dataDoArquivo')
    
    ## filtro pelo ano todo
    # object_list = Chamado.objects.values('tecnico').filter(created_at__year=datetime.datetime.now().year).annotate(totalChamados=Count('tecnico')).order_by('tecnico')
    # object_list = Chamado.objects.filter(isVisible=True).values('tecnico_id').annotate(totalChamados=Count('tecnico_id')).order_by('tecnico_id')
    
    # filtro pelo mês atual
    # object_list = Chamado.objects.values('tecnico').filter(created_at__month=datetime.datetime.now().month).annotate(totalChamados=Count('tecnico')).order_by('tecnico')
    object_list = Chamado.objects.filter(isVisible=True).values('tecnico_id').annotate(totalChamados=Count('tecnico_id')).order_by('tecnico_id').exclude(status=1)
    tecnicos = []
    for item in object_list:
        data = {
            'tecnico': item['tecnico_id'], #item
            'totalChamado': item['totalChamados'],
        }
        tecnicos.append(data)

    # return JsonResponse({'filaEspera':filaEspera, 'filaRegulada': filaRegulada}, safe=False)
    return JsonResponse(tecnicos,  safe=False)

def graficoUnidadesAjax(request):
    ##teste grafico fila
    # historico = Chamado.objects.values('dataDoArquivo', 'tipoFila','totalFila').order_by('dataDoArquivo')
    ## filtro pelo ano todo
    # object_list = Chamado.objects.values('tecnico').filter(created_at__year=datetime.datetime.now().year).annotate(totalChamados=Count('tecnico')).order_by('tecnico')
    # filtro pelo mês atual
    # object_list = Chamado.objects.values('tecnico').filter(created_at__month=datetime.datetime.now().month).annotate(totalChamados=Count('tecnico')).order_by('tecnico')
    object_list = Chamado.objects.values('unidade_id').filter(status__gt=1).annotate(totalChamados=Count('unidade_id')).order_by('unidade_id')
    tecnicos = []
    for item in object_list:
        data = {
            'unidade': item['unidade_id'], #item
            'totalChamado': item['totalChamados'],
        }
        tecnicos.append(data)

    # return JsonResponse({'filaEspera':filaEspera, 'filaRegulada': filaRegulada}, safe=False)
    return JsonResponse(tecnicos,  safe=False)



# Exportar relatório equipamentos
#Computador
@login_required(login_url='userLogin')
def RelatorioComputadores(request):

    # os.remove("RelatórioFilas.xlsx")
    with BytesIO() as b:

        writer = pd.ExcelWriter(b, engine="xlsxwriter")

        # Faz o dataframe da lista de computadores
        listaComputadores = Importar.objects.raw("SELECT eq.id, eq.modelo, eq.patrimonio, eq.equipamento, CASE WHEN eq.alugadoPor = '1' THEN 'PMBP(Equipamento próprio)' WHEN eq.alugadoPor = '2' THEN 'IESP' WHEN eq.alugadoPor = '3' THEN 'Simpress' ELSE 'Não Especificado' END AS 'alugadoPor' , eq.localidade, CASE WHEN eq.status = '1' THEN 'Em uso' WHEN eq.status = '2' THEN 'Depreciado'ELSE 'Não Especificado' END AS 'status', eq.observacao, eq.adesivo, ma.marca, us.nome FROM pmbp_saude_permuta_dev.equipamentos_equipamento eq inner join pmbp_saude_permuta_dev.cadastros_unidadesolicitante us on eq.unidade_id = us.id inner join pmbp_saude_permuta_dev.equipamentos_marca ma on eq.marca_id = ma.id where eq.equipamento = 'Computador';")
        dadosListaDeComputadores = []

        for computador in listaComputadores:
            informacoesDoComputador = []
            informacoesDoComputador.append(computador.equipamento)
            informacoesDoComputador.append(computador.modelo)
            informacoesDoComputador.append(computador.marca)
            informacoesDoComputador.append(computador.patrimonio)
            informacoesDoComputador.append(computador.adesivo)
            informacoesDoComputador.append(computador.observacao)
            informacoesDoComputador.append(computador.nome)
            informacoesDoComputador.append(computador.localidade)
            informacoesDoComputador.append(computador.status)
            informacoesDoComputador.append(computador.alugadoPor)
            dadosListaDeComputadores.append(informacoesDoComputador)

        dfFilaEspera = pd.DataFrame(dadosListaDeComputadores, columns=[
                                    'Tipo de equipamento', 'Modelo', 'Marca', 'Patrimônio', 'Adesivo', 'Observação', 'Unidade', 'Localidade', 'status', 'Alugado por'])

        dfFilaEspera.to_excel(writer, sheet_name="Fila de espera", index=False)
        writer.close()

        filename = "Lista_de_computadores.xlsx"
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['arquivo'] = f'attachment; filename={filename}'

        return response

#Impressora
@login_required(login_url='userLogin')
def RelatorioImpressoras(request):

    # os.remove("RelatórioFilas.xlsx")
    with BytesIO() as b:

        writer = pd.ExcelWriter(b, engine="xlsxwriter")

        # Faz o dataframe da lista de impressoras
        listaImpressoras = Importar.objects.raw("SELECT eq.id, eq.modelo, eq.patrimonio, eq.equipamento, CASE WHEN eq.alugadoPor = '1' THEN 'PMBP(Equipamento próprio)' WHEN eq.alugadoPor = '2' THEN 'IESP' WHEN eq.alugadoPor = '3' THEN 'Simpress' ELSE 'Não Especificado' END AS 'alugadoPor' , eq.localidade, CASE WHEN eq.status = '1' THEN 'Em uso' WHEN eq.status = '2' THEN 'Depreciado'ELSE 'Não Especificado' END AS 'status', eq.observacao, eq.adesivo, ma.marca, us.nome FROM pmbp_saude_permuta_dev.equipamentos_equipamento eq inner join pmbp_saude_permuta_dev.cadastros_unidadesolicitante us on eq.unidade_id = us.id inner join pmbp_saude_permuta_dev.equipamentos_marca ma on eq.marca_id = ma.id where eq.equipamento = 'Impressora';")
        dadosListaDeImpressoras = []

        for impressora in listaImpressoras:
            informacoesDaImpressora = []
            informacoesDaImpressora.append(impressora.equipamento)
            informacoesDaImpressora.append(impressora.modelo)
            informacoesDaImpressora.append(impressora.marca)
            informacoesDaImpressora.append(impressora.patrimonio)
            informacoesDaImpressora.append(impressora.adesivo)
            informacoesDaImpressora.append(impressora.observacao)
            informacoesDaImpressora.append(impressora.nome)
            informacoesDaImpressora.append(impressora.localidade)
            informacoesDaImpressora.append(impressora.status)
            informacoesDaImpressora.append(impressora.alugadoPor)
            dadosListaDeImpressoras.append(informacoesDaImpressora)

        dfFilaEspera = pd.DataFrame(dadosListaDeImpressoras, columns=[
                                    'Tipo de equipamento', 'Modelo', 'Marca', 'Patrimônio', 'Adesivo', 'Observação', 'Unidade', 'Localidade', 'status', 'Alugado por'])

        dfFilaEspera.to_excel(writer, sheet_name="Fila de espera", index=False)
        writer.close()

        filename = "Lista_de_computadores.xlsx"
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['arquivo'] = f'attachment; filename={filename}'

        return response
    
#Lista geral
@login_required(login_url='userLogin')
def RelatorioEquipamentos(request):

    # os.remove("RelatórioFilas.xlsx")
    with BytesIO() as b:

        writer = pd.ExcelWriter(b, engine="xlsxwriter")

        # Faz o dataframe da lista de impressoras
        listaEquipamentos = Importar.objects.raw("SELECT eq.id, eq.modelo, eq.patrimonio, eq.equipamento, CASE WHEN eq.alugadoPor = '1' THEN 'PMBP(Equipamento próprio)' WHEN eq.alugadoPor = '2' THEN 'IESP' WHEN eq.alugadoPor = '3' THEN 'Simpress' ELSE 'Não Especificado' END AS 'alugadoPor' , eq.localidade, CASE WHEN eq.status = '1' THEN 'Em uso' WHEN eq.status = '2' THEN 'Depreciado'ELSE 'Não Especificado' END AS 'status', eq.observacao, eq.adesivo, ma.marca, us.nome FROM pmbp_saude_permuta_dev.equipamentos_equipamento eq inner join pmbp_saude_permuta_dev.cadastros_unidadesolicitante us on eq.unidade_id = us.id inner join pmbp_saude_permuta_dev.equipamentos_marca ma on eq.marca_id = ma.id where eq.equipamento = 'Computador' or eq.equipamento = 'Impressora';")
        dadosListaDeEquipamentos = []

        for equipamento in listaEquipamentos:
            informacoesDoEquipamento = []
            informacoesDoEquipamento.append(equipamento.equipamento)
            informacoesDoEquipamento.append(equipamento.modelo)
            informacoesDoEquipamento.append(equipamento.marca)
            informacoesDoEquipamento.append(equipamento.patrimonio)
            informacoesDoEquipamento.append(equipamento.adesivo)
            informacoesDoEquipamento.append(equipamento.observacao)
            informacoesDoEquipamento.append(equipamento.nome)
            informacoesDoEquipamento.append(equipamento.localidade)
            informacoesDoEquipamento.append(equipamento.status)
            informacoesDoEquipamento.append(equipamento.alugadoPor)
            dadosListaDeEquipamentos.append(informacoesDoEquipamento)

        dfFilaEspera = pd.DataFrame(dadosListaDeEquipamentos, columns=[
                                    'Tipo de equipamento', 'Modelo', 'Marca', 'Patrimônio', 'Adesivo', 'Observação', 'Unidade', 'Localidade', 'status', 'Alugado por'])

        dfFilaEspera.to_excel(writer, sheet_name="Fila de espera", index=False)
        writer.close()

        filename = "Lista_de_computadores.xlsx"
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['arquivo'] = f'attachment; filename={filename}'

        return response
