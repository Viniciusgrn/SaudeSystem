from django.urls import path

from .views import UnidadeDemandaCreate, UnidadeDemandaList, UnidadeDemandaUpdate, UnidadeDemandaDelete

urlpatterns = [
    #create
    path('create/UnidadeDemanda', UnidadeDemandaCreate.as_view(), name="create-unidadeDemanda"),

    #update
    path('update/UnidadeDemanda/<int:pk>', UnidadeDemandaUpdate.as_view(), name="update-unidadeDemanda"),

    #list
    path('list/UnidadeDemanda/', UnidadeDemandaList.as_view(), name="list-unidadeDemanda"),

    #Excluir
    path('delete/UnidadeDemanda/<int:pk>', UnidadeDemandaDelete.as_view(), name="delete-unidadeDemanda"),
]