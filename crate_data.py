from mailbox import NotEmptyError
import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Progressao.settings")
django.setup()

import string
import timeit
from random import choice, randint, random

from cadastros.models import Procedimento



class ProcedimentoClass:

    @staticmethod
    def criar_procedimentos(procedimentos):
        Procedimento.objects.all().delete()
        aux = []
        for proc in procedimentos:
            print(procedimentos)
            data = dict(
               nome = proc
                                               
            )
            obj = Procedimento(**data)
            aux.append(obj)
        Procedimento.objects.bulk_create(aux)

procedimentos = (
'ACUPUNTURA',
'ALERGOLOGIA',
'ALERGOLOGIA-PEDIATRIA',
'ANGIOFLUORESCEINOGRAFIA',
'AUDIOMETRIA E IMITANCIOMETRIA',
'AUDIOMETRIA E IMITANCIOMETRIA - INFANTIL',
'AVALIACAO AUDITIVA COMPORTAMENTAL',
'BERA',
'BERA - POTENCIAL EVOCADO AUDITIVO P/ TRIAGEM AUDITIVA',
'BIOMETRIA ULTRASSONICA',
'CAMPIMETRIA COMPUTADORIZADA',
'CAPSULOTOMIA A YAG LASER',
'CARDIOLOGIA',
'CIRURGIA GERAL',
'CIRURGIA VASCULAR',
'COLONOSCOPIA',
'COLONOSCOPIA COM BIOPSIA',
'COLONOSCOPIA- INTERNADOS',
'COLPOSCOPIA',
'CURVA TENSIONAL DIARIA',
'DENSITOMETRIA',
'DENSITOMETRIA OSSEA - ACIMA DO PESO',
'DERMATOLOGIA',
'ECOCARDIOGRAFIA BI-DIMENSIONAL COM DOPPLER ADULTO',
'ECOCARDIOGRAFIA TRANSESOFAGICA',
'ECOCARDIOGRAFIA TRANSTORACICA',
'ECOCARDIOGRAMA INFANTIL',
'ECODOPPLERCARDIOGRAMA COM ESTRESSE FARMACOLOGICO',
'EED ESOFAG0, HIATO, ESTOMAGO E DUODENO',
'ELETROENCEFALOGRAMA',
'ELETROENCEFALOGRAMA EM VIGILIA E SONO',
'ELETRONEUROMIOGRAFIA - FACE',
'ELETRONEUROMIOGRAFIA DE MMII',
'ELETRONEUROMIOGRAFIA DE MMSS',
'EMISSOES OTOACUSTICA',
'ENDOCRINOLOGIA',
'ENDOSCOPIA',
'ENDOSCOPIA INFANTIL',
'ENDOSCOPIA INTERNADOS',
'ENEMA OPACO',
'ESPIROMETRIA',
'ESTUDO URODINAMICO',
'FOTOCOAGULACAO A LASER',
'FUNDOSCOPIA',
'GASTROENTEROLOGIA',
'GERIATRIA - GERAL',
'GERIATRIA GERAL RETORNO',
'GONIOSCOPIA',
'HEMATOLOGIA',
'HISTEROSSALPINGOGRAFIA',
'HOLTER 24 HORAS',
'INFECTOLOGIA',
'IRIDOTOMIA A LASER',
'MAMOGRAFIA',
'MANOMETRIA ANORETAL',
'MANOMETRIA ESOFAGICA',
'MAPA',
'MAPEAMENTO DE RETINA',
'MASTOLOGIA',
'NASOFIBROSCOPIA',
'NASOFIBROSCOPIA FLEXIVEL',
'NEFROLOGIA ',
'NEUROCIRURGIA',
'NEUROLOGIA',
'NEUROLOGIA - PEDIATRIA',
'OFTALMOLOGIA',
'ORTOPEDIA ',
'OTORRINOLARINGOLOGIA',
'PAQUIMETRIA ULTRASSONICA',
'PHMETRIA',
'PNEUMOLOGIA',
'PNEUMOLOGIA - PEDIATRIA',
'POLISSONOGRAFIA',
'POLISSONOGRAFIA CPAP/BIPAP/SPLIT-NIGHT',
'PROCTOLOGIA',
'PSIQUIATRIA - ADULTO',
'RADIOGRAFIA PANORAMICA',
'RETINOGRAFIA',
'RETOSSIGMOIDOSCOPIA',
'REUMATOLOGIA',
'RM ABDOMEN SUPERIOR',
'RM ABDOMEN SUPERIOR COM CONTRASTE',
'RM ABDOMEN TOTAL',
'RM BACIA / PELVE',
'RM BACIA / PELVE COM CONTRASTE',
'RM COLUNA CERVICAL',
'RM COLUNA LOMBAR',
'RM COLUNA LOMBO-SACRA',
'RM COLUNA TORACICA',
'RM COTOVELO ESQUERDO',
'RM CRANIO',
'RM CRANIO COM CONTRASTE',
'RM DE COLUNA DORSAL ADULTO',
'RM DE SEIOS DA FACE ADULTO C/ CONTRASTE S/SEDACAO',
'RM HIPOFISE',
'RM JOELHO (UNILATERAL)',
'RM MAO DIREITA',
'RM MASTOIDES OU OUVIDOS',
'RM MEMBRO INFERIOR (UNILATERAL)',
'RM OMBRO (UNILATERAL)',
'RM OSSOS TEMPORAIS',
'RM PERNA DIREITA',
'RM PERNA ESQUERDA',
'RM PESCOCO E REGIAO CERVICAL',
'RM TORAX',
'RM TORNOZELO OU PE (UNILATERAL)',
'TC ABDOMEN INFERIOR',
'TC ABDOMEN INFERIOR COM CONTRASTE',
'TC ABDOMEN SUPERIOR',
'TC ABDOMEN SUPERIOR COM CONTRASTE',
'TC ABDOMEN TOTAL',
'TC ABDOMEN TOTAL COM CONTRASTE',
'TC APARELHO URINARIO - COM LAUDO',
'TC ARTICULACOES COXO-FEMURAIS',
'TC COERANCIA OPTICA',
'TC COLUNA CERVICAL',
'TC COLUNA CERVICAL COM CONTRASTE',
'TC COLUNA LOMBO-SACRA',
'TC COLUNA LOMBO-SACRA COM CONTRASTE',
'TC COLUNA TORACICA',
'TC COTOVELO ESQUERDO',
'TC CRANIO',
'TC CRANIO COM CONTRASTE',
'TC FACE OU SEIOS DE FACE SEM CONTRASTE',
'TC MASTOIDES OU OUVIDOS',
'TC OMBRO DIREITO',
'TC PELVE OU BACIA',
'TC PELVE OU BACIA COM CONTRASTE',
'TC PESCOCO COM CONTRASTE',
'TC QUADRIL ADULTO S/C',
'TC SEIOS DE FACE',
'TC TORAX',
'TC TORAX ADULTO SEM SEDACAO',
'TC TORAX COM CONTRASTE',
'TC TORNOZELO ESQUERDO',
'TESTE DE ESFORCO OU TESTE ERGOMETRICO',
'TESTE ORTOPTICO',
'TESTES DE CONTATOS',
'TONOMETRIA',
'URETROCISTOGRAFIA',
'UROGRAFIA EXCRETORA',
'UROLOGIA',
'UROLOGIA - GERAL II',
'UROLOGIA - RETORNO',
'UROLOGIA GERAL - PEDIATRIA',
'UROLOGIA GERAL RETORNO',
'USG ABDOMEM TOTAL',
'USG ABDOMEN INFERIOR',
'USG ABDOMEN SUPERIOR (FIGADO, VESICULA, VIAS BILIARES)',
'USG APARELHO URINARIO (RINS, BEXIGA)',
'USG ARTICULACAO - ANTEBRACO',
'USG ARTICULACAO - BRACO',
'USG ARTICULACAO - MAO',
'USG ARTICULACAO CLAVICULA',
'USG BOLSA ESCROTAL',
'USG BOLSA ESCROTAL COM DOPPLER COLORIDO',
'USG BRACO DIREITO',
'USG BRACO ESQUERDO',
'USG CERVICAL (PESCOCO)',
'USG COTOVELO',
'USG COTOVELO DIREITO',
'USG COTOVELO ESQUERDO',
'USG COXA',
'USG DOPPLER - ARTERIAS RENAIS',
'USG DOPPLER - CAROTIDAS E VERTEBRAIS',
'USG DOPPLER - TRANSVAGINAL',
'USG DOPPLER ARTERIAL DE MMII',
'USG DOPPLER CAROTIDAS E VERTEBRAIS',
'USG DOPPLER DAS ARTERIAS DOS MEMBROS SUPERIORES',
'USG DOPPLER DE ARTERIA AORTA ABDOMINAL',
'USG DOPPLER DE TIREOIDE',
'USG DOPPLER PELVICA - GINECOLOGICA',
'USG DOPPLER PENIANO',
'USG DOPPLER VENOSO DE MI',
'USG DOPPLER VENOSO DE MMII',
'USG FACE',
'USG GLOBO OCULAR OU DE ORBITA',
'USG JOELHO',
'USG JOELHO DIREITO',
'USG JOELHO ESQUERDO',
'USG MAMARIA',
'USG MAO DIREITA',
'USG MAO ESQUERDA',
'USG OBSTETRICA',
'USG OMBRO',
'USG OMBRO DIREITO',
'USG OMBRO ESQUERDO',
'USG PAREDE ABDOMINAL',
'USG PAROTIDAS',
'USG PARTES MOLES',
'USG PE DIREITO',
'USG PE ESQUERDO',
'USG PE/CALCANEO',
'USG PELVICA',
'USG PENIANA',
'USG PERNA DIREITA',
'USG PERNA ESQUERDA',
'USG PROSTATA',
'USG PROSTATA ( VIA TRANSRETAL)',
'USG PROSTATA VIA ABDOMINAL',
'USG PUNHO',
'USG PUNHO DIREITO',
'USG QUADRIL',
'USG QUADRIL/COXO-FEMURAL',
'USG QUADRIL/COXO-FEMURAL DIREITO',
'USG QUADRIL/COXO-FEMURAL ESQUERDO',
'USG REGIAO CERVICAL (PESCOCO) COM DOPPLER',
'USG REGIAO INGUINAL',
'USG TIREOIDE',
'USG TORAX (EXTRACARDIACO)',
'USG TORNOZELO',
'USG TORNOZELO DIREITO',
'USG TORNOZELO ESQUERDO',
'USG TRANSVAGINAL',
'VECTOELETRONISTAGMOGRAFIA(VENG)',
'VIDEODEGLUTOGRAMA',
'VIDEOENDOSCOPIA NASAL RIGIDA',
'VIDEONASOFIBROSCOPIA',
)

ProcedimentoClass.criar_procedimentos(procedimentos)
print('ok')