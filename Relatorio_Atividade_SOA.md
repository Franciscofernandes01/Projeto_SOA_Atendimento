# Relatório de Atividade: Programação Orientada a Serviços (UERN)

Este documento apresenta a modelagem e implementação de um sistema orientado a serviços (SOA) utilizando Web Services SOAP, conforme os requisitos da Unidade 1 da disciplina.

## 1. Estudo de Caso

O sistema escolhido para este trabalho é um **Sistema de Atendimento e Solicitações**. O objetivo é permitir que usuários registrem problemas ou solicitações, consultem o status de seus chamados e listem todos os seus atendimentos vinculados.

| Ator | Papel no Sistema |
| :--- | :--- |
| **Usuário** | Registra novas solicitações e consulta o andamento de seus atendimentos. |
| **Sistema de Atendimento** | Web Service SOAP que processa as requisições e gerencia os dados das solicitações. |

## 2. Modelagem do Sistema

A arquitetura segue o padrão SOA, onde o serviço é exposto via protocolo HTTP utilizando mensagens XML formatadas conforme o padrão SOAP 1.1.

### Serviços e Operações

O serviço de atendimento expõe as seguintes operações lógicas:

1.  **registrar_solicitacao**: Recebe o nome do usuário e a descrição do problema, retornando uma confirmação com o ID gerado.
2.  **consultar_status**: Recebe o ID de uma solicitação e retorna o status atual (ex: Pendente, Em andamento).
3.  **listar_atendimentos**: Recebe o nome do usuário e retorna uma lista de todas as suas solicitações registradas.

## 3. Especificação do Contrato (WSDL)

O contrato do serviço define os tipos de dados, as mensagens e os endpoints. Abaixo, destaca-se a estrutura principal do WSDL gerado automaticamente pelo framework Spyne.

> O WSDL completo pode ser acessado na URL do serviço em execução (`/?wsdl`).

### Trecho do Contrato (Tipos e Mensagens)

```xml
<wsdl:message name="registrar_solicitacao">
    <wsdl:part name="registrar_solicitacao" element="tns:registrar_solicitacao"/>
</wsdl:message>
<wsdl:portType name="Application">
    <wsdl:operation name="registrar_solicitacao">
        <wsdl:input message="tns:registrar_solicitacao"/>
        <wsdl:output message="tns:registrar_solicitacaoResponse"/>
    </wsdl:operation>
</wsdl:portType>
```

## 4. Exemplos de Mensagens SOAP

Abaixo estão exemplos reais de requisições e respostas capturadas durante os testes do serviço.

### Registrar Solicitação (Request)
```xml
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://uern.br/atendimento">
    <soap11env:Body>
        <tns:registrar_solicitacao>
            <tns:usuario>carlos</tns:usuario>
            <tns:descricao>Troca de senha</tns:descricao>
        </tns:registrar_solicitacao>
    </soap11env:Body>
</soap11env:Envelope>
```

### Registrar Solicitação (Response)
```xml
<soap11env:Envelope xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://uern.br/atendimento">
    <soap11env:Body>
        <tns:registrar_solicitacaoResponse>
            <tns:registrar_solicitacaoResult>Solicitação 3 registrada com sucesso para o usuário carlos.</tns:registrar_solicitacaoResult>
        </tns:registrar_solicitacaoResponse>
    </soap11env:Body>
</soap11env:Envelope>
```

## 5. Testes Realizados

Os testes foram conduzidos utilizando um script cliente em Python que realiza chamadas HTTP POST enviando envelopes SOAP para o endpoint `http://localhost:8000/`.

1.  **Teste de Registro**: Validou-se que o sistema incrementa o ID corretamente e armazena os dados.
2.  **Teste de Consulta**: Verificou-se que o status retornado condiz com o ID solicitado.
3.  **Teste de Listagem**: Confirmou-se que o retorno é um array de strings contendo os detalhes dos atendimentos do usuário.

## 6. Instruções de Execução

### Requisitos de Ambiente
- Python 3.8 ou superior.
- Bibliotecas: `spyne`, `werkzeug`, `requests`.

### Passos para Executar
1. Instale as dependências: `pip install spyne werkzeug`.
2. Execute o servidor: `python soap_service.py`.
3. O serviço estará disponível em `http://localhost:8000/`.
4. O WSDL pode ser visualizado em `http://localhost:8000/?wsdl`.

### Passos para Consumir
- Utilize o script `soap_client.py` fornecido ou qualquer ferramenta de teste SOAP (como SoapUI ou Postman).
