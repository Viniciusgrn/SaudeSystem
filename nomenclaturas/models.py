from tabnanny import verbose
from django.db import models

# Create your models here.

class consulta(models.Model):
    CONSULTA_CHOICES = [
       (1, '1ª vez'),
       (2, 'Retorno'),
    ]

    tipo = models.IntegerField(choices=CONSULTA_CHOICES, verbose_name="Tipo")
    nomenclaturaSisreg = models.CharField(max_length=254, verbose_name="Nomenclatura SISREG")   
    Prestador = models.CharField(max_length=254, null=True, blank=True,  verbose_name="Prestador")   
    Profissionais = models.CharField(max_length=254, null=True, blank=True, verbose_name="Profissionais Ambulatório de Especialidades do Municipio")
    nomenclaturaCross = models.CharField(max_length=254, null=True, blank=True, verbose_name="Nomenclatura CROSS")
    observacao = models.CharField(max_length=254, null=True, blank=True, verbose_name="Observação")


class exames(models.Model):
    especialidade = models.CharField(max_length=254, null=True, blank=True, verbose_name="Esp")
    complexidade = models.CharField(max_length=254, null=True, blank=True, verbose_name="Complex")
    quemAgenda = models.CharField(max_length=254, null=True, blank=True, verbose_name="Quem agenda?")
    observacao = models.CharField(max_length=254, null=True, blank=True, verbose_name="Observação")
    orientacaoProcedimento =models.CharField(max_length=254, null=True, blank=True, verbose_name="Orientação sobre o procedimento")
    nomenclaturaCross =models.CharField(max_length=254, null=True, blank=True, verbose_name="Nomenclatura CROSS")
    formulario = models.CharField(max_length=254, null=True, blank=True, verbose_name="Formulário")
