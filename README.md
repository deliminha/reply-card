# AGIL Sistemas

## Reply Card

Este projeto foi gerado com [Django](https://github.com/django/django) version 2.0.

#### Set Up
Clone esse projeto:

`$ https://github.com/I-am-Miguel/reply-card.git`

`$ cd reply-card`

Crie um ambiente virtual e instale as dependências:
`$ virtualenv venv`

`(venv)$ source /venv/bin/activate`

`(venv)$ pip install -r requeriments.txt`

## Servidor de desenvolvimento
Setup banco de dados:
~~~~bash
(venv)$ python manage.py makemigrations
(venv)$ python manage.py migrate
~~~~
Rodando a aplicação
~~~~bash
$ python manage.py runserver
~~~~
Agora você pode ir até [http://localhost:8000](http://localhost:8000).
fetch