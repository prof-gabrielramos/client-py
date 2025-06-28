# 📱 Cliente Python para SMS Gateway for Android™

[![PyPI version](https://badge.fury.io/py/android-sms-gateway.svg)](https://badge.fury.io/py/android-sms-gateway)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

Um cliente Python moderno e robusto para integração transparente com a API do [SMS Gateway for Android](https://sms-gate.app). Envie mensagens SMS programaticamente por meio de seus dispositivos Android com esta biblioteca poderosa, tipada e fácil de usar.

## ✨ Funcionalidades

- 🚀 **Cliente Duplo**: Suporte a interfaces síncronas (`APIClient`) e assíncronas (`AsyncAPIClient`)
- 🔒 **Criptografia de Ponta a Ponta**: Criptografia opcional de mensagens usando AES-CBC-256
- 🌐 **Múltiplos Backends HTTP**: Suporte nativo a `requests`, `aiohttp` e `httpx`
- 🔗 **Gestão de Webhooks**: Crie, consulte e exclua webhooks programaticamente
- ⚙️ **URL Base Personalizável**: Aponte para diferentes endpoints da API
- 📝 **Type Hinting Completo**: Totalmente tipado para melhor experiência de desenvolvimento
- 🛡️ **Tratamento de Erros Robusto**: Exceções específicas e mensagens de erro claras
- 📊 **Relatórios de Entrega**: Acompanhe o status de entrega das suas mensagens

## 📋 Índice

- [📱 Cliente Python para SMS Gateway for Android™](#-cliente-python-para-sms-gateway-for-android)
  - [✨ Funcionalidades](#-funcionalidades)
  - [📋 Índice](#-índice)
  - [⚙️ Requisitos](#️-requisitos)
  - [📦 Instalação](#-instalação)
  - [🚀 Primeiros Passos](#-primeiros-passos)
  - [🤖 Guia do Cliente](#-guia-do-cliente)
  - [🌐 Clientes HTTP](#-clientes-http)
  - [🔒 Segurança](#-segurança)
  - [📚 Documentação](#-documentação)
  - [🧪 Testes](#-testes)
  - [👥 Contribuindo](#-contribuindo)
  - [📄 Licença](#-licença)

## ⚙️ Requisitos

- **Python**: 3.9 ou superior
- **Cliente HTTP** (escolha um):
  - 🚀 [requests](https://pypi.org/project/requests/) (síncrono)
  - ⚡ [aiohttp](https://pypi.org/project/aiohttp/) (assíncrono)
  - 🌈 [httpx](https://pypi.org/project/httpx/) (síncrono + assíncrono)

**Dependências Opcionais**:
- 🔒 [pycryptodome](https://pypi.org/project/pycryptodome/) - Para suporte à criptografia ponta a ponta

## 📦 Instalação

### Instalação Básica

```bash
pip install android-sms-gateway
```

### Instalação com Cliente HTTP Específico

```bash
# Escolha um cliente HTTP:
pip install android-sms-gateway[requests]    # Para uso síncrono
pip install android-sms-gateway[aiohttp]     # Para uso assíncrono
pip install android-sms-gateway[httpx]       # Para uso síncrono e assíncrono
```

### Instalação com Criptografia

```bash
# Para mensagens criptografadas:
pip install android-sms-gateway[encryption]

# Ou instale tudo:
pip install android-sms-gateway[requests,encryption]
```

### Instalação para Desenvolvimento

```bash
git clone https://github.com/android-sms-gateway/client-py.git
cd client-py
pip install -e ".[dev,requests,encryption]"
```

## 🚀 Primeiros Passos

### Configuração Inicial

1. **Configure suas credenciais**:
   ```bash
   export ANDROID_SMS_GATEWAY_LOGIN="seu_usuario"
   export ANDROID_SMS_GATEWAY_PASSWORD="sua_senha"
   ```

2. **Exemplo básico de uso**:

```python
import asyncio
import os
from android_sms_gateway import client, domain

# Configuração
login = os.getenv("ANDROID_SMS_GATEWAY_LOGIN")
password = os.getenv("ANDROID_SMS_GATEWAY_PASSWORD")

# Criação da mensagem
message = domain.Message(
    "Olá! Esta é uma mensagem de teste.",
    ["+5511999999999"],
    with_delivery_report=True
)

# Cliente Síncrono
def exemplo_sincrono():
    with client.APIClient(login, password) as c:
        # Envia a mensagem
        state = c.send(message)
        print(f"Mensagem enviada com ID: {state.id}")
        
        # Consulta o status
        status = c.get_state(state.id)
        print(f"Status: {status.state}")

# Cliente Assíncrono
async def exemplo_assincrono():
    async with client.AsyncAPIClient(login, password) as c:
        # Envia a mensagem
        state = await c.send(message)
        print(f"Mensagem enviada com ID: {state.id}")
        
        # Consulta o status
        status = await c.get_state(state.id)
        print(f"Status: {status.state}")

if __name__ == "__main__":
    print("=== Exemplo Síncrono ===")
    exemplo_sincrono()
    
    print("\n=== Exemplo Assíncrono ===")
    asyncio.run(exemplo_assincrono())
```

### Exemplo com Criptografia

```python
from android_sms_gateway import client, domain, Encryptor

# Configuração de criptografia
encryptor = Encryptor("minha-frase-secreta-super-segura")

# Mensagem criptografada
message = domain.Message(
    "Esta mensagem será criptografada!",
    ["+5511999999999"],
    is_encrypted=True
)

# Cliente com criptografia
with client.APIClient(login, password, encryptor=encryptor) as c:
    state = c.send(message)
    print(f"Mensagem criptografada enviada: {state.id}")
```

## 🤖 Guia do Cliente

### Configuração do Cliente

Ambos os clientes (`APIClient` e `AsyncAPIClient`) suportam os seguintes parâmetros:

| Parâmetro   | Tipo                | Descrição                           | Padrão                                    |
|-------------|---------------------|-------------------------------------|-------------------------------------------|
| `login`     | `str`               | Usuário da API                      | **Obrigatório**                           |
| `password`  | `str`               | Senha da API                        | **Obrigatório**                           |
| `base_url`  | `str`               | URL base da API                     | `"https://api.sms-gate.app/3rdparty/v1"`  |
| `encryptor` | `Encryptor`         | Instância para criptografia         | `None`                                    |
| `http`      | `HttpClient`        | Cliente HTTP customizado            | Detectado automaticamente                 |

### Métodos Disponíveis

| Método                                           | Descrição                    | Retorno                   |
|--------------------------------------------------|------------------------------|---------------------------|
| `send(message: domain.Message)`                  | Envia uma mensagem SMS       | `domain.MessageState`     |
| `get_state(id: str)`                             | Consulta o estado da mensagem| `domain.MessageState`     |
| `create_webhook(webhook: domain.Webhook)`        | Cria um novo webhook         | `domain.Webhook`          |
| `get_webhooks()`                                 | Lista todos os webhooks      | `List[domain.Webhook]`    |
| `delete_webhook(id: str)`                        | Exclui um webhook            | `None`                    |

### Estruturas de Dados

#### Message
```python
class Message:
    message: str                    # Texto da mensagem
    phone_numbers: List[str]        # Lista de números de telefone
    with_delivery_report: bool = True  # Relatório de entrega
    is_encrypted: bool = False      # Se a mensagem é criptografada
    
    # Campos opcionais
    id: Optional[str] = None        # ID da mensagem
    ttl: Optional[int] = None       # Time-to-live em segundos
    sim_number: Optional[int] = None # Número do SIM
```

#### MessageState
```python
class MessageState:
    id: str                         # ID único da mensagem
    state: ProcessState             # Estado atual (SENT, DELIVERED, etc.)
    recipients: List[RecipientState] # Status por destinatário
    is_hashed: bool                 # Se a mensagem foi hasheada
    is_encrypted: bool              # Se a mensagem foi criptografada
```

#### Webhook
```python
class Webhook:
    id: Optional[str]               # ID do webhook
    url: str                        # URL de callback
    event: WebhookEvent             # Tipo de evento
```

Para mais detalhes, consulte [`domain.py`](./android_sms_gateway/domain.py).

## 🌐 Clientes HTTP

A biblioteca detecta automaticamente os clientes HTTP instalados com a seguinte prioridade:

| Cliente   | Síncrono | Assíncrono | Prioridade |
|-----------|----------|------------|------------|
| aiohttp   | ❌       | 1️⃣         | Assíncrono |
| requests  | 1️⃣       | ❌         | Síncrono   |
| httpx     | 2️⃣       | 2️⃣         | Universal  |

### Uso de Cliente Específico

```python
from android_sms_gateway import http

# Forçar uso do httpx
client.APIClient(..., http=http.HttpxHttpClient())

# Forçar uso do requests
client.APIClient(..., http=http.RequestsHttpClient())

# Forçar uso do aiohttp (apenas assíncrono)
async with client.AsyncAPIClient(..., http=http.AiohttpHttpClient()) as c:
    # ...
```

### Cliente HTTP Customizado

Você pode implementar seu próprio cliente HTTP seguindo os protocolos `http.HttpClient` ou `ahttp.HttpClient`.

## 🔒 Segurança

### Boas Práticas

⚠️ **IMPORTANTE**: Sempre siga estas práticas de segurança:

- 🔐 **Credenciais**: Armazene credenciais em variáveis de ambiente
- 🚫 **Código**: Nunca exponha credenciais em código do lado do cliente
- 🔒 **HTTPS**: Use HTTPS para todas as comunicações em produção
- 🔑 **Criptografia**: Use criptografia ponta a ponta para mensagens sensíveis
- 🔄 **Rotação**: Troque suas credenciais regularmente

### Exemplo de Configuração Segura

```python
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração segura
login = os.getenv("ANDROID_SMS_GATEWAY_LOGIN")
password = os.getenv("ANDROID_SMS_GATEWAY_PASSWORD")

if not login or not password:
    raise ValueError("Credenciais não configuradas!")
```

## 📦 Executando com Docker (Interface Web)

A interface web `sms-gateway-web` pode ser facilmente executada usando Docker e Docker Compose.

1.  **Navegue até o diretório `sms-gateway-web`**:
    ```bash
    cd sms-gateway-web
    ```

2.  **Construa e execute o container Docker**:
    ```bash
    docker-compose up --build
    ```
    A interface web estará acessível em `http://localhost:5000`.

    Para executar em segundo plano (detached mode):
    ```bash
    docker-compose up --build -d
    ```

3.  **Parar os containers**:
    ```bash
    docker-compose down
    ```

A configuração e o banco de dados da interface web são persistidos no volume `./config` dentro do diretório `sms-gateway-web`, que é montado em `/root/.sms-gateway-web` no container.

## 🚀 Deploy

Consulte a documentação completa para guias detalhados de deploy:
- **[Documentação de Deploy](./docs/deployment.md)** (Será criada com MkDocs)

Brevemente:

### Coolify
- Configure seu projeto no Coolify apontando para este repositório.
- Use o `sms-gateway-web/Dockerfile` e `sms-gateway-web/docker-compose.yml` como base para a configuração do serviço.
- Certifique-se de configurar as variáveis de ambiente necessárias e o mapeamento de volumes persistentes.

### VPS com Portainer + Traefik
1.  **Prepare sua VPS**: Instale Docker, Docker Compose, Portainer e Traefik.
2.  **Configure o Traefik**: Para lidar com SSL e roteamento de domínio.
3.  **Clone o repositório na VPS**.
4.  **Use Portainer para adicionar um novo "Stack"**:
    *   Aponte para o arquivo `sms-gateway-web/docker-compose.yml`.
    *   Ajuste as `labels` do Traefik no `docker-compose.yml` para seu domínio.
    *   Configure as variáveis de ambiente e volumes conforme necessário.
5.  **Deploy o Stack**.

## 📚 Documentação Completa (MkDocs)

Uma documentação mais detalhada e navegável está disponível (ou será criada em breve) usando MkDocs. Para visualizar:

1.  **Instale MkDocs e o tema Material**:
    ```bash
    pip install mkdocs mkdocs-material
    ```
2.  **Construa e sirva a documentação**:
    ```bash
    mkdocs serve
    ```
    Acesse em `http://localhost:8000`.

### Documentação da API (Cliente Python)

Para documentação completa da API do cliente Python, incluindo todos os métodos disponíveis, esquemas de requisição/resposta e códigos de erro, acesse:

📘 **[Documentação Oficial da API SMS Gateway](https://docs.sms-gate.app/integration/api/)**

### Documentação da Biblioteca Cliente Python

- 📖 [Guia de Instalação](https://docs.sms-gate.app/integration/python/)
- 🔐 [Guia de Criptografia](https://docs.sms-gate.app/privacy/encryption/)
- 🌐 [Exemplos de Uso](https://docs.sms-gate.app/integration/python/examples/)

## 🧪 Testes

### Executando os Testes

```bash
# Instalar dependências de teste
pip install -e ".[dev]"

# Executar todos os testes
pytest

# Executar com cobertura
pytest --cov=android_sms_gateway --cov-report=html

# Executar testes específicos
pytest tests/test_client.py
```

### Qualidade do Código

```bash
# Verificação de estilo
flake8 android_sms_gateway tests
black --check android_sms_gateway tests
isort --check-only android_sms_gateway tests

# Verificação de tipos
mypy android_sms_gateway
```

## 👥 Contribuindo

Contribuições são muito bem-vindas! 🎉

### Como Contribuir

1. 🍴 Faça um fork do repositório
2. 🌿 Crie sua branch de funcionalidade (`git checkout -b feature/NovaFuncionalidade`)
3. 💾 Faça commit das suas alterações (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. 📤 Faça push para a branch (`git push origin feature/NovaFuncionalidade`)
5. 🔄 Abra um Pull Request

### Padrões de Commit

Seguimos o padrão [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Documentação
- `style:` Formatação de código
- `refactor:` Refatoração
- `test:` Testes
- `chore:` Tarefas de manutenção

### Ambiente de Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/android-sms-gateway/client-py.git
cd client-py

# Configure o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instale dependências
pip install -e ".[dev,requests,encryption]"

# Configure pre-commit hooks
pre-commit install
```

### Checklist para Pull Requests

- [ ] Código segue os padrões de estilo (black, isort, flake8)
- [ ] Testes passam localmente
- [ ] Documentação foi atualizada
- [ ] Commits seguem o padrão Conventional Commits
- [ ] Cobertura de testes mantida ou melhorada

## 📄 Licença

Este projeto está licenciado sob a **Licença Apache 2.0** - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🤝 Suporte

- 📧 **Email**: [suporte@sms-gate.app](mailto:suporte@sms-gate.app)
- 💬 **Discord**: [Comunidade SMS Gateway](https://discord.gg/sms-gateway)
- 📖 **Documentação**: [docs.sms-gate.app](https://docs.sms-gate.app)
- 🐛 **Issues**: [GitHub Issues](https://github.com/android-sms-gateway/client-py/issues)

---

**Nota**: Android é uma marca registrada da Google LLC. Este projeto não é afiliado nem endossado pela Google.
![CodeRabbit Pull Request Reviews](https://img.shields.io/coderabbit/prs/github/prof-gabrielramos/client-py?utm_source=oss&utm_medium=github&utm_campaign=prof-gabrielramos%2Fclient-py&labelColor=171717&color=FF570A&link=https%3A%2F%2Fcoderabbit.ai&label=CodeRabbit+Reviews)