# Memorial Descritivo de Arquitetura: Serviço de Atendimento SOAP

Este repositório hospeda a implementação de um Sistema de Atendimento Corporativo baseado nos padrões de **Arquitetura Orientada a Serviços (SOA)**, utilizando o protocolo **SOAP (Simple Object Access Protocol)**. O projeto atua como um barramento de serviços robusto, integrando persistência relacional, segurança em nível de mensagem e auditoria automatizada.

---

## 🏛️ 1. Decisões de Engenharia e Infraestrutura

### ⚠️ Justificativa de Arquitetura: Downgrade Estratégico do Interpretador (Python 3.10)
Diferente do ecossistema REST/JSON moderno, o protocolo SOAP corporativo em Python baseia-se em engines maduras de parsing e serialização, especificamente o framework **Spyne** e o motor analítico **lxml** (escrito em C). 

Durante a fase de design de infraestrutura, identificou-se que as versões mais recentes do interpretador Python (3.11, 3.12 e superiores) apresentam quebras de retrocompatibilidade de binários na compilação do `lxml` em ambiente Windows, resultando em falhas críticas de Linkagem Dinâmica (DLLs) e corrupção de memória. 

A equipe de desenvolvimento adotou o **downgrade estratégico para o Python 3.10**. Esta decisão de engenharia garantiu:
1. **Estabilidade Absoluta:** Geração dinâmica resiliente do contrato formal WSDL sem estouro de pilha.
2. **Conformidade de Esquema:** Validação rigorosa de tipos complexos no XML Schema (XSD).
3. **Determinismo na Instalação:** Compilação limpa de pacotes nativos diretamente pelo gerenciador de pacotes (`pip`).

### 📦 Isolamento de Escopo Local (.venv)
Para mitigar o problema global conhecido como *"Dependency Hell"* (conflitos de versões de bibliotecas globais no sistema operacional), o projeto adota um **Ambiente Virtual Isolado (`.venv`)**. Toda a árvore de dependências, interpretadores locais e scripts de ativação e segurança da aplicação ficam encapsulados neste diretório, garantindo a portabilidade estrita do ecossistema.

---

## 📂 2. Árvore de Diretórios do Ecossistema

O projeto foi desacoplado seguindo o princípio de separação de conceitos (*Separation of Concerns*):

