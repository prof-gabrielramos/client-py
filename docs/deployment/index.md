# Deployment: Visão Geral

Esta seção da documentação aborda como fazer o deploy da interface web `sms-gateway-web`. A biblioteca cliente Python `android-sms-gateway` em si é uma biblioteca e é integrada em suas aplicações Python, não "deployada" da mesma forma.

## Foco do Deploy: Interface Web (`sms-gateway-web`)

A interface web é uma aplicação Flask que foi projetada para ser facilmente containerizada usando Docker. Portanto, os guias de deploy se concentrarão em cenários que utilizam Docker.

**Principais considerações para o deploy:**

1.  **Persistência de Dados**: A interface web armazena sua configuração (conexão da API, credenciais da aplicação) e o histórico de mensagens/contatos em um diretório. No Docker, isso é gerenciado montando um volume. Você precisa garantir que este volume seja persistente entre reinicializações e atualizações do container.
    *   Local no container: `/root/.sms-gateway-web/`
    *   Conteúdo: `config.json` (configurações), `sms_gateway.db` (banco de dados SQLite)

2.  **Variáveis de Ambiente**: Embora muitas configurações sejam feitas via interface web, `FLASK_ENV=production` é definida no `docker-compose.yml`. Você pode precisar de outras variáveis de ambiente dependendo da sua configuração de proxy reverso ou plataforma de hospedagem.

3.  **Acesso à Rede**:
    *   O container da interface web precisa ser capaz de fazer requisições HTTP de saída para a URL base da API do seu SMS Gateway for Android (o celular).
    *   Se você configurar webhooks para que o SMS Gateway notifique a interface web (para atualizações de status, por exemplo), o celular precisará ser capaz de fazer requisições HTTP de entrada para a URL da interface web. Isso geralmente requer que a interface web seja acessível publicamente ou que haja um túnel/proxy configurado.

4.  **Segurança**:
    *   **HTTPS**: Para qualquer deploy em produção, você deve servir a interface web sobre HTTPS. Isso geralmente é tratado por um proxy reverso (como Nginx ou Traefik) que lida com os certificados SSL/TLS e encaminha o tráfego para o container da aplicação Flask.
    *   **Autenticação da Aplicação**: Use o recurso de autenticação embutido na interface web ("Settings" -> "Enable Authentication") para proteger o acesso.
    *   **Credenciais da API do Gateway**: As credenciais para o SMS Gateway for Android são armazenadas no `config.json` (persistido no volume). Proteja o acesso a este volume.

## Métodos de Deploy Cobertos

Os seguintes guias fornecem instruções para plataformas e métodos específicos:

*   **[Docker (Geral)](./docker.md)**: Princípios básicos para deploy usando o `Dockerfile` e `docker-compose.yml` fornecidos em um servidor genérico com Docker.
*   **[Coolify](./coolify.md)**: Como fazer deploy em uma instância do [Coolify](https://coolify.io/), uma plataforma PaaS auto-hospedável de código aberto.
*   **[VPS com Portainer + Traefik](./vps-portainer-traefik.md)**: Um guia para deploy em um Servidor Privado Virtual (VPS) usando Portainer para gerenciamento de Docker e Traefik como proxy reverso para HTTPS e roteamento.

## Antes de Começar

*   **Tenha o SMS Gateway for Android funcionando**: Certifique-se de que seu dispositivo Android com o aplicativo SMS Gateway está configurado, conectado à rede e a API está habilitada e testada.
*   **Escolha um método de deploy**: Familiarize-se com as opções e escolha aquela que melhor se adapta à sua infraestrutura e conhecimento técnico.
*   **Considere DNS e Nomes de Domínio**: Se você planeja acessar a interface web publicamente, precisará de um nome de domínio e configurar os registros DNS apropriados.

Selecione um dos guias de deploy no menu para instruções detalhadas.
