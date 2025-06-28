# Cliente Python API: Visão Geral

A `android-sms-gateway` é uma biblioteca cliente Python moderna e robusta projetada para uma integração transparente com a API do [SMS Gateway for Android™](https://sms-gate.app/). Ela permite que você envie mensagens SMS programaticamente através dos seus dispositivos Android de forma eficiente e fácil.

Esta biblioteca é ideal para desenvolvedores que precisam incorporar funcionalidades de envio de SMS em suas aplicações Python, seja para notificações, alertas, automações ou qualquer outro caso de uso que envolva comunicação via SMS.

## Funcionalidades Principais

*   🚀 **Cliente Duplo**: Oferece suporte tanto para interfaces síncronas (`APIClient`) quanto assíncronas (`AsyncAPIClient`), permitindo flexibilidade para diferentes arquiteturas de aplicação.
*   🔒 **Criptografia de Ponta a Ponta**: Suporta criptografia opcional de mensagens usando AES-CBC-256, garantindo que o conteúdo das mensagens permaneça confidencial entre o cliente e o dispositivo Android que envia o SMS.
*   🌐 **Múltiplos Backends HTTP**: Suporte nativo para bibliotecas HTTP populares como `requests` (síncrono), `aiohttp` (assíncrono) e `httpx` (síncrono e assíncrono). A biblioteca detecta automaticamente o cliente HTTP disponível ou permite que você especifique um.
*   🔗 **Gerenciamento de Webhooks**: Permite criar, consultar e excluir webhooks programaticamente para receber notificações sobre eventos de mensagens (enviada, entregue, falha, etc.).
*   ⚙️ **URL Base Personalizável**: Flexibilidade para apontar para diferentes endpoints da API, útil para gateways auto-hospedados ou configurações de proxy.
*   📝 **Type Hinting Completo**: Totalmente tipada com type hints do Python, proporcionando uma excelente experiência de desenvolvimento com checagem de tipos estática e melhor autocompletar em IDEs.
*   🛡️ **Tratamento de Erros Robusto**: Define exceções específicas para diferentes tipos de erros da API, com mensagens claras para facilitar a depuração.
*   📊 **Relatórios de Entrega**: Permite solicitar e consultar relatórios de entrega para rastrear o status das mensagens enviadas.

## Casos de Uso Comuns

*   Envio de códigos de autenticação de dois fatores (2FA).
*   Notificações de sistema e alertas.
*   Lembretes de compromissos.
*   Marketing por SMS (respeitando as regulamentações).
*   Automação de respostas ou interações baseadas em SMS.
*   Integração com sistemas de CRM ou ERP para comunicação com clientes.

## Próximos Passos

*   **[Instalação](./installation.md)**: Como instalar a biblioteca no seu projeto.
*   **[Primeiros Passos](./first-steps.md)**: Um guia rápido para enviar sua primeira mensagem.
*   **[Guia do Cliente](./client-guide.md)**: Detalhes sobre a configuração do cliente, métodos disponíveis e estruturas de dados.
*   **[Criptografia](./encryption.md)**: Como usar a funcionalidade de criptografia de ponta a ponta.

Esta documentação foca no uso da biblioteca cliente Python. Para informações sobre a interface web que utiliza esta biblioteca, consulte a seção [Interface Web](../web-interface/index.md).
Para informações sobre a API REST subjacente do SMS Gateway for Android™, consulte a [documentação oficial da API](https://docs.sms-gate.app/integration/api/).
