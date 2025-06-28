# Documentação da API SMS Gateway

Esta documentação detalha os endpoints públicos da API do SMS Gateway, seus formatos de solicitação/resposta, exemplos de uso e quaisquer limitações.

## Autenticação

A maioria dos endpoints requer autenticação. A autenticação é feita através de um token Bearer no cabeçalho `Authorization`.

`Authorization: Bearer <SEU_TOKEN_DE_API>`

Endpoints que não requerem autenticação são explicitamente mencionados.

---

## Endpoints

### 1. Enviar SMS

*   **Endpoint:** `POST /api/send`
*   **Descrição:** Envia uma mensagem SMS para um ou mais números de telefone.
*   **Autenticação:** Requerida.
*   **Limite de Taxa:** 10 solicitações por minuto.

#### Solicitação

*   **Método:** `POST`
*   **URL:** `/api/send`
*   **Cabeçalhos:**
    *   `Authorization: Bearer <SEU_TOKEN_DE_API>`
    *   `Content-Type: application/json`
*   **Corpo da Solicitação (JSON):**
    ```json
    {
        "message": "Olá, esta é uma mensagem de teste!",
        "phone_numbers": ["+11234567890", "+442071838750"],
        "with_delivery_report": true,
        "sim_number": "1",
        "ttl": 3600
    }
    ```
    *   `message` (string, obrigatório): O conteúdo da mensagem SMS. Máximo de 1600 caracteres.
    *   `phone_numbers` (array de strings, obrigatório): Lista de números de telefone para enviar o SMS. Máximo de 10 números por solicitação. Os números devem estar em formato internacional (ex: `+11234567890`).
    *   `with_delivery_report` (boolean, opcional, padrão: `true`): Solicitar relatório de entrega.
    *   `sim_number` (string, opcional): Especificar o número do SIM para enviar a mensagem (se aplicável e suportado pelo gateway).
    *   `ttl` (integer, opcional): Tempo de vida da mensagem em segundos.

#### Resposta

*   **Código de Sucesso:** `200 OK`
    ```json
    {
        "id": "message_id_12345",
        "state": "PENDING",
        "recipients": ["+11234567890", "+442071838750"]
    }
    ```
    *   `id` (string): O ID único da mensagem.
    *   `state` (string): O estado inicial da mensagem (ex: PENDING, SENT, FAILED).
    *   `recipients` (array de strings): Lista de números de telefone para os quais o SMS foi (ou será) enviado.

*   **Códigos de Erro:**
    *   `400 Bad Request`:
        ```json
        {
            "error": "Message too long (max 1600 characters)"
        }
        ```
        ```json
        {
            "error": "Invalid phone number format: <número_inválido>"
        }
        ```
        ```json
        {
            "error": "Maximum 10 recipients per message"
        }
        ```
    *   `401 Unauthorized`: Token de autenticação inválido ou ausente.
    *   `429 Too Many Requests`: Limite de taxa excedido.
    *   `500 Internal Server Error`:
        ```json
        {
            "error": "Failed to send SMS"
        }
        ```

#### Exemplo de Uso (cURL)

```bash
curl -X POST \
  https://seu-dominio.com/api/send \
  -H 'Authorization: Bearer <SEU_TOKEN_DE_API>' \
  -H 'Content-Type: application/json' \
  -d '{
        "message": "Olá do cURL!",
        "phone_numbers": ["+11234567890"]
      }'
```

#### Limitações

*   Máximo de 1600 caracteres por mensagem.
*   Máximo de 10 destinatários por solicitação.
*   Números de telefone devem ser validados e sanitizados.

---

### 2. Obter Mensagens

*   **Endpoint:** `GET /api/messages`
*   **Descrição:** Recupera uma lista paginada de mensagens enviadas pelo usuário autenticado.
*   **Autenticação:** Requerida.
*   **Limite de Taxa:** 30 solicitações por minuto.

#### Solicitação

*   **Método:** `GET`
*   **URL:** `/api/messages`
*   **Cabeçalhos:**
    *   `Authorization: Bearer <SEU_TOKEN_DE_API>`
*   **Parâmetros de Query:**
    *   `page` (integer, opcional, padrão: `1`): O número da página para resultados paginados.
    *   `per_page` (integer, opcional, padrão: `25`, máx: `100`): O número de mensagens a serem retornadas por página.
    *   `state` (string, opcional): Filtrar mensagens por estado (ex: `SENT`, `FAILED`, `DELIVERED`).

#### Resposta

