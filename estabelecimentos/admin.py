from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserEstabelecimento, TipoEstabelecimento, Estabelecimento, EstabelecimentoConfiguracoes

# class UserUnidadeInline(admin.StackedInline):
#     model = UserEstabelecimento
#     verbose_name = "Selecione um estabelecimento para"
#     can_delete = False

# class UserConfigurationInline(admin.StackedInline):
#     model = EstabelecimentoConfiguracoes
#     verbose_name = "Configurações do Estabelecimento"
#     can_delete = False

# class UserAdmin(UserAdmin):
#     inlines = (UserUnidadeInline, UserConfigurationInline,)

# admin.site.unregister(User)
# admin.site.register(User, UserAdmin)
# admin.site.register(Estabelecimento)
