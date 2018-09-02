from django.contrib import admin

# Register your models here.

from .models import Turma, Questionario, Sessao


class TurmaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome', 'descricao']
    fieldsets = [
        ('Turma', {'fields': ['nome', 'descricao','data_referencia']}),
    ]

admin.site.register(Turma, TurmaAdmin)
admin.site.register(Questionario)
admin.site.register(Sessao)

