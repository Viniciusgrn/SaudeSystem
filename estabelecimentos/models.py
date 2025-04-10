from django.db import models
from django.contrib.auth.models import User


class TipoEstabelecimento(models.Model):
    codTipoEstabelecimento = models.CharField(max_length=50, verbose_name='Código do tipo de estabelecimento')
    nomeTipoEstabelecimento = models.CharField(max_length=100, verbose_name='Código do tipo de estabelecimento')
    descricao = models.TextField(max_length=800, null=True, verbose_name='Descrição')
    legislacao = models.CharField(max_length=255, null=True, verbose_name='Legislação')
    parent = models.ForeignKey('self', models.PROTECT, null=True)
    createdBy_user = models.ForeignKey(User, models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}".format(self.nomeTipoEstabelecimento)

class Estabelecimento(models.Model):

    tipoUnidade = [
        (1, "Solicitante"),
        (2, "Executante"),
        (3, "Solicitante/Executante"),
    ]
    
    # tipo_estabelecimento = [
    #     (1, '01 - Posto de Saúde'),
    #     (2, '02 - Centro de Saúde/Unidade Básica de Saúde'),
    #     (3, '04 - Policlínica'),
    #     (4, '05 - Hospital Geral'),
    #     (5, '07 - Hospital Especializado'),
    #     (6, '15 - Unidade Mista'),
    #     (7, '20 - Pronto Socorro Geral'),
    #     (8, '21 - Pronto Socorro Especializado'),
    #     (9, '22 - Consultório Isolado'),
    #     (10, '32 - Unidade Móvel Fluvial'),
    #     (11, '36 - Clínica Especializada/Amb. Especializado'),
    #     (12, '39 - Unidade de Serviço de Apoio de Diagnose e Terapia'),
    #     (13, '40 - Unidade Móvel Terrestre'),
    #     (14, '42 - Unidade Móvel de Nível Pré-hospitalar na Área de Urgência e Emergência'),
    #     (15, '43 - Farmácia'),
    #     (16, '50 - Unidade de Vigilância em Saúde'),
    #     (17, '60 - Cooperativa'),
    #     (18, '61 - Centro de Parto Normal Isolado'),
    #     (19, '62 - Hospital /Dia- Isolado'),
    #     (20, '64 - Central de Regulação de Serviços de Saúde'),
    #     (21, '67 - Laboratório Central de Saúde Pública - LACEN'),
    #     (22, '68 - Secretaria de Saúde'),
    #     (23, '69 - Centro de atenção hemoterapica e ou hematologica'),
    #     (24, '70 - Centro de atenção psicossocial'),
    #     (25, '71 - Centro de apoio a saúde da família'),
    #     (26, '72 - Unidade de atenção a saúde indigena'),
    #     (27, '73 - Pronto atendimento'),
    #     (28, '74 - Polo academia da saúde'),
    #     (29, '75 - Telessaúde'),
    #     (20, '76 - Central de regulação médica de urgências'),
    # ]

    # subtipo_estabelecimento = [
    #     (1, '1'),
    #     (2, '2'),
    #     (3, '3')
    # ]


    cnes = models.CharField(max_length=20, unique=True, verbose_name="Codigo do CNES")    
    tipoEstabelecimento = models.ForeignKey(TipoEstabelecimento, models.DO_NOTHING, verbose_name="Tipo de Estabelecimento")
    documentoEstabelecimento = models.CharField(max_length=14, unique=True, verbose_name="Documento, CPF ou CNPJ do estabelecimento", null=True)
    cnpjMantenedora = models.CharField(max_length=14, verbose_name="CNPJ da Mantenedora", null=True, blank=True)
    naturezaJuridica = models.CharField(max_length=255, verbose_name="Natureza juridica", null=True, blank=True)
    nomeEmpresarial = models.CharField(max_length=255, verbose_name="Nome Empresarial", null=True, blank=True)
    nomeFantasia = models.CharField(max_length=250, verbose_name="Nome da Unidade / Nome Fantasia")    
    alias = models.CharField(max_length=250, null=True, blank=True)
    tipoEstrutura = models.CharField(max_length=255, verbose_name="Tipo de estrutura", null=True, blank=True)
    logradouro = models.CharField(max_length=255, verbose_name="Logradouro",  null=True, blank=True)
    numeroEndereco = models.CharField(max_length=10, verbose_name="Número de endereço",  null=True, blank=True)
    complementoEndereco = models.CharField(max_length=255, verbose_name="Complemento", null=True, blank=True)
    bairro = models.CharField(max_length=255, verbose_name="Bairro", null=True, blank=True)
    municipio = models.CharField(max_length=255, verbose_name="Município",  null=True, blank=True)
    uf = models.CharField(max_length=2, verbose_name="UF", null=True, blank=True) #Unidade Federal
    cep = models.CharField(max_length=8, verbose_name="CEP", null=True, blank=True)
    rSaude = models.CharField(max_length=6, verbose_name="Região de saúde", null=True, blank=True)
    microrregiao = models.CharField(max_length=255, verbose_name="Microrregião", null=True, blank=True)
    distritosRegioesAdministrativas = models.CharField(max_length=255, null=True, blank=True, verbose_name="Distrito/Regiões administrativas")
    gerente = models.CharField(max_length=255, verbose_name="Gerente/Administrador", null=True, blank=True)
    registroConselhoDeClasse = models.CharField(max_length=60, null=True, blank=True, verbose_name="Registro Conselho de Classe")
    email = models.EmailField(max_length=150, null=True, blank=True,)
    telefone = models.CharField(max_length=12, null=True, blank=True, verbose_name="Telefone para contato")
    url = models.CharField(max_length=255, null=True, blank=True, verbose_name="URL")
    latitude = models.CharField(max_length=15, null=True, blank=True,verbose_name="Latitude")
    longitude = models.CharField(max_length=15, null=True, blank=True, verbose_name="Longitude")
    createdBy_user = models.ForeignKey(User, models.PROTECT, null=True, blank=True)    
    colaboradores = models.ManyToManyField(User, related_name='colaboradores', verbose_name='Funcionarios') #verificar
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    comentario = models.CharField(max_length=255, null=True, blank=True, verbose_name="Comentário")
    tipo = models.IntegerField(choices=tipoUnidade, default=1, null=False, verbose_name="Tipo Unidade")
    isVisible = models.BooleanField(default=True, verbose_name='Visível nas listagens?')
    isActive = models.BooleanField(default=True, verbose_name='Unidade esta ativa?')
    useCnesSms = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return "{}".format(self.nomeFantasia)    

class EstabelecimentoConfiguracoes(models.Model):
    estabelecimento = models.OneToOneField(Estabelecimento, models.CASCADE)
    createdBy_user = models.ForeignKey(User, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class UserEstabelecimento(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, unique=False, verbose_name="Colaboradores", related_name='Colaboradores')
    estabelecimento = models.ForeignKey(Estabelecimento, on_delete=models.PROTECT, verbose_name="Local de Trabalho", unique=False, related_name="estabelecimentoOrigem")

    def __str__(self):
        return "{}".format(self.user.first_name)