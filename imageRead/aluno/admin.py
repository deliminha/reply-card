from django.contrib import admin

from .models import Aluno, AlunoSessao
# Register your models here.

admin.site.register(Aluno)
admin.site.register(AlunoSessao)