```text
Projeto_SOA_Atendimento/
│
├── database/
│   ├── __init__.py
│   ├── connection.py####### Camada de Conexão: Engine SQLAlchemy e gerenciador SessionLocal
│   └── models.py########### Camada de Modelo: Mapeamento ORM da tabela 'solicitacoes' (MySQL)
│
├── client/
│   └── soap_client.py###### Script cliente automatizado para testes rápidos de integração
│
├── .gitignore############## Filtro de segurança: Impede vazamento de logs e binários locais (.venv)
├── README.md############### Documentação técnica institucional (Este arquivo)
├── servidor_soap.log####### Sistema de Auditoria: Logs persistidos em tempo real
└── soap_service.py######### Core Application: Servidor SOAP, Endpoints CRUD e Middleware de Segurança

🚀 3. Manual de Deploy Local e Inicialização
Siga rigorosamente as instruções abaixo para instanciar o ambiente e inicializar o servidor de barramento.

Passo 1: Posicionamento no Diretório Raiz
Abra o terminal do seu ambiente de desenvolvimento (PowerShell preferencialmente) e navegue até a raiz do projeto:

PowerShell
cd C:\Users\franc\OneDrive\Documentos\MeuProjetos\Projeto_SOA_Atendimento
Passo 2: Reconstrução e Saneamento do Ambiente Virtual
Caso seu ambiente virtual (.venv) esteja ausente, corrompido ou com a pasta Scripts vazia devido a divergências de sincronismo de branches do Git, limpe o resíduo e recrie a estrutura do zero executando:

PowerShell
# Remove resquícios corrompidos de forma forçada se necessário
Remove-Item -Recurse -Force .venv -ErrorAction SilentlyContinue

# Instancia uma nova estrutura limpa isolada com Python 3.10
python -m venv .venv
Passo 3: Ativação do Escopo de Contexto (.venv)
Selecione o comando adequado com base no interpretador de linha de comando utilizado no seu terminal:

No Windows (PowerShell - Padrão do VS Code):

PowerShell
.\.venv\Scripts\Activate.ps1
Nota de Contingência: Caso o Windows bloqueie a execução por diretivas restritivas de execução da máquina, contorne via:

PowerShell
powershell -ExecutionPolicy Bypass -File .\.venv\Scripts\Activate.ps1
No Windows (Prompt de Comando - CMD Tradicional):

DOS
.venv\Scripts\activate.bat
🔍 Indicador de Sucesso: A linha de comando do seu terminal deve obrigatoriamente exibir o prefixo (.venv) antes do caminho do diretório.

Passo 4: Instalação Descritiva de Dependências
Com o contexto (.venv) devidamente ativo, realize a ingestão dos pacotes necessários:

PowerShell
pip install spyne sqlalchemy pymysql cryptography werkzeug lxml zeep
Passo 5: Inicialização do Servidor de Barramento
Execute o script principal:

PowerShell
python soap_service.py
O framework SQLAlchemy invocará o banco de dados MySQL (soa_atendimento), validará a integridade estrutural e criará de forma transparente a tabela caso ela não exista. O servidor passará a escutar requisições de forma síncrona na porta 8000.

📝 4. Rastreabilidade de Requisitos de Negócio (Checklist Acadêmico)
4.1 Implementação do Serviço SOAP (Requisito 4.1)
Contrato Formal: O contrato WSDL é gerado dinamicamente em tempo de execução e exposto na URL: http://localhost:8000/?wsdl

Definição de Tipos (XSD): Dados fortemente tipados mapeados no XML Schema via estruturas complexas do Spyne (SolicitacaoModel), utilizando tipos primitivos como Integer e Unicode.

Persistência Relacional (CRUD Completo): Integração via ORM mapeando as 4 operações de ciclo de vida do dado:

criar_solicitacao (Create) -> Insere novos registros com status padrão "Pendente".

consultar_solicitacao (Read) -> Captura e serializa dados filtrados por ID.

atualizar_status (Update) -> Altera o estado do ciclo do chamado no MySQL.

deletar_solicitacao (Delete) -> Remove fisicamente o registro da base de dados.

4.2 Documentação do Serviço (Requisito 4.2)
O serviço encontra-se auto-documentado através de metadados nativos expostos na especificação técnica do WSDL. Ferramentas de mercado como o SoapUI são capazes de interpretar o link e gerar automaticamente toda a estrutura visual de payloads suportados pelo barramento.

4.3 Segurança de Mensagem - WS-Security (Requisito 4.3)
Injeção de SOAP Headers: O barramento não aceita chamadas anônimas. Toda requisição precisa conter obrigatoriamente no envelope XML o bloco <soapenv:Header> encapsulando o objeto complexo AuthHeader (composto pelas chaves <username> e <password>).

Interceptação e Validação: Um validador intercepta as requisições antes de chegarem à camada de banco de dados. Credenciais inválidas (diferentes de admin / Root@123456) abortam a execução imediatamente, devolvendo ao chamador uma mensagem de erro padronizada no elemento <soap:Fault>.

4.4 Massa de Testes e Evidências (Requisito 4.4)
O barramento está homologado para testes nas principais ferramentas de API do mercado:

SoapUI / Postman: Permite validar cenários de sucesso (persistência de dados confirmada na tabela do MySQL) e cenários de falha (injeção de credenciais incorretas simulando tentativas de invasão, retornando erro HTTP 500 controlado).

4.5 Mecanismos de Logs e Auditoria (Requisito 4.5)
O ecossistema implementa gravação em modo contínuo usando o módulo nativo logging do Python.

Todas as interações críticas do sistema (inicialização de tabelas, chamadas do CRUD de sucesso, deleções e, crucialmente, erros de autenticação barrados) são registradas cronologicamente com carimbo de data/hora no arquivo físico servidor_soap.log, servindo como evidência de auditoria exigida para o relatório.

✉️ 5. Template de Payload XML para Validação (Postman / SoapUI)
Para disparar requisições manuais ao servidor, configure o método como POST, aponte para http://localhost:8000/, inclua o cabeçalho HTTP Content-Type: text/xml; charset=utf-8 e injete o seguinte envelope XML:

XML
<soapenv:Envelope xmlns:soapenv="[http://schemas.xmlsoap.org/soap/envelope/](http://schemas.xmlsoap.org/soap/envelope/)"
                  xmlns:aten="spyne.examples.atendimento">
   <soapenv:Header>
      <aten:AuthHeader>
         <aten:username>admin</aten:username>
         <aten:password>Root@123456</aten:password>
      </aten:AuthHeader>
   </soapenv:Header>
   <soapenv:Body>
      <aten:criar_solicitacao>
         <aten:usuario>Francisco Fernandes - DevSenior</aten:usuario>
         <aten:descricao>Teste homologado de barramento arquitetural SOA.</aten:descricao>
      </aten:criar_solicitacao>
   </soapenv:Body>
</soapenv:Envelope>