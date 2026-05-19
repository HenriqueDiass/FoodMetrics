from sqlalchemy.orm import Session
from backend.models import Comida
from backend.schemas import ComidaCreate, ComidaUpdate


def listar_comidas(db: Session):
    return db.query(Comida).all()


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
    comida.descricao = dados.descricao
    comida.preco = dados.preco
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
