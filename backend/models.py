from sqlalchemy import Column, Integer, String, Numeric
from backend.database import Base

class Comida(Base):
    __tablename__ = "comidas"

    id        = Column(Integer, primary_key=True, index=True)
    nome      = Column(String, nullable=False)
    preco     = Column(Numeric(10, 2), nullable=False)
    descricao = Column(String, default="")
