# Cliente Python API: Criptografia

A biblioteca `android-sms-gateway` oferece suporte opcional para criptografia de ponta a ponta (E2EE) de mensagens SMS. Isso significa que o conteúdo da mensagem é criptografado pela biblioteca cliente antes de ser enviado para a API do SMS Gateway e só é descriptografado no dispositivo Android que efetivamente envia o SMS. A API do SMS Gateway em si (seja ela auto-hospedada ou a pública `sms-gate.app`) apenas encaminha o conteúdo criptografado.

**Importante**: Para que a criptografia funcione, tanto a biblioteca cliente quanto o aplicativo SMS Gateway for Android no seu celular devem estar configurados com a **mesma frase secreta (secret phrase)**.

## Mecanismo de Criptografia

*   **Algoritmo**: AES-CBC-256
*   **Chave**: A chave de criptografia é derivada da sua "frase secreta" usando um processo de derivação de chave (como PBKDF2).
*   **Vetor de Inicialização (IV)**: Um IV único é gerado para cada mensagem.
*   **Formato**: A mensagem criptografada (ciphertext + IV) é então codificada em Base64 antes de ser enviada.

## Configuração

### 1. No Aplicativo SMS Gateway for Android

*   Abra o aplicativo SMS Gateway no seu dispositivo Android.
*   Vá para as configurações da API.
*   Encontre a opção relacionada à "Secret Phrase" ou "Encryption Key".
*   Defina uma frase secreta forte e memorável. **Anote-a com segurança.**

### 2. Na Biblioteca Cliente Python

Para usar a criptografia na biblioteca cliente, você precisa:

*   **Instalar o extra `encryption`**:
    ```bash
    pip install android-sms-gateway[encryption]
    # ou, por exemplo, com requests:
    # pip install android-sms-gateway[requests,encryption]
    ```
    Isso instalará a dependência `pycryptodome`.

*   **Criar uma instância de `Encryptor`**:
    A classe `android_sms_gateway.encryption.Encryptor` é usada para lidar com as operações de criptografia e descriptografia. Você precisa inicializá-la com a mesma frase secreta que configurou no aplicativo Android.

    ```python
    from android_sms_gateway.encryption import Encryptor

    minha_frase_secreta = "esta-e-minha-frase-secreta-muito-segura" # Substitua pela sua frase real
    encryptor = Encryptor(secret_phrase=minha_frase_secreta)
    ```

*   **Passar o `Encryptor` para o Cliente da API**:
    Ao inicializar `APIClient` ou `AsyncAPIClient`, passe a instância do `encryptor`.

    ```python
    from android_sms_gateway import client

    # Para APIClient (Síncrono)
    # api = client.APIClient(login, password, base_url, encryptor=encryptor)

    # Para AsyncAPIClient (Assíncrono)
    # async_api = client.AsyncAPIClient(login, password, base_url, encryptor=encryptor)
    ```

## Enviando Mensagens Criptografadas

Uma vez que o cliente da API esteja configurado com um `Encryptor`:

1.  Ao criar um objeto `domain.Message`, defina o atributo `is_encrypted=True`.

    ```python
    from android_sms_gateway import domain

    mensagem_criptografada = domain.Message(
        message="Este é um segredo!",
        phone_numbers=["+1234567890"],
        is_encrypted=True, # Importante!
        with_delivery_report=True
    )
    ```

2.  Envie a mensagem normalmente usando o método `send()` do cliente.

    ```python
    # Com APIClient síncrono
    # with client.APIClient(login, password, base_url, encryptor=encryptor) as api:
    #     state = api.send(mensagem_criptografada)
    #     print(f"Mensagem criptografada enviada. ID: {state.id}")
    #     print(f"Estava criptografada no envio? {state.is_encrypted}") # Deve ser True

    # Com AsyncAPIClient assíncrono
    # async with client.AsyncAPIClient(login, password, base_url, encryptor=encryptor) as async_api:
    #     state = await async_api.send(mensagem_criptografada)
    #     print(f"Mensagem criptografada enviada. ID: {state.id}")
    #     print(f"Estava criptografada no envio? {state.is_encrypted}") # Deve ser True
    ```

A biblioteca automaticamente:
*   Verificará se `is_encrypted` é `True`.
*   Usará o `Encryptor` fornecido para criptografar o `message.message`.
*   Enviará a mensagem com o payload criptografado e o sinalizador `isEncrypted: true` para a API do SMS Gateway.

O campo `MessageState.is_encrypted` no retorno indicará se a mensagem foi tratada como criptografada pelo gateway.

## Recebendo Mensagens Criptografadas (via Webhooks)

Se você estiver configurando webhooks para receber mensagens SMS de entrada através do SMS Gateway for Android, e essas mensagens foram criptografadas na origem (por outro sistema usando a mesma frase secreta), você precisará descriptografá-las.

O payload do webhook para uma mensagem recebida criptografada conteria o texto cifrado. Você usaria o método `decrypt` do `Encryptor`:

```python
# Suponha que 'encrypted_payload_from_webhook' é o conteúdo da mensagem criptografada
# recebida do webhook (geralmente em formato Base64).

# encryptor = Encryptor(secret_phrase="sua_mesma_frase_secreta") # Mesma instância

# try:
#     original_message = encryptor.decrypt(encrypted_payload_from_webhook)
#     print(f"Mensagem descriptografada: {original_message}")
# except Exception as e:
#     print(f"Falha ao descriptografar: {e}")
```
**Nota**: A biblioteca cliente `android-sms-gateway` em si é primariamente para *enviar* SMS. O tratamento de webhooks de *entrada* (mensagens MO - Mobile Originated) geralmente é feito pela sua aplicação que consome os webhooks. A interface web `sms-gateway-web` incluída neste projeto não lida, por padrão, com a descriptografia de mensagens recebidas via webhooks, pois seu foco é o envio.

## Considerações de Segurança

*   **Frase Secreta Forte**: Use uma frase secreta longa, complexa e única. Não a compartilhe desnecessariamente.
*   **Gerenciamento da Frase Secreta**: Armazene sua frase secreta de forma segura, por exemplo, em variáveis de ambiente, gerenciadores de segredos (como HashiCorp Vault, AWS Secrets Manager) ou arquivos de configuração protegidos. **Não a codifique diretamente no seu código de produção.**
*   **HTTPS**: Sempre use HTTPS para a comunicação com a API do SMS Gateway para proteger as credenciais da API e os metadados da mensagem, mesmo que o payload da mensagem esteja criptografado. A criptografia E2EE da mensagem protege o *conteúdo*, enquanto o HTTPS protege a *transmissão*.
*   **Consistência da Frase**: A frase secreta deve ser absolutamente idêntica entre o cliente Python (ao criar o `Encryptor`) e o aplicativo SMS Gateway for Android. Qualquer diferença resultará em falha na descriptografia.

A criptografia de ponta a ponta adiciona uma camada significativa de privacidade às suas comunicações SMS quando usada corretamente.
