from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from cadastros.models import Importar
from django.urls import reverse_lazy
from braces.views import GroupRequiredMixin
from .models import DicionarioDeProcedimentos
from cadastros.models import HistoricoImportacao
import pandas as pd
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required 
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from io import BytesIO
from datetime import datetime



class RelatorioAgrupadoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    # paginate_by = 10
    login_url = reverse_lazy('userLogin')
    group_required = ['regulacao', 'administrator', 'relatorios']
    template_name = 'listRelatorio.html'
    model = Importar

    # def get_queryset(self):
    #     relatorioFilaSimples= Importar.objects.raw(
    #         "SELECT DISTINCT s.id, s.alias, s.codSigtap, r.fila, r.dataMaisAntiga FROM(
    #           SELECT alias, COUNT(alias) AS fila, MIN(data_solicitacao) AS dataMaisAntiga 
    #               FROM cadastros_importar WHERE tipoFila=2 GROUP BY alias ORDER BY alias) r 
    #                   INNER JOIN cadastros_importar s ON s.alias=r.alias 
    #                       AND s.data_solicitacao=r.dataMaisAntiga AND s.alias <> ''"
    #     )

    #     # relatorioFilaRegulada = Importar.objects.raw(
    #     #     "SELECT DISTINCT s.id, s.alias, s.codSigtap, r.fila, r.dataMaisAntiga FROM(SELECT alias, COUNT(alias) AS fila, MIN(data_solicitacao) AS dataMaisAntiga FROM cadastros_importar WHERE tipoFila=1 GROUP BY alias ORDER BY alias) r INNER JOIN cadastros_importar s ON s.alias=r.alias AND s.data_solicitacao=r.dataMaisAntiga AND s.alias <> ''"
    #     # )
    #     ProcedimentosDicionario = DicionarioDeProcedimentos.objects.all()
    #     for procedimento in ProcedimentosDicionario:
    #         Importar.objects.filter(descricao=procedimento.nomenclatura).update(alias=procedimento.alias)
    #     return relatorioFilaSimples

    def get_context_data(self, **kwargs):
        context = super(RelatorioAgrupadoList, self).get_context_data(**kwargs)

        # ProcedimentosDicionario = DicionarioDeProcedimentos.objects.all()
        # for procedimento in ProcedimentosDicionario:
        #     Importar.objects.filter(descricao=procedimento.nomenclatura).update(alias=procedimento.alias)
        
        filaSimples = Importar.objects.raw("SELECT * FROM v_relatorioFilaEsperaCompleta ORDER BY alias ASC")
        filaRegulada = Importar.objects.raw("SELECT * FROM v_relatorioFilaReguladaCompleta ORDER BY alias ASC")

        filaSimplesConsultas = Importar.objects.raw("SELECT * from v_relatoriofilaesperaconsultas ORDER BY alias")#
        filaSimplesExames = Importar.objects.raw("SELECT * from v_relatoriofilaesperaexames ORDER BY alias")#

        filaReguladaConsultas = Importar.objects.raw("SELECT * from v_relatorioFilaReguladaConsultas ORDER BY alias")
        filaReguladaExames = Importar.objects.raw("SELECT * from v_relatorioFilaReguladaExames ORDER BY alias")
        # filaReguladaCirurgias = Importar.objects.raw("SELECT * from v_relatorioFilaReguladaCirurgias ORDER BY alias")
        filaReguladaCirurgias = Importar.objects.raw("SELECT * from v_agrupaporprocedimentofilareguladacirurgias ORDER BY alias")

        context['filaSimples'] = filaSimples
        context['filaRegulada'] = filaRegulada
        context['filaSimplesConsultas'] = filaSimplesConsultas
        context['filaSimplesExames'] = filaSimplesExames
        context['filaReguladaConsultas'] = filaReguladaConsultas
        context['filaReguladaExames'] = filaReguladaExames
        context['filaReguladaCirurgias'] = filaReguladaCirurgias
        context['totalPessoasFila'] = Importar.objects.filter(alias__isnull=False).count()
        context['quantidadeFilaSimples'] = Importar.objects.filter(tipoFila=2).filter(alias__isnull=False).count()
        # context['quantidadeFilaRegulada'] = Importar.objects.filter(tipoFila=1).filter(alias__isnull=False).count()
        context['quantidadeFilaRegulada'] = Importar.objects.filter(tipoFila=1).filter(codSigtap__startswith='40').filter(alias__isnull=False).count()
        context['quantidadeSemDicionario'] = Importar.objects.filter(alias__isnull=True).count()
        context['procedimentosSemDicionario'] = Importar.objects.raw("SELECT * FROM v_procedimentosSemDicionario")
        context['procedimentosSemDemanda'] = Importar.objects.raw("SELECT * FROM v_procedimentosSemDemanda")
        context['ultimaImportacaoSimples'] = HistoricoImportacao.objects.filter(tipoFila=2).order_by('-id')[0]
        context['ultimaImportacaoRegulada'] = HistoricoImportacao.objects.filter(tipoFila=1).order_by('-id')[0]

        return context
    
