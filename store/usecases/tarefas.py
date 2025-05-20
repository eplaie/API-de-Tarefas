from datetime import datetime
from typing import List, Dict, Any
from bson import ObjectId
from fastapi import HTTPException, Depends

from motor.motor_asyncio import AsyncIOMotorClient
from store.core.config import settings
from store.schemas.tarefas import TarefaIn, TarefaUpdate

class TarefaUsecase:
    """Classe que implementa os casos de uso para gerenciar tarefas."""
    
    def __init__(self, client=None):
        """Inicializa o caso de uso com um cliente MongoDB opcional."""
        self._client = client or AsyncIOMotorClient(settings.DATABASE_URL)
        db_url = settings.DATABASE_URL
        self._database_name = db_url.split('/')[-1].split('?')[0]
        self._database = self._client[self._database_name]
        self._collection = self._database.tarefas
        
        print(f"TarefaUsecase inicializado com database: {self._database_name}")
    
    async def create(self, body):
        return await self.criar_tarefa(body)
    
    async def get(self, id_str):
        return await self.obter_tarefa(id_str)
    
    async def query(self):
        return await self.listar_tarefas()
    
    async def update(self, id_str, body):
        return await self.atualizar_tarefa(id_str, body)
    
    async def delete(self, id_str):
        await self.deletar_tarefa(id_str)
        return True
    
    async def criar_tarefa(self, tarefa_in):
        """Cria uma nova tarefa."""
        try:
            if hasattr(tarefa_in, 'model_dump'):
                nova_tarefa = tarefa_in.model_dump()
            else:
                nova_tarefa = dict(tarefa_in)
            
            timestamp = datetime.utcnow()
            nova_tarefa["created_at"] = timestamp
            nova_tarefa["updated_at"] = timestamp
            
            # Insere no banco
            result = await self._collection.insert_one(nova_tarefa)
            
            # Adiciona o ID
            nova_tarefa["_id"] = str(result.inserted_id)
            
            return nova_tarefa
        except Exception as e:
            print(f"Erro ao criar tarefa: {e}")
            raise HTTPException(
                status_code=500, 
                detail=f"Ocorreu um erro ao criar a tarefa: {e}"
            )
    
    async def obter_tarefa(self, tarefa_id):
        """Obtém uma tarefa pelo ID."""
        try:
            # Valida o ID
            if not ObjectId.is_valid(tarefa_id):
                raise HTTPException(
                    status_code=404,
                    detail=f"ID de tarefa inválido: {tarefa_id}"
                )
            
            # Busca a tarefa - versão segura
            query = {"_id": ObjectId(tarefa_id)}
            result = await self._collection.find_one(query)
            
            if not result:
                raise HTTPException(
                    status_code=404,
                    detail=f"Tarefa não encontrada com o ID: {tarefa_id}"
                )
            
            # Converte ObjectId para string
            result["_id"] = str(result["_id"])
            
            return result
        except HTTPException:
            raise
        except Exception as e:
            print(f"Erro ao obter tarefa: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao buscar tarefa: {e}"
            )
    
    async def listar_tarefas(self):
        """Lista todas as tarefas."""
        try:
            print("Listando tarefas...")
            
            # Busca todas as tarefas 
            cursor = self._collection.find()
            docs = []
            
            # Executa a query manualmente
            async for doc in cursor:
                doc["_id"] = str(doc["_id"])
                docs.append(doc)
            
            print(f"Encontradas {len(docs)} tarefas")
            return docs
        except Exception as e:
            print(f"Erro ao listar tarefas: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao listar tarefas: {e}"
            )
    
    async def atualizar_tarefa(self, tarefa_id, tarefa_update):
        """Atualiza uma tarefa existente."""
        try:
            # Valida o ID
            if not ObjectId.is_valid(tarefa_id):
                raise HTTPException(
                    status_code=404,
                    detail=f"ID de tarefa inválido: {tarefa_id}"
                )
            
            # Verifica se a tarefa existe
            tarefa = await self._collection.find_one({"_id": ObjectId(tarefa_id)})
            if tarefa is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Tarefa não encontrada com o ID: {tarefa_id}"
                )
            
            # Prepara os dados para atualização
            update_data = {}
            if hasattr(tarefa_update, 'model_dump'):
                data_dict = tarefa_update.model_dump(exclude_none=True)
                update_data = {k: v for k, v in data_dict.items() if v is not None}
            else:
                update_data = {k: v for k, v in dict(tarefa_update).items() if v is not None}
            
            # Adiciona timestamp de atualização
            update_data["updated_at"] = datetime.utcnow()
            
            # Atualiza a tarefa
            await self._collection.update_one(
                {"_id": ObjectId(tarefa_id)},
                {"$set": update_data}
            )
            
            # Busca a tarefa atualizada
            tarefa_atualizada = await self._collection.find_one({"_id": ObjectId(tarefa_id)})
            tarefa_atualizada["_id"] = str(tarefa_atualizada["_id"])
            
            return tarefa_atualizada
        except HTTPException:
            raise
        except Exception as e:
            print(f"Erro ao atualizar tarefa: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao atualizar tarefa: {e}"
            )
    
    async def deletar_tarefa(self, tarefa_id):
        """Remove uma tarefa do banco de dados."""
        try:
            # Valida o ID
            if not ObjectId.is_valid(tarefa_id):
                raise HTTPException(
                    status_code=404,
                    detail=f"ID de tarefa inválido: {tarefa_id}"
                )
            
            # Remove a tarefa
            result = await self._collection.delete_one({"_id": ObjectId(tarefa_id)})
            
            if result.deleted_count == 0:
                raise HTTPException(
                    status_code=404,
                    detail=f"Tarefa não encontrada com o ID: {tarefa_id} para deleção."
                )
        except HTTPException:
            raise
        except Exception as e:
            print(f"Erro ao deletar tarefa: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Erro ao deletar tarefa: {e}"
            )

# Instância global para injeção de dependência
def get_tarefa_usecase():
    """Factory para criar instância do TarefaUsecase."""
    return TarefaUsecase()

# Instância global
tarefa_usecase = get_tarefa_usecase()
