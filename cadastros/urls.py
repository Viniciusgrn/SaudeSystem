from django.urls import path

from .views import ImportarDelete, PacienteCreate, PermutaConcluidaDelete, PermutaConcluidaList, UnidadeExecutanteCreate,UnidadeSolicitanteCreate,ProcedimentoCreate, \
     UnificacaoCreate, UnificacaoDelete, UnificacaoList, UnificacaoUpdate, VagaOfertadaCreate, PermutaCreate, vagaOfertadaStatusTrue,  verificaCnsAjax, historicoFilaEsperaAjax, historicoFilaReguladaAjax, buscaDadosPacienteAjax
from .views import PacienteUpdate, UnidadeExecutanteUpdate,UnidadeSolicitanteUpdate,ProcedimentoUpdate, VagaOfertadaUpdate, PermutaUpdate
from .views import PacienteDelete, UnidadeExecutanteDelete,UnidadeSolicitanteDelete,ProcedimentoDelete, VagaOfertadaDelete
from .views import PacienteList, UnidadeSolicitanteList, UnidadeExecutanteList,ProcedimentoList,VagaOfertadaList, PermutaList, ImportarList
from .views import showPermuta, permutaStore, importar, sincronizarDicionarioFilaEspera


from . import views

urlpatterns = [
     path('cadastrar/paciente/', PacienteCreate.as_view(), name="cadastrar-paciente"),
     path('cadastrar/unidsolic/', UnidadeSolicitanteCreate.as_view(), name="cadastrar-unidsolic"),
     path('cadastrar/unidexec/', UnidadeExecutanteCreate.as_view(), name="cadastrar-unidexec"),
     path('cadastrar/procedimento/', ProcedimentoCreate.as_view(), name="cadastrar-procedimento"),
     path('cadastrar/vagaofertada/', VagaOfertadaCreate.as_view(), name="cadastrar-vagaofertada"),        
     path('cadastrar/permuta/<int:pk>/', PermutaCreate.as_view(), name="cadastrar-permuta"),
     path('cadastrar/unificacao/<int:pk>/', UnificacaoCreate.as_view(), name="cadastrar_unificacao"),
     path('cadastrar/fazerPermuta/<int:id>/', showPermuta, name="fazer-permuta"),
     path('cadastrar/permuta/novo', permutaStore, name='permuta-store'),
     path('cadastrar/vagaOfertada/vagaUpdateStatus/<int:id>', vagaOfertadaStatusTrue, name='vagaUpdateStatus'),
     path('cadastrar/importar', importar, name="importar-fila"),     
     path('cadastrar/sincronizarDicionarioFilaEspera', sincronizarDicionarioFilaEspera, name="sincronizarDicionarioFilaEspera"),     
     path('editar/paciente/<int:pk>/', PacienteUpdate.as_view(), name="editar-paciente"),
     path('editar/unidsolic/<int:pk>/', UnidadeSolicitanteUpdate.as_view(), name="editar-unidsolic"), 
     path('editar/unidexec/<int:pk>/', UnidadeExecutanteUpdate.as_view(), name="editar-unidexec"),
     path('editar/procedimento/<int:pk>/', ProcedimentoUpdate.as_view(), name="editar-procedimento"),
     path('editar/vagaofertada/<int:pk>/',VagaOfertadaUpdate.as_view(), name="editar-vagaofertada" ), 
     path('editar/unificacao/<int:pk>/',UnificacaoUpdate.as_view(), name="editar_unificacao" ),
     path('excluir/paciente/<int:pk>/', PacienteDelete.as_view(), name="excluir-paciente"),
     path('excluir/unidsolic/<int:pk>/', UnidadeSolicitanteDelete.as_view(), name="excluir-unidsolic"), 
     path('excluir/unidexec/<int:pk>/', UnidadeExecutanteDelete.as_view(), name="excluir-unidexec"),
     path('excluir/procedimento/<int:pk>/', ProcedimentoDelete.as_view(), name="excluir-procedimento"),
     path('excluir/vagaofertada/<int:pk>/', VagaOfertadaDelete.as_view(), name="excluir-vagaofertada"),
     path('excluir/permutaConcluida/<int:pk>/', PermutaConcluidaDelete.as_view(), name="excluir-permutaConcluida"),
     path('excluir/importar/<int:pk>/', ImportarDelete.as_view(), name="excluir-importar"), 
     path('excluir/unificacao/<int:pk>/', UnificacaoDelete.as_view(), name="excluir_unificacao"),
     path('listar/paciente/', PacienteList.as_view(), name = "listar-paciente"),
     path('listar/unidsol/', UnidadeSolicitanteList.as_view(), name = "listar-unidsol"),
     path('listar/unidexec/', UnidadeExecutanteList.as_view(), name = "listar-unidexec"),
     path('listar/procedimento/',ProcedimentoList.as_view(), name = "listar-procedimento"),
     path('listar/vagaofertada/',VagaOfertadaList.as_view(), name = "listar-vagaofertada"),
     path('listar/importar/',ImportarList.as_view(), name = "listar-importar"),
    #  path('listar/permutas/', views.permutaList, name = "listar_permutas"),
     path('listar/permutasConcluidas/', PermutaConcluidaList.as_view(), name = "listar-permutas-concluidas"),
     path('listar/permutas/', PermutaList.as_view(), name = "listar_permutas"),
     path('listar/permutas/', UnificacaoList.as_view(), name = "listar_unificacao"),
    #  path('listar/<int:id>/showPermuta/', views.showPermuta, name = "show_permuta")
     path('listar/<int:id>/showPermuta/', PermutaUpdate.as_view(), name="show_permuta"),
     path('cartaoSus/ajax/', views.buscaCartaoSusAjax, name="busca-cartao-sus"),
     path('buscaDadosPacienteAjax/ajax/', views.buscaDadosPacienteAjax, name="buscaDadosPacienteAjax"),
     path('verificaCns/ajax/', views.verificaCnsAjax, name="verifica-cns"),
     path('api/historicoFilaEsperaAjax', views.historicoFilaEsperaAjax, name="historicoFilaEsperaAjax"),
     path('api/historicoFilaReguladaAjax', views.historicoFilaReguladaAjax, name="historicoFilaReguladaAjax"),
     path('api/analyticsSupport/graficoUnidadesDiarioAjax', views.graficoUnidadesDiarioAjax, name="graficoUnidadesDiarioAjax"),
     
 ]
     