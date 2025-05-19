
"""
Testes para a API de tarefas.
Versão limpa apenas com testes funcionais.
"""

import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_controller_criar_tarefa_deve_retornar_sucesso(client, tarefas_url, tarefa_data):
    """Testa a criação de uma nova tarefa."""
    response = await client.post(tarefas_url, json=tarefa_data)
    
    assert response.status_code == status.HTTP_201_CREATED
    
    content = response.json()
    assert "_id" in content
    assert content["titulo"] == tarefa_data["titulo"]
    assert content["descricao"] == tarefa_data["descricao"]
    assert content["concluida"] == tarefa_data["concluida"]
    assert "created_at" in content
    assert "updated_at" in content

@pytest.mark.asyncio
async def test_controller_criar_tarefa_com_dados_invalidos_deve_retornar_erro(client, tarefas_url):
    """Testa a criação de uma tarefa com dados inválidos."""
    dados_invalidos = {
        "titulo": "Oi",  # Título muito curto
        "descricao": "Desc muito curta", 
        "concluida": "não é booleano"  # Tipo inválido
    }
    
    response = await client.post(tarefas_url, json=dados_invalidos)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "detail" in response.json()
