# Guia do Desenvolvedor - Android SMS Gateway Python Client

## 📋 Índice
- [1. Instruções de Configuração](#1-instruções-de-configuração)
- [2. Visão Geral da Estrutura do Projeto](#2-visão-geral-da-estrutura-do-projeto)
- [3. Fluxo de Trabalho de Desenvolvimento](#3-fluxo-de-trabalho-de-desenvolvimento)
- [4. Abordagem de Testes](#4-abordagem-de-testes)
- [5. Etapas Comuns de Solução de Problemas](#5-etapas-comuns-de-solução-de-problemas)

---

## 1. Instruções de Configuração

### 1.1 Requisitos do Sistema

**Hardware/Software:**
- Python 3.9 ou superior
- Git 2.0+
- Mínimo 100MB de espaço livre
- Conexão com internet para dependências

**Sistemas Operacionais Suportados:**
- Windows 10+
- macOS 10.15+
- Linux (Ubuntu 18.04+, CentOS 7+)

### 1.2 Configuração Passo a Passo

#### Passo 1: Clone o Repositório
```bash
git clone https://github.com/android-sms-gateway/client-py.git
cd client-py
```

#### Passo 2: Instale o Pipenv
```bash
# No Linux/macOS
python3 -m pip install --user pipenv

# No Windows
python -m pip install --user pipenv
```

#### Passo 3: Configure o Ambiente Virtual
```bash
# Instala todas as dependências de desenvolvimento
pipenv install --dev --categories encryption,requests,httpx,aiohttp

# Ativa o ambiente virtual
pipenv shell
```

#### Passo 4: Configure Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:
```bash
# Credenciais para testes (opcional)
API_LOGIN=seu_login_aqui
API_PASSWORD=sua_senha_aqui
API_BASE_URL=https://api.sms-gate.app/3rdparty/v1

# Configurações de desenvolvimento
PYTHONPATH=.
```

#### Passo 5: Verifique a Instalação
```bash
# Execute os testes para verificar se tudo está funcionando
pipenv run pytest tests/

# Verifique o linting
pipenv run flake8 android_sms_gateway tests
```

### 1.3 Resolução de Problemas Comuns

**Problema: Erro de permissão ao instalar pipenv**
```bash
# Solução: Use --user flag
python -m pip install --user pipenv
```

**Problema: Pipenv não encontrado após instalação**
```bash
# Adicione ao PATH (Linux/macOS)
export PATH="$HOME/.local/bin:$PATH"

# Windows - Adicione manualmente às variáveis de ambiente
```

**Problema: Falha na instalação de pycryptodome**
```bash
# Linux/macOS - Instale dependências do sistema
sudo apt-get install python3-dev build-essential  # Ubuntu
brew install python3  # macOS

# Windows - Instale Visual C++ Build Tools
```

---

## 2. Visão Geral da Estrutura do Projeto

### 2.1 Estrutura de Diretórios

```
android-sms-gateway-client-py/
├── .github/                    # Configurações do GitHub Actions
│   └── workflows/
│       ├── close-issues.yml    # Automação para fechar issues
│       ├── publish.yml         # Pipeline de publicação no PyPI
│       └── testing.yml         # Pipeline de testes automatizados
├── android_sms_gateway/        # Código principal da biblioteca
│   ├── __init__.py            # Exportações públicas da API
│   ├── ahttp.py               # Cliente HTTP assíncrono
│   ├── client.py              # Clientes API (sync/async)
│   ├── constants.py           # Constantes globais (versão, URLs)
│   ├── domain.py              # Modelos de dados e DTOs
│   ├── encryption.py          # Funcionalidades de criptografia
│   ├── enums.py               # Enumerações (estados, eventos)
│   └── http.py                # Cliente HTTP síncrono
├── tests/                     # Suite de testes
│   ├── test_client.py         # Testes dos clientes API
│   ├── test_domain.py         # Testes dos modelos de dados
│   └── test_encryption.py     # Testes de criptografia
├── .flake8                    # Configuração do linter
├── .gitignore                 # Arquivos ignorados pelo Git
├── .isort.cfg                 # Configuração de ordenação de imports
├── LICENSE                    # Licença Apache 2.0
├── Makefile                   # Comandos automatizados
├── Pipfile                    # Dependências do projeto
├── pyproject.toml             # Configuração de build e metadados
└── README.md                  # Documentação principal
```

### 2.2 Componentes Principais

#### 2.2.1 Módulo `client.py` - Core da API
**Responsabilidades:**
- Implementa `APIClient` (síncrono) e `AsyncAPIClient` (assíncrono)
- Gerencia autenticação Basic Auth
- Coordena criptografia de mensagens
- Fornece métodos para envio de SMS e gerenciamento de webhooks

**Arquitetura:**
```python
BaseClient (classe abstrata)
├── APIClient (herda de BaseClient)
│   ├── send() → MessageState
│   ├── get_state() → MessageState
│   └── webhook methods
└── AsyncAPIClient (herda de BaseClient)
    ├── async send() → MessageState
    ├── async get_state() → MessageState
    └── async webhook methods
```

#### 2.2.2 Módulo `domain.py` - Modelos de Dados
**Classes principais:**
- `Message`: Representa uma mensagem SMS a ser enviada
- `MessageState`: Estado atual de uma mensagem enviada
- `RecipientState`: Estado de entrega para um destinatário específico
- `Webhook`: Configuração de webhook

#### 2.2.3 Módulos HTTP (`http.py` e `ahttp.py`)
**Padrão de Design:** Protocol/Interface Pattern
- Define contratos para clientes HTTP
- Suporte automático para `requests`, `httpx` e `aiohttp`
- Implementação de fallback gracioso

#### 2.2.4 Módulo `encryption.py`
**Funcionalidades:**
- Criptografia AES-256-CBC com PBKDF2-SHA1
- Suporte opcional (requer `pycryptodome`)
- Compatível com o protocolo do servidor

---

## 3. Fluxo de Trabalho de Desenvolvimento

### 3.1 Práticas de Codificação

#### 3.1.1 Padrões de Código
```python
# Estilo de código seguindo PEP 8
# Máximo de 88 caracteres por linha (Black formatter)
# Type hints obrigatórios

def send_message(
    client: APIClient, 
    message: str, 
    recipients: List[str]
) -> MessageState:
    """
    Envia uma mensagem SMS.
    
    Args:
        client: Cliente API configurado
        message: Texto da mensagem
        recipients: Lista de números de telefone
        
    Returns:
        Estado da mensagem enviada
        
    Raises:
        ValueError: Se os parâmetros forem inválidos
    """
    pass
```

#### 3.1.2 Comandos de Desenvolvimento
```bash
# Formatação automática de código
pipenv run black android_sms_gateway tests

# Verificação de lint
pipenv run flake8 android_sms_gateway tests

# Ordenação de imports
pipenv run isort android_sms_gateway tests

# Executar todos os checks de qualidade
make lint
```

### 3.2 Gerenciamento de Versão (Git)

#### 3.2.1 Branch Strategy
```
main                    # Branch principal (produção)
├── develop            # Branch de desenvolvimento
├── feature/nova-func  # Branches de funcionalidades
├── bugfix/correcao   # Branches de correção
└── release/v1.1.0    # Branches de release
```

#### 3.2.2 Convenção de Commits
```bash
# Formato: tipo(escopo): descrição

# Exemplos:
git commit -m "feat(client): adiciona suporte a webhooks"
git commit -m "fix(encryption): corrige bug na descriptografia"
git commit -m "docs(readme): atualiza exemplos de uso"
git commit -m "test(client): adiciona testes para timeout"
```

### 3.3 Integração Contínua

#### 3.3.1 Pipeline de Testes (.github/workflows/testing.yml)
```yaml
# Testa em múltiplas versões do Python (3.9-3.13)
# Executa em cada Pull Request
# Passos:
1. Setup do Python
2. Instalação de dependências
3. Linting com flake8
4. Execução de testes com pytest
```

#### 3.3.2 Pipeline de Deploy (.github/workflows/publish.yml)
```yaml
# Triggered em: criação de release
# Passos:
1. Build do pacote
2. Atualização da versão
3. Upload para PyPI
```

### 3.4 Comandos Makefile

```bash
# Instalar dependências
make install

# Executar testes
make test

# Verificar qualidade do código
make lint

# Build do pacote
make build

# Publicar no PyPI
make publish

# Limpar arquivos temporários
make clean
```

---

## 4. Abordagem de Testes

### 4.1 Estratégia de Testes

#### 4.1.1 Pirâmide de Testes
```
    E2E Tests (Integração completa)
         /\
        /  \
   Integration Tests (Componentes)
      /      \
     /        \
Unit Tests (Funções/Classes)
```

### 4.2 Tipos de Testes Implementados

#### 4.2.1 Testes Unitários
**Localização:** `tests/test_domain.py`, `tests/test_encryption.py`

**Exemplo de teste unitário:**
```python
def test_message_state_from_dict():
    """Testa a criação de MessageState a partir de dict"""
    payload = {
        "id": "123",
        "state": "Pending",
        "recipients": [
            {"phoneNumber": "123", "state": "Pending"},
        ],
        "isHashed": True,
        "isEncrypted": False,
    }

    message_state = MessageState.from_dict(payload)
    assert message_state.id == payload["id"]
    assert message_state.state.name == payload["state"]
```

#### 4.2.2 Testes de Integração
**Localização:** `tests/test_client.py`

**Configuração necessária:**
```bash
# Variáveis de ambiente para testes reais
export API_LOGIN=seu_login
export API_PASSWORD=sua_senha
export API_BASE_URL=https://api.sms-gate.app/3rdparty/v1
```

**Exemplo de teste de integração:**
```python
@pytest.mark.skipif(
    not all([
        os.environ.get("API_LOGIN"),
        os.environ.get("API_PASSWORD"),
    ]),
    reason="API credentials are not set"
)
def test_webhook_create(client: APIClient):
    """Testa criação real de webhook"""
    webhook = Webhook(
        id="test_123",
        url="https://example.com/webhook",
        event=WebhookEvent.SMS_RECEIVED,
    )
    
    created = client.create_webhook(webhook)
    assert created.id == webhook.id
```

### 4.3 Ferramentas de Teste

#### 4.3.1 Pytest
**Configuração principal:**
```bash
# Executar todos os testes
pipenv run pytest

# Executar com verbose
pipenv run pytest -v

# Executar testes específicos
pipenv run pytest tests/test_client.py::TestAPIClient::test_webhook_create

# Executar com coverage
pipenv run pytest --cov=android_sms_gateway
```

#### 4.3.2 Fixtures
```python
@pytest.fixture
def client():
    """Fixture que fornece cliente configurado"""
    with RequestsHttpClient() as h, APIClient(
        os.environ.get("API_LOGIN") or "test",
        os.environ.get("API_PASSWORD") or "test",
        http=h,
    ) as c:
        yield c
```

### 4.4 Executando Testes

#### 4.4.1 Testes Locais (sem credenciais)
```bash
# Testa apenas funcionalidades que não precisam de API real
pipenv run pytest tests/test_domain.py tests/test_encryption.py
```

#### 4.4.2 Testes Completos (com credenciais)
```bash
# Configure as variáveis primeiro
export API_LOGIN=seu_login
export API_PASSWORD=sua_senha

# Execute todos os testes
pipenv run pytest tests/
```

---

## 5. Etapas Comuns de Solução de Problemas

### 5.1 Problemas de Configuração

#### 5.1.1 Ambiente Virtual
**Sintoma:** Módulos não encontrados
```bash
# Verificar se está no ambiente correto
which python  # Deve apontar para .venv

# Reativar o ambiente
pipenv shell

# Verificar dependências instaladas
pipenv graph
```

#### 5.1.2 Dependências
**Sintoma:** ImportError para bibliotecas opcionais
```bash
# Reinstalar categorias específicas
pipenv install --categories encryption  # Para criptografia
pipenv install --categories requests    # Para cliente HTTP
```

### 5.2 Problemas de Conectividade

#### 5.2.1 Timeout de API
```python
# Debug de conectividade
import requests

try:
    response = requests.get(
        "https://api.sms-gate.app/3rdparty/v1/ping",
        timeout=10
    )
    print(f"Status: {response.status_code}")
except requests.Timeout:
    print("Timeout - verifique sua conexão")
except requests.ConnectionError:
    print("Erro de conexão - verifique proxy/firewall")
```

#### 5.2.2 Autenticação
```python
# Testar credenciais
import base64
from android_sms_gateway import APIClient

login = "seu_login"
password = "sua_senha"

# Verificar encoding das credenciais
credentials = base64.b64encode(f"{login}:{password}".encode()).decode()
print(f"Credentials: Basic {credentials}")

# Testar com cliente
try:
    with APIClient(login, password) as client:
        webhooks = client.get_webhooks()
        print("Autenticação OK")
except Exception as e:
    print(f"Erro de auth: {e}")
```

### 5.3 Problemas de Desenvolvimento

#### 5.3.1 Debugging
```python
import logging

# Habilitar logs detalhados
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('android_sms_gateway')

# No código do client.py já existe:
logger = logging.getLogger(__name__)
logger.debug("Debug info aqui")
```

#### 5.3.2 Teste de Componentes Isolados
```python
# Testar apenas o HTTP client
from android_sms_gateway.http import get_client

with get_client() as http:
    try:
        response = http.get("https://httpbin.org/get")
        print("HTTP client OK")
    except Exception as e:
        print(f"HTTP error: {e}")

# Testar apenas criptografia
from android_sms_gateway.encryption import Encryptor

try:
    enc = Encryptor("test-passphrase")
    encrypted = enc.encrypt("test message")
    decrypted = enc.decrypt(encrypted)
    assert decrypted == "test message"
    print("Encryption OK")
except Exception as e:
    print(f"Encryption error: {e}")
```

### 5.4 Análise de Logs

#### 5.4.1 Logs de API
```python
# Interceptar requests para debug
import requests
import logging

# Habilitar logs HTTP
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True
```

#### 5.4.2 Logs de Aplicação
```python
# Configurar logging personalizado
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
```

### 5.5 Ferramentas de Diagnóstico

#### 5.5.1 Script de Diagnóstico
```python
#!/usr/bin/env python3
"""Script de diagnóstico do ambiente"""

import sys
import os
import importlib

def check_python_version():
    version = sys.version_info
    print(f"Python: {version.major}.{version.minor}.{version.micro}")
    if version < (3, 9):
        print("❌ Python 3.9+ necessário")
        return False
    print("✅ Versão do Python OK")
    return True

def check_dependencies():
    deps = ["requests", "httpx", "aiohttp", "Crypto"]
    for dep in deps:
        try:
            importlib.import_module(dep)
            print(f"✅ {dep} disponível")
        except ImportError:
            print(f"⚠️  {dep} não instalado (opcional)")

def check_environment():
    env_vars = ["API_LOGIN", "API_PASSWORD"]
    for var in env_vars:
        if os.getenv(var):
            print(f"✅ {var} configurado")
        else:
            print(f"⚠️  {var} não configurado")

if __name__ == "__main__":
    print("=== Diagnóstico do Ambiente ===")
    check_python_version()
    check_dependencies()
    check_environment()
```

#### 5.5.2 Comandos Úteis
```bash
# Verificar instalação do pacote
python -c "import android_sms_gateway; print(android_sms_gateway.__version__)"

# Verificar dependências
pipenv graph

# Limpar cache do pip
pip cache purge

# Reinstalar ambiente do zero
pipenv --rm
pipenv install --dev --categories encryption,requests
```

### 5.6 Problemas Comuns e Soluções

| Problema | Causa Provável | Solução |
|----------|----------------|---------|
| `ImportError: No module named 'android_sms_gateway'` | Pacote não instalado ou ambiente errado | `pipenv install` e `pipenv shell` |
| `ImportError: Please install requests or httpx` | Cliente HTTP não instalado | `pipenv install --categories requests` |
| `ImportError: Please install cryptodome` | Biblioteca de criptografia ausente | `pipenv install --categories encryption` |
| `ValueError: Session not initialized` | Cliente usado fora do context manager | Use `with client.APIClient(...) as c:` |
| `HTTPError: 401 Unauthorized` | Credenciais incorretas | Verifique `API_LOGIN` e `API_PASSWORD` |
| `ConnectionError` | Problemas de rede | Verifique firewall, proxy, DNS |

---

## 📚 Recursos Adicionais

- **Documentação da API:** https://docs.sms-gate.app/
- **Repositório:** https://github.com/android-sms-gateway/client-py
- **PyPI:** https://pypi.org/project/android-sms-gateway/
- **Issues:** https://github.com/android-sms-gateway/client-py/issues