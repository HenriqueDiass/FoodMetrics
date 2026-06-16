from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend import crud, auth
from backend.database import Base, engine, get_db
from backend.schemas import (
    ComidaCreate, ComidaResponse, ComidaUpdate,
    DesperdicioCreate, DesperdicioResponse, DesperdicioUpdate,
    PaginatedComida, PaginatedDesperdicio
)
from typing import Optional

Base.metadata.create_all(bind=engine)  # cria as tabelas ao iniciar

app = FastAPI(title="API FOODmetrics")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Rota de Autenticação ---

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    if form_data.username != "admin" or not auth.verificar_senha(form_data.password, auth.gerar_hash_senha("123")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.criar_token_acesso(data={"sub": form_data.username})
    return {"access_token": access_token, "token_type": "bearer"}


# --- Rotas para Comidas ---

@app.get("/comidas", response_model=PaginatedComida)
def listar(nome: Optional[str] = None, page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    return crud.listar_comidas(db, nome=nome, page=page, limit=limit)


@app.get("/comidas/{comida_id}", response_model=ComidaResponse)
def buscar(comida_id: int, db: Session = Depends(get_db)):
    comida = crud.buscar_comida(db, comida_id)
    if not comida:
        raise HTTPException(status_code=404, detail="Comida não encontrada")
    return comida


@app.post("/comidas", response_model=ComidaResponse, status_code=201)
def criar(dados: ComidaCreate, db: Session = Depends(get_db), current_user: str = Depends(auth.obter_usuario_atual)):
    return crud.criar_comida(db, dados)


@app.put("/comidas/{comida_id}", response_model=ComidaResponse)
def substituir(comida_id: int, dados: ComidaCreate,
               db: Session = Depends(get_db), current_user: str = Depends(auth.obter_usuario_atual)):
    comida = crud.substituir_comida(db, comida_id, dados)
    if not comida:
        raise HTTPException(status_code=404, detail="Comida não encontrada")
    return comida


@app.patch("/comidas/{comida_id}", response_model=ComidaResponse)
def atualizar(comida_id: int, dados: ComidaUpdate,
              db: Session = Depends(get_db), current_user: str = Depends(auth.obter_usuario_atual)):
    comida = crud.atualizar_comida(db, comida_id, dados)
    if not comida:
        raise HTTPException(status_code=404, detail="Comida não encontrada")
    return comida


@app.delete("/comidas/{comida_id}", status_code=204)
def deletar(comida_id: int, db: Session = Depends(get_db), current_user: str = Depends(auth.obter_usuario_atual)):
    comida = crud.deletar_comida(db, comida_id)
    if not comida:
        raise HTTPException(status_code=404, detail="Comida não encontrada")


# --- Rotas para Desperdicio ---

@app.get("/desperdicios", response_model=PaginatedDesperdicio)
def listar_desperdicios(setor: Optional[str] = None, page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    return crud.listar_desperdicios(db, setor=setor, page=page, limit=limit)


@app.get("/desperdicios/{desperdicio_id}", response_model=DesperdicioResponse)
def buscar_desperdicio(desperdicio_id: int, db: Session = Depends(get_db)):
    desperdicio = crud.buscar_desperdicio(db, desperdicio_id)
    if not desperdicio:
        raise HTTPException(status_code=404, detail="Registro de desperdício não encontrado")
    return desperdicio


@app.post("/desperdicios", response_model=DesperdicioResponse, status_code=201)
def criar_desperdicio(dados: DesperdicioCreate, db: Session = Depends(get_db), current_user: str = Depends(auth.obter_usuario_atual)):
    desperdicio = crud.criar_desperdicio(db, dados)
    if not desperdicio:
        raise HTTPException(status_code=404, detail="Comida não encontrada para associar ao desperdício")
    return desperdicio


@app.patch("/desperdicios/{desperdicio_id}", response_model=DesperdicioResponse)
def atualizar_desperdicio(desperdicio_id: int, dados: DesperdicioUpdate,
                         db: Session = Depends(get_db), current_user: str = Depends(auth.obter_usuario_atual)):
    desperdicio = crud.atualizar_desperdicio(db, desperdicio_id, dados)
    if not desperdicio:
        raise HTTPException(status_code=404, detail="Registro de desperdício não encontrado")
    return desperdicio


@app.delete("/desperdicios/{desperdicio_id}", status_code=204)
def deletar_desperdicio(desperdicio_id: int, db: Session = Depends(get_db), current_user: str = Depends(auth.obter_usuario_atual)):
    desperdicio = crud.deletar_desperdicio(db, desperdicio_id)
    if not desperdicio:
        raise HTTPException(status_code=404, detail="Registro de desperdício não encontrado")
