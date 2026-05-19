from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend import crud
from backend.database import Base, engine, get_db
from backend.schemas import ComidaCreate, ComidaResponse, ComidaUpdate

Base.metadata.create_all(bind=engine)  # cria as tabelas ao iniciar

app = FastAPI(title="API FOODmetrics")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/comidas", response_model=list[ComidaResponse])
def listar(db: Session = Depends(get_db)):
    return crud.listar_comidas(db)



@app.post("/comidas", response_model=ComidaResponse, status_code=201)
def criar(dados: ComidaCreate, db: Session = Depends(get_db)):
    return crud.criar_comida(db, dados)


@app.put("/comidas/{comida_id}", response_model=ComidaResponse)
def substituir(comida_id: int, dados: ComidaCreate,
               db: Session = Depends(get_db)):
    comida = crud.substituir_comida(db, comida_id, dados)
    if not comida:
        raise HTTPException(status_code=404, detail="Comida nao encontrada")
    return comida


@app.patch("/comidas/{comida_id}", response_model=ComidaResponse)
def atualizar(comida_id: int, dados: ComidaUpdate,
              db: Session = Depends(get_db)):
    comida = crud.atualizar_comida(db, comida_id, dados)
    if not comida:
        raise HTTPException(status_code=404, detail="Comida nao encontrada")
    return comida


@app.delete("/comidas/{comida_id}", status_code=204)
def deletar(comida_id: int, db: Session = Depends(get_db)):
    crud.deletar_comida(db, comida_id)
