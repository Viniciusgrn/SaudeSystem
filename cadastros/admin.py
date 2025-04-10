from django.conf import PASSWORD_RESET_TIMEOUT_DAYS_DEPRECATED_MSG
from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authUser.models import Perfil

# importar as classes

from .models import Paciente, UnidadeSolicitante, UnidadeExecutante, Procedimento, VagaOfertada, UserUnidade, Configuration, Importar

class UserUnidadeInline(admin.StackedInline):
    model = UserUnidade
    verbose_name = "Selecione uma unidade para"
    can_delete = False

class UserConfigurationInline(admin.StackedInline):
    model = Configuration
    verbose_name = "Configurações do usuário"
    can_delete = False

class UserAdmin(UserAdmin):
    inlines = (UserUnidadeInline, UserConfigurationInline,)

class UserProfileInLine(admin.StackedInline):
    model = Perfil
    


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Paciente)
admin.site.register(UnidadeSolicitante)
admin.site.register(UnidadeExecutante)
admin.site.register(Procedimento)
admin.site.register(VagaOfertada)
admin.site.register(Importar)
