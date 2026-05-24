# Arquivo: database/models.py
from sqlalchemy import Column, Integer, Unicode, String
from .connection import Base, engine

class SolicitacaoDB(Base):
    """Modelo ORM para a tabela 'solicitacoes' no MySQL."""
    __tablename__ = 'solicitacoes'

    id = Column(Integer, primary_key=True, index=True)
    usuario = Column(Unicode(100), nullable=False, index=True)
    descricao = Column(String(500), nullable=False)
    status = Column(Unicode(50), default='Pendente')

# Cria a tabela no MySQL se ela não existir
Base.metadata.create_all(bind=engine)
print("Tabelas do banco de dados verificadas/criadas.")