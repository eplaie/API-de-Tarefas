from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from store.core.exceptions import NotFoundException
from store.schemas.tarefas import TarefaIn, TarefaOut, TarefaUpdate, TarefaUpdateOut
from store.usecases.tarefas import tarefa_usecase, TarefaUsecase 

router = APIRouter(tags=["Tarefas"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def criar_tarefa(
    body: TarefaIn = Body(...), 
    usecase: TarefaUsecase = Depends(lambda: tarefa_usecase) 
) -> TarefaOut:
    """
    Cria uma nova tarefa.
    Espera um corpo de requisição com 'titulo', 'descricao', e 'concluida' (opcional, padrão False).
    Retorna a tarefa criada, incluindo seu ID gerado e timestamps.
    """
    try:
        return await usecase.criar_tarefa(body)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao criar a tarefa: {e}"
        )

@router.get(path="/{id_tarefa}", status_code=status.HTTP_200_OK)
async def obter_tarefa(
    id_tarefa: str = Path(description="ID da tarefa a ser buscada"),
    usecase: TarefaUsecase = Depends(lambda: tarefa_usecase)
) -> TarefaOut:
    """
    Obtém uma tarefa específica pelo seu ID.
    O ID da tarefa é passado como um parâmetro de caminho.
    """
    try:
        return await usecase.obter_tarefa(id_tarefa)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao buscar a tarefa: {e}"
        )


@router.get(path="/", status_code=status.HTTP_200_OK)
async def listar_tarefas(
    usecase: TarefaUsecase = Depends(lambda: tarefa_usecase)
) -> List[TarefaOut]:
    """
    Lista todas as tarefas cadastradas.
    """
    try:
        return await usecase.listar_tarefas()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao listar as tarefas: {e}"
        )

@router.put(path="/{id_tarefa}", status_code=status.HTTP_200_OK)
async def atualizar_tarefa(
    id_tarefa: str = Path(description="ID da tarefa a ser atualizada"),
    body: TarefaUpdate = Body(...),
    usecase: TarefaUsecase = Depends(lambda: tarefa_usecase)
) -> TarefaUpdateOut: 
    """
    Atualiza uma tarefa existente.
    Permite atualizações parciais dos campos 'titulo', 'descricao', 'concluida'.
    """
    try:
        return await usecase.atualizar_tarefa(id_tarefa, body)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao atualizar a tarefa: {e}"
        )

@router.delete(path="/{id_tarefa}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_tarefa(
    id_tarefa: str = Path(description="ID da tarefa a ser deletada"),
    usecase: TarefaUsecase = Depends(lambda: tarefa_usecase)
) -> None:
    """
    Deleta uma tarefa existente pelo seu ID.
    Retorna status 204 (No Content) se a deleção for bem-sucedida.
    """
    try:
        await usecase.deletar_tarefa(id_tarefa)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao deletar a tarefa: {e}"
        )
    return None 