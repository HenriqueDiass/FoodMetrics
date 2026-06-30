from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ComidaCreate(BaseModel):
    nome:           str
    categoria:      str
    custo_unitario: float

class ComidaUpdate(BaseModel):
    nome:           Optional[str]   = None
    categoria:      Optional[str]   = None
    custo_unitario: Optional[float] = None
    ativo:          Optional[bool]  = None

class ComidaResponse(BaseModel):
    id:             int
    nome:           str
    categoria:      str
    custo_unitario: float
    ativo:          bool
    criado_em:      datetime
    atualizado_em:  datetime

    model_config = ConfigDict(from_attributes=True)

# Schemas para Desperdicio 

class DesperdicioCreate(BaseModel):
    comida_id:      int
    quantidade:     float
    setor:          str
    motivo:         str
    observacao:     Optional[str] = None

class DesperdicioUpdate(BaseModel):
    quantidade:     Optional[float] = None
    setor:          Optional[str]   = None
    motivo:         Optional[str]   = None
    observacao:     Optional[str]   = None

class DesperdicioResponse(BaseModel):
    id:             int
    comida_id:      int
    quantidade:     float
    setor:          str
    motivo:         str
    observacao:     Optional[str]
    custo_estimado: float
    criado_em:      datetime
    
    comida:         Optional[ComidaResponse] = None

    model_config = ConfigDict(from_attributes=True)

class PaginatedComida(BaseModel):
    data: list[ComidaResponse]
    total: int
    page: int
    limit: int
    pages: int

class PaginatedDesperdicio(BaseModel):
    data: list[DesperdicioResponse]
    total: int
    page: int
    limit: int
    pages: int



class UsuarioCreate(BaseModel):
    nome:       str
    email:      str
    senha:      str

class UsuarioResponse(BaseModel):
    id:         int
    nome:       str
    email:      str
    criado_em:  datetime

    model_config = ConfigDict(from_attributes=True)
