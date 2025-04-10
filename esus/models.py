from django.db import models
from django.core.exceptions import PermissionDenied

class Ta_Cidadao(models.Model):
    co_seq_tacidadao = models.BigAutoField(null=False, primary_key=True)
    co_tipo_auditoria = models.CharField(null=False, max_length=1)
    dt_auditoria = models.DateTimeField(null=False) #somente a data
    co_seq_cidadao = models.BigIntegerField(null=True)
    co_unico_cidadao_prontuario = models.CharField(max_length=36, null=True)
    co_unico_prontuario = models.CharField(max_length=36, null=True)
    st_desconhece_nome_mae = models.IntegerField(null=True)
    co_localidade = models.IntegerField(null=True)
    nu_area = models.CharField(max_length=3, null=True)
    nu_micro_area = models.CharField(max_length=3, null=True)
    nu_nis_pis_pasep = models.CharField(max_length=50, null=True)
    dt_atualizado = models.DateTimeField(max_length=6, null=True) #somente a data
    nu_cns_responsavel = models.CharField(max_length=16, null=True)
    no_responsavel = models.CharField(max_length=255, null=True)
    dt_nascimento_responsavel = models.DateTimeField(max_length=6, null=True) #somente a data
    nu_cns_cuidador = models.CharField(max_length=16, null=True)
    no_cuidador = models.CharField(max_length=255, null=True)
    dt_nascimento_cuidador = models.DateTimeField(max_length=6, null=True) #somente a data
    tp_cds_cuidador = models.BigIntegerField(null=True)
    co_unico_cidadao = models.CharField(max_length=96, null=True)
    co_nacionalidade = models.BigIntegerField(null=True)
    co_pais_nascimento = models.BigIntegerField(null=True)
    co_unico_ultima_ficha = models.CharField(max_length=96, null=True)
    dt_ultima_ficha = models.DateTimeField(null=True) #somente a data
    st_registro_cadsus = models.IntegerField(null=True)
    dt_atualizado_cadsus = models.DateField(null=True)
    st_desconhece_nome_pai = models.IntegerField(null=True)
    dt_naturalizacao = models.DateTimeField(null=True)
    dt_entrada_brasil = models.DateTimeField(null=True)
    nu_portaria_naturalizacao = models.CharField(max_length=16, null=True)
    st_fora_area = models.IntegerField(null=True)
    st_infrm_orientacao_sexual = models.IntegerField(null=True)
    tp_orientacao_sexual = models.CharField(max_length=25, null=True)
    st_infrm_identidade_genero = models.IntegerField(null=True)
    tp_identidade_genero = models.CharField(max_length=25, null=True)
    st_compartilhamento_prontuario = models.IntegerField(null=True)
    st_ativo = models.IntegerField(null=True)
    st_nao_possui_cuidador = models.IntegerField(null=True)
    nu_cpf = models.CharField(max_length=11, null=True)
    nu_cns = models.CharField(max_length=16, null=True)
    no_cidadao = models.CharField(max_length=500, null=True)
    no_cidadao_filtro = models.CharField(max_length=600, null=True)
    co_escolaridade = models.BigIntegerField(null=True)
    co_raca_cor = models.BigIntegerField(null=True)
    co_etnia = models.BigIntegerField(null=True)
    co_estado_civil = models.BigIntegerField(null=True)
    co_cbo = models.DateField(null=True)
    dt_nascimento = models.DateField(null=True)
    dt_obito = models.DateField(null=True)
    no_mae = models.CharField(max_length=500, null=True)
    no_mae_filtro = models.CharField(max_length=600, null=True)
    no_pai = models.CharField(max_length=500, null=True)
    no_social = models.CharField(max_length=255, null=True)
    st_faleceu = models.IntegerField(null=True)
    nu_documento_obito = models.CharField(max_length=255, null=True)
    st_dados_obito_cadsus = models.IntegerField(null=True)
    no_localidade_exterior = models.CharField(max_length=255, null=True)
    co_pais_exterior = models.BigIntegerField(null=True)
    ds_cep = models.CharField(max_length=8, null=True)
    ds_complemento = models.CharField(max_length=50, null=True)
    ds_ponto_referencia = models.CharField(max_length=50, null=True)
    ds_logradouro = models.CharField(max_length=100, null=True)
    co_uf = models.CharField(max_length=150, null=True)
    co_localidade_endereco = models.BigIntegerField(null=True)
    nu_numero = models.CharField(max_length=20, null=True)
    st_sem_numero = models.IntegerField(null=True)
    no_bairro = models.CharField(max_length=255, null=True)
    no_bairro_filtro = models.CharField(max_length=255, null=True)
    tp_logradouro = models.BigIntegerField(null=True)
    nu_telefone_residencial = models.CharField(max_length=255, null=True)
    nu_telefone_celular = models.CharField(max_length=255, null=True)
    nu_telefone_contato = models.CharField(max_length=255, null=True)
    ds_email = models.CharField(max_length=255, null=True)
    st_ativo_para_exibicao = models.IntegerField(null=True)
    st_unificado = models.IntegerField(null=True)
    st_territorio_utiliza_cpf = models.IntegerField(null=True)
    nu_cpf_cuidador = models.CharField(max_length=255, null=True)
    nu_cpf_responsavel = models.CharField(max_length=255, null=True)
    no_tipo_sanguineo = models.CharField(max_length=255, null=True)
    no_sexo = models.CharField(max_length=255, null=True)
    
    class Meta:
        db_table = 'ta_cidadao'
        managed = False
        default_permissions = ['view']
        
    def save(self, *args, **kwargs):
        if self.pk is None:
            raise PermissionDenied("Criação de registros não é permitida.")
        else: 
            raise PermissionDenied("Atualização de registros não é permitida.")
    
    def delete(self, *args, **kwargs):
        raise PermissionDenied("Exclusão de registros não é permitida.")