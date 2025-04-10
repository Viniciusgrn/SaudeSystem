from django import forms
from .models import Chamado, Tecnico

class ChamadoForm(forms.ModelForm):
    class Meta:
        model = Chamado
        fields = ['dataAbertura', 'unidade', 'solicitante', 'assunto', 'ocorrencia', 'tecnico', 'dataOperacao', 'dataResolucao', 'observacao', 'status']
        
    def __init__(self, *args, **kwargs):
        super(ChamadoForm, self).__init__(*args, **kwargs)
        # Filtrar o campo tecnico para mostrar apenas técnicos ativos
        self.fields['tecnico'].queryset = Tecnico.objects.filter(status=True)