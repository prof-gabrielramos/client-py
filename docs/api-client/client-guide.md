# Cliente Python API: Guia do Cliente

Este guia detalha a configuração dos clientes da API (`APIClient` e `AsyncAPIClient`), os métodos disponíveis e as principais estruturas de dados usadas pela biblioteca `android-sms-gateway`.

## Configuração do Cliente

Tanto o cliente síncrono (`client.APIClient`) quanto o assíncrono (`client.AsyncAPIClient`) compartilham um conjunto similar de parâmetros de inicialização.

```python
from android_sms_gateway import client, domain, http, encryption

# Exemplo de inicialização do cliente síncrono
# api_client = client.APIClient(
#     login="seu_login_api",
#     password="sua_senha_api",
#     base_url="http://<IP_DO_CELULAR>:<PORTA>", # Opcional se ANDROID_SMS_GATEWAY_BASE_URL estiver definido
#     encryptor=None,  # Instância de Encryptor opcional
#     http_client=None # Cliente HTTP customizado opcional
# )

# Exemplo de inicialização do cliente assíncrono
# async_api_client = client.AsyncAPIClient(
#     login="seu_login_api",
#     password="sua_senha_api",
#     base_url="http://<IP_DO_CELULAR>:<PORTA>",
#     encryptor=None,
#     http_client=None
# )
```

**Parâmetros:**

| Parâmetro     | Tipo                          | Descrição                                                                                                                                 | Padrão (se não fornecido)                                   |
|---------------|-------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| `login`       | `str`                         | O nome de usuário (login) para autenticação na API do SMS Gateway.                                                                        | **Obrigatório.**                                            |
| `password`    | `str`                         | A senha para autenticação na API do SMS Gateway.                                                                                          | **Obrigatório.**                                            |
| `base_url`    | `Optional[str]`               | A URL base da API do SMS Gateway (ex: `http://192.168.1.100:8080`).                                                                       | Tenta ler de `os.getenv("ANDROID_SMS_GATEWAY_BASE_URL")`. Se não definida, usa o URL da API pública `sms-gate.app` (que pode não ser o desejado para gateways auto-hospedados). |
| `encryptor`   | `Optional[encryption.Encryptor]` | Uma instância da classe `Encryptor` para habilitar a criptografia de ponta a ponta. Veja a seção [Criptografia](./encryption.md).        | `None` (criptografia desabilitada).                         |
| `http_client` | `Optional[http.HttpClient]` ou `Optional[ahttp.AsyncHttpClient]` | Uma instância de um cliente HTTP customizado. Útil se você precisar de configurações HTTP específicas (proxies, timeouts, etc.). | A biblioteca detecta automaticamente um cliente HTTP compatível instalado (`httpx`, `requests` para síncrono; `httpx`, `aiohttp` para assíncrono). |

**Context Managers:**
Ambos os clientes são context managers, o que garante que a sessão HTTP subjacente seja fechada corretamente. É altamente recomendado usá-los com `with` (para `APIClient`) ou `async with` (para `AsyncAPIClient`):

```python
# Síncrono
with client.APIClient(login, password, base_url) as api:
    # use api ...

# Assíncrono
async with client.AsyncAPIClient(login, password, base_url) as api:
    # use await api ...
```

## Métodos Disponíveis

Os seguintes métodos estão disponíveis em ambas as instâncias `APIClient` e `AsyncAPIClient` (no cliente assíncrono, eles são métodos `async` e devem ser chamados com `await`).

### 1. Enviar Mensagem

*   **Síncrono**: `send(message: domain.Message) -> domain.MessageState`
*   **Assíncrono**: `async send(message: domain.Message) -> domain.MessageState`

Envia uma mensagem SMS.

*   **Parâmetros**:
    *   `message`: Uma instância de `domain.Message` contendo os detalhes da mensagem a ser enviada.
*   **Retorna**: Uma instância de `domain.MessageState` representando o estado inicial da mensagem após o envio.
*   **Lança**: `SMSGatewayError` ou suas subclasses em caso de falha.

**Exemplo (Síncrono):**
```python
msg = domain.Message(message="Teste", phone_numbers=["+12345"])
state = api.send(msg)
print(state.id, state.state)
```

### 2. Consultar Estado da Mensagem

*   **Síncrono**: `get_state(message_id: str) -> domain.MessageState`
*   **Assíncrono**: `async get_state(message_id: str) -> domain.MessageState`

Consulta o estado de uma mensagem previamente enviada usando seu ID.

*   **Parâmetros**:
    *   `message_id`: O ID da mensagem (string) retornado pelo método `send`.
*   **Retorna**: Uma instância de `domain.MessageState` com o estado atualizado da mensagem.
*   **Lança**: `MessageNotFoundError` se o ID não for encontrado, ou outras `SMSGatewayError`.

**Exemplo (Síncrono):**
```python
# Supondo que state.id foi obtido de um envio anterior
current_status = api.get_state(state.id)
print(current_status.state)
```

### 3. Criar Webhook

*   **Síncrono**: `create_webhook(webhook: domain.Webhook) -> domain.Webhook`
*   **Assíncrono**: `async create_webhook(webhook: domain.Webhook) -> domain.Webhook`

Registra um novo webhook com a API do SMS Gateway.

*   **Parâmetros**:
    *   `webhook`: Uma instância de `domain.Webhook` definindo a URL e o evento para o webhook.
*   **Retorna**: Uma instância de `domain.Webhook` confirmando a criação (pode incluir o ID atribuído pelo gateway).
*   **Lança**: `SMSGatewayError` em caso de falha.

