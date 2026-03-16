from spyne import Application, rpc, ServiceBase, Integer, Unicode, Array, ComplexModel
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from werkzeug.serving import run_simple

class Solicitacao(ComplexModel):
    id = Integer
    usuario = Unicode
    descricao = Unicode
    status = Unicode

# Banco de dados em memória para demonstração
solicitacoes_db = {
    1: {"usuario": "joao", "descricao": "Problema no login", "status": "Pendente"},
    2: {"usuario": "maria", "descricao": "Erro ao emitir boleto", "status": "Em andamento"}
}

class AtendimentoService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Unicode)
    def registrar_solicitacao(ctx, usuario, descricao):
        """Registra uma nova solicitação de atendimento."""
        new_id = max(solicitacoes_db.keys()) + 1 if solicitacoes_db else 1
        solicitacoes_db[new_id] = {
            "usuario": usuario,
            "descricao": descricao,
            "status": "Pendente"
        }
        return f"Solicitação {new_id} registrada com sucesso para o usuário {usuario}."

    @rpc(Integer, _returns=Unicode)
    def consultar_status(ctx, id_solicitacao):
        """Consulta o status de uma solicitação pelo ID."""
        solicitacao = solicitacoes_db.get(id_solicitacao)
        if solicitacao:
            return f"Status da solicitação {id_solicitacao}: {solicitacao['status']}"
        return f"Solicitação {id_solicitacao} não encontrada."

    @rpc(Unicode, _returns=Array(Unicode))
    def listar_atendimentos(ctx, usuario):
        """Lista as descrições de todos os atendimentos de um usuário."""
        atendimentos = [
            f"ID {id}: {info['descricao']} ({info['status']})"
            for id, info in solicitacoes_db.items()
            if info['usuario'] == usuario
        ]
        if not atendimentos:
            return [f"Nenhum atendimento encontrado para o usuário {usuario}."]
        return atendimentos

application = Application(
    [AtendimentoService],
    tns='http://uern.br/atendimento',
    in_protocol=Soap11(validator='soft'),
    out_protocol=Soap11()
)

wsgi_app = WsgiApplication(application)

if __name__ == '__main__':
    print("Servidor SOAP rodando em http://0.0.0.0:8000")
    print("WSDL disponível em http://0.0.0.0:8000/?wsdl")
    run_simple('0.0.0.0', 8000, wsgi_app)
