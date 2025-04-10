from tkinter import PROJECTING
from django.db import models
from django.contrib.auth.models import User
from estabelecimentos.models import Estabelecimento
from django.core.exceptions import PermissionDenied
import re

class Unificacao(models.Model):
    cns = models.CharField(max_length=19, unique=True, verbose_name="Cartao Sus")
    nome = models.CharField(max_length=255, verbose_name="Nome")
    dataNascimento = models.DateField(verbose_name="Data de Nascimento")
    telefone = models.CharField(max_length=15)
    altura = models.CharField(max_length=4, verbose_name="Altura")
    peso = models.CharField(max_length=6, verbose_name="Peso")
    isVisible = models.BooleanField(default=True)
    isActive = models.BooleanField(default=True)
    createdBy_user = models.ForeignKey(User, models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.nome)

class UnidadeSolicitante(models.Model):
    
    tipoUnidade = [
        (1, "Solicitante"),
        (2, "Executante"),
        (3, "Solicitante/Executante"),
    ]
    
    cnes = models.CharField(max_length=10, verbose_name="Codigo do CNES")
    nome = models.CharField(max_length=250, verbose_name="Nome da Unidade")
    alias = models.CharField(max_length=250, null=True, blank=True)
    user = models.ManyToManyField(User, related_name='users', verbose_name='usuarios')
    isVisible = models.BooleanField(default=True, verbose_name='Visível nas listagens?')
    isActive = models.BooleanField(default=True, verbose_name='Unidade esta ativa?')
    useCnesSms = models.BooleanField(default=False, editable=False)
    comentario = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    tipo = models.IntegerField(choices=tipoUnidade, default=1, null=False, verbose_name="Tipo Unidade")
    createdBy_user = models.ForeignKey(User, models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.nome)

class UnidadeExecutante(models.Model):
    cnes = models.CharField(max_length=7, unique=True, verbose_name="Codigo do CNES")
    nome = models.CharField(max_length=250)
    alias = models.CharField( max_length=250, null=True, blank=True)
    createdBy_user = models.ForeignKey(User, models.PROTECT, null=True, blank=True)
    isVisible = models.BooleanField(default=True, verbose_name="Visível nas listagens?")
    isActive = models.BooleanField(default=True)
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.nome)