**Exemplo (Síncrono):**
```python
hook = domain.Webhook(url="https://meuservidor.com/callback", event=domain.WebhookEvent.MESSAGE_DELIVERED)
created_hook = api.create_webhook(hook)
print(created_hook.id)
```

### 4. Listar Webhooks

*   **Síncrono**: `get_webhooks() -> list[domain.Webhook]`
*   **Assíncrono**: `async get_webhooks() -> list[domain.Webhook]`

Recupera uma lista de todos os webhooks atualmente configurados no SMS Gateway.

*   **Retorna**: Uma lista de instâncias `domain.Webhook`.
*   **Lança**: `SMSGatewayError` em caso de falha.

**Exemplo (Síncrono):**
```python
hooks = api.get_webhooks()
for hook in hooks:
    print(hook.id, hook.url, hook.event)
```

### 5. Excluir Webhook

*   **Síncrono**: `delete_webhook(webhook_id: str) -> None`
*   **Assíncrono**: `async delete_webhook(webhook_id: str) -> None`

Remove um webhook existente pelo seu ID.

*   **Parâmetros**:
    *   `webhook_id`: O ID (string) do webhook a ser excluído.
*   **Lança**: `SMSGatewayError` em caso de falha (ex: webhook não encontrado).

**Exemplo (Síncrono):**
```python
# Supondo que created_hook.id foi obtido de uma criação anterior
api.delete_webhook(created_hook.id)
print("Webhook excluído.")
```

## Estruturas de Dados (`android_sms_gateway.domain`)

O módulo `domain` contém as classes Pydantic que modelam os dados trocados com a API.

### `Message`
Representa uma mensagem a ser enviada.

```python
class Message(BaseModel):
    message: str  # O conteúdo textual da mensagem SMS.
    phone_numbers: list[str]  # Lista de números de telefone dos destinatários (formato internacional).

    # Campos opcionais
    id: Optional[str] = None  # Um ID de mensagem opcional fornecido pelo cliente.
    sim_number: Optional[int] = None  # Índice do chip SIM a ser usado (0 para SIM1, 1 para SIM2, etc.).
    ttl: Optional[int] = None  # Time-to-live para a mensagem em segundos.
    with_delivery_report: bool = True  # Solicitar um relatório de entrega.
    is_encrypted: bool = False  # Indica se a mensagem deve ser criptografada (requer Encryptor configurado).
```

### `MessageState`
Representa o estado de uma mensagem após o envio ou ao ser consultada.

```python
class RecipientState(BaseModel):
    phone_number: str
    state: ProcessState # Enum: PENDING, SENT, DELIVERED, FAILED, CANCELED
    error_code: Optional[int] = None
    error_message: Optional[str] = None

class MessageState(BaseModel):
    id: str  # ID único da mensagem atribuído pelo gateway.
    state: ProcessState # Estado geral da mensagem.
    recipients: list[RecipientState] # Lista de estados para cada destinatário.
    is_hashed: bool
    is_encrypted: bool
    created_at: Optional[datetime] = None # Data e hora UTC da criação
```
Onde `ProcessState` é um enum:
```python
class ProcessState(str, Enum):
    PENDING = "PENDING"
    SENT = "SENT"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    CANCELED = "CANCELED"
    # ... outros estados possíveis
```

### `Webhook`
Representa um webhook.

```python
class Webhook(BaseModel):
    id: Optional[str] = None # ID atribuído pelo gateway (presente após criação/listagem)
    url: str  # URL de callback para o webhook.
    event: WebhookEvent # Tipo de evento que aciona o webhook.
    # Outros campos como 'secret', 'method' podem existir dependendo da API do gateway.
```
Onde `WebhookEvent` é um enum:
```python
class WebhookEvent(str, Enum):
    MESSAGE_PENDING = "MESSAGE_PENDING"
    MESSAGE_SENT = "MESSAGE_SENT"
    MESSAGE_DELIVERED = "MESSAGE_DELIVERED"
    MESSAGE_FAILED = "MESSAGE_FAILED"
    MESSAGE_CANCELED = "MESSAGE_CANCELED"
    # ... outros eventos
```

### Outras Estruturas

*   `EncryptedMessage`: Usado internamente ao enviar mensagens criptografadas.
*   Exceções customizadas como `SMSGatewayError`, `AuthenticationError`, `MessageNotFoundError`, `NetworkError`, etc., todas herdando de uma `BaseSMSGatewayError`.

## Clientes HTTP

A biblioteca tentará detectar e usar um cliente HTTP instalado na seguinte ordem de prioridade:

**Para `APIClient` (Síncrono):**
1.  `httpx`
2.  `requests`

**Para `AsyncAPIClient` (Assíncrono):**
1.  `httpx`
2.  `aiohttp`

Você pode forçar o uso de um cliente HTTP específico passando uma instância dele para o parâmetro `http_client` do construtor do `APIClient` ou `AsyncAPIClient`.

**Exemplo: Forçando `RequestsHttpClient`:**
```python
from android_sms_gateway.http import RequestsHttpClient

http_client_custom = RequestsHttpClient(timeout=30) # Custom timeout
with client.APIClient(login, password, base_url, http_client=http_client_custom) as api:
    # ...
```

Para criar seu próprio cliente HTTP customizado, você precisará implementar a interface definida em `android_sms_gateway.http.HttpClient` (para síncrono) ou `android_sms_gateway.ahttp.AsyncHttpClient` (para assíncrono).

Este guia cobre os aspectos centrais do uso dos clientes da API. Para detalhes sobre criptografia, consulte a seção [Criptografia](./encryption.md). Para exemplos práticos, veja [Primeiros Passos](./first-steps.md).
