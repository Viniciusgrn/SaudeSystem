from email.policy import default
from random import choices
from tabnanny import verbose
from django.db import models
from django.forms import CharField, IntegerField
from django.contrib.auth.models import User

# Create your models here.

class Contato(models.Model):

    AVALIATION_CHOICES = [
        (1, 'Escolha um'),
        (2, 'Escolha dois'),
        (3, 'Escolha tres'),
        (4, 'Escolha quatro'),
        (5, 'Escolha cinco'),
        (6, 'Escolha seis'),
    ]
    
    dataAbertura = models.DateTimeField(auto_now_add=True, verbose_name="Data de Abertura") 
    nomeCompleto = models.CharField(max_length=255, verbose_name = 'Nome completo')
    cargo = models.CharField(max_length=255, verbose_name='Cargo', null=True)
    unidade = models.CharField(max_length=255, verbose_name='Unidade', null=True)
    assunto = models.IntegerField(choices=AVALIATION_CHOICES, default=1 )
    mensagem = models.TextField(max_length=500, verbose_name='Mensagem')
    updated_at = models.DateTimeField(auto_now=True)
    createdBy_user = models.ForeignKey(User, models.DO_NOTHING, editable=False)

    


