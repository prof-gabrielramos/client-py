# Interface Web: Visão Geral

A interface web `sms-gateway-web` fornece uma maneira amigável de interagir com a funcionalidade de envio de SMS oferecida pela biblioteca `android-sms-gateway`. Construída com Flask, ela permite que você:

*   Envie mensagens SMS para destinatários individuais ou múltiplos.
*   Visualize o histórico de mensagens e o status de entrega.
*   Gerencie as configurações de conexão do SMS Gateway.
*   Mantenha um gerenciamento simples de contatos para destinatários frequentes.
*   Configure webhooks para notificações de eventos (mensagem enviada, entregue, falha, etc.).

## Funcionalidades Principais

*   **Dashboard**: Uma visão geral das mensagens recentes e estatísticas básicas.
*   **Enviar SMS**: Componha e envie mensagens facilmente.
*   **Histórico de Mensagens**: Navegue pelo histórico de mensagens enviadas com informações de status.
*   **Contatos**: Gerencie uma lista de contatos para facilitar o envio para números usados com frequência.
*   **Webhooks**: Configure URLs para receber notificações de eventos do ciclo de vida das mensagens.
*   **Configurações**:
    *   Configure os detalhes de conexão com a API do SMS Gateway (login, senha, URL base).
    *   Habilite ou desabilite a autenticação para proteger o acesso à interface web.
    *   Gerencie as configurações de criptografia (se aplicável).

## Tecnologia

*   **Backend**: Python com [Flask](https://flask.palletsprojects.com/)
*   **Frontend**: HTML, CSS (templates Jinja2)
*   **Banco de Dados**: SQLite (para armazenar histórico de mensagens local, contatos e configurações)
*   **Containerização**: Docker e Docker Compose para fácil execução e deploy.

## Próximos Passos

*   [Instalação e Execução](./installation.md)
*   [Configuração](./configuration.md)
*   [Uso](./usage.md)
