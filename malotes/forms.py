from django import forms
from .models import Malote

class EtapaForm(forms.ModelForm):

    etapa_choices = [
        (4, "Cirurgia"),
        (5, "Hospital de olhos"),
        (6, "Alta complexidade"),
        (7, "AME"),
    ]

    etapa = forms.ChoiceField(choices=etapa_choices)

    class Meta:
        model = Malote
        fields = ['etapa']


class ScannerForm(forms.ModelForm):

    scanner = forms.BooleanField()

    class Meta:
        model = Malote
        fields = ['scanner']