class RelatorioAgrupadoPorProcedimento(GroupRequiredMixin, LoginRequiredMixin, ListView):
    # paginate_by = 10
    login_url = reverse_lazy('userLogin')
    group_required = ['regulacao', 'administrator', 'relatorios']
    template_name = 'relatorioAgrupadoPorProcedimento.html'
    model = Importar
    
    def get_context_data(self, **kwargs):
        context = super(RelatorioAgrupadoPorProcedimento, self).get_context_data(**kwargs)

        # filaSimples = Importar.objects.raw("SELECT * FROM v_relatorioFilaEsperaCompleta")

        # filaSimplesConsultas = Importar.objects.raw("SELECT * from v_relatoriofilaesperaconsultas ORDER BY alias")
        # filaSimplesExames = Importar.objects.raw("SELECT * from v_relatoriofilaesperaexames ORDER BY alias")

        filaReguladaCompleta = Importar.objects.raw("SELECT * FROM v_agrupaPorProcedimentoFilaReguladaCompleta ORDER BY alias")
        filaReguladaConsultas = Importar.objects.raw("SELECT * from v_agrupaPorProcedimentoFilaReguladaConsultas ORDER BY alias")
        filaReguladaExames = Importar.objects.raw("SELECT * from v_agrupaPorProcedimentoFilaReguladaExames ORDER BY alias")
        filaReguladaCirurgias = Importar.objects.raw("SELECT * from v_agrupaPorProcedimentoFilaReguladaCirurgias ORDER BY alias")
        procedimentosSemDicionario = Importar.objects.raw("SELECT * FROM v_procedimentosSemDicionario ORDER BY alias")
        procedimentosSemDemanda = Importar.objects.raw("SELECT * FROM v_procedimentosSemDemanda ORDER BY alias")
        ultimaImportacaoRegulada = HistoricoImportacao.objects.filter(tipoFila=1).order_by('-id')[0]
        ##contadores
        # totalPessoasFila = Importar.objects.filter(alias__isnull=False).count()
        countFilaRegulada = Importar.objects.filter(tipoFila=1).filter(alias__isnull=False).count()
        countConsultas = Importar.objects.filter(tipoFila=1).filter(codSigtap__startswith='20').filter(alias__isnull=False).count()
        countExames = Importar.objects.filter(tipoFila=1).filter(codSigtap__startswith='30').filter(alias__isnull=False).count()
        # countCirurgias = Importar.objects.filter(tipoFila=1).filter(codSigtap__startswith='40').filter(alias__isnull=False).count()
        countCirurgias = Importar.objects.raw("SELECT count(*) FROM v_procedimentosSemDemanda ORDER BY alias")


        # context['filaSimples'] = filaSimples
        # context['filaSimplesConsultas'] = filaSimplesConsultas
        # context['filaSimplesExames'] = filaSimplesExames
        context['filaReguladaCompleta'] = filaReguladaCompleta
        context['filaReguladaConsultas'] = filaReguladaConsultas
        context['filaReguladaExames'] = filaReguladaExames
        context['filaReguladaCirurgias'] = filaReguladaCirurgias
        # context['totalPessoasFila'] = totalPessoasFila
        # context['quantidadeFilaSimples'] = Importar.objects.filter(tipoFila=2).filter(alias__isnull=False).count()
        context['countFilaRegulada'] = countFilaRegulada
        context['countConsultas'] = countConsultas
        context['countExames'] = countExames
        context['countCirurgias'] = countCirurgias
        # context['quantidadeSemDicionario'] = quantidadeSemDicionario
        context['procedimentosSemDicionario'] = procedimentosSemDicionario
        context['procedimentosSemDemanda'] = procedimentosSemDemanda
        # context['ultimaImportacaoSimples'] = HistoricoImportacao.objects.filter(tipoFila=2).order_by('-id')[0]
        context['ultimaImportacaoRegulada'] = ultimaImportacaoRegulada

        return context
    
    
