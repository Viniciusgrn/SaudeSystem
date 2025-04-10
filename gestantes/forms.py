from django import forms
from .models import Gestantes


class GestantesForm(forms.ModelForm):
    cross = forms.CharField(required=False)

    class Meta:
        model = Gestantes
        fields = ['nome', 'dataNascimento', 'telefoneParaContato', 'etapaGestacao', 'cns', 'cross',  'statusProcesso', 'unidade', 'dataInicioPrenatal', 'gestaoGemelar', 'dum', 'idadeGestacionalUltrassom',
                  'idadeGestacional', 'ddp', 'trimestre', 'observacaoUnidade', 'dataSolicitacaoUsObstetrico', 'dataAgendada', 'codigoSolicitacao', 'observacaoSMS']
