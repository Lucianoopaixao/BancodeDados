from pydantic import BaseModel
from typing import Optional

class EquipeBase(BaseModel):
    cod_equipe: int
    atuacao: str

class EquipeCreate(EquipeBase):
    pass

class EquipeUpdate(BaseModel):
    atuacao: Optional[str] = None

class Equipe(EquipeBase):
    class Config:
        from_attributes = True