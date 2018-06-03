from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Unidade


# Create your views here.

def index(request):
    return render(request, 'index.html')


class UnidadeCreate(CreateView):
    model = Unidade
    extra_context = {"operacao": "Cadastro"}
    fields = ['nome', 'descricao', 'endereco']
    template_name = 'unidades/form.html'


class UnidadeDetail(DetailView):
    model = Unidade
    template_name = 'unidades/detail.html'


class UnidadeUpdate(UpdateView):
    model = Unidade
    extra_context = {"operacao": "Atualização"}
    fields = ['nome', 'descricao', 'endereco']
    template_name = 'unidades/form.html'


class UnidadeDelete(DeleteView):
    model = Unidade
    success_url = reverse_lazy('unidade-list')
    template_name = 'unidades/delete.html'

class UnidadeList(ListView):
    model = Unidade
    template_name = 'unidades/list.html'