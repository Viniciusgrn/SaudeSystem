from django.urls import path

from .views import AgendaList, AgendaCreate, AgendaUpdate, AgendaDelete

urlpatterns = [
    path('agendas/', AgendaList.as_view(), name='list-agenda'),
    path('agendas/create', AgendaCreate.as_view(), name='create-agenda'),
    path('agendas/delete/<int:pk>/', AgendaDelete.as_view(), name='delete-agenda'),
    path('agendas/update/<int:pk>/', AgendaUpdate.as_view(), name='update-agenda'),
]
