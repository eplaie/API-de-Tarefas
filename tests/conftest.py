import pytest
from typing import List, Dict, Any, AsyncGenerator
import os
import sys

# Importações para MongoDB e ObjectID
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Importações dos seus esquemas e use cases
from store.schemas.tarefas import TarefaIn, TarefaUpdate
from store.usecases.tarefas import TarefaUsecase

# Importação para o cliente HTTP de teste
from httpx import AsyncClient, ASGITransport

# Importação da sua aplicação FastAPI
from store.main import app

# Importação da configuração
from store.core.config import settings

# Obtém a URL do banco de teste
def get_test_database_url():
    """Retorna a URL do banco de dados de teste."""
    if '/store?' in settings.DATABASE_URL:
        return settings.DATABASE_URL.replace('/store?', '/store_test?')
    elif settings.DATABASE_URL.endswith('/store'):
        return settings.DATABASE_URL + '_test'
    else:
        return settings.DATABASE_URL + '_test'

@pytest.fixture
async def mongo_client():
    """
    Fixture para criar e fechar uma instância do AsyncIOMotorClient.
    """
    test_db_url = get_test_database_url()
    print(f"Conectando ao MongoDB de teste: {test_db_url}")
    
    # Cria o cliente sem parâmetros especiais
    client = AsyncIOMotorClient(test_db_url)
    
    try:
        # Verifica a conexão
        await client.admin.command('ping')
        print("Conexão com MongoDB de teste bem-sucedida.")
        yield client
    except Exception as e:
        print(f"Erro ao conectar ao MongoDB: {e}")
        raise
    finally:
        print("Fechando conexão com MongoDB de teste.")
        client.close()


@pytest.fixture
async def tarefa_usecase(mongo_client):
    """Fixture para criar um TarefaUsecase para testes."""
    # Obtém o nome do banco de dados de teste
    test_db_url = settings.DATABASE_URL.replace('/store?', '/store_test?')
    db_name = test_db_url.split('/')[-1].split('?')[0]
    print(f"Criando TarefaUsecase com banco de dados: {db_name}")
    
    # Cria o usecase com o cliente MongoDB
    usecase = TarefaUsecase(client=mongo_client)
    
    # Define explicitamente o banco de dados e a coleção
    usecase._database_name = db_name
    usecase._database = mongo_client[db_name]
    usecase._collection = usecase._database.tarefas
    
    print(f"TarefaUsecase criado com database: {usecase._database_name}")
    print(f"Collection: {usecase._collection.name}")
    
    return usecase
@pytest.fixture
async def client(tarefa_usecase):
    """
    Fixture para fornecer um cliente HTTP para testes.
    Substitui a dependência de tarefa_usecase.
    """
    # Obtém a função original de tarefa_usecase
    from store.usecases.tarefas import tarefa_usecase as original_func
    
    # Define uma função que retorna o usecase de teste
    def get_test_usecase():
        print("Dependency override: Retornando o TarefaUsecase para teste")
        return tarefa_usecase
    
    # Substitui a dependência
    app.dependency_overrides[original_func] = get_test_usecase
    
    # Cria o cliente de teste
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    
    # Restaura as dependências originais
    app.dependency_overrides = {}

@pytest.fixture(autouse=True)
async def clear_collections(mongo_client):
    """Limpa as coleções de teste antes e depois de cada teste."""
    # Obtém o nome do banco de dados de teste
    db_name = get_test_database_url().split('/')[-1].split('?')[0]
    
    # Limpa antes do teste
    try:
        print(f"Preparando banco de dados de teste: {db_name}")
        db = mongo_client[db_name]
        # Garante que a coleção tarefas existe
        if "tarefas" not in await db.list_collection_names():
            await db.create_collection("tarefas")
            print("Coleção tarefas criada.")
    except Exception as e:
        print(f"Erro ao preparar banco de dados: {e}")
    
    # Executa o teste
    yield
    
    # Limpa após o teste
    try:
        print(f"Limpando coleções do banco de dados: {db_name}")
        db = mongo_client[db_name]
        collections = await db.list_collection_names()
        for collection in collections:
            if not collection.startswith('system.'):
                await db[collection].delete_many({})
                print(f"Coleção {collection} limpa.")
    except Exception as e:
        print(f"Erro ao limpar coleções: {e}")

# --- Fixtures para URL e dados ---
@pytest.fixture
def tarefas_url():
    """URL base para os endpoints de tarefas."""
    return "/tarefas/"

@pytest.fixture
def tarefa_data():
    """Dados para criar uma tarefa de teste."""
    return {
        "titulo": "Prova de POO",
        "descricao": "Estudar todas APIs.",
        "concluida": False
    }

@pytest.fixture
def tarefa_in(tarefa_data):
    """Cria um objeto TarefaIn para testes."""
    return TarefaIn(**tarefa_data)

@pytest.fixture
def tarefa_up_data():
    """Dados para atualizar uma tarefa."""
    return {
        "titulo": "Título Atualizado em Teste",
        "concluida": True
    }

@pytest.fixture
def tarefa_update(tarefa_up_data):
    """Cria um objeto TarefaUpdate para testes."""
    return TarefaUpdate(**tarefa_up_data)

@pytest.fixture
def sample_tarefa_id_str():
    """Gera um ID de tarefa de exemplo."""
    return str(ObjectId())