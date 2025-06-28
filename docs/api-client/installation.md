# Cliente Python API: Instalação

A biblioteca `android-sms-gateway` pode ser facilmente instalada usando `pip`.

## Requisitos

*   **Python**: 3.9 ou superior.
*   **Cliente HTTP**: Você precisará de pelo menos um cliente HTTP compatível instalado. A biblioteca pode usar `requests`, `aiohttp`, ou `httpx`.
    *   `requests` (para operações síncronas)
    *   `aiohttp` (para operações assíncronas)
    *   `httpx` (para operações síncronas e assíncronas)
*   **Dependência Opcional para Criptografia**:
    *   `pycryptodome` (para suporte à criptografia de ponta a ponta)

## Métodos de Instalação

Escolha o método de instalação que melhor se adapta às suas necessidades.

### 1. Instalação Básica

Esta é a instalação mais simples e tentará usar `httpx` se disponível, ou outro cliente HTTP que você já possa ter.

```bash
pip install android-sms-gateway
```
Se você não tiver `httpx`, `requests` ou `aiohttp` já instalados, você pode precisar instalar um deles separadamente ou usar os extras (veja abaixo).

### 2. Instalação com Cliente HTTP Específico (Recomendado)

É recomendado instalar a biblioteca com o extra para o cliente HTTP que você pretende usar. Isso garante que a dependência correta seja instalada.

*   **Para uso síncrono com `requests`**:
    ```bash
    pip install android-sms-gateway[requests]
    ```
*   **Para uso assíncrono com `aiohttp`**:
    ```bash
    pip install android-sms-gateway[aiohttp]
    ```
*   **Para uso síncrono e assíncrono com `httpx`**:
    ```bash
    pip install android-sms-gateway[httpx]
    ```

Você pode instalar múltiplos extras se necessário, por exemplo, se você quiser ter tanto `requests` quanto `aiohttp` disponíveis:
```bash
pip install android-sms-gateway[requests,aiohttp]
```

### 3. Instalação com Suporte a Criptografia

Se você planeja usar a funcionalidade de criptografia de ponta a ponta, você precisa instalar o extra `encryption`, que trará a dependência `pycryptodome`.

```bash
pip install android-sms-gateway[encryption]
```

Você pode combinar isso com um cliente HTTP específico:

*   **Com `requests` e criptografia**:
    ```bash
    pip install android-sms-gateway[requests,encryption]
    ```
*   **Com `httpx` e criptografia**:
    ```bash
    pip install android-sms-gateway[httpx,encryption]
    ```
*   **Com `aiohttp` e criptografia**:
    ```bash
    pip install android-sms-gateway[aiohttp,encryption]
    ```

### 4. Instalação Completa (Todos os Extras)

Para instalar a biblioteca com todos os clientes HTTP suportados e suporte a criptografia:

```bash
pip install android-sms-gateway[all]
```
Ou especifique todos manualmente:
```bash
pip install android-sms-gateway[requests,aiohttp,httpx,encryption]
```

### 5. Instalação para Desenvolvimento

Se você planeja contribuir para o desenvolvimento da biblioteca:

1.  **Clone o repositório**:
    ```bash
    git clone https://github.com/prof-gabrielramos/client-py.git
    cd client-py
    ```
2.  **Crie e ative um ambiente virtual** (recomendado):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # ou
    # venv\Scripts\activate    # Windows
    ```
3.  **Instale em modo editável com dependências de desenvolvimento**:
    O projeto usa `Pipfile` para gerenciamento de dependências, mas também fornece extras para `pip`.
    ```bash
    pip install -e ".[dev,requests,aiohttp,httpx,encryption]"
    ```
    Isso instalará a biblioteca em modo editável (`-e`) junto com todas as dependências opcionais e ferramentas de desenvolvimento como `pytest`, `black`, `flake8`, `isort`, `mypy`.

    Se você usa `pipenv`:
    ```bash
    pipenv install --dev
    ```

## Verificando a Instalação

Após a instalação, você pode verificar se a biblioteca está acessível importando-a em um interpretador Python:

```python
import android_sms_gateway
print(android_sms_gateway.__version__)
```

Se nenhum erro ocorrer e a versão for impressa, a instalação foi bem-sucedida.

## Próximos Passos

Agora que você instalou a biblioteca, vá para [Primeiros Passos](./first-steps.md) para aprender como enviar sua primeira mensagem.
