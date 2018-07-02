from django.db import models
from django.urls import reverse

from ..aluno.models import Aluno


# Create your models here.
class Questionario(models.Model):
    nome    = models.CharField('Nome', max_length=60)
    pontMax = models.PositiveIntegerField('Pontuação Máxima')
    pontMin = models.PositiveIntegerField('Pontuação Mínima')
    media   = models.PositiveIntegerField('Média')

    # Retorna o nome dos atributos
    def __str__(self):
        return self.nome

    # Formatacao do nome da classe
    class Meta:
        verbose_name        = 'Questionario'
        verbose_name_plural = 'Questionarios'
        ordering            = ['nome', 'pontMin','pontMax','media']





class Turma(models.Model):
    nome            = models.CharField('Nome', max_length=60)
    descricao       = models.CharField('descricao', max_length=80)
    data_referencia = models.DateField('ano',blank=True)
    alunos          = models.ManyToManyField(Aluno, blank= True)

    # Retorna o nome dos atributos
    def __str__(self):
        return self.nome + ', ' + self.descricao

    # Formatacao do nome da classe
    class Meta:
        verbose_name        = 'Turma'
        verbose_name_plural = 'Turmas'
        ordering            = ['nome', 'descricao','data_referencia']

    def get_absolute_url(self):
        return reverse('turma-read', kwargs={'pk': self.pk})


class Sessao(models.Model):
    questionarios = models.ManyToManyField(Questionario)
    dataAplicacao = models.DateTimeField('Data de Aplicação',blank=True, null=True)
    turma         = models.ForeignKey(Turma, on_delete=False)

    # Retorna o nome dos atributos
    def __str__(self):
        return '/'.join(q.nome for q in self.questionarios.all()) \
               + " Data: {}".format(self.dataAplicacao.strftime('%d/%m/%Y'))

    # Formatacao do nome da classe
    class Meta:
        verbose_name        = 'Sessao'
        verbose_name_plural = 'Sessoes'
        ordering            = ['pk','dataAplicacao']


class Topping(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Pizza(models.Model):
    name = models.CharField(max_length=50)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return "%s (%s)" % (
            self.name,
            ", ".join(topping.name for topping in self.toppings.all()),
        )