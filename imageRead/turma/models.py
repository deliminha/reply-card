from django.db import models
from django.urls import reverse


# Create your models here.
class Questionario(models.Model):
    nome                  = models.CharField('Nome', max_length=60)
    pontMax               = models.PositiveIntegerField('Pontuação Máxima')
    pontMin               = models.PositiveIntegerField('Pontuação Mínima')
    media                 = models.PositiveIntegerField('Média')
    quantidade_questoes   = models.PositiveIntegerField('Quantidade Questões')
    descricao_alterativas = models.CharField('Descrição de Alternativas', max_length=60, blank=True)

    # Retorna o nome dos atributos
    def __str__(self):
        return "{} - {}Questões".format(self.nome,self.quantidade_questoes)


    def get_absolute_url(self):
        return reverse('questionario-create-details', kwargs={'pk': self.pk})


    # Formatacao do nome da classe
    class Meta:
        verbose_name        = 'Questionario'
        verbose_name_plural = 'Questionarios'
        ordering            = ['nome', 'pontMin','pontMax','media','quantidade_questoes']


class Turma(models.Model):
    nome            = models.CharField('Nome', max_length=60)
    descricao       = models.CharField('Descricao', max_length=80)
    data_referencia = models.DateField('Data Referência',blank=True)

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
    questionario  = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    dataAplicacao = models.DateField('Data de Aplicação')
    turma         = models.ForeignKey(Turma, on_delete=False)

    # Retorna o nome dos atributos
    def __str__(self):
        return "{} Data: {}".format(self.questionario.nome,self.dataAplicacao.strftime('%d/%m/%Y'))

    # Formatacao do nome da classe
    class Meta:
        verbose_name        = 'Sessao'
        verbose_name_plural = 'Sessoes'
        ordering            = ['pk','dataAplicacao']

    def get_absolute_url(self):
        return reverse('aluno-turma-list', kwargs={'pk': self.turma.pk})
