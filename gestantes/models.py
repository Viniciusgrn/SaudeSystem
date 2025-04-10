from django.db import models
from django.contrib.auth.models import User
from cadastros.models import UnidadeSolicitante


class Gestantes(models.Model):

    status_processo = [
        (1, 'Aguardando'),
        (2, 'Vaga solicitada'),
        (3, 'Agendado'),
        (4, 'Pendente'),
        (5, 'Urgente'),
    ]

    etapa_gestacao = [
        (1, 'US OBSTÉTRICO COMUM'),
        (2, 'TRANSLUSCENCIA NUCAL'),
        (3, 'MORFOLOGICO'),
        (4, 'US DOPPLER OBSTETRICO'),
        (5, 'ECO / ECODOPPLER FETAL'),
    ]

    statusProcesso = models.IntegerField(choices=status_processo, verbose_name='Status', default=1)
    unidade = models.ForeignKey(UnidadeSolicitante, models.PROTECT, verbose_name='Unidade')
    dataInicioPrenatal = models.DateField(verbose_name='Data de início pré-natal') #Dia que a gestante chegou na unidade
    cns = models.CharField(max_length=19, unique=True, verbose_name="CNS")
    cross = models.CharField(max_length=19, null=True, verbose_name="CROSS")
    nome = models.CharField(max_length=255, verbose_name="Nome")
    dataNascimento = models.DateField(verbose_name="Data de nascimento")
    telefoneParaContato = models.CharField(max_length=15, verbose_name="Telefone para contato")
    gestaoGemelar = models.IntegerField(verbose_name="Gestação gemelar")
    dum = models.DateField(verbose_name="Inserir Data da Última Menstruação(DUM)")  # Inserir Data da Última Menstruação (Calculo automatico)
    idadeGestacional = models.CharField(max_length=255, null=True, blank=True, verbose_name="Inserir Idade Gestacional") #(Calculo automatico)
    idadeGestacionalUltrassom = models.BooleanField(verbose_name="IG Ultrassom")
    semanasGestacao = models.IntegerField(null=True, blank=True, verbose_name='Semanas de gestação')
    diasGestcao = models.IntegerField(null=True, blank=True, verbose_name="Dias de gestação")
    ddp = models.DateField(verbose_name="Data provável do parto(DDP)") #Calculo automatico
    trimestre = models.IntegerField( verbose_name="Informar se é de 1º, 2º ou 3º trimestre.") #Calculo automatico
    observacaoUnidade = models.CharField(max_length=255, null=True, blank=True, verbose_name="Observação da unidade")
    dataSolicitacaoUsObstetrico = models.DateField(null=True,verbose_name="Data solicitação US obstetrico") #
    dataAgendada = models.DateField(verbose_name="Inserir a data em que a gestante completa 12 semanas") # calculo automatico  para 12 semanas translucencia nucal, para 21 semanas no ultrassom morfológico
    codigoSolicitacao = models.CharField(max_length=255, verbose_name="Código para imprimir a filipeta no SISREG.")
    observacaoSMS= models.CharField(max_length=255, null=True, blank=True, verbose_name="Observação da Secretaria de Saúde")
    etapaGestacao = models.IntegerField(choices=etapa_gestacao, verbose_name='Etapa na gestação')
    createdBy_user = models.ForeignKey(User, models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Fazer Alerta de data limite para TRANSLUSCENCIA NUCAL(confirmar se são 12 ou 13 semanas)

    # def __str__(self):
    #     return "{}".format(self.variavel)