class ListaPacientePorProcedimento(GroupRequiredMixin, LoginRequiredMixin, ListView):    
    login_url = reverse_lazy('userLogin')
    group_required = ['regulacao', 'administrator']
    template_name = 'listaPacientesPorProcedimento.html'
    model = Importar

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            procedimento = Importar.objects.get(pk = self.kwargs.get('alias'))
            pacientes = Importar.objects.filter(descricao = procedimento)
            alias = procedimento
            totalPessoasFila = Importar.objects.filter(descricao = procedimento).count()
        except:
            pacientes = Importar.objects.filter(alias = self.kwargs.get('alias'))
            alias = self.kwargs.get('alias')
            totalPessoasFila = Importar.objects.filter(alias = self.kwargs.get('alias')).count()
        
        # Importar.objects.filter(descricao = self.kwargs.get('descricao'))
        
        # Importar.objects.filter(descricao = self.kwargs.get('descricao')).count()
        # raise Exception(self.kwargs.get('alias'))
        context['pacientes'] = pacientes
        context['procedimento'] = alias
        context['totalPessoasFila'] = totalPessoasFila
        context['ultimaImportacaoSimples'] = HistoricoImportacao.objects.filter(tipoFila=2).order_by('-id')[0]
        return context    
    

#####Exportar relatório fila simples
@login_required(login_url='userLogin')
def RelatorioFilaSimples(request):
       
    # os.remove("RelatórioFilas.xlsx")
    with BytesIO() as b:

        writer = pd.ExcelWriter(b, engine="xlsxwriter")

        #Faz o dataframe da fila simples
        filaEspera = Importar.objects.raw("SELECT id, codSigtap, alias, fila, dataMaisAntiga, quantidadeMesesNaFila FROM v_relatorioFilaEsperaCompleta")
        dataFilaDeEspera = []
        

        for espera in filaEspera:
            teste = []
            teste.append(espera.codSigtap)
            teste.append(espera.alias)
            teste.append(espera.fila)
            data = espera.dataMaisAntiga
            dataFormatada = datetime.strftime(data, "%d/%m/%Y")
            teste.append(dataFormatada)
            teste.append(espera.quantidadeMesesNaFila)
            dataFilaDeEspera.append(teste)

        dfFilaEspera = pd.DataFrame(dataFilaDeEspera, columns=['Código Sigtap', 'Descrição do procedimento', 'Total de pacientes na fila', 'Data mais antiga', 'Meses aguardando na fila'])

        dfFilaEspera.to_excel(writer, sheet_name="Fila de espera", index=False)
        writer.close()

        filename = "RelatorioFila.xlsx"
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['arquivo'] = f'attachment; filename={filename}'

        return response
    
