import os
from dotenv import load_dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. CARREGA O SEU .ENV E CONECTA NO SUPABASE
load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")

# O SQLAlchemy é o motor que vai fazer as consultas SQL para você
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. MAPEIA A SUA TABELA DO BANCO DE DADOS
# Isso avisa ao Python como a sua tabela 'equipe' é lá no Supabase
class Equipe(Base):
    __tablename__ = "equipe"
    
    cod_equipe = Column(Integer, primary_key=True)
    atuacao = Column(String)

# 3. CRIA A API FASTAPI
app = FastAPI(title="Minha API do Festival")

# 4. ROTA QUE FAZ A CONSULTA (O SEU SELECT)
@app.get("/equipes")
def listar_equipes():
    # Abre a conexão com o banco
    db = SessionLocal()
    try:
        # Faz a consulta: SELECT * FROM equipe;
        equipes = db.query(Equipe).all()
        return {"dados": equipes}
    finally:
        # Fecha a conexão
        db.close()