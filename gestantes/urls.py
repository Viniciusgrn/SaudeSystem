from django.urls import path

from .views import GestanteCreate, GestanteList, GestanteUpdate, GestanteDelete

urlpatterns = [
    path('gestantes/', GestanteList.as_view(), name='list-gestantes'),
    path('gestante/create', GestanteCreate.as_view(), name='create-gestante'),
    path('gestante/delete/<int:pk>/', GestanteDelete.as_view(), name='delete-gestante'),
    path('gestante/update/<int:pk>/', GestanteUpdate.as_view(), name='update-gestante'),
]