from django.urls import path

from .views import EstabelecimentoList, EstabelecimentoCreate, EstabelecimentoUpdate, EstabelecimentoDelete, EstabelecimentoConfiguracoesUpdate, EstabelecimentoProfissionaisList, EstabelecimentoProfissionalCreate

urlpatterns = [
    path('estabelecimentos/', EstabelecimentoList.as_view(), name='list-estabelecimentos'),
    path('estabelecimento/configuracoes/<int:pk>', EstabelecimentoConfiguracoesUpdate.as_view(), name='estabelecimentoConfiguracoesUpdate'),
    path('estabelecimento/profissionais/<int:pk>', EstabelecimentoProfissionaisList.as_view(), name='estabelecimentoProfissionaisList'),
    path('estabelecimentos/create', EstabelecimentoCreate.as_view(), name='create-estabelecimentos'),
    path('estabelecimento/<int:pk>/profissional/create', EstabelecimentoProfissionalCreate.as_view(), name='estabelecimentoProfissionalCreate'),
    path('estabelecimentos/delete/<int:pk>/', EstabelecimentoDelete.as_view(), name='delete-estabelecimentos'),
    path('estabelecimentos/update/<int:pk>/', EstabelecimentoUpdate.as_view(), name='update-estabelecimentos'),
]