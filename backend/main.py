from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional

import crud
import auth
from database import Base, engine, get_db
from schemas import (
    ComidaCreate, ComidaResponse, ComidaUpdate,
    DesperdicioCreate, DesperdicioResponse, DesperdicioUpdate,
    PaginatedComida, PaginatedDesperdicio, UsuarioCreate, UsuarioResponse
)

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
    usuario = crud.obter_usuario_por_email(db, email=form_data.username)
    
    if not usuario or not auth.verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.criar_token_acesso(data={"sub": usuario.email})
    return {"access_token": access_token, "token_type": "bearer"}


# --- Rotas de Acesso (Usuários) ---
@app.post("/usuarios", response_model=UsuarioResponse, status_code=201)
def criar_usuario(dados: UsuarioCreate, db: Session = Depends(get_db)):
    
    # 1. Verifica se o email já existe no banco
    usuario_existente = crud.obter_usuario_por_email(db, email=dados.email)
    
    # 2. Retorna erro caso o email seja duplicado (Mudado para 409 conforme REQ 2)
    if usuario_existente:
        raise HTTPException(status_code=409, detail="Email já cadastrado.")
    
    # 3. CRIPTOGRAFIA DE SENHA
    dados.senha = auth.gerar_hash_senha(dados.senha)
    
    # 4. Cria o usuário no banco
    novo_usuario = crud.criar_usuario(db, dados)
    
    # 5. ENVIO DE E-MAIL
    auth.enviar_email_boas_vindas(destinatario=novo_usuario.email, nome=novo_usuario.nome)
    
    return novo_usuario


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