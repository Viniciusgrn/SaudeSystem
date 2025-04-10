from django.db import models
from django.contrib.auth.models import User
from cadastros.models import UnidadeSolicitante

class Tecnico(models.Model):

    tecnico_vinculo =[
        (1, "Estagiario"),
        (2, "OS"),
        (3, "Concursado"),
        (4, "Comissionado"),
    ]

    nome = models.CharField(max_length=100, verbose_name="Nome do técnico")
    status = models.BooleanField(verbose_name="Técnico ativo")
    observacao = models.CharField(max_length=255, null=True, blank=True, verbose_name="Observação")
    vinculo = models.IntegerField(choices=tecnico_vinculo)
    createdBy_user = models.ForeignKey(User, models.PROTECT)
    updatedBy_user = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.nome)

class Equipe(models.Model):
    descricao = models.CharField(max_length=255, verbose_name="Coloque o nome dos integrantes")    
    observacao = models.CharField(max_length=255, null=True, blank=True, verbose_name="Observação")
    isActive = models.BooleanField(default=1, verbose_name="Técnico ativo")
    isVisible = models.BooleanField(default=1)
    createdBy_user = models.ForeignKey(User, models.PROTECT)
    updatedBy_user = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.descricao)

class Chamado(models.Model):

    STATUS_CHOICES = [
        (1,'Aguardando atendimento'),
        (2,'Aguardando peça de reposição'),
        (3,'Em andamento'),
        (4,'Concluído'),
        (5,'Equipamento sem conserto'),
        (6,'Equipamento retirado para depreciação'),
        (7,'Chamado duplicado (existe outro chamado igual)'),
    ]

    ASSUNTO_CHOICES = [
        (1,'Computador'),
        (2,'Impressora'),
        (3,'Internet'),
        (4,'Outros'),        
    ]
        
    PRIORIDADE_CHOICES = [
        (1, 'Planejada'),
        (2, 'Baixa'),
        (3, 'Média'),
        (4, 'Alta'),
        (5, 'Muito Alta'),
    ]
    
   
    unidade = models.ForeignKey(UnidadeSolicitante, on_delete=models.DO_NOTHING, verbose_name="Unidade")
    solicitante = models.CharField(max_length=100, null=True, blank=False, verbose_name="Qual é o seu nome?")
    assunto = models.IntegerField(choices=ASSUNTO_CHOICES, default=1, null=True, blank=True, verbose_name="Escolha o motivo do atendimento")
    ocorrencia = models.TextField(max_length=2000, verbose_name="Descreva os detalhes do problema, setor e a sala.")
    tecnico = models.ForeignKey(Tecnico, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Técnico responsável pelo atendimento")
    equipe = models.ForeignKey(Equipe, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="Selecione a equipe se o chamado tem mais de um técnico")    
    dataOperacao = models.DateTimeField(null=True, blank=True, verbose_name="Data da operação")
    dataResolucao = models.DateTimeField(null=True, blank=True, verbose_name="Data da resolução") 
    observacao = models.CharField(max_length=255, null=True, blank=True, verbose_name="Observação")
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)    
    dataAbertura = models.DateTimeField(verbose_name="Data de Abertura")    
    urgencia = models.PositiveSmallIntegerField(verbose_name="Prioridade", default=2, choices=PRIORIDADE_CHOICES)    
    isVisible = models.BooleanField(default=True)
    createdBy_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable=False, related_name="createSupport")    
    updatedBy_user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name="updateSupport")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def save(self, *args, **kwargs):
        # self.solicitante = self.unidade.upper()
        # self.telefone2 = re.sub(r'[^\w\s]','',self.telefone2)        
        super(Chamado,self).save(*args,**kwargs)

    def __str__(self):
        return "Unidade: {}, Solicitante: {} Ocorrencia: {}".format(self.unidade, self.solicitante, self.ocorrencia)