"""Progressao URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from paginas import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('paginas.urls')),
    path('', include('cadastros.urls')),
    path('', include('analytics.urls')),
    path('', include('authUser.urls')),
    path('', include('support.urls')),
    path('', include('import.urls')),
    path('', include('contato.urls')),
    path('', include('classificacaoDeRisco.urls')),
    path('', include('Filipetas.urls')),
    path('', include('relatorios.urls')),
    path('', include('equipamentos.urls')),
    path('', include('estabelecimentos.urls')),
    path('', include('profissionais.urls')),
    path('', include('gestantes.urls')),
    path('', include('agendas.urls')),
    path('', include('unidadeDemanda.urls')),
    path('', include('malotes.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)