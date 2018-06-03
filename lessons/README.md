# reply-card

Repositório para testes da biblioteca OpenCV, 
o projeto destinasse a identificar elementos através da WebCan 

#### Set Up
Clone esse projeto:

~~~~
$ git clone https://github.com/I-am-Miguel/reply-card.git
~~~~


Certifique-se que as dependencias do projeto se encontram atualizadas:
~~~~
sudo apt-get install libopencv-dev python-opencv
~~~~

#### Rodando localmente
Você primeiramente deve adicionar um ambiente virtual
~~~~
$ virtualenv venv
$ source /venv/bin/activate
~~~~

Instalar as dependências do projeto
~~~~
(venv)$ pip install -r requirements.txt
~~~~
E por fim, rodar o projeto localmente
~~~~
(venv)$ python WebCan.py
~~~~
