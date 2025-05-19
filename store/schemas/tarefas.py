from typing import Optional
from pydantic import BaseModel, Field
from store.schemas.base import BaseSchemaMixin, OutSchema

class TarefaBase(BaseSchemaMixin):
    
    titulo: str = Field(..., min_length=3, max_length=50, description="Título da tarefa")
    descricao: str = Field(..., min_length=5, max_length=255, description="Descrição detalhada da tarefa")
    concluida: bool = Field(False, description="Indica se a tarefa foi concluída")

class TarefaIn(TarefaBase):

    pass

class TarefaOut(TarefaBase, OutSchema):

    pass 

class TarefaUpdate(BaseSchemaMixin):
    """
    Esquema para dados de entrada ao atualizar uma Tarefa existente.
    Todos os campos são opcionais, permitindo atualizações parciais.
    """
    titulo: Optional[str] = Field(None, min_length=3, max_length=50, description="Novo título da tarefa (opcional)")
    descricao: Optional[str] = Field(None, min_length=5, max_length=255, description="Nova descrição da tarefa (opcional)")
    concluida: Optional[bool] = Field(None, description="Novo status de conclusão da tarefa (opcional)")

class TarefaUpdateOut(TarefaOut):
    """
    Esquema para dados de saída após atualizar uma Tarefa.
    É idêntico a TarefaOut, retornando a tarefa completa atualizada.
    """
    pass