from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import engine, get_db

# cria as tabelas no banco caso nao existam
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# criacao (POST)
@app.post("/equipes/", response_model=schemas.Equipe)
def criar_equipe(equipe: schemas.EquipeCreate, db: Session = Depends(get_db)):
    db_equipe = crud.obter_equipe(db, cod_equipe=equipe.cod_equipe)
    if db_equipe:
        raise HTTPException(status_code=400, detail="Equipe com este codigo ja existe")
    return crud.criar_equipe(db=db, equipe=equipe)

# leitura de todas (GET)
@app.get("/equipes/", response_model=list[schemas.Equipe])
def listar_equipes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.listar_equipes(db, skip=skip, limit=limit)

# leitura de uma especifica (GET)
@app.get("/equipes/{cod_equipe}", response_model=schemas.Equipe)
def obter_equipe(cod_equipe: int, db: Session = Depends(get_db)):
    db_equipe = crud.obter_equipe(db, cod_equipe=cod_equipe)
    if db_equipe is None:
        raise HTTPException(status_code=404, detail="Equipe nao encontrada")
    return db_equipe

# atualizacao (PUT)
@app.put("/equipes/{cod_equipe}", response_model=schemas.Equipe)
def atualizar_equipe(cod_equipe: int, equipe: schemas.EquipeUpdate, db: Session = Depends(get_db)):
    db_equipe = crud.atualizar_equipe(db, cod_equipe, equipe)
    if db_equipe is None:
        raise HTTPException(status_code=404, detail="Equipe nao encontrada")
    return db_equipe

# exclusao (DELETE)
@app.delete("/equipes/{cod_equipe}")
def deletar_equipe(cod_equipe: int, db: Session = Depends(get_db)):
    db_equipe = crud.deletar_equipe(db, cod_equipe)
    if db_equipe is None:
        raise HTTPException(status_code=404, detail="Equipe nao encontrada")
    return {"mensagem": "Equipe deletada com sucesso"}