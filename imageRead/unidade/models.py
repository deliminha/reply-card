from django.db import models
from django.urls import reverse

# Create your models here.

class Endereco(models.Model):
    cep     = models.CharField('CEP',       max_length=8)
    rua     = models.CharField('Rua',       max_length=40)
    numero  = models.CharField('Numero',    max_length=10)
    bairro  = models.CharField('Bairro',    max_length=20)
    cidade  = models.CharField('Cidade',    max_length=20)
    estado  = models.CharField('Estado',    max_length=2)

    # Retorna o nome dos atributos
    def __str__(self):
        return self.rua + ', ' + self.numero + ' - ' + self.cidade

    # Formatacao do nome da classe
    class Meta:
        verbose_name        = 'Endereco'
        verbose_name_plural = 'Enderecos'
        ordering            = ['estado','cidade','bairro']

class Unidade(models.Model):
    nome        = models.CharField('Nome',        max_length=60)
    descricao   = models.CharField("descricao",   max_length=80)
    endereco    = models.ForeignKey(Endereco,     on_delete=False, blank=False, null=False)

    # Retorna o nome dos atributos
    def __str__(self):
        return self.nome + ', ' + self.descricao

    # Formatacao do nome da classe
    class Meta:
        verbose_name        = 'Unidade'
        verbose_name_plural = 'Unidades'
        ordering            = ['nome', 'descricao']

    def get_absolute_url(self):
        return reverse('unidade-read', kwargs={'pk': self.pk})
