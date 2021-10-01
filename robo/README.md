# SEL0373 - Projetos em Sistemas Digitais


## Projeto de Robô controlado por *Joystick* via rede

### Alunos:
Nome        | NUSP  
------------- |:-------------:
Lucas Tetsuo Mizumoto | 9807170
Victor de Mattos Arzolla    |  9039312


>**Objetivo do trabalho:**
Desenvolver um *webserver* para controlar robôs de duas rodas com sistema Linux a partir de *joysticks* de um *site* em rede local.

___

## Sobre:
O trabalho foi desenvolvido em ```Python 3.7.8``` utilizando os seguintes pacotes:

**Dependências:**
Pacote         | Versão  
------------- |:-------------:
Flask            |  2.0.1  
Flask-Login      |  0.5.0  
Flask-SocketIO   |  4.3.2  
Flask-SQLAlchemy |  2.5.1  
Jinja2           |  3.0.1  
Pillow           |  8.2.0  
python-engineio  |  3.14.2 
python-socketio  |  4.6.1  
SQLAlchemy       |  1.4.21 
websocket-client |  1.1.0  
Werkzeug         |  2.0.1  

## Instruções:


Execute o script ```run_server.sh``` para abrir o servidor que hostea o *site*. Este pode ser acessado pelo IP local da máquina.
<br>

Os *joysticks* são disponibilizados após realizar login no *site*.
Pode-se utilizar o login padrao:
<br>
***Your email:*** asd@asd
<br>
***Your password:*** asd
<br>

Execute os arquivos ```listen1.py``` e ```listen2.py``` para receber os comandos roteados pelo servidor. Ao executar o arquivo, insira o IP onde o servidor está sendo hosteado.