#####Exportar relatório fila regulada
@login_required(login_url='userLogin')
def RelatorioFilaRegulada(request):
       
    # os.remove("RelatórioFilas.xlsx")
    with BytesIO() as b:

        writer = pd.ExcelWriter(b, engine="xlsxwriter")

        #Faz o dataframe
        filaEspera = Importar.objects.raw("SELECT id, codSigtap, alias, fila, dataMaisAntiga, quantidadeMesesNaFila FROM v_relatorioFilaReguladaCompleta")
        dataFilaDeEspera = []
        
        for espera in filaEspera:
            teste = []
            teste.append(espera.codSigtap)
            teste.append(espera.alias)
            teste.append(espera.fila)
            data = espera.dataMaisAntiga
            dataFormatada = datetime.strftime(data, "%d/%m/%Y")
            teste.append(dataFormatada)
            teste.append(espera.quantidadeMesesNaFila)
            dataFilaDeEspera.append(teste)

        dfFilaEspera = pd.DataFrame(dataFilaDeEspera, columns=['Código Sigtap', 'Descrição do procedimento', 'Total de pacientes na fila', 'Data mais antiga', 'Meses aguardando na fila'])

        dfFilaEspera.to_excel(writer, sheet_name="Fila simples", index=False)
        writer.close()

        filename = "RelatorioFila.xlsx"
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['arquivo'] = f'attachment; filename={filename}'

        return response
    
# Exportar relatório fila de consultas
@login_required(login_url='userLogin')
def RelatorioConsultas(request):
       
    # os.remove("RelatórioFilas.xlsx")
    with BytesIO() as b:

        writer = pd.ExcelWriter(b, engine="xlsxwriter")

        #Faz o dataframe
        filaEspera = Importar.objects.raw("SELECT id, codSigtap, alias, fila, dataMaisAntiga, quantidadeMesesNaFila FROM v_relatoriofilaesperaconsultas ORDER BY alias")
        dataFilaDeEspera = []
        
        for espera in filaEspera:
            teste = []
            teste.append(espera.codSigtap)
            teste.append(espera.alias)
            teste.append(espera.fila)
            data = espera.dataMaisAntiga
            dataFormatada = datetime.strftime(data, "%d/%m/%Y")
            teste.append(dataFormatada)
            teste.append(espera.quantidadeMesesNaFila)
            dataFilaDeEspera.append(teste)

        dfFilaEspera = pd.DataFrame(dataFilaDeEspera, columns=['Código Sigtap', 'Descrição do procedimento', 'Total de pacientes na fila', 'Data mais antiga', 'Meses aguardando na fila'])

        dfFilaEspera.to_excel(writer, sheet_name="Fila simples", index=False)
        writer.close()

        filename = "RelatorioFila.xlsx"
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['arquivo'] = f'attachment; filename={filename}'

        return response
    
@login_required(login_url='userLogin')
def RelatorioCirurgias(request):
    # os.remove("RelatórioFilas.xlsx")
    with BytesIO() as b:

        writer = pd.ExcelWriter(b, engine="xlsxwriter")

        #Faz o dataframe
        filaEspera = Importar.objects.raw("SELECT id, codSigtap, alias, fila, dataMaisAntiga, quantidadeMesesNaFila FROM v_relatorioFilaReguladaCompleta")
        dataFilaDeEspera = []
        
        for espera in filaEspera:
            teste = []
            teste.append(espera.codSigtap)
            teste.append(espera.alias)
            teste.append(espera.fila)
            data = espera.dataMaisAntiga
            dataFormatada = datetime.strftime(data, "%d/%m/%Y")
            teste.append(dataFormatada)
            teste.append(espera.quantidadeMesesNaFila)
            dataFilaDeEspera.append(teste)

        dfFilaEspera = pd.DataFrame(dataFilaDeEspera, columns=['Código Sigtap', 'Descrição do procedimento', 'Total de pacientes na fila', 'Data mais antiga', 'Meses aguardando na fila'])

        dfFilaEspera.to_excel(writer, sheet_name="Fila simples", index=False)
        writer.close()

        filename = "RelatorioFila.xlsx"
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['arquivo'] = f'attachment; filename={filename}'

        return response

    
