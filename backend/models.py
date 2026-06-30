from sqlalchemy import Column, Integer, String, Numeric, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from backend.database import Base

class Comida(Base):
    __tablename__ = "comidas"

    id              = Column(Integer, primary_key=True, index=True)
    nome            = Column(String, nullable=False)
    categoria       = Column(String, nullable=False) # Ex: Hortifruti, Carnes, Bebidas
    custo_unitario  = Column(Numeric(10, 2), nullable=False)
    ativo           = Column(Boolean, default=True)
    criado_em       = Column(DateTime, server_default=func.now())
    atualizado_em   = Column(DateTime, server_default=func.now(), onupdate=func.now())

    
    desperdicios    = relationship("Desperdicio", back_populates="comida")

class Desperdicio(Base):
    __tablename__ = "desperdicios"

    id              = Column(Integer, primary_key=True, index=True)
    comida_id       = Column(Integer, ForeignKey("comidas.id"), nullable=False)
    quantidade      = Column(Numeric(10, 2), nullable=False)
    setor           = Column(String, nullable=False) # Ex: Cozinha Quente, Estoque
    motivo          = Column(String, nullable=False) # Ex: Validade, Erro de preparo
    observacao      = Column(String, nullable=True)
    custo_estimado  = Column(Numeric(10, 2), nullable=False) # Valor calculado (quantidade * custo_unitario)
    criado_em       = Column(DateTime, server_default=func.now())
    comida          = relationship("Comida", back_populates="desperdicios")

class Usuario(Base):
    __tablename__ = "usuarios"

    id        = Column(Integer, primary_key=True, index=True)
    nome      = Column(String, nullable=False)
    email     = Column(String, unique=True, index=True, nullable=False)
    senha     = Column(String, nullable=False) # Lembre-se: aqui o banco vai salvar o hash, e não a senha pura
    criado_em = Column(DateTime, server_default=func.now())
