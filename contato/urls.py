from django.urls import path
from .views import ContatoCreate, ContatoUpdate, ContatoList



urlpatterns = [
   
     path('contato/create/', ContatoCreate.as_view(),name = 'contato-create'), 
     path('contato/update/<int:pk>/', ContatoUpdate.as_view(), name ='contato-update'),
     path('contato/list/', ContatoList.as_view(), name ='contato-list')
]     