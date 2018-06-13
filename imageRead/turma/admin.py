from django.contrib import admin

# Register your models here.

from .models import Aluno, Turma, Questionario, Sessao


class TurmaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome', 'descricao']
    filter_horizontal = ('alunos',)
    fieldsets = [
        ('Turma', {'fields': ['nome', 'descricao']}),
        ('Alunos', {'fields': ['alunos']}),
        ('Avaliações', {'fields': ['sessoes']}),
    ]

admin.site.register(Turma, TurmaAdmin)
admin.site.register(Aluno)
admin.site.register(Questionario)
admin.site.register(Sessao)

