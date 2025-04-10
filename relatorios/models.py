from django.db import models
from django.contrib.auth.models import User
# Create your models here.

#Código do Sigtap
#Nomeclatura
#alias
#Profissional


class DicionarioDeProcedimentos(models.Model):
    tipoFila_choices = (
        (2, "Fila de Espera"),
        (1, "Fila Regulada"),        
    )
    
    tipo_choices = (
        (1, "1ª Consulta"),
        (2, "Retorno"),
        (3, "Exame"),
    )
    
    complexidade_choices = (
        (1, "Média Complexidade"),
        (2, "Alta Complexidade"),
    )

    codigoSisreg = models.CharField(max_length=15, null=True, unique=True, verbose_name="Código Sisreg")
    codigoSigtap = models.CharField(max_length=20, null=True, verbose_name="Código Sigtap")
    nomenclatura = models.CharField(max_length=255, unique=True, verbose_name='Nomenclatura no Sisreg')
    especialidade = models.CharField(null=True, blank=True, max_length=255, verbose_name='Especialidade')
    complexidade = models.IntegerField(null=True, blank=True, default=1, choices=complexidade_choices, verbose_name='Complexidade')
    alias = models.CharField(max_length=255, null=True, verbose_name='Nomenclatura no dicionário')
    profissional = models.CharField(max_length=150, null=True, blank=True, verbose_name='Nome do profissional ou Prestador')
    observacao = models.CharField(max_length=255, null=True, blank=True, verbose_name='Observação')
    tipo = models.IntegerField(default=2, choices=tipo_choices, null=True, blank=False, verbose_name='Tipo (1ª consulta ou retorno)')
    tipoFila = models.IntegerField(default=2, choices=tipoFila_choices, null=False, blank=False, verbose_name="Tipo da Fila (Fila de Espera ou Fila Regulada)")
    isVisible = models.BooleanField(default=1, verbose_name="Visível nas listagens?")
    isActive =  models.BooleanField(default=1, verbose_name="Este procedimento esta ativo?")
    createdBy_user = models.ForeignKey(User, models.PROTECT, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} | cód: {}".format(self.nomenclatura, self.codigoSisreg )