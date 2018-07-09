from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Aluno
from ..turma.models import Turma


@method_decorator(login_required, name='dispatch')
class AlunoTurmaList(ListView):
    model = Aluno
    extra_context = {
        "operacao": "Estudantes",
    }
    success_url = reverse_lazy('turma-aluno-list')
    template_name = 'turmas/form_alunos.html'

    def get_queryset(self):
        self.turma = get_object_or_404(Turma, pk=self.kwargs['pk'])
        self.extra_context['turma'] = self.turma
        return Aluno.objects.filter(turma=self.turma)


@method_decorator(login_required, name='dispatch')
class AlunoCreate(CreateView):
    model = Aluno
    extra_context = {"operacao": "Cadastro"}
    fields = ['matricula', 'nome', 'turma']
    success_url = reverse_lazy('turma-aluno-list')
    template_name = 'alunos/form.html'


@method_decorator(login_required, name='dispatch')
class AlunoUpdate(UpdateView):
    model = Aluno
    extra_context = {"operacao": "Atualização"}
    fields = ['matricula', 'nome']
    template_name = 'alunos/form.html'


@method_decorator(login_required, name='dispatch')
class AlunoDelete(DeleteView):
    model = Aluno
    success_url = reverse_lazy('turma-aluno-list')
    template_name = 'alunos/delete.html'
