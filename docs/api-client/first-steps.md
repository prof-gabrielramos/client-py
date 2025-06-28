# Cliente Python API: Primeiros Passos

Este guia mostrará como enviar rapidamente sua primeira mensagem SMS usando a biblioteca `android-sms-gateway`.

## Pré-requisitos

1.  **Biblioteca Instalada**: Certifique-se de que você instalou a biblioteca `android-sms-gateway` com um cliente HTTP (veja [Instalação](./installation.md)). Por exemplo:
    ```bash
    pip install android-sms-gateway[requests] # Para cliente síncrono
    # ou
    pip install android-sms-gateway[aiohttp]  # Para cliente assíncrono
    ```

2.  **SMS Gateway for Android Configurado**:
    *   O aplicativo [SMS Gateway for Android™](https://sms-gate.app/) deve estar instalado e rodando no seu dispositivo Android.
    *   A API deve estar habilitada no aplicativo, e você deve ter anotado:
        *   O **Login da API** (usuário).
        *   A **Senha da API**.
        *   O **Endereço IP e Porta** do seu dispositivo Android (visível no app, ex: `192.168.1.100:8080`). A URL base da API será `http://<IP_DO_CELULAR>:<PORTA>`.

3.  **Variáveis de Ambiente (Recomendado para Credenciais)**:
    Para segurança, é uma boa prática armazenar suas credenciais da API em variáveis de ambiente em vez de codificá-las diretamente no script.
    ```bash
    export ANDROID_SMS_GATEWAY_LOGIN="seu_usuario_api"
    export ANDROID_SMS_GATEWAY_PASSWORD="sua_senha_api"
    export ANDROID_SMS_GATEWAY_BASE_URL="http://<IP_DO_CELULAR>:<PORTA>"
    ```
    Substitua pelos seus valores reais. Se não definir `ANDROID_SMS_GATEWAY_BASE_URL`, você precisará passá-la ao instanciar o cliente. O padrão da biblioteca é para a API pública `sms-gate.app`.

## Exemplo de Uso

Vamos criar um script Python simples para enviar uma mensagem.

### Exemplo Síncrono (usando `APIClient`)

Este exemplo usa o cliente síncrono, que é mais simples para scripts diretos. Requer `requests` ou `httpx` instalado com o extra correspondente.

```python
import os
from android_sms_gateway import client, domain

# Carregar credenciais e URL base das variáveis de ambiente
login = os.getenv("ANDROID_SMS_GATEWAY_LOGIN")
password = os.getenv("ANDROID_SMS_GATEWAY_PASSWORD")
base_url = os.getenv("ANDROID_SMS_GATEWAY_BASE_URL") # Ex: "http://192.168.1.100:8080"

if not all([login, password, base_url]):
    print("Por favor, defina as variáveis de ambiente: "
          "ANDROID_SMS_GATEWAY_LOGIN, ANDROID_SMS_GATEWAY_PASSWORD, ANDROID_SMS_GATEWAY_BASE_URL")
    exit(1)

# 1. Criar o objeto da mensagem
# Substitua pelo número de telefone do destinatário em formato internacional
recipient_phone_number = "+12345678900" # Exemplo
message_text = "Olá do cliente Python do SMS Gateway! (Síncrono)"

message_to_send = domain.Message(
    message=message_text,
    phone_numbers=[recipient_phone_number],
    with_delivery_report=True  # Solicitar relatório de entrega
)

# 2. Inicializar o cliente da API
# O APIClient é um context manager, então use 'with' para garantir que a sessão seja fechada.
try:
    with client.APIClient(login, password, base_url=base_url) as api:
        print(f"Enviando mensagem para: {recipient_phone_number}")
        print(f"Texto: {message_text}")

        # 3. Enviar a mensagem
        message_state = api.send(message_to_send)

        print(f"Mensagem enviada com sucesso!")
        print(f"  ID da Mensagem: {message_state.id}")
        print(f"  Estado Inicial: {message_state.state}")
        for recipient_state in message_state.recipients:
            print(f"    Destinatário: {recipient_state.phone_number}, Estado: {recipient_state.state}")

        # 4. (Opcional) Consultar o estado da mensagem após um tempo
        # import time
        # time.sleep(10) # Espere 10 segundos (apenas para exemplo)
        # updated_state = api.get_state(message_state.id)
        # print(f"\nEstado Atualizado da Mensagem (ID: {updated_state.id}): {updated_state.state}")
        # for r_state in updated_state.recipients:
        #     print(f"    Destinatário: {r_state.phone_number}, Estado: {r_state.state}")

except Exception as e:
    print(f"Ocorreu um erro: {e}")

```

### Exemplo Assíncrono (usando `AsyncAPIClient`)

Este exemplo usa o cliente assíncrono, adequado para aplicações baseadas em `asyncio`. Requer `aiohttp` ou `httpx` instalado com o extra correspondente.

```python
import asyncio
import os
from android_sms_gateway import client, domain

# Carregar credenciais e URL base das variáveis de ambiente
login = os.getenv("ANDROID_SMS_GATEWAY_LOGIN")
password = os.getenv("ANDROID_SMS_GATEWAY_PASSWORD")
base_url = os.getenv("ANDROID_SMS_GATEWAY_BASE_URL") # Ex: "http://192.168.1.100:8080"

if not all([login, password, base_url]):
    print("Por favor, defina as variáveis de ambiente: "
          "ANDROID_SMS_GATEWAY_LOGIN, ANDROID_SMS_GATEWAY_PASSWORD, ANDROID_SMS_GATEWAY_BASE_URL")
    exit(1)

async def main():
    # 1. Criar o objeto da mensagem
    recipient_phone_number = "+12345678900" # Exemplo
    message_text = "Olá do cliente Python do SMS Gateway! (Assíncrono)"

    message_to_send = domain.Message(
        message=message_text,
        phone_numbers=[recipient_phone_number],
        with_delivery_report=True
    )

    # 2. Inicializar o cliente da API assíncrono
    # O AsyncAPIClient é um context manager assíncrono, use 'async with'.
    try:
        async with client.AsyncAPIClient(login, password, base_url=base_url) as api:
            print(f"Enviando mensagem para: {recipient_phone_number}")
            print(f"Texto: {message_text}")

            # 3. Enviar a mensagem
            message_state = await api.send(message_to_send)

            print(f"Mensagem enviada com sucesso!")
            print(f"  ID da Mensagem: {message_state.id}")
            print(f"  Estado Inicial: {message_state.state}")
            for recipient_state in message_state.recipients:
                print(f"    Destinatário: {recipient_state.phone_number}, Estado: {recipient_state.state}")

            # 4. (Opcional) Consultar o estado da mensagem após um tempo
            # await asyncio.sleep(10) # Espere 10 segundos (apenas para exemplo)
            # updated_state = await api.get_state(message_state.id)
            # print(f"\nEstado Atualizado da Mensagem (ID: {updated_state.id}): {updated_state.state}")
            # for r_state in updated_state.recipients:
            #     print(f"    Destinatário: {r_state.phone_number}, Estado: {r_state.state}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Executando os Exemplos

1.  Salve um dos exemplos como um arquivo Python (ex: `send_sms_sync.py` ou `send_sms_async.py`).
2.  Certifique-se de que suas variáveis de ambiente (`ANDROID_SMS_GATEWAY_LOGIN`, `ANDROID_SMS_GATEWAY_PASSWORD`, `ANDROID_SMS_GATEWAY_BASE_URL`) estão definidas no terminal onde você executará o script.
3.  Execute o script:
    ```bash
    python send_sms_sync.py
    # ou
    python send_sms_async.py
    ```

Se tudo estiver configurado corretamente, a mensagem SMS será enviada através do seu dispositivo Android, e você verá a confirmação e o ID da mensagem no console.

## Solução de Problemas Comuns

*   **Erro de Conexão (`ConnectionRefusedError`, `Timeout`)**:
    *   Verifique se o aplicativo SMS Gateway está rodando no seu celular.
    *   Confirme se o IP e a porta na `BASE_URL` estão corretos e acessíveis a partir da máquina que executa o script.
    *   Verifique se o celular e a máquina estão na mesma rede e se não há firewall bloqueando a conexão.
*   **Erro de Autenticação (`UnauthorizedError`)**:
    *   Verifique se o `LOGIN` e `PASSWORD` correspondem exatamente aos configurados na API do aplicativo SMS Gateway.
*   **`ModuleNotFoundError`**:
    *   Certifique-se de que a biblioteca e suas dependências (como `requests` ou `aiohttp`) estão instaladas no ambiente Python que você está usando.

Com estes primeiros passos, você está pronto para explorar funcionalidades mais avançadas da biblioteca. Prossiga para o [Guia do Cliente](./client-guide.md) para mais detalhes.
