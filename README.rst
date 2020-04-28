Yet Another Task Schedule Manager
=================================

:License: GPLv3


Gerenciamento de tarefas em background
--------------------------------------

Este projeto visa integrar componentes do ecossistema python para compor uma plataforma de gerenciamento de tarefas em background que pode,
pode ser gerenciada por uma API REST simplificada.


Arquitetura do projeto
----------------------

O Projeto está dividido em 3 componentes:

  * API Rest de Jobs
    
    * Cria jobs
    * Consulta jobs
    
  * Worker

    * Executa jobs
    * Salva resultado em um redis
    
  * Scheduler
    
    * Processo em background que dispara os jobs conforme agendamento.
    
    

Pré-requisitos
--------------

* Docker -> https://docs.docker.com/engine/install/
* Docker Compose -> https://github.com/docker/compose


Desenvolvimento
---------------

Projeto foi desenvolvido principalmente com:

  * poetry: Gerenciamento de dependências e empacotamento.
  * fastapi: Rest API.
  * typer: Kit para CLI.
  * pytest: Testes.
  * APSchedule: Kit de implementação de Schedulers.
  * dramatiq: Kit de implementação de Task Queue.



Quickstart
----------

  $ docker-compose up -d


Documentação
------------

A API disponibiliza uma documentação por OpenApi Specification no endereço:

http://localhost/docs

Nela você encontra informações de como criar e acompanhar a execução dos jobs.



Instalaçao de dependências
--------------------------

  $ poetry install 


Testes
------

  $ poetry run pytest



TODO
----

  * Separar Scheduler;
  * Implementar desenho de canvas/pipelines de jobs via REST Api.
  * Implementar monitoramento de jobs com níveis de progresso.
