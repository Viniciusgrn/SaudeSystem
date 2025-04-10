from django.urls import path

from .views import RelatorioAgrupadoList, RelatorioAgrupadoPorProcedimento, ListaPacientePorProcedimento, RelatorioFilaSimples, RelatorioFilaRegulada, RelatorioConsultas, RelatorioExames, Relatorios, RelatorioFilaReguladaCirurgias

urlpatterns = [
    path('relatorioFilaPorGrupo/', RelatorioAgrupadoList.as_view(), name='relatorioFilaPorGrupo'),
    path('relatorioAgrupadoPorProcedimento/', RelatorioAgrupadoPorProcedimento.as_view(), name='relatorioAgrupadoPorProcedimento'),
    path('listaPacientePorProcedimento/<str:alias>/', ListaPacientePorProcedimento.as_view(), name="listaPacientePorProcedimento"), 
    path('RelatorioFilaSimples', RelatorioFilaSimples, name="RelatorioFilaSimples"),
    path('RelatorioFilaRegulada', RelatorioFilaRegulada, name="RelatorioFilaRegulada"),
    path('RelatorioConsultas', RelatorioConsultas, name="RelatorioConsultas"),
    path('RelatorioExames', RelatorioExames, name="RelatorioExames"),
    path('RelatorioCirurgias', RelatorioFilaReguladaCirurgias, name="RelatorioCirurgias"),
    path('Relatorios', Relatorios, name="Relatorios"),
]