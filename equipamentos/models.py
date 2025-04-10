from django.db import models
from cadastros.models import UnidadeSolicitante
from django.contrib.auth.models import User
from django.forms import ModelForm



class Marca(models.Model):

    marca = models.CharField(max_length=50, verbose_name='Marca')
    descricao = models.CharField(max_length=150, verbose_name='Descrição', null=True, blank=True)
    observacao = models.CharField(max_length=150, verbose_name='Observação', null=True, blank=True)
    status = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    createdBy_user = models.ForeignKey(User, models.DO_NOTHING, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{}".format(self.marca)

 
class Modelo(models.Model):

    modelo = models.CharField(max_length=50)
    marca = models.ForeignKey(Marca, models.PROTECT)
    descricao = models.CharField(max_length=150, verbose_name='Descrição', null=True, blank=True)
    observacao = models.CharField(max_length=150, verbose_name='Observação', null=True, blank=True)
    status = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    createdBy_user = models.ForeignKey(User, models.DO_NOTHING, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Equipamento(models.Model):
    
    STATUS_CHOICES = [
        (1, 'PMBP (Equipamento próprio)'),
        (2, 'IESP'),
        (3, 'Simpress')
    ]

    status = [
        (1, 'Em uso'),
        (2, 'Depreciado'),
        (3, 'Furto'),
        
    ]

    status_TipoEquipamento = [
        ('Computador' , 'Computador'),
        ('Impressora', 'Impressora'),
        ('Tablet', 'Tablet'),
        ('Notebook', 'Notebook'),
        ('Monitor', 'Monitor'),
        ('Outros', 'Outros'),
    ]
    
    unidade = models.ForeignKey(UnidadeSolicitante, models.PROTECT)
    modelo = models.CharField(max_length=80, verbose_name='modelo', null=True, blank=True)
    marca = models.ForeignKey(Marca, models.PROTECT)
    patrimonio = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name='Nº do patrimonio ou Nº de série')
    adesivo = models.CharField(max_length=30, unique=True, null=True, blank=True, verbose_name='Nº do adesivo')
    equipamento = models.CharField(max_length = 50, choices=status_TipoEquipamento, verbose_name='Equipamento')
    alugadoPor = models.IntegerField(choices=STATUS_CHOICES, default=1, verbose_name='Origem do equipamento')
    localidade= models.CharField(max_length=255,verbose_name = 'Localização do equipamento')#Indicar localidade ou especificação do equipamento
    observacao = models.CharField(max_length=150, verbose_name='Observação', null=True, blank=True)
    status = models.IntegerField(choices=status, default=1)
    updated_at = models.DateTimeField(auto_now=True)
    createdBy_user = models.ForeignKey(User, models.DO_NOTHING, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