#####Exportar relatório fila simples exames
@login_required(login_url='userLogin')
def RelatorioExames(request):
       
    # os.remove("RelatórioFilas.xlsx")
    with BytesIO() as b:

        writer = pd.ExcelWriter(b, engine="xlsxwriter")

        #Faz o dataframe da fila simples
        filaEspera = Importar.objects.raw("SELECT id, codSigtap, alias, fila, dataMaisAntiga, quantidadeMesesNaFila FROM v_relatoriofilaesperaexames ORDER BY alias")
        dataFilaDeEspera = []
        

        for espera in filaEspera:
            teste = []
            teste.append(espera.codSigtap)
            teste.append(espera.alias)
            teste.append(espera.fila)
            data = espera.dataMaisAntiga
            dataFormatada = datetime.strftime(data, "%d/%m/%Y")
            teste.append(dataFormatada)
            teste.append(espera.quantidadeMesesNaFila)
            dataFilaDeEspera.append(teste)

        dfFilaEspera = pd.DataFrame(dataFilaDeEspera, columns=['Código Sigtap', 'Descrição do procedimento', 'Total de pacientes na fila', 'Data mais antiga', 'Meses aguardando na fila'])

        dfFilaEspera.to_excel(writer, sheet_name="Fila de espera", index=False)
        writer.close()

        filename = "RelatorioFila.xlsx"
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['arquivo'] = f'attachment; filename={filename}'

        return response
    
#####Exportar relatórios
@login_required(login_url='userLogin')
def Relatorios(request):
       
    # os.remove("RelatórioFilas.xlsx")
    with BytesIO() as b:

        writer = pd.ExcelWriter(b, engine="xlsxwriter")

        ################################################### Faz o dataframe da fila simples ###################################################
        filaEspera = Importar.objects.raw("SELECT id, codSigtap, alias, fila, dataMaisAntiga, quantidadeMesesNaFila FROM v_relatorioFilaEsperaCompleta")
        dataFilaDeEspera = []
        
        for procedimento in filaEspera:
            simples = []
            simples.append(procedimento.codSigtap)
            simples.append(procedimento.alias)
            simples.append(procedimento.fila)
            data = procedimento.dataMaisAntiga
            dataFormatada = datetime.strftime(data, "%d/%m/%Y")
            simples.append(dataFormatada)
            simples.append(procedimento.quantidadeMesesNaFila)
            dataFilaDeEspera.append(simples)

        dfFilaEspera = pd.DataFrame(dataFilaDeEspera, columns=['Código Sigtap', 'Descrição do procedimento', 'Total de pacientes na fila', 'Data mais antiga', 'Meses aguardando na fila'])

        ################################################### Faz o dataframe da fila regulada ###################################################

        filaRegulada = Importar.objects.raw("SELECT id, codSigtap, alias, fila, dataMaisAntiga, quantidadeMesesNaFila FROM v_relatorioFilaReguladaCompleta")
        datafilaRegulada = []
        
        for procedimento in filaRegulada:
            regulada = []
            regulada.append(procedimento.codSigtap)
            regulada.append(procedimento.alias)
            regulada.append(procedimento.fila)
            data = procedimento.dataMaisAntiga
            dataFormatada = datetime.strftime(data, "%d/%m/%Y")
            regulada.append(dataFormatada)
            regulada.append(procedimento.quantidadeMesesNaFila)
            datafilaRegulada.append(regulada)

        dffilaRegulada = pd.DataFrame(datafilaRegulada, columns=['Código Sigtap', 'Descrição do procedimento', 'Total de pacientes na fila', 'Data mais antiga', 'Meses aguardando na fila'])

        ################################################### Faz o dataframe da consulta ###################################################

        consultas = Importar.objects.raw("SELECT id, codSigtap, alias, fila, dataMaisAntiga, quantidadeMesesNaFila FROM v_relatoriofilaesperaconsultas ORDER BY alias")
        dataconsultas = []
        
        for procedimento in consultas:
            consulta = []
            consulta.append(procedimento.codSigtap)
            consulta.append(procedimento.alias)
            consulta.append(procedimento.fila)
            data = procedimento.dataMaisAntiga
            dataFormatada = datetime.strftime(data, "%d/%m/%Y")
            consulta.append(dataFormatada)
            consulta.append(procedimento.quantidadeMesesNaFila)
            dataconsultas.append(consulta)

        dfConsultas = pd.DataFrame(dataconsultas, columns=['Código Sigtap', 'Descrição do procedimento', 'Total de pacientes na fila', 'Data mais antiga', 'Meses aguardando na fila'])

        ################################################### Faz o dataframe de exames ###################################################

        exames = Importar.objects.raw("SELECT id, codSigtap, alias, fila, dataMaisAntiga, quantidadeMesesNaFila FROM v_relatoriofilaesperaexames ORDER BY alias")
        dfexame = []
        
        for procedimento in exames:
            exame = []
            exame.append(procedimento.codSigtap)
            exame.append(procedimento.alias)
            exame.append(procedimento.fila)
            data = procedimento.dataMaisAntiga
            dataFormatada = datetime.strftime(data, "%d/%m/%Y")
            exame.append(dataFormatada)
            exame.append(procedimento.quantidadeMesesNaFila)
            dfexame.append(exame)
            
        dfexame = pd.DataFrame(dfexame, columns=['Código Sigtap', 'Descrição do procedimento', 'Total de pacientes na fila', 'Data mais antiga', 'Meses aguardando na fila'])


        dfFilaEspera.to_excel(writer, sheet_name="Fila simples", index=False)
        dffilaRegulada.to_excel(writer, sheet_name="Fila regulada", index=False)
        dfConsultas.to_excel(writer, sheet_name="Consultas", index=False)
        dfexame.to_excel(writer, sheet_name="Exames", index=False)
        writer.close()

        filename = "RelatorioFila.xlsx"
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['arquivo'] = f'attachment; filename={filename}'

        return response
    