*   **Código de Sucesso:** `200 OK`
    ```json
    {
        "messages": [
            {
                "id": "msg_1",
                "content": "Olá, esta é a mensagem 1...",
                "recipients": ["+11234567890"],
                "state": "DELIVERED",
                "created_at": "2023-10-27T10:30:00Z"
            },
            {
                "id": "msg_2",
                "content": "Outra mensagem de teste...",
                "recipients": ["+442071838750", "+15551234567"],
                "state": "FAILED",
                "created_at": "2023-10-27T10:35:00Z"
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 2,
            "total": 100,
            "pages": 50,
            "has_next": true,
            "has_prev": false
        }
    }
    ```
    *   `messages` (array de objetos):
        *   `id` (string): ID da mensagem.
        *   `content` (string): Conteúdo da mensagem (truncado em 100 caracteres se mais longo).
        *   `recipients` (array de strings): Lista de destinatários.
        *   `state` (string): Estado da mensagem.
        *   `created_at` (string): Data e hora de criação no formato ISO 8601.
    *   `pagination` (objeto):
        *   `page` (integer): Página atual.
        *   `per_page` (integer): Itens por página.
        *   `total` (integer): Número total de mensagens.
        *   `pages` (integer): Número total de páginas.
        *   `has_next` (boolean): Se existe uma próxima página.
        *   `has_prev` (boolean): Se existe uma página anterior.

*   **Códigos de Erro:**
    *   `401 Unauthorized`: Token de autenticação inválido ou ausente.
    *   `429 Too Many Requests`: Limite de taxa excedido.
    *   `500 Internal Server Error`:
        ```json
        {
            "error": "Failed to fetch messages"
        }
        ```

#### Exemplo de Uso (cURL)

```bash
curl -X GET \
  'https://seu-dominio.com/api/messages?page=1&per_page=10&state=DELIVERED' \
  -H 'Authorization: Bearer <SEU_TOKEN_DE_API>'
```

#### Limitações

*   Máximo de 100 mensagens por página (`per_page`).

---

### 3. Gerenciar Contatos

#### 3.1. Obter Contatos

*   **Endpoint:** `GET /api/contacts`
*   **Descrição:** Recupera todos os contatos associados ao usuário autenticado.
*   **Autenticação:** Requerida.
*   **Limite de Taxa:** 20 solicitações por minuto.

##### Solicitação

*   **Método:** `GET`
*   **URL:** `/api/contacts`
*   **Cabeçalhos:**
    *   `Authorization: Bearer <SEU_TOKEN_DE_API>`

##### Resposta

*   **Código de Sucesso:** `200 OK`
    ```json
    [
        {
            "id": 1,
            "name": "João Silva",
            "phone": "+5511987654321",
            "group_name": "Trabalho",
            "notes": "Cliente VIP"
        },
        {
            "id": 2,
            "name": "Maria Oliveira",
            "phone": "+351912345678",
            "group_name": "Amigos",
            "notes": ""
        }
    ]
    ```
    *   Cada objeto no array representa um contato com os seguintes campos:
        *   `id` (integer): ID do contato.
        *   `name` (string): Nome do contato.
        *   `phone` (string): Número de telefone do contato.
        *   `group_name` (string): Nome do grupo ao qual o contato pertence (opcional).
        *   `notes` (string): Anotações sobre o contato (opcional).

*   **Códigos de Erro:**
    *   `401 Unauthorized`: Token de autenticação inválido ou ausente.
    *   `429 Too Many Requests`: Limite de taxa excedido.
    *   `500 Internal Server Error`:
        ```json
        {
            "error": "Failed to fetch contacts"
        }
        ```

##### Exemplo de Uso (cURL)

```bash
curl -X GET \
  https://seu-dominio.com/api/contacts \
  -H 'Authorization: Bearer <SEU_TOKEN_DE_API>'
```

#### 3.2. Criar Contato

*   **Endpoint:** `POST /api/contacts`
*   **Descrição:** Cria um novo contato para o usuário autenticado.
*   **Autenticação:** Requerida.
*   **Limite de Taxa:** 20 solicitações por minuto.

##### Solicitação

*   **Método:** `POST`
*   **URL:** `/api/contacts`
*   **Cabeçalhos:**
    *   `Authorization: Bearer <SEU_TOKEN_DE_API>`
    *   `Content-Type: application/json`
*   **Corpo da Solicitação (JSON):**
    ```json
    {
        "name": "Carlos Pereira",
        "phone": "+14155552671",
        "group_name": "Família",
        "notes": "Aniversário em Dezembro"
    }
    ```
    *   `name` (string, obrigatório): Nome do contato.
    *   `phone` (string, obrigatório): Número de telefone do contato. Deve ser um formato válido.
    *   `group_name` (string, opcional): Nome do grupo.
    *   `notes` (string, opcional): Anotações adicionais.

##### Resposta

