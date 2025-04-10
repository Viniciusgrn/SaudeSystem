from email.headerregistry import Group
from django.shortcuts import render
from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from .models import Estabelecimento, EstabelecimentoConfiguracoes
from profissionais.models import Profissional
# from .forms import EquipamentoForm
from cadastros.models import UnidadeSolicitante, UnidadeExecutante
from django.db.models import Q

###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
# As classes de unidades solicitantes e executantes unificarão em 
# uma nova classe chamada "Estabelecimentos"
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################

class UnidadeSolicitanteCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = UnidadeSolicitante
    fields = ['cnes', 'nome', 'tipo']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-unidsol')
    
class UnidadeSolicitanteUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = UnidadeSolicitante
    fields = ['cnes', 'nome','tipo','isActive','isVisible']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-unidsol')
    
class UnidadeSolicitanteDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = UnidadeSolicitante
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-unidsol')
    
class UnidadeSolicitanteList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    # paginate_by = 10
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = UnidadeSolicitante
    template_name = 'cadastros/listas/unidsol.html'
    
    
class UnidadeExecutanteCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = UnidadeExecutante
    fields = ['cnes', 'nome']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-unidexec')
    
class UnidadeExecutanteUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = UnidadeExecutante
    fields = ['cnes', 'nome']
    template_name = 'cadastros/form.html'
    success_url = reverse_lazy('listar-unidexec')
    
class UnidadeExecutanteDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = UnidadeExecutante
    template_name = 'cadastros/form-excluir.html'
    success_url = reverse_lazy('listar-unidexec')
    
class UnidadeExecutanteList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    # paginate_by = 10
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"callcenter"]
    model = UnidadeExecutante
    template_name = 'cadastros/listas/unidexec.html'
    success_url = reverse_lazy('index')

###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
# INICIO DA CLASSE ESTABELECIMENTOS
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################
###################################################################

class EstabelecimentoCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"regulacao"]
    template_name = "estabelecimentos/form.html"
    model = Estabelecimento
    fields = ['cnes','nomeFantasia','tipoEstabelecimento','gerente','email', 'tipo']
    success_url = reverse_lazy('list-estabelecimentos')


    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url
    
class EstabelecimentoProfissionalCreate(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"regulacao"]
    template_name = "profissionais/form.html"
    model = Profissional
    fields = ['cpf', 'cns', 'nome', 'municipioAtuacao']
    success_url = reverse_lazy('list-profissionais')

    def get_context_data(self, **kwargs):
        context = super(EstabelecimentoProfissionalCreate, self).get_context_data(**kwargs) # get the default context data
        context['estabelecimento'] = Estabelecimento.objects.first()        
        return context

    def form_valid(self, form, *args, **kwargs):        
        form.instance.estabelecimento_id = self.request.POST.get('estabelecimento_id')
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url

class EstabelecimentoList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"regulacao"]
    template_name = "estabelecimentos/list-estabelecimentos.html"
    model = Estabelecimento
    success_url = reverse_lazy('list-estabelecimentos')

class EstabelecimentoProfissionaisList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"regulacao"]
    template_name = "estabelecimentos/estabelecimentoProfissionais.html"
    model = Profissional
    success_url = reverse_lazy('index')

    def get_context_data(self, *args, **kwargs):        
        context = super(EstabelecimentoProfissionaisList, self).get_context_data(**kwargs)   
        estabelecimento = Estabelecimento.objects.get(pk=self.kwargs.get('pk'))      
        context['estabelecimento'] = estabelecimento        
        context['profissionais'] = Profissional.objects.filter(estabelecimento_id=self.kwargs.get('pk'))        
        
        return context

class EstabelecimentoUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"regulacao"]
    template_name = "estabelecimentos/form.html"
    model = Estabelecimento
    fields = ['cnes', 'tipoEstabelecimento',  'documentoEstabelecimento', 'cnpjMantenedora', 'naturezaJuridica', 'nomeEmpresarial', 'nomeFantasia', 'tipoEstrutura',
              'logradouro', 'numeroEndereco', 'complementoEndereco', 'bairro', 'municipio', 'uf', 'cep', 'rSaude', 'microrregiao', 'distritosRegioesAdministrativas', 'gerente', 'registroConselhoDeClasse',
              'email', 'url', 'latitude', 'longitude']
    success_url = reverse_lazy('list-estabelecimentos')

    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url

class EstabelecimentoConfiguracoesUpdate(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator", u"regulacao"]
    template_name = "estabelecimentos/estabelecimentoConfiguracoes.html"
    model = EstabelecimentoConfiguracoes
    fields = ['createdBy_user','updatedBy_user']
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        form.instance.createdBy_user = self.request.user
        url = super().form_valid(form)
        return url

    

class EstabelecimentoDelete(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    model = Estabelecimento
    template_name = 'estabelecimentos/form-excluir.html'
    success_url = reverse_lazy('list-estabelecimentos')
