# Arquivo: database/connection.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SUBISTITUA COM SUAS CREDENCIAIS DO MYSQL
# Formato: mysql+mysqlconnector://[usuario]:[senha]@[host]/[nome_do_banco]
# Note que trocamos o "@" de dentro da senha por "%40"
DATABASE_URL = "mysql+mysqlconnector://root:Root%40123456@localhost:3306/soa_atendimento"

# Cria o motor de conexão
engine = create_engine(DATABASE_URL, echo=True) # echo=True loga o SQL no terminal

# Cria a base para os modelos orm
Base = declarative_base()

# Fábrica de sessões para o CRUD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Função utilitária para obter uma sessão de banco."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()