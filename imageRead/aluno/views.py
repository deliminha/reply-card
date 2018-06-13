from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Aluno
from ..turma.models import Turma

class AlunoTurmaList(UpdateView):
    model = Turma
    extra_context = {
        "operacao": "Estudantes",
        "movimentarTurma": False
    }
    fields = ['alunos']
    success_url = reverse_lazy('turma-aluno-list')
    template_name = 'turmas/form_alunos.html'