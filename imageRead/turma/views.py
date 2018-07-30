import string

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Turma, Sessao, Questionario
from ..aluno.models import Aluno, AlunoSessao


from ..core.corretor.CameraRecognition import CameraRecognition

# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')


@method_decorator(login_required, name='dispatch')
class TurmaCreate(CreateView):
    model = Turma
    extra_context = {"operacao": "Cadastro"}
    fields = ['nome', 'descricao', 'data_referencia']
    success_url = reverse_lazy('turma-list')
    template_name = 'turmas/form.html'


@method_decorator(login_required, name='dispatch')
class TurmaUpdate(UpdateView):
    model = Turma
    extra_context = {"operacao": "Atualização"}
    fields = ['nome', 'descricao', 'data_referencia']
    success_url = reverse_lazy('turma-list')
    template_name = 'turmas/form.html'


@method_decorator(login_required, name='dispatch')
class TurmaDelete(DeleteView):
    model = Turma
    success_url = reverse_lazy('turma-list')
    template_name = 'turmas/delete.html'


@method_decorator(login_required, name='dispatch')
class TurmaList(ListView):
    model = Turma
    extra_context = {
        "movimentarTurma": True
    }
    template_name = 'turmas/list.html'


@method_decorator(login_required, name='dispatch')
class TurmaAlunosList(ListView):
    model = Turma

    def get_queryset(self):
        self.object_list = Turma.objects.all()
        return self.object_list

    def get_context_data(self, **kwargs):
        extra_context = super().get_context_data(**kwargs)
        extra_context["movimentarTurma"] = False
        return extra_context

    template_name = 'turmas/list.html'


@method_decorator(login_required, name='dispatch')
class QuestionarioCreate(CreateView):
    model = Questionario
    extra_context = {"operacao": "Cadastro"}
    fields = ['nome', 'pontMax', 'pontMin', 'media', 'quantidade_questoes']
    template_name = 'sessao/questionario/form.html'


@method_decorator(login_required, name='dispatch')
class QuestionarioCreateQuestoes(UpdateView):
    model = Questionario
    fields = ['descricao_alterativas']
    extra_context = {
        "operacao": "Atualização"
    }
    success_url = reverse_lazy('sessao-create')
    template_name = 'sessao/questionario/form_questoes.html'

    def get_context_data(self, **kwargs):
        extra_context = super().get_context_data(**kwargs)
        questionario = Questionario.objects.get(pk=self.kwargs.get('pk'))
        extra_context["questionario"] = questionario
        extra_context["quantidade_questoes"] = range(questionario.quantidade_questoes)
        return extra_context


@method_decorator(login_required, name='dispatch')
class QuestionarioUpdate(UpdateView):
    model = Questionario
    extra_context = {
        "operacao": "Atualização",
        "atualizacao": True
    }
    fields = ['nome', 'pontMax', 'pontMin', 'media', 'quantidade_questoes']
    template_name = 'sessao/questionario/form.html'


@method_decorator(login_required, name='dispatch')
class QuestionarioDelete(DeleteView):
    model = Questionario
    success_url = reverse_lazy('turma-aluno-list')
    template_name = 'sessao/questionario/delete.html'


@method_decorator(login_required, name='dispatch')
class SessaoCreate(CreateView):
    model = Sessao
    extra_context = {"operacao": "Cadastro"}
    fields = ['questionario', 'dataAplicacao', 'turma']
    template_name = 'sessao/form.html'


@method_decorator(login_required, name='dispatch')
class SessaoUpdate(UpdateView):
    model = Sessao
    extra_context = {
        "operacao": "Atualização",
        "atualizacao": True
    }
    fields = ['questionario', 'dataAplicacao', 'turma']
    template_name = 'sessao/form.html'


@method_decorator(login_required, name='dispatch')
class SessaoDelete(DeleteView):
    model = Sessao
    template_name = 'sessao/delete.html'
    success_url = reverse_lazy('turma-aluno-list')

    def delete(self, request, *args, **kwargs):
        self.sessao = self.get_object()
        self.questionario = self.sessao.questionario
        self.questionario.delete()
        self.sessao.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)


@method_decorator(login_required, name='dispatch')
class SessaoGabarito(DetailView):
    model = Sessao
    extra_context = {
        "alternativas": list(string.ascii_uppercase)[:5]
    }
    fields = ['questionario', 'dataAplicacao', 'turma']
    success_url = reverse_lazy('turma-aluno-list')
    template_name = 'sessao/folha_resposta_generica.html'

    def get_context_data(self, **kwargs):
        extra_context = super().get_context_data(**kwargs)
        sessao = Sessao.objects.get(pk=self.kwargs.get('pk'))
        questionario = sessao.questionario
        extra_context["questionario"] = questionario
        extra_context["quantidade_questoes"] = range(questionario.quantidade_questoes)
        return extra_context


@method_decorator(login_required, name='dispatch')
class SessaoGabaritoTurma(DetailView):
    model = Sessao
    extra_context = {
        "alternativas": list(string.ascii_uppercase)[:5]
    }
    fields = ['questionario', 'dataAplicacao', 'turma']
    success_url = reverse_lazy('turma-aluno-list')
    template_name = 'sessao/folha_resposta_generica_turma.html'

    def get_context_data(self, **kwargs):
        extra_context = super().get_context_data(**kwargs)

        sessao = Sessao.objects.get(pk=self.kwargs.get('pk'))
        alunos = Aluno.objects.filter(turma_id=sessao.turma.pk)

        if not alunos:
            extra_context["mensagem_erro"] = "não há alunos matriculados na turma!"

        questionario = sessao.questionario
        extra_context["questionario"] = questionario
        extra_context["alunos"] = alunos
        extra_context["quantidade_questoes"] = range(questionario.quantidade_questoes)
        return extra_context


class SessaoEvaluate(DetailView):
    model = Sessao
    extra_context = {
        "alternativas": list(string.ascii_uppercase)[:5]
    }
    fields = ['questionario', 'dataAplicacao', 'turma']
    success_url = reverse_lazy('turma-aluno-list')
    template_name = 'sessao/avaliar_sessao.html'

    def get_context_data(self, **kwargs):
        extra_context = super().get_context_data(**kwargs)

        sessao = Sessao.objects.get(pk=self.kwargs.get('pk'))
        alunosSessao = AlunoSessao.objects.filter(sessao_id=sessao.pk)
        alunos = Aluno.objects.filter(turma_id=sessao.turma.pk)
        if not alunosSessao or (alunosSessao.count() != alunos.count()):
            for aluno in alunos:
                AlunoSessao.objects.update_or_create(aluno=aluno, sessao=sessao, media=0, descricao_alterativas='')

        questionario = sessao.questionario
        extra_context["questionario"] = questionario
        extra_context["alunosSessao"] = alunosSessao
        extra_context["quantidade_questoes"] = range(questionario.quantidade_questoes)
        return extra_context
