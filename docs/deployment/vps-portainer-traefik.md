# Deployment: VPS com Portainer + Traefik

Este guia detalha como fazer o deploy da interface `sms-gateway-web` em um Servidor Privado Virtual (VPS) usando Portainer para gerenciamento de containers Docker e Traefik como proxy reverso para lidar com HTTPS e roteamento de domínio.

**Pré-requisitos:**

*   Um VPS com um sistema operacional Linux (ex: Ubuntu).
*   Acesso root ou sudo ao VPS.
*   Docker e Docker Compose instalados no VPS.
*   Portainer instalado e funcionando no VPS. (Veja [documentação do Portainer](https://docs.portainer.io/start/install-ce/server/docker/linux) para instalação).
*   Traefik instalado e configurado como um serviço Docker no VPS. (Veja [documentação do Traefik](https://doc.traefik.io/traefik/getting-started/quick-start-with-docker/) e [Traefik com Docker Compose](https://doc.traefik.io/traefik/user-guides/docker-compose/basic-example/)).
    *   Traefik deve estar configurado para usar um resolvedor de certificados (ex: Let's Encrypt) para SSL.
    *   Traefik deve estar escutando nas portas 80 e 443 e conectado a uma rede Docker (ex: `traefik_proxy`).
*   Um nome de domínio apontando para o endereço IP do seu VPS.
*   Git instalado no VPS.

## Estrutura de Deploy

1.  **Traefik**: Atua como o ponto de entrada para o tráfego web, lida com certificados SSL e roteia o tráfego para o container `sms-gateway-web` com base no nome do host.
2.  **Portainer**: Usado para gerenciar o stack Docker Compose da aplicação `sms-gateway-web`.
3.  **Aplicação `sms-gateway-web`**: Rodará como um container Docker, construído a partir do `Dockerfile` do projeto.

## Passos para Deploy

### 1. Preparar o Ambiente no VPS

*   **Conecte-se ao seu VPS via SSH.**
*   **Clone o repositório do projeto**:
    ```bash
    git clone https://github.com/prof-gabrielramos/client-py.git
    cd client-py/sms-gateway-web
    ```
    Ou, se for seu fork privado, clone-o.

### 2. Ajustar `docker-compose.yml` para Traefik

Modifique o arquivo `sms-gateway-web/docker-compose.yml` para incluir labels que o Traefik usará para descobrir e configurar o roteamento para o serviço.

```yaml
version: '3.8'

services:
  web:
    build: .
    image: sms-gateway-web:latest # Considere usar tags específicas para produção
    container_name: sms-gateway-web
    restart: unless-stopped
    volumes:
      # Escolha um local seguro e persistente no seu VPS para os dados de configuração.
      # Ex: /opt/docker_data/sms_gateway_web_config:/root/.sms-gateway-web
      # Certifique-se de que este diretório no host exista e tenha permissões adequadas.
      - ./config:/root/.sms-gateway-web # Simples para começar, mas considere um caminho absoluto
    environment:
      - FLASK_ENV=production
      # - GUNICORN_CMD_ARGS=--workers=2 # Exemplo se você modificar o Dockerfile para usar Gunicorn
    networks:
      - traefik_proxy # Nome da rede Docker que o Traefik está usando
      # - default # Mantém a rede default do compose se precisar de links internos
    labels:
      - "traefik.enable=true"
      # Substitua 'sms.seudominio.com' pelo seu domínio/subdomínio real
      - "traefik.http.routers.sms-gateway-web.rule=Host(`sms.seudominio.com`)"
      - "traefik.http.routers.sms-gateway-web.entrypoints=websecure" # Assumindo que 'websecure' é seu entrypoint HTTPS no Traefik
      - "traefik.http.services.sms-gateway-web.loadbalancer.server.port=5000" # A porta interna do container Flask
      - "traefik.http.routers.sms-gateway-web.tls.certresolver=myresolver" # Substitua 'myresolver' pelo nome do seu cert resolver no Traefik
      # Opcional: Adicionar middleware (ex: para headers de segurança)
      # - "traefik.http.routers.sms-gateway-web.middlewares=secHeaders@file"

networks:
  traefik_proxy: # Define a rede externa que o Traefik usa
    external: true
  # default: # A rede default do compose ainda pode ser definida se necessário
  #   driver: bridge
```

**Notas sobre o `docker-compose.yml` acima:**

*   **`volumes`**: É crucial. `- ./config:/root/.sms-gateway-web` mapeia um diretório `config` (relativo ao `docker-compose.yml`) para o local de configuração dentro do container. Para produção, você pode preferir um caminho absoluto no host (ex: `/srv/docker/sms-gateway-web/config`) ou um volume nomeado do Docker. Certifique-se de que o diretório no host exista.
*   **`networks`**:
    *   `traefik_proxy`: Este deve ser o nome da rede Docker à qual seu container Traefik está conectado. Verifique a configuração do seu Traefik. Se for diferente, ajuste o nome. Declarar como `external: true` significa que o Docker Compose não tentará criar esta rede, mas sim usar uma existente.
*   **`labels`**:
    *   `traefik.enable=true`: Habilita o Traefik para este serviço.
    *   `Host(\`sms.seudominio.com\`)`: Define o domínio que o Traefik usará para rotear para este serviço. **Substitua pelo seu domínio real.**
    *   `entrypoints=websecure`: Diz ao Traefik para usar o entrypoint HTTPS (geralmente chamado `websecure` e configurado para escutar na porta 443).
    *   `loadbalancer.server.port=5000`: Informa ao Traefik que o serviço `sms-gateway-web` está escutando na porta 5000 dentro do container.
    *   `tls.certresolver=myresolver`: Diz ao Traefik para usar seu resolvedor de certificados configurado (ex: Let's Encrypt, geralmente nomeado `myresolver`, `le`, ou similar na configuração do Traefik) para obter um certificado SSL para o domínio. **Substitua pelo nome do seu resolvedor.**

### 3. Deploy com Portainer Stacks

1.  **Acesse sua interface Portainer** no navegador.
2.  Vá para **Stacks** no menu lateral.
3.  Clique em **+ Add stack**.
4.  **Configuração do Stack**:
    *   **Name**: Dê um nome para seu stack (ex: `sms-gateway-stack`).
    *   **Build method**: Escolha **Git Repository**.
        *   **Repository URL**: URL do seu repositório Git (ex: `https://github.com/prof-gabrielramos/client-py.git`).
        *   **Repository reference**: `refs/heads/main` (ou a branch que você quer deployar).
        *   **Compose path**: Caminho para o arquivo `docker-compose.yml` dentro do repositório. Se você clonou `client-py` e o arquivo está em `sms-gateway-web/docker-compose.yml`, então o caminho é `sms-gateway-web/docker-compose.yml`.
        *   **Skip Pull** (Deixe desmarcado para puxar a última versão).
    *   **Environment variables**: Você pode adicionar variáveis de ambiente aqui se necessário, mas para este projeto, `FLASK_ENV=production` já está no compose file.
5.  Clique em **Deploy the stack**.

Portainer irá:
*   Puxar o código do seu repositório Git.
*   Usar o `docker-compose.yml` especificado para construir a imagem Docker (se `build: .` estiver presente e a imagem não existir localmente com a tag esperada) e iniciar os containers.
*   Conectar o container à rede `traefik_proxy`.

Traefik deve detectar automaticamente o novo serviço através das labels do Docker e começar a rotear o tráfego do seu domínio para ele, incluindo a obtenção de um certificado SSL.

### 4. Verifique o Deploy

*   **Logs no Portainer**: Verifique os logs do container `sms-gateway-web` no Portainer para garantir que ele iniciou sem erros.
*   **Logs do Traefik**: Verifique os logs do seu container Traefik para ver se ele detectou o novo serviço e se há algum erro relacionado a certificados ou roteamento.
*   **Acesse sua Aplicação**: Abra seu navegador e vá para o domínio que você configurou (ex: `https://sms.seudominio.com`). Você deve ver a interface `sms-gateway-web`.

### 5. Configuração Inicial da Aplicação

*   Acesse a interface `sms-gateway-web` através do seu domínio.
*   Vá para "Settings".
*   Configure os detalhes da API do seu SMS Gateway for Android (login, senha, URL base do celular).
    *   **URL Base do Gateway**: Seu VPS (onde o Traefik e `sms-gateway-web` rodam) precisa conseguir alcançar a API do seu celular. Se o celular estiver em uma rede local diferente, você precisará expor a API do SMS Gateway do celular para a internet de forma segura (ngrok, Cloudflare Tunnel, port forwarding com DDNS, etc.) e usar essa URL pública aqui.
*   Habilite a autenticação da aplicação na interface web e defina um nome de usuário e senha fortes.

## Atualizando a Aplicação

1.  Faça push das suas alterações para a branch Git que o Portainer está monitorando.
2.  Em Portainer:
    *   Vá para o seu Stack (`sms-gateway-stack`).
    *   Na seção "Stack details", você pode encontrar informações sobre o Git.
    *   Para atualizar:
        *   Clique em **"Pull and redeploy"** (ou uma opção similar que puxe as últimas alterações do Git e recrie os containers). Se esta opção não estiver visível diretamente, você pode precisar ir em "Editor", certificar-se que "Re-pull image" (se aplicável a imagens pré-construídas) ou uma opção de reconstrução está ativa, e clicar em "Update the stack". Portainer V2.9+ tem melhorado a integração com Git.
        *   Se você alterou o `docker-compose.yml` no Git, Portainer deve aplicar essas alterações.
        *   Se o `Dockerfile` ou código fonte mudou, Portainer (via Docker Compose) deve reconstruir a imagem.

## Backup

*   **Dados da Aplicação**: Faça backup regularmente do diretório no host que você mapeou para `/root/.sms-gateway-web` no container (ex: `/opt/docker_data/sms_gateway_web_config/` ou o diretório `./config` se você usou um caminho relativo e sabe onde ele está no seu VPS). Este diretório contém `config.json` e `sms_gateway.db`.
*   **Configuração do Portainer/Traefik**: Também é uma boa ideia ter backups das configurações do Portainer e do Traefik.

Este método de deploy fornece uma solução robusta e escalável, com gerenciamento de HTTPS e fácil atualização através do Portainer e Git.
