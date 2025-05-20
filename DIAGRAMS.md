# API de Tarefas

## Diagramas de sequência para o módulo de Tarefas

### Diagrama de criação de tarefa

```mermaid
sequenceDiagram
    title Create Task
    Client->>+API: Request task creation
    Note right of Client: POST /tarefas

    API->>API: Validate body (TarefaIn)

    alt Invalid body
        API->Client: Error Response
        Note right of Client: Status Code: 422 - Unprocessable Entity
    end

    API->>+Database: Request task creation (via TarefaUsecase)
    alt Error on insertion
        API->Client: Error Response
        Note right of Client: Status Code: 500 - Internal Server Error
    end
    Database->>-API: Successfully created

    API->>-Client: Successful Response (TarefaOut)
    Note right of Client: Status Code: 201 - Created
```

### Diagrama de listagem de tarefas

```mermaid
sequenceDiagram
    title List Tasks
    Client->>+API: Request tasks list
    Note right of Client: GET /tarefas

    API->>+Database: Request tasks list (via TarefaUsecase)

    Database->>-API: Successfully queried

    API->>-Client: Successful Response (List[TarefaOut])
    Note right of Client: Status Code: 200 - Ok
```

### Diagrama de detalhamento de uma tarefa

```mermaid
sequenceDiagram
    title Get Task
    Client->>+API: Request task
    Note right of Client: GET /tarefas/{id_tarefa}<br/> Path Params:<br/>     - id_tarefa: <id_da_tarefa>

    API->>+Database: Request task (via TarefaUsecase)
    alt Error on query
        API->Client: Error Response
        Note right of Client: Status Code: 500 - Internal Server Error
    else Task not found
        API->Client: Error Response
        Note right of Client: Status Code: 404 - Not Found
    end

    Database->>-API: Successfully queried

    API->>-Client: Successful Response (TarefaOut)
    Note right of Client: Status Code: 200 - Ok
```

### Diagrama de atualização de tarefa

```mermaid
sequenceDiagram
    title Update Task (PUT)
    Client->>+API: Request task update
    Note right of Client: PUT /tarefas/{id_tarefa}<br/> Path Params:<br/>     - id_tarefa: <id_da_tarefa>

    API->>API: Validate body (TarefaUpdate)

    alt Invalid body
        API->Client: Error Response
        Note right of Client: Status Code: 422 - Unprocessable Entity
    end

    API->>+Database: Request task update (via TarefaUsecase)
    alt Task not found
        API->Client: Error Response
        Note right of Client: Status Code: 404 - Not Found
    else Error on update
        API->Client: Error Response
        Note right of Client: Status Code: 500 - Internal Server Error
    end

    Database->>-API: Successfully updated

    API->>-Client: Successful Response (TarefaUpdateOut)
    Note right of Client: Status Code: 200 - Ok
```

### Diagrama de exclusão de tarefa

```mermaid
sequenceDiagram
    title Delete Task
    Client->>+API: Request task deletion
    Note right of Client: DELETE /tarefas/{id_tarefa}<br/> Path Params:<br/>     - id_tarefa: <id_da_tarefa>

    API->>+Database: Request task deletion (via TarefaUsecase)
    alt Task not found
        API->Client: Error Response
        Note right of Client: Status Code: 404 - Not Found
    else Error on deletion
        API->Client: Error Response
        Note right of Client: Status Code: 500 - Internal Server Error
    end
    
    Database->>-API: Successfully deleted

    API->>-Client: Successful Response
    Note right of Client: Status Code: 204 - No Content
```