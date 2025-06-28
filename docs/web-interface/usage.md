# Interface Web: Uso

Depois que a interface `sms-gateway-web` estiver instalada, configurada e em execução, você poderá usá-la para gerenciar suas mensagens SMS.

## Acessando a Interface

Abra seu navegador e navegue até o endereço onde a aplicação está hospedada (por exemplo, `http://localhost:5000`). Se a autenticação estiver habilitada, você será solicitado a fazer login com o nome de usuário e senha da aplicação que você configurou.

## Seções Principais

A interface é dividida em várias seções acessíveis através do menu de navegação:

### 1. Dashboard

*   **Visão Geral**: Exibe um resumo da atividade recente, como o número de mensagens enviadas, status de entrega recentes e possivelmente outras estatísticas.
*   **Links Rápidos**: Pode fornecer botões para ações comuns, como "Enviar Nova Mensagem".

### 2. Send (Enviar)

Esta é a seção principal para compor e enviar novas mensagens SMS.

*   **Recipients (Destinatários)**: Insira um ou mais números de telefone.
    *   Múltiplos números devem ser separados por vírgula (ex: `+1234567890, +0987654321`).
    *   Você pode usar números de contatos salvos digitando o nome do contato (o sistema deve sugerir).
*   **Message (Mensagem)**: Digite o texto da sua mensagem SMS.
    *   Um contador de caracteres pode estar presente para ajudá-lo a ficar dentro dos limites de SMS (normalmente 160 caracteres por SMS, mensagens mais longas podem ser divididas em várias partes).
*   **SIM Card (Chip SIM)**: Se o seu dispositivo Android conectado tiver múltiplos SIM cards, você poderá selecionar qual SIM usar para enviar a mensagem. Deixe como "Any" (Qualquer) para permitir que o SMS Gateway decida.
*   **With Delivery Report (Com Relatório de Entrega)**: Marque esta caixa se desejar solicitar um relatório de entrega para a mensagem. Isso permite que você acompanhe se a mensagem foi entregue ao destinatário.
*   **Is Encrypted (Criptografada)**: Esta opção só estará disponível e funcional se você tiver configurado uma "Encryption Key" (Chave de Criptografia) nas Configurações que corresponda à frase secreta no seu aplicativo SMS Gateway.
    *   Se marcada, a mensagem será criptografada antes de ser enviada para a API do SMS Gateway. O aplicativo no celular precisará da mesma chave para descriptografá-la antes de enviar via rede da operadora.
*   **Send Button (Botão Enviar)**: Clique para enviar a mensagem.

Após o envio, você geralmente será redirecionado para a página de "Messages" ou verá uma notificação de status.

### 3. Messages (Mensagens)

Esta seção exibe um histórico de todas as mensagens enviadas através da interface web.

*   **Lista de Mensagens**: Cada entrada normalmente mostra:
    *   ID da Mensagem
    *   Destinatário(s)
    *   Trecho da mensagem
    *   Status (ex: Pending, Sent, Delivered, Failed)
    *   Data e Hora
*   **Detalhes da Mensagem**: Clicar em uma mensagem pode mostrar informações mais detalhadas, incluindo o status para cada destinatário individualmente se a mensagem foi enviada para múltiplos números.
*   **Filtros e Paginação**: Se houver muitas mensagens, podem existir opções para filtrar por status ou data, e paginação para navegar pelo histórico.
*   **Atualizar Status**: Pode haver um botão para atualizar manualmente o status das mensagens pendentes.

### 4. Contacts (Contatos)

Permite gerenciar uma lista simples de contatos para facilitar o envio de mensagens.

*   **View Contacts (Visualizar Contatos)**: Lista os contatos existentes com nome e número de telefone.
*   **Add Contact (Adicionar Contato)**: Formulário para adicionar um novo contato:
    *   **Name (Nome)**: Nome do contato.
    *   **Phone Number (Número de Telefone)**: Número de telefone do contato (em formato internacional, ex: `+1234567890`).
*   **Edit/Delete Contact (Editar/Excluir Contato)**: Opções para modificar ou remover contatos existentes.

Ao enviar uma mensagem, se você começar a digitar um nome de contato no campo "Recipients", a interface pode sugerir automaticamente o número correspondente.

### 5. Webhooks

Webhooks permitem que a API do SMS Gateway notifique sua interface `sms-gateway-web` (ou qualquer outro serviço) sobre eventos relacionados às mensagens. A interface web pode usar isso para atualizar o status das mensagens automaticamente.

*   **View Webhooks (Visualizar Webhooks)**: Lista os webhooks atualmente configurados com a API do SMS Gateway.
    *   Cada webhook terá uma URL de destino e um tipo de evento ao qual está inscrito (ex: `MESSAGE_SENT`, `MESSAGE_DELIVERED`, `MESSAGE_FAILED`).
*   **Create Webhook (Criar Webhook)**:
    *   **URL**: A URL que a API do SMS Gateway chamará quando o evento ocorrer. Para a própria interface `sms-gateway-web`, isso geralmente é uma URL interna da aplicação (ex: `http://<host_da_interface_web>/webhook_callbacks`).
    *   **Event Type (Tipo de Evento)**: Selecione o evento que acionará o webhook.
    *   **Nota**: A interface `sms-gateway-web` pode gerenciar automaticamente seus próprios webhooks para atualização de status. Esta seção pode ser mais para visualização ou gerenciamento avançado.

### 6. Settings (Configurações)

Esta seção já foi detalhada na página [Configuração](./configuration.md). É onde você gerencia:

*   Conexão com a API do SMS Gateway (credenciais, URL, chave de criptografia).
*   Configurações da aplicação (autenticação, nome de usuário/senha da aplicação, mensagens por página).

## Fluxo de Trabalho Típico

1.  **Configurar**: Na primeira vez, vá para "Settings" e configure os detalhes da API do SMS Gateway e, opcionalmente, a autenticação da aplicação.
2.  **Adicionar Contatos (Opcional)**: Vá para "Contacts" para adicionar números frequentemente usados.
3.  **Enviar Mensagem**: Vá para "Send", componha sua mensagem, adicione destinatários e envie.
4.  **Verificar Status**: Vá para "Messages" para ver o histórico e o status das mensagens enviadas. O status pode levar algum tempo para ser atualizado de "Sent" para "Delivered", dependendo da rede da operadora e da configuração de webhooks.
5.  **Ajustar Configurações**: Retorne a "Settings" se precisar alterar alguma configuração.

Lembre-se de que a funcionalidade de entrega e o status dependem do correto funcionamento do aplicativo SMS Gateway for Android no seu celular e da sua conexão com a rede da operadora. A interface web é um cliente para essa API.
