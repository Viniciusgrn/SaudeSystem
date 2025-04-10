
from django.db import models
from django.contrib.auth.models import User
from cadastros.models import UnidadeSolicitante, Procedimento, UnidadeExecutante, Paciente
from relatorios.models import DicionarioDeProcedimentos
from django.urls import reverse

#App local do arquivo Adicionar campo

# Create your models here.

class Malote(models.Model):
    status = [
        (1, "Pendente"), #aguardando status
        (2, "Enviado"), #agendado
        (3, "Recebido"), #arquivado
        (4, "Devolvido"), 
        (5, "Arquivado"), #encaminhado        
        (6, "Retirado SMSA"),
        (7, "Saída de Malote")
    ]
    unidadeOrigem = models.ForeignKey(UnidadeSolicitante, on_delete=models.DO_NOTHING, verbose_name="Unidade origem", related_name="maloteUnidadeOrigem")
    unidadeDestino = models.ForeignKey(UnidadeSolicitante, null=True, on_delete=models.DO_NOTHING, verbose_name="Unidade destino", related_name="maloteUnidadeDestino")
    dataRecebimento = models.DateTimeField(null=True, verbose_name='Data de recebido')
    dataEnvio = models.DateTimeField(null=True, verbose_name='Data de envio')
    status = models.IntegerField(choices=status, default=1, verbose_name='Status do Malote')
    isVisible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sentBy_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name="maloteSentByUser")
    createdBy_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="maloteCreatedByUser")
    updatedBy_user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name="maloteUpdatedByUser")
    
    def __str__(self):
        return "Origem: {} - Destino: {} - Data do Envio: {}".format(self.unidadeOrigem, self.unidadeDestino, self.dataEnvio)

class Guia(models.Model):

    tipo_choices = [
        (1, "Aguardadando Tipo"), # ???
        (2 ,"Cirurgia"),
        (3 ,"Devolução"),
        (4 ,"Remarcação"),
        (5 ,"Retorno"),
        (6 ,"Biópsia"),
        (7 ,"Resultado de Exame"),
    ]

    classificacao_choices = [
        (1, "Aguardadando classificação"),
        (2, "Urgente"),
        (3, "Prioridade"),
        (4, "Eletivo"),
    ]

    statusProcesso_choices = [
        (1, "Pendente"), #aguardando status
        (2, "Enviado"), #agendado
        (3, "Recebido"), #arquivado
        (4, "Devolvido"), 
        (5, "Arquivado"), #encaminhado
        (6, "Pendente"),
        (7, "Recebido"),
        (8, "Não veio no malote"),
        (9, "Retirado SMSA"),
        (10, "Para avaliação do médico regulador"),
    ]
    
    #Retirar 3, 7, 5, 9, 2 e o 6
    justificativa_choices = [
        (1, "Aguardando justificativa"),
        (2, "Faltam Dados/Exames"),
        (3, "Preencher APAC"),
        (4, "Agendamento é realizado pela unidade"),
        (5, "Falta carta de sedação"),
        (6, "Encaminhar para assistente social"),
        (7, "Encaminhar para planejamento familiar"),
        (8, "Encaminhar para ambulatório de especialidades"),
        (9, "Encaminhar/Retorno no HUSF"),
        (10, "Falta autorização para retirada do exame no AME"),
        (11, "Encaminhar para centro de reabilitação(FISIO)"),
        (12, "Guia e cadweb de pacientes diferentes"),
        (13, "Encaminhar para saúde mental infantil"),
        (14, "Inserir no CDR e fila de espera"),
        (15, "Não veio no malote"),
        (16, "Atualização de cadastro"),
        (17, "Aguardando regulação"),
    ]

    etapa_choices = [
        #Etapa 1
        (1, "Recebidos"),
        #Etapa 2
        (2, "Médico"),
        #Etapa 3
        (3, "Encaminhamento"),
        #Etapa 4 - Vai para um desses:
        (4, "Cirurgia"),
        (5, "Hospital de olhos"),
        (6, "Alta complexidade"),
        (7, "AME"),
        (8, "Biópsia"),
        (11, "Bera"),
        #Etapa 5 - Após ser adicionado na fila por um desses vai para:
        (9, "Arquivo"),
        (10, "Malote saída"),
    ]
    
    unidadeOrigem = models.ForeignKey(UnidadeSolicitante, on_delete=models.DO_NOTHING, verbose_name="Unidade origem")
    malote = models.ForeignKey(Malote, null=True, blank=True, on_delete=models.DO_NOTHING)
    nome = models.CharField(max_length=155, verbose_name='nome')
    dataNascimento = models.DateField(verbose_name='Data de nascimento')
    procedimento = models.ForeignKey(DicionarioDeProcedimentos, null=False, blank=False, on_delete=models.DO_NOTHING)
    # procedimentos = models.Choices(QuerySet=DicionarioDeProcedimentos.objects.values_list('nomenclatura', flat=True))
    tipo = models.IntegerField(choices=tipo_choices, default=1, null=True, blank=True, verbose_name='Tipo')
    classificacao = models.IntegerField(choices=classificacao_choices, default=1 , null=True, blank=True, verbose_name='Classificação')
    cross = models.CharField(max_length=10, null=True, blank=True, verbose_name='Cross')
    sus = models.CharField(max_length=20, verbose_name='SUS')
    justificativa = models.IntegerField(choices=justificativa_choices, default=1 , null=True,blank=True, verbose_name='Justificativa')
    observacaoUnidade = models.TextField(max_length=500, verbose_name='Campo de observação',null=True, blank=True)
    observacaoRegulacao = models.TextField(max_length=500, verbose_name='Campo de observação',null=True, blank=True)
    observacaoPrestadores = models.TextField(max_length=500, verbose_name='Campo de observação',null=True, blank=True)
    observacaoMedico = models.CharField(max_length=255, verbose_name='Motivo de devolução',null=True, blank=True)
    scanner = models.BooleanField(default=False)
    dataScanner = models.DateTimeField(null=True, verbose_name='Data de scanneado')
    medicoRegulador = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name="medicoReguladorUser")
    statusProcesso = models.IntegerField(choices=statusProcesso_choices, default=1 ,null=True, blank=True, verbose_name='Status')
    is_visible = models.BooleanField(default=True)
    createdBy_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="guiaCreatedByUser")
    updatedBy_user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name="guiaUpdatedByUser")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # statusUser = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name="statusUser")
    regulado = models.BooleanField(default=False)
    cid = models.CharField(max_length=255, verbose_name='Cid.',null=True, blank=True )
    etapa = models.IntegerField(choices=etapa_choices, default=1 , verbose_name='Etapa')    
    #Para possuir mais de uma chave estrageira de um mesmo model utilizar related_name para cada uma delas
    
    # def get_absolute_url(self):
    #     return reverse("list-malotes-regulacao", kwargs={"pk": self.unidadeSolicitante_id})
    
    def __str__(self):
        return "{} - {} - {}".format(self.nome, self.sus, self.procedimento)



