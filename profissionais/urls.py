from django.urls import path

from .views import ProfissionalList, ProfissionalCreate, ProfissionalUpdate, ProfissionalDelete

urlpatterns = [
    path('profissionais/', ProfissionalList.as_view(), name='list-profissionais'),    
    path('profissionais/create', ProfissionalCreate.as_view(), name='create-profissional'),
    path('profissionais/delete/<int:pk>/',ProfissionalDelete.as_view(), name='delete-profissional'),
    path('profissionais/update/<int:pk>/',ProfissionalUpdate.as_view(), name='update-profissional'),
]
