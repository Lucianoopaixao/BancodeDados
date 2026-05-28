from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, time

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

class FestivalBase(BaseModel):
    cod_equipe: int
    cod_festival: int
    nome: str
    local_festival: str
    data_inicio: date
    data_admissao_equipe: date
    data_fim: date
    horario: time

class FestivalCreate(FestivalBase):
    pass

class Festival(FestivalBase):
    model_config = ConfigDict(from_attributes=True)

class IngressoBase(BaseModel):
    lote: int
    entrada: str
    tipo: str
    lounge: Optional[bool] = False
    cpf: str # O CPF do Fã
    valor_pago: float
    data_transacao: date

class IngressoCreate(IngressoBase):
    pass

class Ingresso(IngressoBase):
    id_ingresso: int
    model_config = ConfigDict(from_attributes=True)

class PessoaBase(BaseModel):
    cpf: str
    nome: str
    rua: Optional[str] = None
    numero: Optional[str] = None
    cidade: Optional[str] = None
    data_nascimento: Optional[date] = None
    id_patrocinador: Optional[int] = None
    telefone: Optional[str] = None

class PessoaCreate(PessoaBase):
    pass

class Pessoa(PessoaBase):
    model_config = ConfigDict(from_attributes=True)

class FaBase(BaseModel):
    cpf: str
    indicado_por: Optional[str] = None

class FaCreate(FaBase):
    pass

class Fa(FaBase):
    model_config = ConfigDict(from_attributes=True)

class PatrocinadorBase(BaseModel):
    # Não colocamos atributos aqui porque o banco gera o ID sozinho
    pass

class PatrocinadorCreate(PatrocinadorBase):
    pass

class Patrocinador(PatrocinadorBase):
    id_patrocinador: int
    model_config = ConfigDict(from_attributes=True)

class EmpresaBase(BaseModel):
    cnpj: str
    id_patrocinador: Optional[int] = None
    nome: str
    razao_social: Optional[str] = None

class EmpresaCreate(EmpresaBase):
    pass

class Empresa(EmpresaBase):
    model_config = ConfigDict(from_attributes=True)

class FinanciaBase(BaseModel):
    id_patrocinador: int
    cod_equipe: int
    verba: float

class FinanciaCreate(FinanciaBase):
    pass

class Financia(FinanciaBase):
    model_config = ConfigDict(from_attributes=True)  

class AtracaoMusicalBase(BaseModel):
    nome_atracao: str
    cod_equipe: int
    cod_festival: int

class AtracaoMusicalCreate(AtracaoMusicalBase):
    pass

class AtracaoMusical(AtracaoMusicalBase):
    model_config = ConfigDict(from_attributes=True)

class RealizaBase(BaseModel):
    cpf: str # CPF do artista
    cod_festival: int
    cod_equipe: int
    horas: int

class RealizaCreate(RealizaBase):
    pass

class Realiza(RealizaBase):
    model_config = ConfigDict(from_attributes=True)