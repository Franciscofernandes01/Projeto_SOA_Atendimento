import logging
import os

# Configuração do Sistema de Logs (Requisito 4.5)
# Grava no terminal e também em um arquivo 'servidor_soap.log'
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("servidor_soap.log", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SOAP_Service")

# Importações Oficiais do Spyne
from spyne import Application, rpc, ServiceBase, Integer, Unicode, Array, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from spyne.model.fault import Fault 
from werkzeug.serving import run_simple

# Importações do seu Banco de Dados
from database.connection import SessionLocal
from database.models import SolicitacaoDB

# 1. DEFINIÇÃO DA SEGURANÇA (Requisito 4.3 - WS-Security Headers)
class AuthHeader(ComplexModel):
    """Estrutura do cabeçalho SOAP para autenticação."""
    __namespace__ = 'spyne.examples.atendimento'
    username = Unicode(min_occurs=1, max_occurs=1)
    password = Unicode(min_occurs=1, max_occurs=1)

# Estipula o Token Global de validação (Ex: admin / Root@123456)
USUARIO_VALIDO = "admin"
SENHA_VALIDA = "Root@123456"

def validar_autenticacao(ctx):
    """Função auxiliar para validar o Header de Segurança do SOAP."""
    header = ctx.in_header
    
    # Se o header não foi enviado
    if header is None:
        logger.warning("Tentativa de acesso bloqueada: Ausência de headers de segurança.")
        raise Fault(
            faultcode="Client.AuthenticationError", 
            faultstring="Acesso negado: Cabecalho de seguranca (AuthHeader) nao fornecido."
        )
    
    # Se o usuário ou senha estiverem incorretos
    if header.username != USUARIO_VALIDO or header.password != SENHA_VALIDA:
        logger.warning(f"Falha de autenticacao para o usuario: '{header.username}'")
        raise Fault(
            faultcode="Client.AuthenticationError", 
            faultstring="Acesso negado: Usuario ou senha invalidos no SOAP Header."
        )
    
    logger.info(f"Usuario '{header.username}' autenticado com sucesso.")

# 2. DEFINIÇÃO DOS MODELOS DE RETORNO (XSD automático)
class SolicitacaoModel(ComplexModel):
    """Modelo de dados para expor no XML Schema (XSD)"""
    __namespace__ = 'spyne.examples.atendimento'
    id = Integer
    usuario = Unicode
    descricao = Unicode
    status = Unicode

# 3. IMPLEMENTAÇÃO DO SERVIÇO COM CRUD E PROTEÇÃO (Requisitos 4.1, 4.3 e 4.5)
class AtendimentoService(ServiceBase):
    
    # Vincula o Header de segurança para ser exigido no WSDL deste serviço
    __in_header__ = AuthHeader

    @rpc(Unicode, Unicode, _returns=SolicitacaoModel)
    def criar_solicitacao(ctx, usuario, descricao):
        """CREATE: Protegido por autenticação, insere no banco."""
        logger.info(f"Chamada recebida: criar_solicitacao | Solicitante informado no corpo: {usuario}")
        
        # Valida as credenciais do Header SOAP
        validar_autenticacao(ctx)
        
        db = SessionLocal()
        try:
            nova_solicitacao = SolicitacaoDB(usuario=usuario, descricao=descricao, status="Pendente")
            db.add(nova_solicitacao)
            db.commit()
            db.refresh(nova_solicitacao)
            
            logger.info(f"Solicitacao criada com sucesso! ID: {nova_solicitacao.id}")
            return SolicitacaoModel(
                id=nova_solicitacao.id,
                usuario=nova_solicitacao.usuario,
                descricao=nova_solicitacao.descricao,
                status=nova_solicitacao.status
            )
        except Exception as e:
            db.rollback()
            logger.error(f"Erro ao salvar no banco: {e}")
            raise Fault(faultcode="Server.DatabaseError", faultstring="Erro interno ao gravar dados.")
        finally:
            db.close()

    @rpc(Integer, _returns=SolicitacaoModel)
    def consultar_solicitacao(ctx, id_solicitacao):
        """READ: Busca uma solicitação pelo ID."""
        logger.info(f"Chamada recebida: consultar_solicitacao | ID: {id_solicitacao}")
        validar_autenticacao(ctx)
        
        db = SessionLocal()
        try:
            solicitacao = db.query(SolicitacaoDB).filter(SolicitacaoDB.id == id_solicitacao).first()
            if not solicitacao:
                logger.warning(f"Solicitacao ID {id_solicitacao} nao encontrada.")
                raise Fault(faultcode="Client.NotFoundError", faultstring=f"ID {id_solicitacao} nao existe.")
            
            return SolicitacaoModel(
                id=solicitacao.id,
                usuario=solicitacao.usuario,
                descricao=solicitacao.descricao,
                status=solicitacao.status
            )
        finally:
            db.close()

    @rpc(Integer, Unicode, _returns=SolicitacaoModel)
    def atualizar_status(ctx, id_solicitacao, novo_status):
        """UPDATE: Atualiza o status de uma solicitação."""
        logger.info(f"Chamada recebida: atualizar_status | ID: {id_solicitacao} para {novo_status}")
        validar_autenticacao(ctx)
        
        db = SessionLocal()
        try:
            solicitacao = db.query(SolicitacaoDB).filter(SolicitacaoDB.id == id_solicitacao).first()
            if not solicitacao:
                raise Fault(faultcode="Client.NotFoundError", faultstring=f"ID {id_solicitacao} nao existe.")
            
            solicitacao.status = novo_status
            db.commit()
            db.refresh(solicitacao)
            
            logger.info(f"Status da solicitacao {id_solicitacao} atualizado para {novo_status}.")
            return SolicitacaoModel(
                id=solicitacao.id,
                usuario=solicitacao.usuario,
                descricao=solicitacao.descricao,
                status=solicitacao.status
            )
        except Exception as e:
            db.rollback()
            raise Fault(faultcode="Server.DatabaseError", faultstring=str(e))
        finally:
            db.close()

    @rpc(Integer, _returns=Unicode)
    def deletar_solicitacao(ctx, id_solicitacao):
        """DELETE: Remove uma solicitação do banco de dados."""
        logger.info(f"Chamada recebida: deletar_solicitacao | ID: {id_solicitacao}")
        validar_autenticacao(ctx)
        
        db = SessionLocal()
        try:
            solicitacao = db.query(SolicitacaoDB).filter(SolicitacaoDB.id == id_solicitacao).first()
            if not solicitacao:
                raise Fault(faultcode="Client.NotFoundError", faultstring=f"ID {id_solicitacao} nao existe.")
            
            db.delete(solicitacao)
            db.commit()
            
            logger.info(f"Solicitacao {id_solicitacao} deletada do banco.")
            return f"Solicitacao {id_solicitacao} excluida com sucesso."
        except Exception as e:
            db.rollback()
            raise Fault(faultcode="Server.DatabaseError", faultstring=str(e))
        finally:
            db.close()


# 4. CONFIGURAÇÃO DA APLICACÃO E DO SERVIDOR WSGI
application = Application(
    [AtendimentoService],
    tns='spyne.examples.atendimento',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    logger.info("========================================")
    logger.info("Inicializando o Servidor SOAP Corporativo...")
    logger.info("Endereço do WSDL: http://localhost:8000/?wsdl")
    logger.info("========================================")
    
    # Inicia o servidor na porta 8000
    run_simple('localhost', 8000, wsgi_application)