class MaloteSaida(models.Model):

    agendamentoData = models.DateTimeField(null = True, verbose_name='Data de agendamento')
    agendado = models.BooleanField(default=False)
    unidadeExecutante = models.ForeignKey(UnidadeExecutante, on_delete=models.DO_NOTHING, null = True,verbose_name="Unidade executante")
    unidadeSolicitante = models.ForeignKey(UnidadeSolicitante, on_delete=models.DO_NOTHING, verbose_name="Unidade solicitante", blank=True, null= True)
    procedimento = models.ForeignKey(DicionarioDeProcedimentos, on_delete=models.DO_NOTHING, null=True)
    malote = models.ForeignKey(Malote, null=True, blank=True, on_delete=models.DO_NOTHING)
    paciente = models.ForeignKey(Paciente, null=True, blank=False, on_delete=models.DO_NOTHING)
    dataEncaminhado = models.DateTimeField(null= True, verbose_name='Data de encaminhamento') #Data encaminhado para unidade
    recebidoBy_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null= True, related_name="recebido") #Usuario da unidade que recebeu
    updatedBy_user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name="updateSaida")
    createdBy_user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name="createSaida")
    recebidoPelaUnidade = models.BooleanField(default=False) #recebido pela unidade
    recebido_at = models.DateTimeField(null=True) #Quando o usuario da unidade recebeu
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MaloteLog(models.Model):
    acao = models.CharField(max_length=255, null=True, blank=True, verbose_name='acao')
    observacao = models.TextField(max_length=500, verbose_name='Campo de observação',null=True, blank=True)
    malote = models.ForeignKey(Malote, on_delete=models.DO_NOTHING,)
    is_visible = models.BooleanField(default=True)
    createdBy_user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name="createLog")
    created_at = models.DateTimeField(auto_now_add=True)