from django.urls import path

from .views import EquipamentosList, EquipamentoCreate, EquipamentoUpdate, MarcaCreate, MarcaUpdate, MarcaList

urlpatterns = [
    path('equipamentos/', EquipamentosList.as_view(), name='list-equipamentos'),
    path('equipamentos/create', EquipamentoCreate.as_view(), name='create-equipamentos'),
    path('equipamentos/update/<int:pk>/', EquipamentoUpdate.as_view(), name='update-equipamentos'),
    path('equipamentos/marcas', MarcaList.as_view(), name='list-marcas'),
    path('equipamentos/marcas/create', MarcaCreate.as_view(), name='create-marca'),
    path('equipamentos/marcas/update/<int:pk>/', MarcaUpdate.as_view(), name='update-marca'),
]
