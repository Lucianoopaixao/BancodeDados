from sqlalchemy import Column, Integer, String
from database import Base

class Equipe(Base):
    __tablename__ = "equipe"

    cod_equipe = Column(Integer, primary_key=True, index=True)
    atuacao = Column(String)