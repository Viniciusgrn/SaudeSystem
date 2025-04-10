from django.urls import path

from .views import importPacientes

from . import views

urlpatterns = [
    path('import/pacientes', importPacientes, name = "import-pacientes"),
]