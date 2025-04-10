from django.db import models
from django.contrib.auth.models import User
from estabelecimentos.models import Estabelecimento

class Profissional(models.Model):

    atendimento_choices = [
        (1, 'Sim'),
        (2, 'Não')
    ]

    profissional_status = [
        (1, 'Profissional preceptor na equipe'),
        (2, 'Profissional residente na equipe')
    ]

    contratacaoEstabelecimento_choices = [
        (1, '01 - VINCULO EMPREGATICIO'),
        (2, '02 - AUTONOMO'),
        (3, '03 - COOPERATIVA'),
        (4, '04 - OUTROS'),
        (5, '05 - RESIDENCIA'),
        (6, '06 - ESTAGIO'),
        (7, '07 - BOLSA'),
        (8, '08 - INTERMEDIADO'),
        (9, '09 - INFORMAL'),
        (10, '10 - SERVIDOR PUBLICO CEDIDO PARA INCIATIVA PRIVADA'),
    ]

    contratacaoEmpregador_choices = [
        (1, '00 - NÃO SE APLICA'),
        (2, '01 - ESTATUARIO EFETIVO'),
        (3, '02 - EMPREGADO PUBLICO CELETISTA'),
        (4, '03 - CONTRATADO TEMPORÁRIO OU POR PRAZO/TEMPO'),
        (5, '04 - CARGO COMISSIONADO'),
        (6, '05 - CELETISTA'),
    ]

    detalhamento_choices = [
        (1, '00 - NÃO SE APLICA'),
        (2, '01 - CARGO COMISSIONADO NAO CEDIDO'),
        (3, '02 - CARGO COMISSIONADO CEDIDO'),
        (4, '03 - SERVIDOR PUBLICO PROPRIO'),
        (5, '04 - SERVIDOR PUBLICO CEDIDO'),
        (6, '05 - SEM VINCULO COM O SETOR PUBLICO'),
    ]
    
    estabelecimento = models.ForeignKey(Estabelecimento, models.DO_NOTHING, verbose_name="Estabelecimento", null=True)
    nome = models.CharField(max_length=255, verbose_name='Nome do profissional')
    cns = models.CharField(max_length=19, verbose_name="Cartão Sus")
    cpf = models.CharField(max_length=11, null=True, verbose_name="CPF")
    municipioAtuacao = models.CharField(max_length=255, null=True, verbose_name="Município")
    programa = models.CharField(null=True, max_length=255, verbose_name='Programa')
    dataDeAdesao = models.DateTimeField(null=True, verbose_name="Data de adesão") 
    perfil = models.CharField(null=True, max_length=255, verbose_name='Perfil')
    cnesEstabelecimento = models.CharField(null=True, max_length=7, verbose_name="Código do CNES")
    nomeFantasiaEstabelecimento = models.CharField(null=True, max_length=255, verbose_name="Unidade em que esta vinculado")
    cbo = models.CharField(null=True, max_length=255, verbose_name='CBO - Classificação Brasileira de Ocupação')
    orgaoEmissor = models.CharField(null=True, max_length=255, verbose_name='Orgão emissor')
    uf = models.CharField(null=True, max_length=2, verbose_name="UF")  # Unidade Federal
    registroConselhoClasse = models.CharField(null=True, max_length=255, verbose_name="Registro Conselho de Classe")
    cnpjEmpregador = models.CharField(null=True, max_length=14, unique=True, verbose_name="CNPJ do empregrador")
    naturezaJuridica = models.CharField(null=True, max_length=255, verbose_name="Natureza juridica")
    atendimentoSus = models.IntegerField(null=True, choices=atendimento_choices, verbose_name='Atendimento ao SUS')
    cargaHorariaAmbulatorial = models.IntegerField(null=True, verbose_name='Carga horária ambulatorial')
    cargaHorariaHospitalar = models.IntegerField(null=True, verbose_name='Carga horária hospitalar')
    cargaHorariaOutros = models.IntegerField(null=True, verbose_name='Carga horária referente a outros')
    profissionalStatus = models.IntegerField(null=True, choices=profissional_status, verbose_name='Status do profissional')
    formaContratacaoEstabelecimento = models.IntegerField(null=True, choices=contratacaoEstabelecimento_choices, verbose_name='Forma de contratação com o estabelecimento')
    formaContratacaoEmpregador = models.IntegerField(null=True, choices=contratacaoEmpregador_choices, verbose_name='Forma de contratação com o empregador')
    detalhamentoFormaContratacao = models.IntegerField(null=True, choices=detalhamento_choices, verbose_name='Detalhamento da forma de contratação')
    createdBy_user = models.ForeignKey(User, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.nome)

