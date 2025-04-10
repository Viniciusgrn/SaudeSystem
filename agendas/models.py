from django.db import models
from django.contrib.auth.models import User
from estabelecimentos.models import Estabelecimento
from profissionais.models import Profissional
from relatorios.models import DicionarioDeProcedimentos

class Agenda(models.Model):

    consulta_status = [
        (1, 'Consulta'),
        (2, 'Retorno')
    ]

    quantidade = models.IntegerField(verbose_name= 'Quantidade de vagas')
    tipoConsulta = models.IntegerField(choices=consulta_status, verbose_name = 'Tipo de consulta')
    procedimento = models.ForeignKey(DicionarioDeProcedimentos, on_delete=models.DO_NOTHING)
    dataAgendamento = models.DateField(verbose_name='Data de agendamento')
    horarioAgendamento = models.DateTimeField(verbose_name='Horário de agendamento')
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.DO_NOTHING)
    profissional = models.ForeignKey(Profissional, on_delete=models.DO_NOTHING )
    createdBy_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    updatedBy_user = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
