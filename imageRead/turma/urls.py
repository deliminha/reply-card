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
from ..aluno import urls as alunoUrls

urlpatterns = [
    path('', views.index, name='index'),
    path('cadastrar',           views.TurmaCreate.as_view(),        name='turma-create'),
    path('<int:pk>/atualizar',  views.TurmaUpdate.as_view(),        name='turma-update'),
    path('<int:pk>/remover',    views.TurmaDelete.as_view(),        name='turma-delete'),
    path('listar',              views.TurmaList.as_view(),          name='turma-list'),
    path('listar/alunos',       views.TurmaAlunosList.as_view(),    name='turma-aluno-list'),
    path('',                    include(alunoUrls)),

    path('questionario/cadastrar',                   views.QuestionarioCreate.as_view(),         name='questionario-create'),
    path('<int:pk>/questionario/cadastrar/questoes', views.QuestionarioCreateQuestoes.as_view(), name='questionario-create-details'),
    path('<int:pk>/questionario/atualizar',          views.QuestionarioUpdate.as_view(),         name='questionario-update'),
    path('<int:pk>/questionario/remover',            views.QuestionarioDelete.as_view(),         name='questionario-delete'),

    path('sessao/cadastrar',                views.SessaoCreate.as_view(),   name='sessao-create'),
    path('<int:pk>/sessao/atualizar',       views.SessaoUpdate.as_view(),   name='sessao-update'),
    path('<int:pk>/sessao/remover',         views.SessaoDelete.as_view(),   name='sessao-delete'),
    path('<int:pk>/sessao/folha_resposta_padrao', views.SessaoGabarito.as_view(), name='sessao-folha-resposta'),
    path('<int:pk>/sessao/folha_resposta_turma',  views.SessaoGabaritoTurma.as_view(), name='sessao-folha-resposta-turma'),


    path('<int:pk>/sessao/detalhes',                    views.SessaoDetails.as_view(),      name='sessao-details'),
    path('<int:pk_1>/sessao/detalhes/aluno/<int:pk_2>', views.SessaoAlunoDetails.as_view(), name='sessao-aluno-details'),
    path('<int:pk_1>/sessao/detalhes/aluno/<int:pk_2>/avaliar', views.sessaoEvaluate, name='sessao-evaluate'),
]
