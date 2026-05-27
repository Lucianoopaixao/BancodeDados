from sqlalchemy.orm import Session
from models import Equipe
from schemas import EquipeCreate, EquipeUpdate

# criacao
def criar_equipe(db: Session, equipe: EquipeCreate):
    db_equipe = Equipe(**equipe.model_dump())
    db.add(db_equipe)
    db.commit()
    db.refresh(db_equipe)
    return db_equipe

# leitura
def listar_equipes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Equipe).offset(skip).limit(limit).all()

def obter_equipe(db: Session, cod_equipe: int):
    return db.query(Equipe).filter(Equipe.cod_equipe == cod_equipe).first()

# atualizacao
def atualizar_equipe(db: Session, cod_equipe: int, dados: EquipeUpdate):
    db_equipe = db.query(Equipe).filter(Equipe.cod_equipe == cod_equipe).first()
    if db_equipe:
        for key, value in dados.model_dump(exclude_unset=True).items():
            setattr(db_equipe, key, value)
        db.commit()
        db.refresh(db_equipe)
    return db_equipe

# exclusao
def deletar_equipe(db: Session, cod_equipe: int):
    db_equipe = db.query(Equipe).filter(Equipe.cod_equipe == cod_equipe).first()
    if db_equipe:
        db.delete(db_equipe)
        db.commit()
    return db_equipe