class Paciente(models.Model):    
    racaCor = [
        (1, "Amarela"),
        (2, "Branca"),
        (3, "Parda"),
        (4, "Preta"),
        (5, "Raça/Etnia Indígena"),
    ]
    sexo = [
        (1, "Feminino"),
        (2, "Masculino"),
        (3, "Não Binário"),        
        (4, "Prefiro Não Dizer"),
    ]
    
    tipoSanguineo = [
        (1, "AB+"),
        (2, "AB-"),
        (3, "A+"),
        (4, "A-"),
        (5, "B+"),
        (6, "B-"),
        (7, "O+"),
        (8, "O-")
    ]
    
    cpf = models.CharField(max_length=11, unique=True, verbose_name="CPF", null=True, blank=True)
    cns = models.CharField(max_length=19, unique=True, verbose_name="Cartao Sus")    
    numeroProntuario = models.CharField(max_length=20, verbose_name="Nº prontuário do paciente", null=True, blank=True)
    nome = models.CharField(max_length=255, verbose_name="Nome")
    nomeSocial = models.CharField(max_length=255, verbose_name="Nome Social", null=True, blank=True)
    rg = models.CharField(max_length=10, verbose_name="Matricula", null=True, blank=True) #verificar
    orgaoEmissor = models.CharField(max_length=3, verbose_name="Orgão Emissor", null=True, blank=True) #verificar
    estadoEmissor = models.CharField(max_length=2, verbose_name="UF Emissor", null=True, blank=True) #verificar
    dataEmissao = models.DateField(verbose_name="Data de Emissão", null=True, blank=True)
    dataNascimento = models.DateField(verbose_name="Data de Nascimento")
    sexo = models.PositiveSmallIntegerField(choices=sexo, null=True, blank=True, verbose_name="Sexo")
    telefonePrincipal = models.CharField(max_length=16, verbose_name="Telefone/Celular")
    telefoneRecado = models.CharField(max_length=16, null=True, blank=True, verbose_name="Telefone para Recado")
    celularPrincipal = models.CharField(max_length=16, null=True, blank=True, verbose_name="Celular para Contato")
    celularRecado = models.CharField(max_length=16, null=True, blank=True, verbose_name="Celular para Recado")
    allowMessage = models.BooleanField(default=False, blank=False, verbose_name="Aceita receber mensagem por aplicativo? (Ex: Whatsapp, Telegram, sms...)") #atender a LGPD
    racaCor = models.PositiveSmallIntegerField(choices=racaCor, null=True, blank=True, verbose_name="Raça/Cor")
    tipoSanguineo = models.PositiveSmallIntegerField(choices=tipoSanguineo, null=True, blank=True,verbose_name="Tipo Sanguíneo")
    nomeDaMae = models.CharField(max_length=150, null=True, blank=True, verbose_name="Nome da Mãe")
    nomePai = models.CharField(max_length=150, null=True, blank=True, verbose_name="Nome do Pai")
    nomeResponsavel = models.CharField(max_length=150, null=True, blank=True, verbose_name="Nome do Responsável")
    altura = models.CharField(default=0, max_length=6, blank=False, verbose_name="Altura")
    peso = models.CharField(default=0, max_length=10, blank=False, verbose_name="Peso")
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    isVisible = models.BooleanField(default=True, verbose_name="Visível nas listagens?")
    isActive = models.BooleanField(default=True, verbose_name="Cadastro ativo no sistema?")
    createdBy_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    updatedBy_user = models.ForeignKey(User, null=True, on_delete=models.DO_NOTHING, related_name="updatedByUser")
    estabelecimento = models.ForeignKey(Estabelecimento, models.DO_NOTHING, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # cep = models.CharField(max_length=10, null=True, blank=True, verbose_name="CEP")
    # logradouro = models.CharField(max_length=255, null=True, blank=True, verbose_name="Logradouro")
    # bairro = models.CharField(max_length=255, null=True, blank=True, verbose_name="Bairro")
    # numero = models.CharField(max_length=6, null=True, blank=True, verbose_name="Número")
    # localidade = models.CharField(max_length=255, null=True, blank=True, verbose_name="Municipio")
    # localidadeResidencia = models.CharField(max_length=255, null=True, blank=True, verbose_name="Município de Residência")
    # uf = models.CharField(max_length=2, null=True, blank=True, verbose_name="UF")
    # ibge = models.CharField(max_length=10, null=True, blank=True, verbose_name="Ibge", editable=False)
    # gia = models.CharField(max_length=6, null=True, blank=True, verbose_name="Gia", editable=False)
    # ddd = models.CharField(max_length=2, null=True, blank=True, verbose_name="DDD", editable=False)
    # siafi = models.CharField(max_length=6, null=True, blank=True, verbose_name="Siafi", editable=False)

    def save(self, *args, **kwargs):
        self.nome = self.nome.upper()
        # self.nomeSocial= self.nomeSocial.upper()        
        # self.orgaoEmissor= self.orgaoEmissor.upper()
        # self.estadoEmissor= self.estadoEmissor.upper()
        # self.nomeDaMae= self.nomeDaMae.upper()
        # self.nomePai= self.nomePai.upper()
        # self.nomeResponsavel= self.nomeResponsavel.upper()
        self.cns = re.sub(r'[^\w\s]','',self.cns)
        # self.cpf = re.sub(r'[^\w\s]','',self.cpf)
        # self.rg = re.sub(r'[^\w\s]','',self.rg)
        self.telefonePrincipal = re.sub(r'[^\w\s]','',self.telefonePrincipal)        
        # self.telefoneRecado = re.sub(r'[^\w\s]','',self.telefoneRecado)        
        # self.celularPrincipal = re.sub(r'[^\w\s]','',self.celularPrincipal)        
        # self.celularRecado = re.sub(r'[^\w\s]','',self.celularRecado)
        super(Paciente,self).save(*args,**kwargs)

    def __str__(self):
        return "{} - {}".format(self.nome, self.cns)

class Procedimento(models.Model):
    codProcedimento = models.CharField(max_length=15, unique=True, null=True)
    nome = models.CharField(max_length=255, unique=True)
    createdBy_user = models.ForeignKey(User, models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.nome)

class VagaOfertada(models.Model):
    tipo_choices = (
        ("EXAME", "EXAME"),
        ("CONSULTA", "CONSULTA"),
        ("INSERÇÃO ERRADA NA FILA DE ESPERA", "INSERÇÃO ERRADA NA FILA DE ESPERA"),
    )

    tipo = models.CharField(max_length=50, choices=tipo_choices, null=False, verbose_name="Tipo")
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, verbose_name="Nome do Paciente", null=True)
    data_vagaOfertada = models.DateField(verbose_name="Data do Exame/Consulta")
    hora_vagaOfertada = models.TimeField(verbose_name="Hora do Exame/Consulta")
    procedimento = models.ForeignKey(Procedimento, on_delete=models.PROTECT, verbose_name="Procedimento", null=True)
    unidadeExecutante = models.ForeignKey(UnidadeExecutante, on_delete=models.PROTECT, null=True, verbose_name="Unidade Executante")
    unidadeSolicitante = models.ForeignKey(UnidadeSolicitante, on_delete=models.PROTECT, null=True, related_name="us")
    motivo = models.CharField(max_length=250)
    codSolicitacao = models.CharField(max_length=12, verbose_name="Código da Solicitação")
    status = models.BooleanField(default=False, null=True, blank=True, editable=False)
    createdBy_user = models.ForeignKey(User, models.PROTECT, default=1, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Vagas Ofertadas"

    def __str__(self):
        return "{} | Paciente: {}".format(self.procedimento.nome, self.paciente.nome)

class Permuta(models.Model):
    nomePacienteAgendado = models.ForeignKey(Paciente, on_delete=models.PROTECT, null=True, blank=True, unique=False, related_name="nomePacienteAgendado", verbose_name="Paciente Para Agendar")
    nomePacienteOfertado = models.ForeignKey(Paciente, on_delete=models.PROTECT, null=True, blank=True, unique=False, related_name="nomePacienteOfertado")
    data_vagaOfertada = models.DateTimeField(verbose_name="Data do Exame/Consulta")
    hora_vagaOfertada = models.TimeField(verbose_name="Hora do Exame/Consulta")
    procedimento = models.ForeignKey(Procedimento, on_delete=models.PROTECT, verbose_name="Procedimento")
    unidadeExecutante = models.ForeignKey(UnidadeExecutante, on_delete=models.PROTECT, verbose_name="Unidade Executante")
    unidadeSolicitante = models.ForeignKey(UnidadeSolicitante, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Unidade Solicitante")
    motivo = models.CharField(max_length=255, null=True, blank=True)
    atendenteUnidade = models.IntegerField(null=True, blank=True, verbose_name="Atendente")
    codSolicitacaoPacienteAgendado = models.CharField(max_length=15, null=True, blank=True, verbose_name="Solicitação Paciente Agendado")
    codSolicitacaoPacienteOfertado = models.CharField(max_length=15, null=True, blank=True, verbose_name="Solicitação Paciente Ofertado")
    comment = models.CharField(max_length=254, null=True, blank=True, verbose_name="Comentário")
    createdBy_user = models.ForeignKey(User, models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return "{}".format(self.nomePacienteAgendado.nome)

class UserUnidade(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, unique=False, verbose_name="users", related_name='user')
    unidadeSolicitante = models.ForeignKey(UnidadeSolicitante, on_delete=models.PROTECT, verbose_name="Local de Trabalho", unique=False, related_name="unidadeOrigem")

    def __str__(self):
        return "{}".format(self.user.first_name)

class Log(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    target_id = models.PositiveBigIntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Configuration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phoneMask = models.BooleanField(default=True, verbose_name='Formatar telefone')
    cellphoneMask = models.BooleanField(default=True, verbose_name='Formatar celular')
    cnsMask = models.BooleanField(default=True, verbose_name='Formatar cartão SUS')
    cpfMask = models.BooleanField(default=True, verbose_name='Formatar CPF')

class Importar(models.Model):
    data_solicitacao = models.DateTimeField(verbose_name="Data da Solicitação")
    codigoDoProcedimento = models.CharField(max_length=12,null=True,verbose_name='Código interno do item do grupo de procedimentos')
    descricao = models.CharField(max_length=255, verbose_name="Descrição")#Descrição interna do item do grupo de procedimentos
    alias = models.CharField(max_length=255, null=True)
    cns = models.CharField(max_length=19, verbose_name="Cartao Sus")#CNS do usuario
    cod_class = models.CharField(max_length=3)#Classificação de risco
    posicao = models.CharField(max_length=10)
    createdBy_user = models.ForeignKey(User, models.PROTECT, null=True, blank=True)
    tipoFila = models.IntegerField(null=True)
    codSigtap = models.CharField(null=True, max_length=15, verbose_name="Código Sigtap")
    cnesSolicitante = models.CharField(null=True, max_length=10, verbose_name='Código CNES do solicitante')
    nomeUnidadeSolicitante = models.CharField(null=True,max_length=100 ,verbose_name='Nome da unidade solicitante')
    nomeUsuario = models.CharField(null=True,max_length=150, verbose_name='Nome do usuario')
    nascimentoUsuario = models.DateField(null=True,verbose_name='Data de nascimento do usuario')
    maeUsuario = models.CharField(null=True,max_length=150, verbose_name='Nome da mãe do usuario')
    cpfUsuario = models.CharField(null=True,max_length=15, verbose_name='CPF do usuario')
    sexoUsuario = models.IntegerField(null=True,verbose_name='Sexo do usuario')
    codigoCid = models.CharField(null=True,max_length=10, verbose_name='Código CID')
    descricaoCid = models.CharField(null=True,max_length=255, verbose_name='Descrição do CID')
    codigoSolicitacao = models.CharField(null=True,max_length=15, verbose_name='Código da solicitação')
    statusDuplicidade = models.IntegerField(default=0)
 
    def __str__(self):
        return "{}".format(self.descricao)
    
    

class ImportarCirurgiaSantaCasa(models.Model):
    situacaoCirurgia = (
        (1, 'Realizado'),
        (2, 'Devolvido'),
        (3, 'Contraindicado'),
        (4, 'Não Compareceu'),
        (5, 'Óbito'),
        (6, 'Desistência'),
        (7, 'Mudou do Município'),
        (8, 'Alta para Acompanhamento Ambulatorial'),
        (9, 'Hospital Terciário'),
        (10, 'Em Andamento'),
    )

    solicitacao = models.CharField(null=True,max_length=15, verbose_name='Código da solicitação')
    codigoInterno = models.CharField(max_length=12,null=True,verbose_name='Código interno do item do grupo de procedimentos')
    codigoSigtap = models.CharField(null=True, max_length=15, verbose_name="Código Sigtap")
    descricao = models.CharField(max_length=255, verbose_name="Descrição")#Descrição interna do item do grupo de procedimentos    
    especialidade = models.CharField(max_length=100, null=True, verbose_name="Especialidade")#Descrição da especialidade no dicionario
    dataAgendamento = models.DateTimeField(verbose_name="Data do Agendamento")    
    hora_vagaOfertada = models.TimeField(null=True, verbose_name="Hora do Exame/Consulta")
    cns = models.CharField(max_length=19, verbose_name="Cartao Sus")#CNS do usuario
    nomeUsuario = models.CharField(null=True,max_length=150, verbose_name='Nome do usuario')
    nascimentoUsuario = models.DateField(null=True,verbose_name='Data de nascimento do usuario')
    idade = models.IntegerField(null=True,verbose_name='Idade')
    idadeMeses = models.IntegerField(null=True,verbose_name='Idade em meses')
    maeUsuario = models.CharField(null=True,max_length=150, verbose_name='Nome da mãe do usuario')
    logradouro = models.CharField(max_length=255, null=True, blank=True, verbose_name="Logradouro")
    complemento = models.CharField(max_length=255, null=True, blank=True, verbose_name="Complemento")
    numero = models.CharField(max_length=6, null=True, blank=True, verbose_name="Número")
    bairro = models.CharField(max_length=255, null=True, blank=True, verbose_name="Bairro")
    cep = models.CharField(max_length=10, null=True, blank=True, verbose_name="CEP")
    telefone1 = models.CharField(max_length=16, verbose_name="Telefone/Celular")
    telefone2 = models.CharField(max_length=16, null=True, blank=True, verbose_name="Telefone para Recado")
    celular1 = models.CharField(max_length=16, null=True, blank=True, verbose_name="Celular para Contato")
    celular2 = models.CharField(max_length=16, null=True, blank=True, verbose_name="Celular para Recado")
    localidade = models.CharField(max_length=255, null=True, blank=True, verbose_name="Municipio")
    uf = models.CharField(max_length=2, null=True, blank=True, verbose_name="UF")
    cnesSolicitante = models.CharField(null=True, max_length=10, verbose_name='Código CNES do solicitante')
    unidadeSolicitante = models.CharField(null=True,max_length=100 ,verbose_name='Nome da unidade solicitante')
    sexo = models.PositiveSmallIntegerField(null=True, blank=True,verbose_name="Sexo")
    dataSolicitacao = models.DateTimeField(verbose_name="Data da Solicitação")
    operadorSolicitante = models.CharField(null=True,max_length=255 ,verbose_name='Operador Solicitante')
    dataAutorizacao = models.DateTimeField(verbose_name="Data da Autorização")
    operadorAutorizador = models.CharField(null=True, max_length=100, verbose_name="Operador Autorizador")
    valorProcedimento = models.DecimalField(null=True, max_digits=7, decimal_places=2, verbose_name="Valor do Procedimento")
    situacao = models.CharField(max_length=50, choices=situacaoCirurgia, null=False, verbose_name="Situação")
    cpfProfissionalSolicitante = models.CharField(null=True, max_length=15, verbose_name='CPF do usuario')
    nomeProfissionalSolicitante = models.CharField(null=True, max_length=150, verbose_name='Nome do Profissional Solicitante')
    codigoCid = models.CharField(null=True,max_length=10, verbose_name='Código CID')
    comment = models.CharField(max_length=254, null=True, blank=True, verbose_name="Comentário")
    createdBy_user = models.ForeignKey(User, models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class HistoricoImportacao(models.Model):
    nomeArquivo = models.CharField(max_length=100)
    dataDoArquivo = models.DateTimeField()
    tipoFila = models.IntegerField()    
    totalFila = models.IntegerField(null=True)
    observacao = models.CharField(max_length= 255, null=True)
    createdBy_user = models.ForeignKey(User, models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
