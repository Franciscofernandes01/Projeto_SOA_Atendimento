import requests

def test_soap_service():
    url = "http://localhost:8000/"
    
    # Exemplo 1: Registrar Solicitação
    payload_registrar = """<?xml version="1.0" encoding="UTF-8"?>
    <soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://uern.br/atendimento">
        <soap11env:Body>
            <tns:registrar_solicitacao>
                <tns:usuario>carlos</tns:usuario>
                <tns:descricao>Troca de senha</tns:descricao>
            </tns:registrar_solicitacao>
        </soap11env:Body>
    </soap11env:Envelope>"""
    
    print("--- Testando registrar_solicitacao ---")
    headers = {'Content-Type': 'text/xml; charset=utf-8'}
    response = requests.post(url, data=payload_registrar, headers=headers)
    print("Request Payload:\n", payload_registrar)
    print("\nResponse Status:", response.status_code)
    print("Response Content:\n", response.text)
    
    # Exemplo 2: Consultar Status
    payload_consultar = """<?xml version="1.0" encoding="UTF-8"?>
    <soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://uern.br/atendimento">
        <soap11env:Body>
            <tns:consultar_status>
                <tns:id_solicitacao>1</tns:id_solicitacao>
            </tns:consultar_status>
        </soap11env:Body>
    </soap11env:Envelope>"""
    
    print("\n--- Testando consultar_status ---")
    response = requests.post(url, data=payload_consultar, headers=headers)
    print("Request Payload:\n", payload_consultar)
    print("\nResponse Status:", response.status_code)
    print("Response Content:\n", response.text)

    # Exemplo 3: Listar Atendimentos
    payload_listar = """<?xml version="1.0" encoding="UTF-8"?>
    <soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://uern.br/atendimento">
        <soap11env:Body>
            <tns:listar_atendimentos>
                <tns:usuario>joao</tns:usuario>
            </tns:listar_atendimentos>
        </soap11env:Body>
    </soap11env:Envelope>"""
    
    print("\n--- Testando listar_atendimentos ---")
    response = requests.post(url, data=payload_listar, headers=headers)
    print("Request Payload:\n", payload_listar)
    print("\nResponse Status:", response.status_code)
    print("Response Content:\n", response.text)

if __name__ == "__main__":
    test_soap_service()
