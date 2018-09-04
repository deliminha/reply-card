import os
import string
from functools import reduce

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Turma, Sessao, Questionario
from ..aluno.models import Aluno, AlunoSessao
from ..core.corretor.CameraRecognition import CameraRecognition, myThread


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
    fields = ['descricao_alterativas', 'pesos_alterativas']
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
        extra_context["pesos"] = range(1, questionario.quantidade_questoes + 1)
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


@method_decorator(login_required, name='dispatch')
class SessaoDetails(DetailView):
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


@method_decorator(login_required, name='dispatch')
class SessaoAlunoDetails(DetailView):
    model = AlunoSessao
    extra_context = {
        "operacao": "Respostas"
    }
    template_name = 'sessao/folha_resposta_aluno.html'

    def get_object(self):
        return AlunoSessao.objects.get(pk=self.kwargs.get("pk_2"))

    def get_context_data(self, **kwargs):
        extra_context = super().get_context_data(**kwargs)
        alunoSessao = self.get_object()

        if len(alunoSessao.descricao_alterativas) > 0:
            sessao = Sessao.objects.get(pk=self.kwargs.get("pk_1"))
            extra_context["sessao"] = sessao
            extra_context["questionario"] = sessao.questionario
            extra_context["quantidade_questoes"] = range(sessao.questionario.quantidade_questoes)
            return extra_context

        extra_context["mensagem_erro"] = "Prova do(a) Aluno(a) '{}' ainda não foi avaliada!".format(alunoSessao.aluno.nome)
        return extra_context


@login_required
def sessaoEvaluate(request, pk_1, pk_2):
    sessao = Sessao.objects.get(pk=pk_1)
    cameraThread = myThread()
    cameraThread.start()
    status, answer = cameraThread.run_thread(sessao.questionario.quantidade_questoes)
    if status:
        if answer:
            descricao_resposta = []
            for key, question in answer.items():
                if None in question:
                    question.remove(None)

                if len(question) == 1:
                    for alternative in question:
                        if alternative is not None:
                            descricao_resposta.append(alternative)
                    continue

                if len(question) in range(10):
                    descricao_resposta.append([])
                    continue

            descricao_pontuacao, media, descricao_resposta = evaluate_test(sessao.questionario.descricao_alterativas,
                                                                           sessao.questionario.pesos_alterativas,
                                                                           descricao_resposta)
            alunoSessao = AlunoSessao.objects.get(pk=pk_2)
            aluno = alunoSessao.aluno

            if not alunoSessao:
                AlunoSessao.objects.create(
                    aluno_id=aluno.pk,
                    sessao_id=sessao.pk,
                    media=media,
                    descricao_alterativas=descricao_resposta,
                    descricao_pontuacao=descricao_pontuacao
                )
            else:
                alunoSessao.descricao_alterativas = descricao_resposta
                alunoSessao.descricao_pontuacao = descricao_pontuacao
                alunoSessao.media = media
                alunoSessao.save()

        cameraThread.join(0)
    return redirect(reverse_lazy('sessao-details', kwargs={'pk': sessao.pk}))


def evaluate_test(quest_test, pesos_test, quest_aluno):
    nova_quest_aluno = ''
    descricao_pontuacao = ''
    for q_test, q_aluno in zip(quest_test.split(";"), quest_aluno):
        if not q_aluno:
            nova_quest_aluno += ';'
            descricao_pontuacao += '0;'
            continue

        nova_quest_aluno += q_aluno[0] + ';'
        if q_test == q_aluno:
            descricao_pontuacao += '1;'
        else:
            descricao_pontuacao += '0;'

    pontuacoes = descricao_pontuacao[:-1].split(';')
    pesos = pesos_test[:-1].split(';')

    pontuaca_ponderada = [int(nota)*10 * int(peso) for nota, peso in zip(pontuacoes,pesos)]
    soma_pontuacao_ponderada = reduce(lambda x, y: int(x) + int(y), pontuaca_ponderada)
    pesos_soma = reduce(lambda x, y: int(x) + int(y), pesos)
    media = soma_pontuacao_ponderada / pesos_soma
    return descricao_pontuacao, media, nova_quest_aluno


@login_required
def upload_file_turma(request, pk_1):

    if request.method == 'POST':
        for myfile  in request.FILES.getlist('arquivo'):
            fs = FileSystemStorage(location=os.path.join(os.path.dirname(__file__), '../core/corretor/dataset/submetidas/'))
            filename = fs.save(myfile.name, myfile)

            matricula = myfile._name.split('.')[0]
            alunoSessao = AlunoSessao.objects.filter(sessao_id=pk_1, aluno__matricula=matricula).first()
            uploaded_file_url = fs.path(filename)
            if alunoSessao:
                generate_alunoSessao(pk_1, alunoSessao.pk, uploaded_file_url)

        return redirect(reverse_lazy('sessao-details', kwargs={'pk': pk_1}))


@login_required
def upload_file(request, pk_1, pk_2):

    if request.method == 'POST':
        myfile = request.FILES['arquivo']
        fs = FileSystemStorage(location=os.path.join(os.path.dirname(__file__), '../core/corretor/dataset/submetidas/'))
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.path(filename)

        sessao, alunoSessao = generate_alunoSessao(pk_1,pk_2,uploaded_file_url)

        return redirect(reverse_lazy('sessao-details', kwargs={'pk': sessao.pk}))


def generate_alunoSessao(pk_1,pk_2,uploaded_file_url):
    sessao = Sessao.objects.get(pk=pk_1)
    alunoSessao = AlunoSessao.objects.get(pk=pk_2)
    recognition = CameraRecognition()

    answer = recognition.image_processing(uploaded_file_url)

    if answer:
        descricao_resposta = []
        for key, question in answer.items():
            while None in question:
                question.remove(None)

            if len(question) == 1:
                for alternative in question:
                    if alternative is not None:
                        descricao_resposta.append(alternative)
                continue

            if len(question) in range(10):
                descricao_resposta.append([])
                continue

        descricao_pontuacao, media, descricao_resposta = evaluate_test(sessao.questionario.descricao_alterativas,
                                                                       sessao.questionario.pesos_alterativas,
                                                                       descricao_resposta)
        aluno = alunoSessao.aluno

        if not alunoSessao:
            AlunoSessao.objects.create(
                aluno_id=aluno.pk,
                sessao_id=sessao.pk,
                media=media,
                descricao_alterativas=descricao_resposta,
                descricao_pontuacao=descricao_pontuacao
            )
        else:
            alunoSessao.descricao_alterativas = descricao_resposta
            alunoSessao.descricao_pontuacao = descricao_pontuacao
            alunoSessao.media = media
            alunoSessao.save()

    return sessao, alunoSessao