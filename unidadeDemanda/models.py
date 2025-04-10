from django.db import models
from django.contrib.auth.models import User

class UnidadeDemanda(models.Model):


    unidade = models.CharField(max_length=100, verbose_name="Nome da unidade")
    cnes = models.CharField(max_length= 25, verbose_name="CNES")
    total = models.IntegerField(verbose_name="Quantidade")
    dataSolicitacao = models.DateTimeField(null=True, verbose_name="Data da Solicitação")
    createdBy_user = models.ForeignKey(User, models.PROTECT)
    updatedBy_user = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
