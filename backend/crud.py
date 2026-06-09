from sqlalchemy.orm import Session
from backend.models import Comida, Desperdicio
from backend.schemas import ComidaCreate, ComidaUpdate, DesperdicioCreate, DesperdicioUpdate
import math

def listar_comidas(db: Session, nome: str = None, page: int = 1, limit: int = 10):
    query = db.query(Comida)
    if nome:
        query = query.filter(Comida.nome.ilike(f"%{nome}%"))
    
    totalQuery = query.count()
    if limit > 0:
        totalPage = math.ceil(totalQuery/limit)
    else:
        totalPage = 0
    pular = (page - 1) * limit
    dados = query.offset(pular).limit(limit).all()

    return {
        "data": dados,
        "total": totalQuery,
        "page": page,
        "limit": limit,
        "pages": totalPage
    }


def buscar_comida(db: Session, comida_id: int):
    return db.query(Comida).filter(Comida.id == comida_id).first()


def criar_comida(db: Session, dados: ComidaCreate):
    comida = Comida(**dados.model_dump())
    db.add(comida)
    db.commit()
    db.refresh(comida)
    return comida


def atualizar_comida(db: Session, comida_id: int, dados: ComidaUpdate):
    comida = buscar_comida(db, comida_id)
    if not comida:
        return None
    atualizacoes = dados.model_dump(exclude_unset=True)
    for campo, valor in atualizacoes.items():
        setattr(comida, campo, valor)
    db.commit()
    db.refresh(comida)
    return comida


def substituir_comida(db: Session, comida_id: int, dados: ComidaCreate):
    comida = buscar_comida(db, comida_id)
    if not comida:
        return None
    comida.nome = dados.nome
    comida.categoria = dados.categoria
    comida.custo_unitario = dados.custo_unitario
    db.commit()
    db.refresh(comida)
    return comida


def deletar_comida(db: Session, comida_id: int):
    comida = buscar_comida(db, comida_id)
    if comida:
        db.delete(comida)
        db.commit()
    else:
        print(f"comida {comida_id} nao encontrada para deletar.")
    return comida


#  CRUD para Desperdicio 

def listar_desperdicios(db: Session, setor: str = None, page: int = 1, limit: int = 10):
    query = db.query(Desperdicio)
    if setor:
        query = query.filter(Desperdicio.setor.ilike(f"%{setor}%"))
    
    totalQuery = query.count()
    if limit > 0:
        totalPage = math.ceil(totalQuery/limit)
    else:
        totalPage = 0
    pular = (page - 1) * limit
    dados = query.offset(pular).limit(limit).all()

    return {
        "data": dados,
        "total": totalQuery,
        "page": page,
        "limit": limit,
        "pages": totalPage
    }


def buscar_desperdicio(db: Session, desperdicio_id: int):
    return db.query(Desperdicio).filter(Desperdicio.id == desperdicio_id).first()


def criar_desperdicio(db: Session, dados: DesperdicioCreate):
    comida = db.query(Comida).filter(Comida.id == dados.comida_id).first()
    if not comida:
        return None
    
    custo_total = float(comida.custo_unitario) * dados.quantidade
    
    desperdicio = Desperdicio(
        **dados.model_dump(),
        custo_estimado=custo_total
    )
    db.add(desperdicio)
    db.commit()
    db.refresh(desperdicio)
    return desperdicio


def atualizar_desperdicio(db: Session, desperdicio_id: int, dados: DesperdicioUpdate):
    desperdicio = buscar_desperdicio(db, desperdicio_id)
    if not desperdicio:
        return None
    
    atualizacoes = dados.model_dump(exclude_unset=True)
    for campo, valor in atualizacoes.items():
        setattr(desperdicio, campo, valor)
    
    if "quantidade" in atualizacoes:
        comida = db.query(Comida).filter(Comida.id == desperdicio.comida_id).first()
        if comida:
            desperdicio.custo_estimado = float(comida.custo_unitario) * desperdicio.quantidade
            
    db.commit()
    db.refresh(desperdicio)
    return desperdicio


def deletar_desperdicio(db: Session, desperdicio_id: int):
    desperdicio = buscar_desperdicio(db, desperdicio_id)
    if desperdicio:
        db.delete(desperdicio)
        db.commit()
    return desperdicio
