from django.urls import path

from .views import ChamadoCreate, ChamadoList, ChamadoUnidadeList, ChamadoUpdate, ChamadoDelete, AnalyticsSupport, TecnicoCreate, TecnicoUpdate, TecnicoList, TecnicoDelete, ChamadoUnidadeCreate, RelatorioComputadores, RelatorioImpressoras, RelatorioEquipamentos
from .views import graficoTecnicosAjax

from . import views


urlpatterns = [
    #create
    path('create/chamado', ChamadoCreate.as_view(), name="create-chamado"),
    path('create/chamado/unidade', ChamadoUnidadeCreate.as_view(), name="create-chamado-unidade"),
    path('create/tecnico', TecnicoCreate.as_view(), name="create-tecnico"),

    #update
    path('update/chamado/<int:pk>', ChamadoUpdate.as_view(), name="update-chamado"),
    path('update/tecnico/<int:pk>', TecnicoUpdate.as_view(), name="update-tecnico"),

    #list
    path('list/chamados/', ChamadoList.as_view(), name="list-chamados"),
    path('list/chamados/unidade', ChamadoUnidadeList.as_view(), name="list-chamados-unidade"),
    path('list/tecnico/', TecnicoList.as_view(), name="list-tecnico"),
    path('analyticsSupport/', AnalyticsSupport.as_view(), name="analyticsSupport"),

    #Excluir
    path('delete/chamados/<int:pk>', ChamadoDelete.as_view(), name="delete-chamado"),
    path('delete/tecnico/<int:pk>', TecnicoDelete.as_view(), name="delete-tecnico"),   
    
    path('api/analyticsSupport/graficoTecnicosAjax', views.graficoTecnicosAjax, name="graficoTecnicosAjax"),
    path('api/analyticsSupport/graficoUnidadesAjax', views.graficoUnidadesAjax, name="graficoUnidadesAjax"),

    #Download
    path('RelatorioComputadores', RelatorioComputadores, name="RelatorioComputadores"),
    path('RelatorioImpressoras', RelatorioImpressoras, name="RelatorioImpressoras"),
    path('RelatorioEquipamentos', RelatorioEquipamentos, name="RelatorioEquipamentos"),
]