from django import forms


class ClassificacaoRiscoForm(forms.Form):
    nomePacienteAgendado = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nomePacienteOfertado = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    data_vagaOfertada = forms.DateField(widget=forms.TextInput({'class':'form-control'}))
    hora_vagaOfertada = forms.TimeField(widget=forms.TextInput({'class':'form-control'}))
    procedimento = forms.CharField(max_length=255,widget=forms.TextInput({'class':'form-control'}))
    unidadeExecutante = forms.CharField(max_length=255,widget=forms.TextInput({'class':'form-control'}))
    motivo = forms.CharField(max_length=255,widget=forms.TextInput({'class':'form-control'}))

    # class Meta:
    #     model = Permuta
    #     fields = ["nomePacienteAgendado", "nomePacienteOfertado", "data_vagaOfertada", "hora_vagaOfertada", "procedimento", "unidadeExecutante", "motivo"]


