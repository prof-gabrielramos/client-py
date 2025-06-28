# Interface Web: Configuração

Após instalar e executar a interface web `sms-gateway-web` pela primeira vez, você precisará configurá-la para se conectar à sua instância do SMS Gateway for Android™ e, opcionalmente, proteger a interface com autenticação.

A configuração é feita através da própria interface web, na seção "Settings" (Configurações).

## Acessando as Configurações

1.  Com a aplicação rodando, acesse a interface web (normalmente [http://localhost:5000](http://localhost:5000)).
2.  No menu de navegação, clique em "Settings".

## Opções de Configuração

As seguintes seções de configuração estão disponíveis:

### 1. Gateway Settings (Configurações do Gateway)

Aqui você define como a interface web se conectará à API do seu SMS Gateway for Android.

*   **Gateway API Login**: O nome de usuário que você configurou no aplicativo SMS Gateway for Android para acesso à API.
*   **Gateway API Password**: A senha que você configurou no aplicativo SMS Gateway for Android para acesso à API.
*   **Gateway Base URL**: A URL base da API do seu SMS Gateway.
    *   Se o seu celular e o servidor que roda a interface web estão na mesma rede, isso geralmente será algo como `http://<IP_DO_CELULAR>:8080`. O IP do celular é exibido no aplicativo SMS Gateway.
    *   Se você estiver usando um serviço de túnel ou proxy reverso, use a URL pública correspondente.
    *   O valor padrão para a API pública do `sms-gate.app` é `https://api.sms-gate.app/3rdparty/v1`, mas este cliente é tipicamente para gateways auto-hospedados.
*   **Encryption Key (Chave de Criptografia)**: Se você planeja enviar mensagens criptografadas de ponta a ponta e configurou uma frase secreta no aplicativo SMS Gateway for Android, insira a **mesma frase secreta** aqui. Deixe em branco se não estiver usando criptografia de ponta a ponta.
    *   **Importante**: A criptografia é opcional. Se uma chave for fornecida aqui, você terá a opção de marcar mensagens como "criptografadas" ao enviá-las. O aplicativo SMS Gateway no celular também deve ter a mesma frase secreta configurada para descriptografar as mensagens.

### 2. Application Settings (Configurações da Aplicação)

Estas configurações controlam o comportamento da própria interface web.

*   **Enable Authentication (Habilitar Autenticação)**: Marque esta caixa para proteger o acesso à interface web com um nome de usuário e senha.
    *   Se habilitado, os campos "Application Username" e "Application Password" se tornarão obrigatórios.
*   **Application Username (Nome de Usuário da Aplicação)**: O nome de usuário para fazer login na interface `sms-gateway-web`. Necessário se a autenticação estiver habilitada.
*   **Application Password (Senha da Aplicação)**: A senha para fazer login na interface `sms-gateway-web`. Necessário se a autenticação estiver habilitada.
    *   **Nota de Segurança**: Escolha uma senha forte.
*   **Messages per Page (Mensagens por Página)**: Quantas mensagens serão exibidas por página na seção "Messages".

## Salvando as Configurações

Após fazer as alterações desejadas, clique no botão "Save Settings" (Salvar Configurações) no final da página.

*   Se a autenticação for habilitada (ou as credenciais forem alteradas), você pode ser desconectado e solicitado a fazer login com as novas credenciais.

## Local do Arquivo de Configuração

As configurações são armazenadas em um arquivo `config.json`.

*   **Ao usar Docker**: O arquivo está localizado em `/root/.sms-gateway-web/config.json` dentro do container, que é mapeado para `sms-gateway-web/config/config.json` no seu sistema host (graças à configuração de volume no `docker-compose.yml`).
*   **Ao rodar manualmente**: O arquivo está localizado em `~/.sms-gateway-web/config.json` no seu sistema.

**Nunca edite o `config.json` diretamente enquanto a aplicação estiver rodando, pois suas alterações podem ser sobrescritas.** Use sempre a interface web para modificar as configurações.

## Solução de Problemas

*   **Não consigo conectar ao gateway**:
    *   Verifique se o aplicativo SMS Gateway for Android está rodando no seu celular.
    *   Confirme se o celular e o servidor da interface web podem se comunicar (mesma rede, firewall não bloqueando a porta).
    *   Verifique se a "Gateway Base URL", "Gateway API Login" e "Gateway API Password" estão corretas e correspondem exatamente ao que está configurado no aplicativo SMS Gateway.
    *   Tente acessar a "Gateway Base URL" diretamente do navegador ou usando `curl` do servidor onde a interface web está rodando para ver se a API do gateway está acessível.
*   **Esqueci a senha da aplicação**:
    *   Se você tiver acesso ao sistema de arquivos onde `config.json` está armazenado:
        1.  Pare a aplicação `sms-gateway-web`.
        2.  Abra o arquivo `config.json`.
        3.  Você pode remover as chaves `"app_username"` e `"app_password"` ou definir `"enable_authentication": false`.
        4.  Salve o arquivo e reinicie a aplicação. Agora você deve conseguir acessar as configurações sem login para redefinir a senha.
    *   **CUIDADO**: Este procedimento de recuperação de senha expõe temporariamente sua aplicação se ela estiver acessível publicamente. Faça isso rapidamente e reabilite a autenticação com uma nova senha.

Com as configurações corretas, você estará pronto para usar todas as funcionalidades da interface web. Prossiga para a seção [Uso](./usage.md).
