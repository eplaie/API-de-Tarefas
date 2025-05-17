import pytest
from pydantic import ValidationError
from store.schemas.tarefas import TarefaIn, TarefaUpdate

def tarefa_data_valida():
    """Retorna um dicionário com dados válidos para criar uma TarefaIn."""
    return {"titulo": "Comprar pão", "descricao": "Ir à padaria e comprar pão francês.", "concluida": False}

def tarefa_data_invalida_titulo_curto():
    """Retorna dados com título muito curto."""
    return {"titulo": "Pão", "descricao": "Comprar pão.", "concluida": False}

def tarefa_data_sem_descricao():
    """Retorna dados sem o campo obrigatório 'descricao'."""
    return {"titulo": "Fazer compras", "concluida": False}


class TestTarefaInSchemas:
    def test_tarefa_in_schema_valido(self):
        """Testa a validação de TarefaIn com dados válidos."""
        data = tarefa_data_valida()
        tarefa = TarefaIn.model_validate(data)

        assert tarefa.titulo == data["titulo"]
        assert tarefa.descricao == data["descricao"]
        assert tarefa.concluida == data["concluida"]

    def test_tarefa_in_schema_titulo_obrigatorio(self):
        """Testa se TarefaIn exige o campo 'titulo'."""
        data = tarefa_data_valida()
        data.pop("titulo") # Remove o título

        with pytest.raises(ValidationError) as excinfo:
            TarefaIn.model_validate(data)

        # Verifica se o erro é sobre o campo 'titulo' ausente
        assert any(error["type"] == "missing" and "titulo" in error["loc"] for error in excinfo.value.errors())

    def test_tarefa_in_schema_descricao_obrigatoria(self):
        """Testa se TarefaIn exige o campo 'descricao'."""
        data = tarefa_data_sem_descricao() # Já não tem descrição

        with pytest.raises(ValidationError) as excinfo:
            TarefaIn.model_validate(data)
        
        assert any(error["type"] == "missing" and "descricao" in error["loc"] for error in excinfo.value.errors())

    def test_tarefa_in_schema_titulo_min_length(self):
        """Testa a validação do comprimento mínimo do título."""
        data = {"titulo": "Oi", "descricao": "Descrição válida.", "concluida": False}
        with pytest.raises(ValidationError) as excinfo:
            TarefaIn.model_validate(data)
        
        # Verifica a mensagem de erro específica para string_too_short no campo 'titulo'
        assert any(
            error["type"] == "string_too_short" and "titulo" in error["loc"]
            for error in excinfo.value.errors()
        )


class TestTarefaUpdateSchemas:
    def test_tarefa_update_schema_valido_parcial(self):
        """Testa TarefaUpdate com apenas alguns campos fornecidos."""
        data = {"titulo": "Novo título super legal"}
        tarefa_update = TarefaUpdate.model_validate(data)
        assert tarefa_update.titulo == data["titulo"]
        assert tarefa_update.descricao is None
        assert tarefa_update.concluida is None

    def test_tarefa_update_schema_valido_completo(self):
        """Testa TarefaUpdate com todos os campos opcionais fornecidos."""
        data = {"titulo": "Título atualizado", "descricao": "Descrição atualizada.", "concluida": True}
        tarefa_update = TarefaUpdate.model_validate(data)
        assert tarefa_update.titulo == data["titulo"]
        assert tarefa_update.descricao == data["descricao"]
        assert tarefa_update.concluida == data["concluida"]

    def test_tarefa_update_schema_vazio_valido(self):
        """Testa TarefaUpdate com um dicionário vazio (nenhuma alteração)."""
        data = {}
        tarefa_update = TarefaUpdate.model_validate(data)
        assert tarefa_update.model_dump(exclude_none=True) == {} # Garante que não há valores definidos

    def test_tarefa_update_schema_titulo_min_length_se_fornecido(self):
        """Testa o comprimento mínimo do título em TarefaUpdate, se fornecido."""
        data = {"titulo": "No"} # Título muito curto
        with pytest.raises(ValidationError) as excinfo:
            TarefaUpdate.model_validate(data)
        
        assert any(
            error["type"] == "string_too_short" and "titulo" in error["loc"]
            for error in excinfo.value.errors()
        )

    def test_tarefa_update_schema_descricao_min_length_se_fornecida(self):
        """Testa o comprimento mínimo da descrição em TarefaUpdate, se fornecida."""
        data = {"descricao": "Desc"} # Descrição muito curta
        with pytest.raises(ValidationError) as excinfo:
            TarefaUpdate.model_validate(data)
        
        assert any(
            error["type"] == "string_too_short" and "descricao" in error["loc"]
            for error in excinfo.value.errors()
        )