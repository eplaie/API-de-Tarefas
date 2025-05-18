<div align="center" style="display: inline_block">
  <img align="center" alt="VS" src="https://img.shields.io/badge/Visual_Studio_Code-0078D4?style=for-the-badge&logo=visual%20studio%20code&logoColor=white" />
  <img align="center" alt="Linux" src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" />
  <img align="center" alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img align="center" alt="FastAPI" src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img align="center" alt="MongoDB" src="https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white" />
  <img align="center" alt="Docker" src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
  <img align="center" alt="Poetry" src="https://img.shields.io/badge/Poetry-60A5FA?style=for-the-badge&logo=poetry&logoColor=white" />
  <img align="center" alt="Pytest" src="https://img.shields.io/badge/Pytest-0A9B5C?style=for-the-badge&logo=pytest&logoColor=white" />
</div>

# API de Gerenciamento de Tarefas

API desenvolvida para gerenciar tarefas, permitindo operações de criação, leitura, atualização e deleção (CRUD). Construída com Python, FastAPI e MongoDB, utilizando Docker para o ambiente do banco de dados e Poetry para gerenciamento de dependências.

## Índice

* [Funcionalidades Principais](#funcionalidades-principais)
* [Tecnologias Utilizadas](#tecnologias-utilizadas)
* [Pré-requisitos](#pré-requisitos)
* [Configuração do Ambiente de Desenvolvimento](#configuração-do-ambiente-de-desenvolvimento)
* [Instalação das Dependências](#instalação-das-dependências)
* [Executando o Banco de Dados (MongoDB com Docker)](#executando-o-banco-de-dados-mongodb-com-docker)
* [Executando a API](#executando-a-api)
* [Acessando a Documentação da API](#acessando-a-documentação-da-api)
* [Testando os Endpoints (Manualmente)](#testando-os-endpoints-manualmente)
* [Executando os Testes Automatizados](#executando-os-testes-automatizados)
* [Estrutura do Projeto](#estrutura-do-projeto)
* [Como Foi Pensado (Decisões de Design)](#como-foi-pensado-decisões-de-design)
* [Como Foi Resolvido (Desafios e Soluções)](#como-foi-resolvido-desafios-e-soluções)
* [Etapas de Desenvolvimento](#etapas-de-desenvolvimento)
* [Cenários de Testes Cobertos](#cenários-de-testes-cobertos)
* [Diagramas](#diagramas)

## Funcionalidades Principais

* **Criar Tarefas:** Adicionar novas tarefas com título, descrição e status de conclusão.
* **Listar Tarefas:** Visualizar todas as tarefas cadastradas.
* **Buscar Tarefa por ID:** Obter detalhes de uma tarefa específica.
* **Atualizar Tarefas:** Modificar o título, descrição ou status de conclusão de uma tarefa existente.
* **Deletar Tarefas:** Remover uma tarefa do sistema.

## Tecnologias Utilizadas

* **Python 3.12**
* **FastAPI:** 
* **Pydantic:** 
* **MongoDB:** 
    * **Motor:** 
* **Docker & Docker Compose:** 
* **Poetry:** 
* **Uvicorn:** 
* **Pytest:** 
    * **pytest-asyncio:** 
* **HTTPretty:** 
* **`.env` files:** 

## Configuração do Ambiente de Desenvolvimento

1.  **Clonar o Repositório (se aplicável):**
    Se você estiver obtendo o código de um repositório Git:
    ```bash
    git clone <url-do-seu-repositorio-git>
    cd nome-do-repositorio-clonado
    ```

2.  **Configurar o Arquivo `.env`:**
    Este projeto utiliza um arquivo `.env` para gerenciar variáveis de ambiente, como a string de conexão do banco de dados.
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Adicione o seguinte conteúdo ao arquivo, ajustando se necessário:

    ```env
    DATABASE_URL='mongodb://localhost:27017/store?uuidRepresentation=standard'
    PROJECT_NAME='API de Tarefas (Desenvolvimento)'
    ROOT_PATH='/'
    # Adicione outras variáveis de ambiente que sua aplicação possa precisar
    ```
    * **Nota:** A `DATABASE_URL` acima assume que o MongoDB estará rodando localmente (via Docker) na porta padrão `27017` e usará um banco de dados chamado `store`.

## Instalação das Dependências

Com o Poetry instalado e o projeto clonado/configurado, instale as dependências do projeto:

```bash
poetry install
```
Este comando lerá o arquivo `pyproject.toml`, resolverá as dependências (usando `poetry.lock` se existir) e as instalará em um ambiente virtual gerenciado pelo Poetry.

Para ativar o ambiente virtual explicitamente (opcional, pois `poetry run` pode ser usado para executar comandos dentro do ambiente):
```bash
poetry shell
```

## Executando o Banco de Dados (MongoDB com Docker)

Esta API utiliza o MongoDB como banco de dados, executado em um contêiner Docker gerenciado pelo Docker Compose.

1.  **Inicie o Contêiner do MongoDB:**
    No diretório raiz do projeto (onde o arquivo `docker-compose.yml` está localizado), execute:
    ```bash
    docker compose up -d
    ```

2.  **Verifique se o Contêiner está Rodando:**
    ```bash
    docker compose ps
    ```

3.  **Para Parar o Contêiner:**
    Quando não precisar mais do banco de dados rodando:
    ```bash
    docker compose down
    ```

## Executando a API

Com as dependências instaladas e o banco de dados MongoDB rodando no Docker, você pode iniciar a aplicação FastAPI:

```bash
poetry run uvicorn store.main:app --reload
```
* `poetry run`: Executa o comando dentro do ambiente virtual gerenciado pelo Poetry.
* `uvicorn store.main:app`: Instrui o Uvicorn a encontrar a instância `app` do FastAPI no arquivo `store/main.py`.
* `--reload`: Ativa o recarregamento automático do servidor sempre que houver alterações nos arquivos do projeto (útil para desenvolvimento).

Após a execução bem-sucedida, a API estará acessível em: `http://localhost:8000`

## Acessando a Documentação da API

O FastAPI gera automaticamente documentação interativa para sua API usando os padrões OpenAPI. Você pode acessá-la através dos seguintes URLs no seu navegador enquanto a API estiver rodando:

* **Swagger UI:** `http://localhost:8000/docs`
* **ReDoc:** `http://localhost:8000/redoc`

Essas interfaces permitem visualizar todos os endpoints, seus parâmetros, corpos de requisição esperados, respostas e até mesmo testá-los diretamente no navegador.

## Testando os Endpoints (Manualmente)

Além de usar o Swagger UI, você pode testar os endpoints da API usando ferramentas de cliente HTTP como:

* [Postman](https://www.postman.com/)
* [Insomnia](https://insomnia.rest/)
* `curl` (linha de comando)

**Endpoints Principais:**

* **`POST /tarefas/`**: Cria uma nova tarefa.
    * **Método:** `POST`
    * **URL:** `http://localhost:8000/tarefas/`
    * **Corpo (JSON):**
      ```json
      {
        "titulo": "Minha Nova Tarefa",
        "descricao": "Descrição detalhada da minha nova tarefa.",
        "concluida": false
      }
      ```
* **`GET /tarefas/`**: Lista todas as tarefas.
    * **Método:** `GET`
    * **URL:** `http://localhost:8000/tarefas/`
* **`GET /tarefas/{id_da_tarefa}`**: Retorna uma tarefa específica.
    * **Método:** `GET`
    * **URL:** `http://localhost:8000/tarefas/<id_da_tarefa_aqui>`
* **`PUT /tarefas/{id_da_tarefa}`**: Atualiza uma tarefa existente.
    * **Método:** `PUT`
    * **URL:** `http://localhost:8000/tarefas/<id_da_tarefa_aqui>`
    * **Corpo (JSON) - Exemplo de atualização parcial:**
      ```json
      {
        "titulo": "Título da Tarefa Atualizado",
        "concluida": true
      }
      ```
* **`DELETE /tarefas/{id_da_tarefa}`**: Remove uma tarefa.
    * **Método:** `DELETE`
    * **URL:** `http://localhost:8000/tarefas/<id_da_tarefa_aqui>`

## Executando os Testes Automatizados

O projeto inclui um conjunto de testes automatizados escritos com Pytest para garantir a qualidade e o correto funcionamento das diferentes camadas da aplicação (schemas, use cases e controllers/API).

Para executar todos os testes, utilize o comando:

```bash
make test
```
Ou, diretamente com Poetry:
```bash
poetry run pytest
```

## Como foi pensado 

* **Arquitetura em Camadas:** A aplicação foi estruturada em camadas distintas (controllers/routers, use cases, schemas, models, db) para promover:
    * **Separação de Responsabilidades:** Cada camada tem um foco claro.
    * **Testabilidade:** Facilita a escrita de testes unitários e de integração para cada componente.
    * **Manutenibilidade:** Alterações em uma camada têm menos probabilidade de impactar diretamente outras.
    * **Escalabilidade:** Torna mais simples adicionar novas funcionalidades ou modificar as existentes.

* **MongoDB com Motor:**
    * **MongoDB** foi selecionado como banco de dados NoSQL pela sua flexibilidade.
    * **Motor** é o driver assíncrono oficial para MongoDB, essencial para trabalhar com FastAPI.
* **Docker e Docker Compose:**
    * Utilizados para criar um ambiente de banco de dados MongoDB isolado, consistente e facilmente reproduzível em diferentes máquinas de desenvolvimento ou em ambientes de CI/CD.
* **Poetry:**
    * Escolhido para gerenciamento de dependências e ambiente virtual por sua interface de linha de comando intuitiva, resolução de dependências e gerenciamento de arquivos `pyproject.toml` e `poetry.lock`.
* **Testes com Pytest:**
    * A filosofia foi adotar testes em diferentes níveis (schemas, use cases, controllers) para garantir a confiabilidade da API.
    * `pytest-asyncio` para lidar com código assíncrono nos testes.
    * `httpx.AsyncClient` para realizar testes de integração nos endpoints da API de forma eficiente.
* **Configuração Centralizada:**
    * Uso de um arquivo `.env` e uma classe de configurações Pydantic (`store/core/config.py`) para gerenciar variáveis de ambiente e configurações da aplicação de forma centralizada.

## Como Foi Resolvido (Desafios e Soluções)

Durante o desenvolvimento deste projeto, alguns desafios comuns em aplicações web assíncronas e testes foram encontrados e solucionados:


## Etapas de Desenvolvimento (Resumo)

O desenvolvimento da API seguiu aproximadamente as seguintes etapas:

1.  **Configuração Inicial:** Definição da estrutura do projeto, configuração do Poetry, Docker para MongoDB e ambiente de desenvolvimento.
2.  **Definição dos Schemas (Pydantic):** Criação dos schemas de entrada (`TarefaIn`), saída (`TarefaOut`) e atualização (`TarefaUpdate`) para a entidade `Tarefa` em `store/schemas/`.
3.  **Definição dos Modelos (Pydantic):** Criação dos modelos Pydantic (`TarefaModel`) em `store/models/` para representar os dados como seriam preparados para o banco, incluindo timestamps.
4.  **Configuração do Banco de Dados:** Implementação da lógica de conexão com o MongoDB usando Motor em `store/db/mongo.py` e carregamento da `DATABASE_URL` via `store/core/config.py`.
5.  **Desenvolvimento dos Casos de Uso (Use Cases):** Criação da classe `TarefaUsecase` em `store/usecases/tarefas.py` contendo a lógica de negócios para criar, ler, atualizar e deletar tarefas, interagindo com o banco de dados.
6.  **Criação dos Controllers (Routers):** Definição dos endpoints da API (rotas) em `store/controllers/tarefas.py`, utilizando o `APIRouter` do FastAPI e injetando o `TarefaUsecase`.
7.  **Configuração da Aplicação Principal:** Atualização do `store/main.py` para instanciar o FastAPI, incluir os routers e definir eventos de ciclo de vida (lifespan).
8.  **Implementação de Testes Automatizados:**
    * Testes unitários para os schemas Pydantic (`tests/schemas/`).
    * Testes para os casos de uso (`tests/usecases/`).
    * Testes de integração para os controllers/endpoints da API (`tests/controllers/`).
    * Configuração de fixtures no `tests/conftest.py`.

## Cenários de Testes Cobertos

Os testes automatizados visam cobrir os seguintes cenários:

* **Testes de Schema (`tests/schemas/test_tarefas.py`):**
    * Validação de dados válidos para criação e atualização de tarefas.
    * Verificação de campos obrigatórios (ex: título, descrição).
    * Validação de tipos de dados.
    * Verificação de restrições de campo (ex: comprimento mínimo/máximo para strings).
* **Testes de Use Case (`tests/usecases/test_tarefas.py`):**
    * Criação bem-sucedida de uma tarefa.
    * Busca de uma tarefa existente pelo ID.
    * Tentativa de busca de tarefa com ID inexistente (espera `NotFoundException`).
    * Tentativa de busca de tarefa com ID em formato inválido (espera `NotFoundException`).
    * Listagem de todas as tarefas.
    * Atualização bem-sucedida de uma tarefa existente.
    * Tentativa de atualização de tarefa com ID inexistente (espera `NotFoundException`).
    * Deleção bem-sucedida de uma tarefa existente.
    * Tentativa de deleção de tarefa com ID inexistente (espera `NotFoundException`).
* **Testes de Controller/API (`tests/controllers/test_tarefas.py`):**
    * **POST `/tarefas/`:**
        * Criação de tarefa com dados válidos (espera status 201 e o corpo da tarefa criada).
    * **GET `/tarefas/{id}`:**
        * Busca de tarefa com ID existente (espera status 200 e os dados da tarefa).
        * Busca de tarefa com ID inexistente (espera status 404).
        * Busca de tarefa com ID em formato inválido (espera status 404 ou 422, dependendo da validação).
    * **GET `/tarefas/`:**
        * Listagem de tarefas (espera status 200 e uma lista, possivelmente vazia ou com itens).
    * **PUT `/tarefas/{id}`:**
        * Atualização de tarefa com ID existente e dados válidos (espera status 200 e os dados da tarefa atualizada).
        * Tentativa de atualização de tarefa com ID inexistente (espera status 404).
    * **DELETE `/tarefas/{id}`:**
        * Deleção de tarefa com ID existente (espera status 204).
        * Tentativa de deleção de tarefa com ID inexistente (espera status 404).

## Diagramas