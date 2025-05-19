from datetime import datetime, timezone 
from pydantic import BaseModel, Field

class BaseModelWithTimestamps(BaseModel):
    """
    Modelo base Pydantic que adiciona timestamps de criação e atualização.
    Estes campos seriam preenchidos antes de salvar no banco de dados.
    O _id é gerado pelo MongoDB e não é definido aqui.
    """
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


    class Config:
        from_attributes = True