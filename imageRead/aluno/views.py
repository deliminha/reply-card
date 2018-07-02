from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView

from ..turma.models import Turma


@method_decorator(login_required, name='dispatch')
class AlunoTurmaList(UpdateView):
    model = Turma
    extra_context = {
        "operacao": "Estudantes",
        "movimentarTurma": False
    }
    fields = ['alunos']
    success_url = reverse_lazy('turma-aluno-list')
    template_name = 'turmas/form_alunos.html'

    queryset = Turma.objects.all().prefetch_related('alunos')