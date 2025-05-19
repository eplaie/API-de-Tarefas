from store.models.base import BaseModelWithTimestamps
from store.schemas.tarefas import TarefaIn 

class TarefaModel(TarefaIn, BaseModelWithTimestamps):
    """
    Modelo Pydantic representando uma Tarefa como ela seria preparada
    para ser inserida ou como existe no banco de dados (incluindo timestamps).
    O campo _id é adicionado pelo MongoDB e não faz parte deste modelo de preparação.
    """
    pass

