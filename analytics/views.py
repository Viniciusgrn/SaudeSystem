from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from cadastros.models import Paciente, VagaOfertada, Permuta
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from braces.views import GroupRequiredMixin

class DashboardList(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('userLogin')
    group_required = [u"administrator"]
    success_url = reverse_lazy('index')    

    def get(self, request):
        if (self.request.user.groups.filter(name = "administrator").exists()):
            User = get_user_model()
            users = User.objects.all()
            # pacientes = Paciente.objects.all()            
            return render(request, 'analytics/dashboard.html', {'users': users})