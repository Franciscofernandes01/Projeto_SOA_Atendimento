# Arquivo: soap_client.py (Refatorado)
import requests
import logging

# Configuração simples de log para o client
logging.basicConfig(level=logging.INFO)
client_logger = logging.getLogger("SOAPClient")

def test_soap_service():
    url = "http://localhost:8000/"
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    
    # Token fixo definido no servidor
    VALID_TOKEN = "TOKEN_SUPER_SECRETO_123"

    # ==========================================
    # Exemplo 1: Registrar (Sucesso - COM Header)
    # ==========================================
    payload_registrar_sucesso = f"""<?xml version="1.0" encoding="UTF-8"?>
    <soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://uern.br/atendimento">
        <soap11env:Header>
            <tns:AuthHeader>
                <tns:token>{VALID_TOKEN}</tns:token>
            </tns:AuthHeader>
        </soap11env:Header>
        <soap11env:Body>
            <tns:registrar_solicitacao>
                <tns:solicitacao>
                    <tns:usuario>eduardo</tns:usuario>
                    <tns:descricao>Solicitação de troca de equipamento.</tns:descricao>
                </tns:solicitacao>
            </tns:registrar_solicitacao>
        </soap11env:Body>
    </soap11env:Envelope>"""
    
    client_logger.info("--- Testando registrar_solicitacao (Sucesso) ---")
    response = requests.post(url, data=payload_registrar_sucesso, headers=headers)
    print("\nResponse Status:", response.status_code)
    print("Response Content:\n", response.text)
    
    # ==========================================
    # Exemplo 2: Registrar (Falha - SEM Header)
    # ==========================================
    payload_registrar_falha_sem_header = """<?xml version="1.0" encoding="UTF-8"?>
    <soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://uern.br/atendimento">
        <soap11env:Body>
            <tns:registrar_solicitacao>
                <tns:solicitacao>
                    <tns:usuario>hacker</tns:usuario>
                    <tns:descricao>Acesso não autorizado.</tns:descricao>
                </tns:solicitacao>
            </tns:registrar_solicitacao>
        </soap11env:Body>
    </soap11env:Envelope>"""
    
    client_logger.info("\n--- Testando registrar_solicitacao (Falha: Sem Header) ---")
    response = requests.post(url, data=payload_registrar_falha_sem_header, headers=headers)
    # Esperamos um erro SOAP (status 500)
    print("\nResponse Status (Expected 500):", response.status_code) 
    print("Response Content:\n", response.text)

    # ==========================================
    # Exemplo 3: Consultar (Operação Pública)
    # ==========================================
    payload_consultar = """<?xml version="1.0" encoding="UTF-8"?>
    <soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://uern.br/atendimento">
        <soap11env:Body>
            <tns:consultar_status>
                <tns:id_solicitacao>1</tns:id_solicitacao>
            </tns:consultar_status>
        </soap11env:Body>
    </soap11env:Envelope>"""
    
    client_logger.info("\n--- Testando consultar_status ---")
    response = requests.post(url, data=payload_consultar, headers=headers)
    print("\nResponse Status:", response.status_code)
    print("Response Content:\n", response.text)

if __name__ == "__main__":
    test_soap_service()