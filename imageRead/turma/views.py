from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Turma


# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')


@method_decorator(login_required, name='dispatch')
class TurmaCreate(CreateView):
    model = Turma
    extra_context = {"operacao": "Cadastro"}
    fields = ['nome', 'descricao', 'alunos']
    template_name = 'turmas/form.html'


@method_decorator(login_required, name='dispatch')
class TurmaDetail(DetailView):
    model = Turma
    template_name = 'turmas/detail.html'


@method_decorator(login_required, name='dispatch')
class TurmaUpdate(UpdateView):
    model = Turma
    extra_context = {"operacao": "Atualização"}
    fields = ['nome', 'descricao']
    template_name = 'turmas/form.html'


@method_decorator(login_required, name='dispatch')
class TurmaDelete(DeleteView):
    model = Turma
    success_url = reverse_lazy('turma-list')
    template_name = 'turmas/delete.html'


@method_decorator(login_required, name='dispatch')
class TurmaList(ListView):
    model = Turma
    extra_context = {"movimentarTurma": True}
    template_name = 'turmas/list.html'


@method_decorator(login_required, name='dispatch')
class TurmaAlunosList(ListView):
    model = Turma
    extra_context = {"movimentarTurma": False}
    template_name = 'turmas/list.html'
