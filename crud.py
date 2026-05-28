from sqlalchemy.orm import Session
from models import Equipe, Pessoa, Artista, Festival, Ingresso, Fa, Patrocinador, Empresa, Financia, Realiza, AtracoesMusicais
from sqlalchemy.orm import joinedload
from schemas import EquipeCreate, EquipeUpdate
import schemas

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

#Buscar uma Equipe e trazer TODOS os funcionários dela de uma vez
def obter_equipe_com_funcionarios(db: Session, cod_equipe: int):
    return db.query(Equipe).options(joinedload(Equipe.funcionarios)).filter(Equipe.cod_equipe == cod_equipe).first()


#busca equipe pelo tipo de atuação
def buscar_equipes_por_atuacao(db: Session, atuacao: str):
    return db.query(Equipe).filter(Equipe.atuacao.ilike(f"%{atuacao}%")).all()

# 1. Busca todos os artistas e já traz os dados pessoais (nome real, cidade, telefone)
def listar_artistas_com_detalhes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Artista).options(joinedload(Artista.dados_pessoais)).offset(skip).limit(limit).all()

# 2. Busca artistas por gênero musical
def buscar_artistas_por_genero(db: Session, genero: str):
    return db.query(Artista).filter(Artista.genero_musical.ilike(f"%{genero}%")).all()

# 3. Descobre os artistas mais caros (ordenação decrescente pelo cachê)
def listar_artistas_mais_caros(db: Session, limite: int = 5):
    return db.query(Artista).order_by(Artista.valor_cache.desc()).limit(limite).all()

# 4. Criar um Artista (Como o banco exige que a Pessoa exista primeiro por causa do CPF)
def criar_artista_completo(db: Session, dados_pessoa: dict, dados_artista: dict):
    # Primeiro cria a pessoa
    nova_pessoa = Pessoa(**dados_pessoa)
    db.add(nova_pessoa)
    db.flush() # Salva temporariamente para usar o CPF
    
    # Depois cria o artista vinculado àquela pessoa
    novo_artista = Artista(**dados_artista)
    db.add(novo_artista)
    
    db.commit()
    db.refresh(novo_artista)
    return novo_artista

def listar_festivais(db: Session, skip: int = 0, limit: int = 100):
    # O joinedload já traz os dados da Equipe que vai trabalhar no festival!
    return db.query(Festival).options(joinedload(Festival.equipe)).offset(skip).limit(limit).all()

def criar_festival(db: Session, festival: schemas.FestivalCreate):
    db_festival = Festival(**festival.model_dump())
    db.add(db_festival)
    db.commit()
    db.refresh(db_festival)
    return db_festival

def vender_ingresso(db: Session, ingresso: schemas.IngressoCreate):
    db_ingresso = Ingresso(**ingresso.model_dump())
    db.add(db_ingresso)
    db.commit()
    db.refresh(db_ingresso)
    return db_ingresso

def listar_ingressos_por_fa(db: Session, cpf_fa: str):
    # Retorna todos os ingressos comprados por um CPF específico
    return db.query(Ingresso).filter(Ingresso.cpf == cpf_fa).all()

def criar_pessoa(db: Session, pessoa: schemas.PessoaCreate):
    db_pessoa = Pessoa(**pessoa.model_dump())
    db.add(db_pessoa)
    db.commit()
    db.refresh(db_pessoa)
    return db_pessoa

def criar_fa(db: Session, fa: schemas.FaCreate):
    db_fa = Fa(**fa.model_dump())
    db.add(db_fa)
    db.commit()
    db.refresh(db_fa)
    return db_fa

def criar_patrocinador(db: Session):
    # Cria vazio, pois o banco se encarrega de dar o ID
    db_patrocinador = Patrocinador()
    db.add(db_patrocinador)
    db.commit()
    db.refresh(db_patrocinador)
    return db_patrocinador

def criar_empresa(db: Session, empresa: schemas.EmpresaCreate):
    db_empresa = Empresa(**empresa.model_dump())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

def registrar_financiamento(db: Session, financiamento: schemas.FinanciaCreate):
    db_financia = Financia(**financiamento.model_dump())
    db.add(db_financia)
    db.commit()
    db.refresh(db_financia)
    return db_financia

def adicionar_atracao(db: Session, atracao: schemas.AtracaoMusicalCreate):
    db_atracao = AtracoesMusicais(**atracao.model_dump())
    db.add(db_atracao)
    db.commit()
    db.refresh(db_atracao)
    return db_atracao

def registrar_realizacao(db: Session, realizacao: schemas.RealizaCreate):
    db_realizacao = Realiza(**realizacao.model_dump())
    db.add(db_realizacao)
    db.commit()
    db.refresh(db_realizacao)
    return db_realizacao

def listar_atracoes_do_festival(db: Session, cod_festival: int):
    # Retorna o line-up inteiro de um festival específico
    return db.query(AtracoesMusicais).filter(AtracoesMusicais.cod_festival == cod_festival).all()