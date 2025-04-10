from django.urls import path, re_path

from .views import MaloteCreateRegulcao, MaloteCreateUnidade, MaloteSaidaCreate
from .views import MaloteUnidadesList, MaloteListRegulacao, MaloteListUnidade, MaloteListMedico, MaloteConsulta, MaloteListAme, MaloteListBiopsia, MaloteListHospitalDeOlhos, MaloteListCirurgia, MaloteListAltaComplexidade, MaloteUnidadesSaidaList, MaloteSaidalistRegulacao, MaloteListBERA, MaloteSaidaListUnidade
from .views import MaloteUpdateRegulcao, MaloteUpdateMedico, MaloteUpdateUnidade, MaloteUpdateAdmin, MaloteSaidaUpdate, MaloteUpdateDevolucao
from .views import MaloteDeleteAdmin
from .views import maloteUpdateEtapaUmRegulacao, maloteUpdateEtapaMedico, maloteUpdateScanner, maloteUpdateEtapaTresRegulacao, maloteUpdateAltaComplexidade, maloteUpdateCirurgia, maloteUpdateHospitalDeOlhos, maloteUpdateBiopsia, maloteUpdateAme, maloteUpdateRecebidoPelaUnidade

## Malote simplificado 2024
from .views import UnidadeList, MaloteUnidadesEntrada, UnidadeGuiaCreate, EnviarMaloteDestino

urlpatterns = [
    #List Entrada
    #########################################
    #########MALOTE SIMPLIFICADO#############
    #########################################
    path('unidadeList', UnidadeList.as_view(), name='unidadeList'),
    path('unidadeCreate', UnidadeGuiaCreate.as_view(), name='unidadeCreate'),
    path('unidadesEntrada', MaloteUnidadesEntrada.as_view(), name='unidadesEntrada'),
    path('enviarMaloteDestino', EnviarMaloteDestino, name='enviarMaloteDestino'),
    
    #########################################
    #########MALOTE SIMPLIFICADO#############
    #########################################
    
    
    path('malotes/unidades', MaloteUnidadesList.as_view(), name='list-maloteUnidades'),
    path('malotes/list/regulacao/<int:pk>', MaloteListRegulacao.as_view(), name='list-malotes-regulacao'),
    re_path('malotes/list/all', MaloteListRegulacao.as_view(), name='list-malotes-all'),
    path('malotes/list/unidade', MaloteListUnidade.as_view(), name='list-malotes-unidade'), #list-malotes-unidade
    path('malotes/list/Medico', MaloteListMedico.as_view(), name='list-malotes-medico'),
    path('malotes/list/Ame', MaloteListAme.as_view(), name='list-malotes-Ame'),
    path('malotes/list/Biopsia', MaloteListBiopsia.as_view(), name='list-malotes-Biopsia'),
    path('malotes/list/HospitalDeOlhos', MaloteListHospitalDeOlhos.as_view(), name='list-malotes-HospitalDeOlhos'),
    path('malotes/list/Cirurgia', MaloteListCirurgia.as_view(), name='list-malotes-Cirurgia'),
    path('malotes/list/Bera', MaloteListBERA.as_view(), name='list-malotes-Bera'),
    path('malotes/list/AltaComplexidade', MaloteListAltaComplexidade.as_view(), name='list-malotes-AltaComplexidade'),
    path('malotes/consulta', MaloteConsulta.as_view(), name='list-malotes-consulta'),

    # List Saída
    path('maloteSaida/unidades', MaloteUnidadesSaidaList.as_view(), name='list-maloteUnidadesSaida'),
    path('malotesSaida/list/regulacao/<int:pk>', MaloteSaidalistRegulacao.as_view(), name='list-malotesSaida-regulacao'),
    re_path('malotesSaida/list/all', MaloteSaidalistRegulacao.as_view(), name='list-malotesSaida-all'),
    path('malotesSaida/list/unidade', MaloteSaidaListUnidade.as_view(), name='list-malotesSaida-unidade'),

    #Create
    path('malotes/create/regulacao/', MaloteCreateRegulcao.as_view(), name='create-malote-regulacao'),
    path('malotes/create/unidade/', MaloteCreateUnidade.as_view(), name='create-malote-unidade'),
    path('malotesSaida/create/', MaloteSaidaCreate.as_view(), name='create-maloteSaida-regulacao'),
    
    #Delete
    path('malotes/delete/<int:pk>/', MaloteDeleteAdmin.as_view(), name='delete-malote-admin'),
    
    #Update
    path('malotes/update/regulacao/<int:pk>', MaloteUpdateRegulcao.as_view(), name='update-malote-regulacao'),
    path('malotes/update/unidade/<int:pk>', MaloteUpdateUnidade.as_view(), name='update-malote-unidade'),
    path('malotes/update/medico/<int:pk>', MaloteUpdateMedico.as_view(), name='update-malote-medico'),
    path('malotes/update/admin/<int:pk>', MaloteUpdateAdmin.as_view(), name='update-malote-admin'),
    path('malotes/update/devolucao/<int:pk>', MaloteUpdateDevolucao.as_view(), name='update-malote-devolucao'),
    path('malotesSaida/update/<int:pk>', MaloteSaidaUpdate.as_view(), name='update-malote-saida'),
    path('malotes/update/etapaUmRegulacao', maloteUpdateEtapaUmRegulacao, name='update-malote-etapaUmRegulacao'),
    path('malotes/update/etapaTresRegulacao', maloteUpdateEtapaTresRegulacao, name='update-malote-etapaTresRegulacao'),
    path('malotes/update/etapaMedico', maloteUpdateEtapaMedico, name='update-malote-etapaMedico'),
    path('malotes/update/scanner', maloteUpdateScanner, name='update-malote-scanner'),
    path('malotes/update/AltaComplexidade', maloteUpdateAltaComplexidade, name='update-malote-AltaComplexidade'),
    path('malotes/update/Cirurgia', maloteUpdateCirurgia, name='update-malote-Cirurgia'),
    path('malotes/update/HospitalDeOlhos', maloteUpdateHospitalDeOlhos, name='update-malote-HospitalDeOlhos'),
    path('malotes/update/Biopsia', maloteUpdateBiopsia,  name='update-malote-Biopsia'),
    path('malotes/update/Ame', maloteUpdateAme, name='update-malote-Ame'),
    path('malotes/update/recebidoPelaUnidade', maloteUpdateRecebidoPelaUnidade, name='update-maloteSaida-recebidoPelaUnidade'),

    #urls malote saída
    # path('malotesaida/list', MaloteUnidadesSaidaList.as_view(), name='list-maloteUnidadesSaida'),
    # path('malotesaida/create/<int:pk>', MalotesaidaCreate.as_view(), name='create-malote-saída'),
    # path('malotesaida/update/<int:pk>', MaloteSaidaUpdate.as_view(), name='update-malote-saida'),
    # path('malotesaida/delete', Malotesaidadelete.as_view(), name='delete-malote-saída'),
    # path('malotesaida/list/regulacao/<int:pk>',  MaloteUnidadesSaidaList.as_view(), name='list-malote-saida'),
    # re_path('malotesaida/list/all', MaloteListRegulacao.as_view(), name='list-malotesSaida-all'),
]
