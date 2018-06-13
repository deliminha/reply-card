from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Turma


# Create your views here.

def index(request):
    return render(request, 'index.html')


class TurmaCreate(CreateView):
    model = Turma
    extra_context = {"operacao": "Cadastro"}
    fields = ['nome', 'descricao', 'alunos']
    template_name = 'turmas/form.html'


class TurmaDetail(DetailView):
    model = Turma
    template_name = 'turmas/detail.html'


class TurmaUpdate(UpdateView):
    model = Turma
    extra_context = {"operacao": "Atualização"}
    fields = ['nome', 'descricao']
    template_name = 'turmas/form.html'


class TurmaDelete(DeleteView):
    model = Turma
    success_url = reverse_lazy('turma-list')
    template_name = 'turmas/delete.html'


class TurmaList(ListView):
    model = Turma
    extra_context = {"movimentarTurma": True}
    template_name = 'turmas/list.html'

class TurmaAlunosList(ListView):
    model = Turma
    extra_context = {"movimentarTurma": False}
    template_name = 'turmas/list.html'