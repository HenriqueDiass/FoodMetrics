from typing import Optional
from pydantic import BaseModel, ConfigDict

class ComidaCreate(BaseModel):
    nome:    str
    descricao: str = "desc"
    preco: float

class ComidaUpdate(BaseModel):
    nome:    Optional[str]  = None
    descricao: Optional[str]  = None
    preco: Optional[float] = None

class ComidaResponse(BaseModel):
    id:        int
    nome:    str
    descricao: str
    preco: float

    model_config = ConfigDict(from_attributes=True)
