from django.forms import ModelForm
from django.contrib.auth.forms import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ValidationError
from .models import Agenda


class AgendaForms(ModelForm):
    class Meta:
        model = Agenda
        fields = ['quantidade','tipoConsulta','procedimento','dataAgendamento','horarioAgendamento','idEstabelecimento','idProfissional']


