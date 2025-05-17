from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ConfigDict
from typing import Any


class BaseSchemaMixin(BaseModel):
    """
    Mixin base para esquemas Pydantic.
    Configura o Pydantic para permitir a criação de modelos a partir de atributos de objetos (ORM mode).
    """
    model_config = ConfigDict(from_attributes=True)


class OutSchema(BaseModel):
    """
    Esquema base para respostas da API.
    Inclui campos comuns como id, created_at, e updated_at.
    """
    id: Any = Field(..., alias="_id")
    created_at: datetime = Field()
    updated_at: datetime = Field()

    @model_validator(mode="before")
    @classmethod
    def set_schema(cls, data: Any) -> Any:
        """
        Validador para transformar dados antes da criação do modelo.
        Especificamente, converte o '_id' (ObjectId) do MongoDB para string.
        """
        if isinstance(data, dict):
            if "_id" in data and not isinstance(data["_id"], str):
                data["_id"] = str(data["_id"])
        return data

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
