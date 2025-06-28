# Deployment: Coolify

[Coolify](https://coolify.io/) é uma plataforma PaaS (Platform as a Service) auto-hospedável e de código aberto que simplifica o deploy e gerenciamento de aplicações. Este guia assume que você já tem uma instância do Coolify instalada e funcionando.

A interface `sms-gateway-web` é bem adequada para deploy no Coolify, pois ele tem excelente suporte para aplicações baseadas em Docker e Docker Compose.

**Pré-requisitos:**

*   Uma instância do Coolify V4 funcionando.
*   Um provedor Git conectado ao seu Coolify (GitHub, GitLab, etc.), onde o código do projeto `client-py` está hospedado (pode ser seu fork).
*   (Opcional, mas recomendado) Um nome de domínio que você pode apontar para a aplicação no Coolify.

## Passos para Deploy no Coolify

1.  **Prepare seu Repositório Git**:
    *   Certifique-se de que o diretório `sms-gateway-web` com seu `Dockerfile` e `docker-compose.yml` está presente no seu repositório Git.
    *   O `docker-compose.yml` padrão deve funcionar bem, mas revise-o:
        ```yaml
        version: '3.8'

        services:
          web: # O Coolify usará este nome de serviço
            build:
              context: ./sms-gateway-web # Caminho para o Dockerfile a partir da raiz do repo
              dockerfile: Dockerfile # Nome do Dockerfile dentro do contexto
            image: your-registry/sms-gateway-web:${COOLIFY_GIT_COMMIT_SHA:-latest} # Opcional: para registrar a imagem
            container_name: sms-gateway-web
            # Coolify gerencia as portas, então a seção 'ports' pode ser omitida ou ignorada.
            # Ele exporá a porta definida no Dockerfile (5000).
            volumes:
              # Coolify gerencia volumes. Você definirá isso na UI do Coolify.
              # O caminho interno do container que precisa de persistência é /root/.sms-gateway-web
              - /data/config:/root/.sms-gateway-web # Exemplo de mapeamento, será configurado na UI
            environment:
              - FLASK_ENV=production
              # Adicione mais ENVs se necessário, via UI do Coolify
            restart: unless-stopped
        ```
        **Ajustes para Coolify no `docker-compose.yml` (se você for usar o Docker Compose Engine do Coolify):**
        *   **`build.context`**: Deve ser o caminho para o diretório `sms-gateway-web` *a partir da raiz do seu repositório*. Se o `docker-compose.yml` está DENTRO de `sms-gateway-web`, o contexto é `.`. Se você está usando um `docker-compose.yml` na raiz do projeto para Coolify, o contexto seria `./sms-gateway-web`.
        *   **`image`**: Coolify pode construir a partir do Dockerfile diretamente. Se você quiser que Coolify use um `docker-compose.yml` de dentro do subdiretório, você pode precisar ajustar os caminhos no Coolify ou ter um `docker-compose.yml` na raiz do projeto especificamente para Coolify.
        *   **`volumes`**: Você definirá os volumes persistentes através da UI do Coolify. O importante é saber o caminho *dentro do container* que precisa ser persistido: `/root/.sms-gateway-web`.

    **Alternativa mais simples para Coolify: Usar o Build Pack "Dockerfile" em vez de "Docker Compose"**
    Se a aplicação é um único serviço Docker (como é o caso aqui), pode ser mais direto usar o build pack "Dockerfile" do Coolify. Neste caso, Coolify não usará seu `docker-compose.yml` diretamente para o build, mas sim o `Dockerfile`.

2.  **Crie uma Nova Aplicação no Coolify**:
    *   No seu dashboard Coolify, vá para "Applications" e clique em "Create new Application".
    *   **Choose Source**: Selecione seu provedor Git (GitHub, GitLab).
    *   **Select Repository & Branch**: Escolha o repositório `client-py` (ou seu fork) e a branch que você deseja deployar (ex: `main`, `master`).

3.  **Configure a Aplicação**:

    *   **Build Pack**:
        *   **Opção A (Recomendado para este caso simples): `Dockerfile`**
            *   **Install Command**: (Pode deixar em branco ou `pip install ...` se o Dockerfile não fizesse)
            *   **Build Command**: (Pode deixar em branco, o Dockerfile cuida disso)
            *   **Start Command**: (Pode deixar em branco, o `CMD` no Dockerfile cuida disso)
            *   **Dockerfile Location**: Se o Dockerfile está em `sms-gateway-web/Dockerfile`, coloque `/sms-gateway-web/Dockerfile`.
            *   **Base Directory**: Se seu Dockerfile precisa de contexto do diretório `sms-gateway-web/`, defina como `/sms-gateway-web/`.
        *   **Opção B: `Docker Compose`** (Mais complexo se o compose file não estiver na raiz)
            *   Coolify V4 tem melhorado o suporte a Docker Compose em subdiretórios.
            *   **Docker Compose Location**: Especifique o caminho para o `docker-compose.yml` a partir da raiz do repositório (ex: `/sms-gateway-web/docker-compose.yml`).
            *   Coolify tentará analisar e usar este arquivo.

    *   **General (Geral)**:
        *   **Name**: Dê um nome para sua aplicação (ex: `sms-gateway-web`).
        *   **FQDN(s)**: Defina o(s) domínio(s) ou subdomínio(s) para acessar sua aplicação (ex: `sms.meudominio.com`). Coolify pode gerenciar SSL para estes.

    *   **Network (Rede)**:
        *   **Port Mappings**: Coolify geralmente detecta a porta exposta pelo `Dockerfile` (EXPOSE 5000). Se não, configure para expor a porta `5000`.

    *   **Storage (Armazenamento)**:
        *   Esta é a parte crucial para persistência de dados.
        *   Clique em "Add Persistent Storage".
        *   **Path (Host)**: Este é o nome ou caminho do volume gerenciado pelo Coolify. Você pode deixar o Coolify gerar um, ou dar um nome significativo, ex: `sms_gateway_config_volume`.
        *   **Path (Container)**: **Importante**: Defina como `/root/.sms-gateway-web` (este é o diretório que a aplicação usa dentro do container para `config.json` e `sms_gateway.db`).

    *   **Environment Variables (Variáveis de Ambiente)**:
        *   Adicione `FLASK_ENV` com o valor `production`.
        *   Adicione quaisquer outras variáveis de ambiente que sua aplicação possa precisar. Para este projeto, normalmente não são necessárias outras além de `FLASK_ENV` pois as configurações são feitas via UI e salvas no volume.

4.  **Salve e Faça o Deploy**:
    *   Clique em "Save Configuration".
    *   Vá para a aba "Deployments" da sua aplicação.
    *   Clique em "Deploy" ou "Redeploy".

    Coolify irá clonar seu repositório, construir a imagem Docker (ou usar Docker Compose), configurar os volumes e rede, e iniciar sua aplicação. Você pode acompanhar os logs de build e deploy na UI do Coolify.

5.  **Configure DNS**:
    *   Se você definiu um FQDN, certifique-se de que seu DNS está configurado para apontar esse domínio/subdomínio para o endereço IP do seu servidor Coolify.
    *   Coolify (se configurado com um proxy como Traefik) deve automaticamente obter certificados SSL/TLS para o FQDN.

6.  **Configuração Inicial da Aplicação**:
    *   Acesse sua aplicação `sms-gateway-web` através do FQDN configurado.
    *   Vá para "Settings" na interface web.
    *   Configure as credenciais da API do seu SMS Gateway for Android (login, senha, URL base do celular).
        *   **URL Base do Gateway**: Se o seu celular com SMS Gateway está em uma rede diferente do seu servidor Coolify, você precisará de uma maneira de expor a API do SMS Gateway do celular para a internet (ex: usando um túnel como ngrok, Cloudflare Tunnel, ou configurando port forwarding no seu roteador - use com cautela e considere as implicações de segurança). A instância do Coolify precisa ser capaz de alcançar esta URL.
    *   Habilite a autenticação da aplicação na interface web e defina um nome de usuário e senha fortes.

## Atualizando a Aplicação no Coolify

1.  Faça push das suas alterações para a branch do Git que o Coolify está monitorando.
2.  No Coolify:
    *   Se você configurou webhooks de deploy automático, o Coolify pode detectar as alterações e redeployar automaticamente.
    *   Caso contrário, vá para sua aplicação no Coolify, na aba "Deployments", e clique em "Redeploy".

Coolify irá puxar as últimas alterações, reconstruir a imagem se necessário, e reiniciar a aplicação com o novo código, mantendo o volume de armazenamento persistente.

## Solução de Problemas

*   **Logs de Build/Deploy**: Sempre verifique os logs no Coolify para erros durante o build ou deploy.
*   **Acesso ao Volume**: Certifique-se de que o mapeamento do volume está correto (`/root/.sms-gateway-web` no container).
*   **Conectividade de Rede**:
    *   Verifique se o Coolify consegue acessar a URL base da API do SMS Gateway.
    *   Verifique as configurações de firewall no seu servidor Coolify e na rede do seu celular.
*   **FQDN e SSL**: Se estiver tendo problemas com o domínio ou SSL, verifique as configurações de DNS e os logs do proxy reverso do Coolify.

Deployar com Coolify pode simplificar muito o gerenciamento da sua aplicação `sms-gateway-web`, especialmente com seu manuseio de HTTPS, domínios e atualizações baseadas em Git.
