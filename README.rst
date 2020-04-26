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


Redis
^^^^^
Redis é um pré-requisito fundamental para realização da IPC entre os componentes da aplicação. 

Após instalação do docker, inicie um redis para viabilizar a execução do projeto.

  $ docker run --name yatsm_redis -p 6379:6379 -d redis

Antes de cadastrar qualquer job, você precisar iniciar o worker

Portanto abra um novo terminal e execute:

  $ yatsm worker start


Rest API
^^^^^^^^


Em outro terminal inicialize a API

  $ yatsm api start
  
Por padrão a API é inicializada na porta 8000


Documentação
^^^^^^^^^^^^

A API disponibiliza uma documentação por OpenApi Specification no endereço:

http://localhost:8000/docs

Nela você encontra informações de como criar e acompanhar a execução dos jobs. 


Desenvolvimento
---------------

Projeto foi desenvolvido principalmente com:

  * poetry: Gerenciamento de dependências e empacotamento.
  * fastapi: Rest API.
  * typer: Kit para CLI.
  * pytest: Testes.
  * APSchedule: Kit de implementação de Schedulers.
  * dramatiq: Kit de implementação de Task Queue.




Instalaçao de dependências
--------------------------

  $ poetry install 


Testes
------

  $ poetry run pytest



Possível Roadmap Futuro
-----------------------

  * Separar Scheduler em um processo separado;
  * Implementar desenho de canvas/pipelines de jobs via REST Api.
  * Implementar monitoramento de jobs com níveis de progresso. 
