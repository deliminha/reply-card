from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Unidade


# Create your views here.
@login_required
def index(request):
    return render(request, 'index.html')


@method_decorator(login_required, name='dispatch')
class UnidadeCreate(CreateView):
    model = Unidade
    extra_context = {"operacao": "Cadastro"}
    fields = ['nome', 'descricao', 'endereco']
    template_name = 'unidades/form.html'


@method_decorator(login_required, name='dispatch')
class UnidadeDetail(DetailView):
    model = Unidade
    template_name = 'unidades/detail.html'


@method_decorator(login_required, name='dispatch')
class UnidadeUpdate(UpdateView):
    model = Unidade
    extra_context = {"operacao": "Atualização"}
    fields = ['nome', 'descricao', 'endereco']
    template_name = 'unidades/form.html'


@method_decorator(login_required, name='dispatch')
class UnidadeDelete(DeleteView):
    model = Unidade
    success_url = reverse_lazy('unidade-list')
    template_name = 'unidades/delete.html'


@method_decorator(login_required, name='dispatch')
class UnidadeList(ListView):
    model = Unidade
    template_name = 'unidades/list.html'
