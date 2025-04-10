from django.db import models
from cadastros.models import Paciente, Procedimento, UnidadeExecutante, UnidadeSolicitante
from django.contrib.auth.models import User

# Create your models here.
class ClassificacaoRisco(models.Model):
    status_choices = (
        (1, "AGUARDANDO ANÁLISE"),
        (2, "APROVADO"),
        (3, "REJEITADO"),
    )

    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, verbose_name="Nome do Paciente", null=True)
    data = models.DateField(null=True, verbose_name="Data do Exame/Consulta")
    hora = models.TimeField(null=True, verbose_name="Hora do Exame/Consulta")
    procedimento = models.ForeignKey(Procedimento, on_delete=models.PROTECT, verbose_name="Procedimento", null=True)
    unidadeExecutante = models.ForeignKey(UnidadeExecutante, on_delete=models.PROTECT, verbose_name="Unidade Executante")
    unidadeSolicitante = models.ForeignKey(UnidadeSolicitante, on_delete=models.PROTECT, null=True)
    codSolicitacao = models.CharField(max_length=12, verbose_name="Código da Solicitação")
    status = models.IntegerField(default=1, choices=status_choices, null=False, editable=False)
    comment = models.TextField(null=False, verbose_name="Justificativa")
    file = models.FileField(upload_to="uploads/", null=True, blank=False, verbose_name="Anexar documento")
    createdBy_user = models.ForeignKey(User, models.PROTECT, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Classificação de Risco"

    def __str__(self):
        return "Paciente: {}".format(self.paciente.nome)