*   **Código de Sucesso:** `201 Created`
    ```json
    {
        "id": 3,
        "name": "Carlos Pereira",
        "phone": "+14155552671"
    }
    ```
    *   `id` (integer): ID do contato recém-criado.
    *   `name` (string): Nome do contato.
    *   `phone` (string): Número de telefone do contato.

*   **Códigos de Erro:**
    *   `400 Bad Request`:
        ```json
        {
            "error": "Invalid JSON data"
        }
        ```
        ```json
        {
            "error": "Name and phone are required"
        }
        ```
        ```json
        {
            "error": "Invalid phone number format: <número_inválido>"
        }
        ```
        ```json
        {
            "error": "Contact with this phone number already exists"
        }
        ```
    *   `401 Unauthorized`: Token de autenticação inválido ou ausente.
    *   `429 Too Many Requests`: Limite de taxa excedido.
    *   `500 Internal Server Error`:
        ```json
        {
            "error": "Failed to create contact"
        }
        ```

##### Exemplo de Uso (cURL)

```bash
curl -X POST \
  https://seu-dominio.com/api/contacts \
  -H 'Authorization: Bearer <SEU_TOKEN_DE_API>' \
  -H 'Content-Type: application/json' \
  -d '{
        "name": "Ana Souza",
        "phone": "+5521912345678",
        "group_name": "Colegas"
      }'
```

#### Limitações

*   O número de telefone deve ser único por usuário.

---

### 4. Testar Conexão do Gateway

*   **Endpoint:** `POST /api/test-connection`
*   **Descrição:** Testa a conectividade com um URL de gateway SMS fornecido.
*   **Autenticação:** Requerida.
*   **Limite de Taxa:** 5 solicitações por minuto.

#### Solicitação

*   **Método:** `POST`
*   **URL:** `/api/test-connection`
*   **Cabeçalhos:**
    *   `Authorization: Bearer <SEU_TOKEN_DE_API>`
    *   `Content-Type: application/json`
*   **Corpo da Solicitação (JSON):**
    ```json
    {
        "gateway_url": "http://seu.gateway.sms:8080"
    }
    ```
    *   `gateway_url` (string, obrigatório): O URL base do gateway SMS a ser testado.

#### Resposta

*   **Código de Sucesso:** `200 OK`
    ```json
    {
        "success": true
    }
    ```
    Ou em caso de falha na conexão (mas a solicitação foi processada):
    ```json
    {
        "success": false,
        "error": "Connection failed"
    }
    ```

*   **Códigos de Erro:**
    *   `400 Bad Request`:
        ```json
        {
            "error": "Gateway URL is required"
        }
        ```
        ```json
        {
            "error": "Invalid URL format: <url_inválida>"
        }
        ```
    *   `401 Unauthorized`: Token de autenticação inválido ou ausente.
    *   `429 Too Many Requests`: Limite de taxa excedido.
    *   `500 Internal Server Error`:
        ```json
        {
            "success": false,
            "error": "Connection test failed"
        }
        ```

#### Exemplo de Uso (cURL)

```bash
curl -X POST \
  https://seu-dominio.com/api/test-connection \
  -H 'Authorization: Bearer <SEU_TOKEN_DE_API>' \
  -H 'Content-Type: application/json' \
  -d '{
        "gateway_url": "http://meu.provedor.sms/api"
      }'
```

#### Limitações

*   O URL do gateway deve ser um URL válido e acessível.

---

### 5. Verificação de Saúde (Health Check)

*   **Endpoint:** `GET /api/health`
*   **Descrição:** Verifica o estado de saúde da aplicação, incluindo a conectividade com o banco de dados.
*   **Autenticação:** Não requerida.
*   **Limite de Taxa:** 60 solicitações por minuto.

#### Solicitação

*   **Método:** `GET`
*   **URL:** `/api/health`

#### Resposta

*   **Código de Sucesso:** `200 OK`
    ```json
    {
        "status": "healthy",
        "timestamp": "2023-10-27T12:00:00Z",
        "version": "1.0.0"
    }
    ```
    *   `status` (string): "healthy" indica que a aplicação está funcionando corretamente.
    *   `timestamp` (string): Data e hora da verificação no formato ISO 8601.
    *   `version` (string): Versão da aplicação.

*   **Código de Erro:** `503 Service Unavailable`
    ```json
    {
        "status": "unhealthy",
        "error": "Database connection failed"
    }
    ```
    *   `status` (string): "unhealthy" indica um problema (ex: falha na conexão com o banco de dados).
    *   `error` (string): Descrição do erro.


#### Exemplo de Uso (cURL)

```bash
curl -X GET https://seu-dominio.com/api/health
```

#### Limitações

*   Este endpoint é público e pode ser acessado sem autenticação.
---
