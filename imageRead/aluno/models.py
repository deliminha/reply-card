from django.db import models


# Create your models here.
class Aluno(models.Model):
    nome        = models.CharField('Nome', max_length=60)
    matricula   = models.CharField('matricula', max_length=11)

    # Retorna o nome dos atributos
    def __str__(self):
        return self.matricula + ' - ' + self.nome

    # Formatacao do nome da classe
    class Meta:
        verbose_name        = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering            = ['nome', 'matricula']
