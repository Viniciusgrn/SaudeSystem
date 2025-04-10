import django
from django.views.generic import TemplateView
from cadastros.models import UserUnidade, UnidadeSolicitante, Importar, HistoricoImportacao, Paciente, VagaOfertada, Permuta
from support.models import Chamado
from equipamentos.models import Equipamento
from django.urls import reverse_lazy
import datetime
from datetime import date, timedelta

#Create your views here
#class IndexView(TemplateView):
# template_name = 'modelo.html'

#class PaginaInicial(TemplateView):
#     template_name = "modelo.html"


# A classe PaginaInicial "extends" TemplateView
class PaginaInicial(TemplateView):
    login_url = reverse_lazy('userLogin')
    # Toda classe filha do TemplateView precisa do
    # atributo abaixo para definir um template a ser renderizado
    template_name = 'paginas/index2.html'

    def get_context_data(self, **kwargs):
         context = super(PaginaInicial, self).get_context_data(**kwargs)
         if self.request.user.is_authenticated:
            unidade_id = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.id
            context['unidade_id'] = unidade_id
            context['unidade'] = UserUnidade.objects.filter(user=self.request.user)[0].unidadeSolicitante.nome
            context["colaboradores"] = UserUnidade.objects.filter(unidadeSolicitante_id=unidade_id)

            ############### chamados            
            context['chamadosTotal'] = Chamado.objects.all().count()
            context['chamadosAguardando'] = Chamado.objects.filter(status=1).count()            
            context['chamadosAndamento'] = Chamado.objects.filter(status=3).count()
            context['chamadosConcluido'] = Chamado.objects.filter(status=4).count()
            
            ############### equipamentos
            context['equipamentoTotal'] = Equipamento.objects.all().count()
            context['computadores'] = Equipamento.objects.filter(equipamento="Computador").count()
            context['impressoras'] = Equipamento.objects.filter(equipamento="Impressora").count()
            context['tablets'] = Equipamento.objects.filter(equipamento="Tablet").count()            
            ############### fila
            context['totalPessoasFila'] = Importar.objects.filter(alias__isnull=False).count()
            context['totalPessoasFilaSimples'] = Importar.objects.filter(tipoFila=2).filter(alias__isnull=False).count()
            context['totalPessoasFilaRegulada'] = Importar.objects.filter(tipoFila=1).filter(alias__isnull=False).count()
            context['filaReguladaGrafico'] = HistoricoImportacao.objects.filter(totalFila__isnull=False).values('dataDoArquivo','tipoFila','totalFila')
            
            ############### Pacientes
            context['totalPacientesHoje'] = Paciente.objects.filter(created_at__range=[datetime.datetime.now()+timedelta(days=-1), datetime.datetime.now()]).count()
            context['totalPacientes30'] = Paciente.objects.filter(created_at__range=[datetime.datetime.now()+timedelta(days=-30), datetime.datetime.now()]).count()
            context['totalPacientes15'] = Paciente.objects.filter(created_at__range=[datetime.datetime.now()+timedelta(days=-15), datetime.datetime.now()]).count()
            context['totalPacientes7'] = Paciente.objects.filter(created_at__range=[datetime.datetime.now()+timedelta(days=-7), datetime.datetime.now()]).count()
            
            ############### Vagas
            context['vagaOfertada30'] = VagaOfertada.objects.filter(created_at__range=[datetime.datetime.now()+timedelta(days=-30), datetime.datetime.now()]).count()
            context['vagaOfertada7'] = VagaOfertada.objects.filter(created_at__range=[datetime.datetime.now()+timedelta(days=-7), datetime.datetime.now()]).count()
            context['vagaOfertadaHoje'] = VagaOfertada.objects.filter(created_at__range=[datetime.datetime.now()+timedelta(days=-1), datetime.datetime.now()]).count()
            ############### Permutas
            context['vagaPermutada30'] = Permuta.objects.filter(created_at__range=[datetime.datetime.now()+timedelta(days=-30), datetime.datetime.now()]).count()
            context['vagaPermutada7'] = Permuta.objects.filter(created_at__range=[datetime.datetime.now()+timedelta(days=-7), datetime.datetime.now()]).count()
            context['vagaPermutadaHoje'] = Permuta.objects.filter(created_at__range=[datetime.datetime.now()+timedelta(days=-1), datetime.datetime.now()]).count()


            
            return context
         return context

class SobreView(TemplateView):
   template_name = 'paginas/sobre.html'

class AjudaView(TemplateView):
   template_name = 'paginas/ajuda.html'