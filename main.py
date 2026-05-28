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

# leitura de uma equipe com seus funcionarios (GET)
@app.get("/equipes/{cod_equipe}/detalhes")
def obter_equipe_detalhada(cod_equipe: int, db: Session = Depends(get_db)):
    db_equipe = crud.obter_equipe_com_funcionarios(db, cod_equipe=cod_equipe)
    
    if db_equipe is None:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
        
    return db_equipe

@app.get("/artistas/detalhes")
def listar_artistas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    artistas = crud.listar_artistas_com_detalhes(db, skip=skip, limit=limit)
    return artistas

# buscar artistas por gênero musical
@app.get("/artistas/genero/{genero}")
def buscar_artistas_genero(genero: str, db: Session = Depends(get_db)):
    artistas = crud.buscar_artistas_por_genero(db, genero=genero)
    if not artistas:
        raise HTTPException(status_code=404, detail="Nenhum artista encontrado para este gênero")
    return artistas

# listar os artistas com os maiores cachês
@app.get("/artistas/top-caros")
def listar_artistas_caros(limite: int = 5, db: Session = Depends(get_db)):
    artistas = crud.listar_artistas_mais_caros(db, limite=limite)
    return artistas

@app.get("/festivais/", response_model=list[schemas.Festival])
def listar_festivais(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.listar_festivais(db, skip=skip, limit=limit)

@app.post("/festivais/", response_model=schemas.Festival)
def criar_festival(festival: schemas.FestivalCreate, db: Session = Depends(get_db)):
    return crud.criar_festival(db, festival=festival)

# ==========================================
@app.post("/ingressos/vender", response_model=schemas.Ingresso)
def vender_ingresso(ingresso: schemas.IngressoCreate, db: Session = Depends(get_db)):
    return crud.vender_ingresso(db, ingresso=ingresso)

@app.get("/fas/{cpf}/ingressos", response_model=list[schemas.Ingresso])
def listar_ingressos_do_fa(cpf: str, db: Session = Depends(get_db)):
    ingressos = crud.listar_ingressos_por_fa(db, cpf_fa=cpf)
    if not ingressos:
        raise HTTPException(status_code=404, detail="Nenhum ingresso encontrado para este CPF")
    return ingressos

@app.post("/pessoas/", response_model=schemas.Pessoa)
def criar_pessoa(pessoa: schemas.PessoaCreate, db: Session = Depends(get_db)):
    # Verifica se o CPF já existe para não dar erro no banco
    db_pessoa = db.query(models.Pessoa).filter(models.Pessoa.cpf == pessoa.cpf).first()
    if db_pessoa:
        raise HTTPException(status_code=400, detail="CPF já cadastrado no sistema")
    return crud.criar_pessoa(db, pessoa=pessoa)

@app.post("/fas/", response_model=schemas.Fa)
def criar_fa(fa: schemas.FaCreate, db: Session = Depends(get_db)):
    # Verifica se o Fã já existe
    db_fa = db.query(models.Fa).filter(models.Fa.cpf == fa.cpf).first()
    if db_fa:
        raise HTTPException(status_code=400, detail="Este fã já está cadastrado")
    return crud.criar_fa(db, fa=fa)

@app.post("/patrocinadores/", response_model=schemas.Patrocinador)
def criar_patrocinador(db: Session = Depends(get_db)):
    # Observe que esta rota não pede nenhum dado de entrada (nenhum schema no parênteses)
    return crud.criar_patrocinador(db)

@app.post("/empresas/", response_model=schemas.Empresa)
def criar_empresa(empresa: schemas.EmpresaCreate, db: Session = Depends(get_db)):
    # Validação para não cadastrar CNPJ repetido
    db_empresa = db.query(models.Empresa).filter(models.Empresa.cnpj == empresa.cnpj).first()
    if db_empresa:
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado no sistema")
    return crud.criar_empresa(db, empresa=empresa)

@app.post("/financiamentos/", response_model=schemas.Financia)
def registrar_financiamento(financiamento: schemas.FinanciaCreate, db: Session = Depends(get_db)):
    # Antes de registrar a verba, verifica se a equipe existe para evitar erro 500 do banco
    db_equipe = db.query(models.Equipe).filter(models.Equipe.cod_equipe == financiamento.cod_equipe).first()
    if not db_equipe:
         raise HTTPException(status_code=404, detail="Equipe não encontrada")
    
    return crud.registrar_financiamento(db, financiamento=financiamento)

@app.post("/atracoes/", response_model=schemas.AtracaoMusical)
def adicionar_atracao(atracao: schemas.AtracaoMusicalCreate, db: Session = Depends(get_db)):
    # Verifica se o festival existe antes de cadastrar a atração
    db_festival = db.query(models.Festival).filter(
        models.Festival.cod_festival == atracao.cod_festival,
        models.Festival.cod_equipe == atracao.cod_equipe
    ).first()
    
    if not db_festival:
        raise HTTPException(status_code=404, detail="Festival não encontrado")
        
    return crud.adicionar_atracao(db, atracao=atracao)

@app.post("/realizacoes/", response_model=schemas.Realiza)
def registrar_realizacao(realizacao: schemas.RealizaCreate, db: Session = Depends(get_db)):
    # Verifica se o artista existe
    db_artista = db.query(models.Artista).filter(models.Artista.cpf == realizacao.cpf).first()
    if not db_artista:
        raise HTTPException(status_code=404, detail="Artista não encontrado")
        
    return crud.registrar_realizacao(db, realizacao=realizacao)

@app.get("/festivais/{cod_festival}/atracoes", response_model=list[schemas.AtracaoMusical])
def listar_atracoes(cod_festival: int, db: Session = Depends(get_db)):
    atracoes = crud.listar_atracoes_do_festival(db, cod_festival=cod_festival)
    if not atracoes:
        raise HTTPException(status_code=404, detail="Nenhuma atração encontrada para este festival")
    return atracoes