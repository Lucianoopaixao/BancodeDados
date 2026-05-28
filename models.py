from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, Time, Boolean, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from database import Base

class Equipe(Base):
    __tablename__ = "equipe"

    cod_equipe = Column(Integer, primary_key=True, index=True)
    atuacao = Column(String)

    funcionarios = relationship("Funcionario", back_populates="equipe")
    festivais = relationship("Festival", back_populates="equipe")
    financiamentos = relationship("Financia", back_populates="equipe")

class Funcionario(Base):
    __tablename__ = "funcionario"
    
    cpf = Column(String, ForeignKey("pessoa.cpf"), primary_key=True)
    cargo = Column(String, nullable=False)
    salario = Column(Numeric)
    cod_equipe = Column(Integer, ForeignKey("equipe.cod_equipe"))
    data_inicio = Column(Date)

    dados_pessoais = relationship("Pessoa", back_populates="funcionario", foreign_keys=[cpf])
    equipe = relationship("Equipe", back_populates="funcionarios")


class Festival(Base):
    __tablename__ = "festival"
    
    cod_equipe = Column(Integer, ForeignKey("equipe.cod_equipe"), primary_key=True)
    cod_festival = Column(Integer, primary_key=True)
    nome = Column(String)
    local_festival = Column(String)
    data_inicio = Column(Date)
    data_admissao_equipe = Column(Date)
    data_fim = Column(Date)
    horario = Column(Time)

    equipe = relationship("Equipe", back_populates="festivais")
    atracoes = relationship("AtracoesMusicais", back_populates="festival")
    realizacoes = relationship("Realiza", back_populates="festival")

class Pessoa(Base):
    __tablename__ = "pessoa"

    cpf = Column(String, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    rua = Column(String)
    numero = Column(String)
    cidade = Column(String)
    data_nascimento = Column(Date)
    id_patrocinador = Column(Integer, ForeignKey("patrocinador.id_patrocinador"))
    telefone = Column(String)

    patrocinador = relationship("Patrocinador", back_populates="pessoas")

    # Relacionamento com Artista (Uma pessoa pode ser um artista)
    artista = relationship("Artista", back_populates="dados_pessoais", uselist=False)
    fa = relationship("Fa", back_populates="dados_pessoais", uselist=False)
    funcionario = relationship("Funcionario", back_populates="dados_pessoais", uselist=False)


class Artista(Base):
    __tablename__ = "artista"
    
    cpf = Column(String, ForeignKey("pessoa.cpf"), primary_key=True)
    nome_artistico = Column(String, nullable=False)
    genero_musical = Column(String)
    valor_cache = Column(Numeric)

    dados_pessoais = relationship("Pessoa", back_populates="artista", foreign_keys=[cpf])
    realizacoes = relationship("Realiza", back_populates="artista")

class Patrocinador(Base):
    __tablename__ = "patrocinador"
    
    id_patrocinador = Column(Integer, primary_key=True, autoincrement=True)

    pessoas = relationship("Pessoa", back_populates="patrocinador")
    empresas = relationship("Empresa", back_populates="patrocinador")
    financiamentos = relationship("Financia", back_populates="patrocinador")

class Empresa(Base):
    __tablename__ = "empresa"
    
    cnpj = Column(String, primary_key=True)
    id_patrocinador = Column(Integer, ForeignKey("patrocinador.id_patrocinador"))
    nome = Column(String, nullable=False)
    razao_social = Column(String)

    patrocinador = relationship("Patrocinador", back_populates="empresas")

class Ingresso(Base):
    __tablename__ = "ingresso"
    
    id_ingresso = Column(Integer, primary_key=True, autoincrement=True)
    lote = Column(Integer, nullable=False)
    entrada = Column(String, nullable=False)
    tipo = Column(String, nullable=False)
    lounge = Column(Boolean)
    cpf = Column(String, ForeignKey("fa.cpf"), nullable=False)
    valor_pago = Column(Numeric)
    data_transacao = Column(Date)

    fa = relationship("Fa", back_populates="ingressos")

# Tabelas Associativas e de Relações Complexas (N:M)
class Financia(Base):
    __tablename__ = "financia"
    
    id_patrocinador = Column(Integer, ForeignKey("patrocinador.id_patrocinador"), primary_key=True)
    cod_equipe = Column(Integer, ForeignKey("equipe.cod_equipe"), primary_key=True)
    verba = Column(Numeric)

    patrocinador = relationship("Patrocinador", back_populates="financiamentos")
    equipe = relationship("Equipe", back_populates="financiamentos")

class AtracoesMusicais(Base):
    __tablename__ = "atracoes_musicais"
    
    nome_atracao = Column(String, primary_key=True)
    cod_equipe = Column(Integer, primary_key=True)
    cod_festival = Column(Integer, primary_key=True)
    
    # referência para chave estrangeira composta da tabela Festival
    __table_args__ = (
        ForeignKeyConstraint(
            ['cod_equipe', 'cod_festival'],
            ['festival.cod_equipe', 'festival.cod_festival']
        ),
    )

    festival = relationship("Festival", back_populates="atracoes")

class Realiza(Base):
    __tablename__ = "realiza"
    
    cpf = Column(String, ForeignKey("artista.cpf"), primary_key=True)
    cod_festival = Column(Integer, primary_key=True)
    cod_equipe = Column(Integer, primary_key=True)
    horas = Column(Integer)

    # referência para chave estrangeira composta da tabela Festival
    __table_args__ = (
        ForeignKeyConstraint(
            ['cod_equipe', 'cod_festival'],
            ['festival.cod_equipe', 'festival.cod_festival']
        ),
    )

    artista = relationship("Artista", back_populates="realizacoes")
    festival = relationship("Festival", back_populates="realizacoes")

class Fa(Base):
    __tablename__ = "fa"
    
    cpf = Column(String, ForeignKey("pessoa.cpf"), primary_key=True)
    indicado_por = Column(String, ForeignKey("fa.cpf"))

    dados_pessoais = relationship("Pessoa", back_populates="fa", foreign_keys=[cpf])
    ingressos = relationship("Ingresso", back_populates="fa")
    indicacoes = relationship("Fa", backref="indicador", remote_side=[cpf])