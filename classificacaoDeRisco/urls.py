from django.urls import path

from .views import  classificacaoRiscoStatusTrue, ClassificacaoRiscoCreate, ClassificacaoRiscoPendenteList, AnalisarRiscoUpdate

from . import views

urlpatterns = [
    path('cadastrar/classificacaoRisco/UpdateStatus/<int:id>', classificacaoRiscoStatusTrue, name='classificacaoRiscoUpdateStatus'),
    path('cadastrar/classificacaoRisco/', ClassificacaoRiscoCreate.as_view(), name="classificacaoRisco_create"),
    path('listar/classificacaoRisco/', ClassificacaoRiscoPendenteList.as_view(), name="listar_classificacaoRisco"),
    path('listar/<int:id>/analisarPedido/', AnalisarRiscoUpdate.as_view(), name="analisar_anexo"),
]