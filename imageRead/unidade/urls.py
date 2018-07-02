"""imageRead URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include

from . import views
from ..turma import urls as turmaUrls

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/cadastrar',  views.UnidadeCreate.as_view,  name='unidade-create'),
    path('<int:pk>',            views.UnidadeDetail.as_view,  name='unidade-read'),
    path('<int:pk>/atualizar',  views.UnidadeUpdate.as_view,  name='unidade-update'),
    path('<int:pk>/remover',    views.UnidadeDelete.as_view,  name='unidade-delete'),
    path('turmas/',             include(turmaUrls)),
    path('listar',              views.UnidadeList.as_view,    name='unidade-list'),
]
