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
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:pk>/cadastrar',  views.TurmaCreate.as_view(),  name='turma-create'),
    path('<int:pk>',            views.TurmaDetail.as_view(),  name='turma-read'),
    path('<int:pk>/atualizar',  views.TurmaUpdate.as_view(),  name='turma-update'),
    path('<int:pk>/remover',    views.TurmaDelete.as_view(),  name='turma-delete'),
    path('listar',              views.TurmaList.as_view(),    name='turma-list'),
]
