from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class Paciente(models.Model):
    # dataExportacao = models.CharField(max_length=19, unique=True, verbose_name="Data Exportação")
    # codCentralReguladora = models.CharField(max_length=255, verbose_name="Cód. Central Reguladora")
    # nomeCentralReguladora = models.DateField(verbose_name="Nome Central Reguladora")
    # codCnesSolicitante = models.CharField(max_length=16, verbose_name="Cod. Cnes Solicitante")
    # nomeUnidadeSolicitante = models.CharField(max_length=16, null=True, blank=True, verbose_name="Telefone para Recado")
    # codCentralReguladoraSolicitante = models.CharField(max_length=16, null=True, blank=True, verbose_name="Cod. Central Reguladora Solicitante")
    # nomeCentralReguladoraSolicitante = models.CharField(max_length=16, null=True, blank=True, verbose_name="Nome Central Reguladora Solicitante")
    # codModalidadeFila = models.BooleanField(default=False, blank=False, verbose_name="Cod. Modalidade Fila") #atender a LGPD
    # codTipoFila = models.CharField(default=0, max_length=4, verbose_name="Cod. Tipo Fila")
    # dataSolicitacao = models.CharField(default=0, max_length=6, verbose_name="Data Solicitação")
    # codInternoItemGrupoProcedimentos = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # descInternaItemGrupoProcedimentos = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # codInternoGrupoProcedimentos = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # descInternaGrupoProcedimentos = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # codSigtap = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # descSigtap = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # nomePaciente = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # dataNascimento = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # nomeMaePaciente = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # cnsPaciente = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # cpfPaciente = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # sexo = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # codSolicitacao = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # codClassificacaoRisco = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # posicaoFila = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # estimativaAtendimentoProcedimento = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # estimativaAtendimentoPaciente = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # producaoMediaMensalProcedimento = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # codCid = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # descCid = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    # isVisible = models.BooleanField(default=True)
    # isActive = models.BooleanField(default=True)
    # createdBy_user = models.ForeignKey(User, models.PROTECT, null=True, blank=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        self.cns = re.sub(r'[^\w\s]','',self.cns)
        self.telefone = re.sub(r'[^\w\s]','',self.telefone)
        # self.telefone2 = re.sub(r'[^\w\s]','',self.telefone2)        
        super(Paciente,self).save(*args,**kwargs)

    def __str__(self):
        return "{}".format(self.nome)