# Exportar relatório fila simples


@login_required(login_url='userLogin')
def RelatorioFilaReguladaCirurgias(request):

    # os.remove("RelatórioFilas.xlsx")
    with BytesIO() as b:

        writer = pd.ExcelWriter(b, engine="xlsxwriter")

        # Faz o dataframe da fila simples
        filaCirurgias = Importar.objects.raw(
            "SELECT id, codSigtap, descricao, alias, fila, dataMaisAntiga, quantidadeDiasNaFila, quantidadeMesesNaFila FROM v_agrupaPorProcedimentoFilaReguladaCirurgias ORDER BY alias")
        listaDeProcedimentos = []

        for procedimento in filaCirurgias:
            informacoesDoProcedmento = []
            informacoesDoProcedmento.append(procedimento.codSigtap)
            informacoesDoProcedmento.append(procedimento.descricao)
            informacoesDoProcedmento.append(procedimento.alias)
            informacoesDoProcedmento.append(procedimento.fila)
            data = procedimento.dataMaisAntiga
            dataFormatada = datetime.strftime(data, "%d/%m/%Y")
            informacoesDoProcedmento.append(dataFormatada)
            informacoesDoProcedmento.append(procedimento.quantidadeDiasNaFila)
            informacoesDoProcedmento.append(procedimento.quantidadeMesesNaFila)
            listaDeProcedimentos.append(informacoesDoProcedmento)

        dfFilaDeCirurgias = pd.DataFrame(listaDeProcedimentos, columns=[
                                         'Código Sigtap','Descrição', 'Especialidade', 'Pacientes na fila', 'Data mais antiga', 'Dias aguardando na fila', 'Meses aguardando na fila'])

        dfFilaDeCirurgias.to_excel(
            writer, sheet_name="Fila regulada cirurgias", index=False)
        writer.close()

        filename = "RelatorioCirurgias.xlsx"
        response = HttpResponse(b.getvalue(
        ), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['arquivo'] = f'attachment; filename={filename}'

        return response
