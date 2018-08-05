from django.contrib import admin

# Register your models here.

from .models import Endereco, Unidade


class UnidadeAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao']
    search_fields = ['nome', 'descricao']
    fieldsets = [
        ('Unidade', {'fields': ['nome', 'descricao']}),
        ('Endereco', {'fields': ['endereco']}),
    ]


admin.site.register(Unidade, UnidadeAdmin)
admin.site.register(Endereco)
