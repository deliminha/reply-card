from django.db import models
from django.urls import reverse

from ..turma.models import Turma, Sessao


# Create your models here.
class Aluno(models.Model):
    nome        = models.CharField('Nome', max_length=60)
    matricula   = models.CharField('matricula', max_length=11, unique=True)
    turma       = models.ForeignKey(Turma, on_delete=False, blank=True)

    # Retorna o nome dos atributos
    def __str__(self):
        return self.matricula + ' - ' + self.nome

    # Formatacao do nome da classe
    class Meta:
        verbose_name        = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering            = ['nome', 'matricula']

    def get_absolute_url(self):
        return reverse('aluno-turma-list', kwargs={'pk': self.pk})

class AlunoSessao(models.Model):
    aluno                   = models.ForeignKey(Aluno, on_delete= models.CASCADE)
    sessao                  = models.ForeignKey(Sessao, on_delete=models.CASCADE)
    media                   = models.PositiveIntegerField('Média')
    descricao_alterativas   = models.CharField('Descrição de Alterativas', max_length=60, blank=True)
    descricao_pontuacao     = models.CharField('Descrição de Pontuação', max_length=60, blank=True)

    # Retorna o nome dos atributos
    def __str__(self):
        return "{} - {}".format(self.aluno.nome, self.sessao.questionario.nome)

    # Formatacao do nome da classe
    class Meta:
        verbose_name        = 'AlunoSessao'
        verbose_name_plural = 'AlunosSessao'
        ordering            = ['aluno', 'sessao','media']

    def get_absolute_url(self):
        return reverse('aluno-turma-list', kwargs={'pk': self.sessao.turma.pk})
