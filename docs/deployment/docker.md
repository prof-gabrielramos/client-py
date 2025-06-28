# Deployment: Docker (Geral)

Esta página descreve como fazer o deploy da interface `sms-gateway-web` usando Docker e Docker Compose em um servidor genérico que já tenha Docker e Docker Compose instalados. Este é o método fundamental e a base para muitos outros tipos de deploy.

**Pré-requisitos:**

*   Um servidor (VPS, dedicado, ou máquina local) com Docker e Docker Compose instalados.
*   Acesso de terminal ao servidor.
*   Git instalado no servidor para clonar o repositório.
*   (Opcional, mas recomendado para produção) Um proxy reverso como Nginx ou Traefik configurado para gerenciar HTTPS e acesso externo. Este guia foca apenas em rodar o container da aplicação.

## Passos para Deploy

1.  **Conecte-se ao seu servidor** via SSH.

2.  **Clone o Repositório**:
    Se o código ainda não estiver no servidor, clone-o:
    ```bash
    git clone https://github.com/prof-gabrielramos/client-py.git
    cd client-py/sms-gateway-web
    ```
    Se você já tem o código e quer atualizá-lo:
    ```bash
    cd /path/to/client-py
    git pull
    cd sms-gateway-web
    ```

3.  **Revise o `docker-compose.yml`**:
    O arquivo `sms-gateway-web/docker-compose.yml` fornecido é uma boa base:
    ```yaml
    version: '3.8'

    services:
      web:
        build: .
        image: sms-gateway-web:latest # Você pode querer usar tags específicas em produção
        container_name: sms-gateway-web
        ports:
          # Se você usar um proxy reverso, pode não precisar expor a porta diretamente.
          # O proxy reverso se conectaria à rede Docker do container na porta 5000.
          # Exemplo: - "127.0.0.1:5000:5000" para acesso apenas local pelo proxy.
          - "5000:5000"
        volumes:
          # MUITO IMPORTANTE: Garanta que este caminho no host seja adequado e seguro.
          # Este volume persistirá config.json e sms_gateway.db
          - ./config:/root/.sms-gateway-web
          # Alternativa: Usar um volume nomeado do Docker (mais gerenciado pelo Docker)
          # - sms_gateway_data:/root/.sms-gateway-web
        environment:
          - FLASK_ENV=production
          # Adicione outras variáveis de ambiente se necessário
        restart: unless-stopped

    # Se usar um volume nomeado, defina-o aqui:
    # volumes:
    #   sms_gateway_data:
    ```

    **Considerações Chave para Produção:**
    *   **`ports`**: Se estiver usando um proxy reverso (como Nginx ou Traefik) que também roda em Docker e está na mesma rede Docker, você pode remover a seção `ports` ou ligá-la apenas a `127.0.0.1` (ex: `127.0.0.1:5000:5000`). O proxy reverso então encaminharia o tráfego para `sms-gateway-web:5000` (nome do serviço e porta interna do container). Se você não tem um proxy reverso e quer acesso direto (menos seguro para produção), ` "5000:5000"` funciona, mas certifique-se de que seu firewall está configurado corretamente.
    *   **`volumes`**: O mapeamento `- ./config:/root/.sms-gateway-web` cria um diretório `config` dentro do seu diretório `sms-gateway-web` no host e o mapeia. Isso é simples. Para um gerenciamento mais robusto pelo Docker, considere usar um [volume nomeado](https://docs.docker.com/storage/volumes/).
        Para usar um volume nomeado:
        1.  Mude `volumes` para `- sms_gateway_data:/root/.sms-gateway-web`
        2.  Adicione no final do arquivo:
            ```yaml
            volumes:
              sms_gateway_data:
            ```
            O Docker gerenciará a localização deste volume (geralmente em `/var/lib/docker/volumes/`). Backups deste volume precisariam ser tratados de acordo.
    *   **`image`**: Usar `sms-gateway-web:latest` é conveniente, mas para controlar versões, você pode construir e dar tag à sua imagem (ex: `sms-gateway-web:1.0.2`) e usar essa tag no compose file.
    *   **Redes (Networking)**: Se estiver usando um proxy reverso como Traefik em uma rede Docker separada, você precisará garantir que o container `sms-gateway-web` esteja conectado a essa mesma rede Docker para que o Traefik possa rotear o tráfego para ele. Isso é feito com a diretiva `networks` no `docker-compose.yml`.

4.  **Construa e Inicie os Containers**:
    No diretório `sms-gateway-web` (onde está o `docker-compose.yml`):
    ```bash
    docker-compose up --build -d
    ```
    *   `--build`: Constrói a imagem a partir do `Dockerfile` se ela não existir ou se o `Dockerfile` ou o código fonte tiverem mudado.
    *   `-d`: Executa os containers em modo detached (em segundo plano).

5.  **Verifique os Logs (Opcional)**:
    Para ver se o container iniciou corretamente:
    ```bash
    docker-compose logs -f
    ```
    Pressione `Ctrl+C` para sair dos logs.

6.  **Acesse a Aplicação**:
    *   Se você mapeou a porta diretamente (ex: `5000:5000`) e seu firewall permite, você deve conseguir acessar a interface em `http://<IP_DO_SERVIDOR>:5000`.
    *   Se estiver usando um proxy reverso, acesse através do domínio que você configurou no proxy (ex: `https://sms.seusite.com`).

7.  **Configuração Inicial**:
    Acesse a interface web e vá para "Settings" para:
    *   Configurar os detalhes da API do seu SMS Gateway for Android (login, senha, URL base do celular).
    *   Habilitar a autenticação da aplicação e definir um nome de usuário e senha fortes para a própria interface web.

## Atualizando a Aplicação

1.  **Obtenha o Código Mais Recente**:
    No seu servidor, navegue até o diretório do projeto e puxe as últimas alterações do Git:
    ```bash
    cd /path/to/client-py
    git pull
    cd sms-gateway-web
    ```

2.  **Reconstrua e Reinicie os Containers**:
    Docker Compose tornará isso simples. No diretório `sms-gateway-web`:
    ```bash
    docker-compose up --build -d --force-recreate
    ```
    *   `--build`: Reconstrói a imagem se houver alterações no `Dockerfile` ou no código fonte.
    *   `--force-recreate`: Para e recria os containers mesmo que a configuração deles não tenha mudado, garantindo que a nova imagem seja usada.

    Se você estiver usando imagens com tags específicas (não `latest`), você precisaria primeiro construir e dar tag à nova imagem, e depois rodar `docker-compose up -d --force-recreate` (após atualizar a tag da imagem no `docker-compose.yml`).

3.  **Limpar Imagens Antigas (Opcional)**:
    Com o tempo, você pode acumular imagens Docker antigas e não utilizadas. Você pode limpá-las com:
    ```bash
    docker image prune
    ```

## Backup da Configuração

É crucial fazer backup do volume que armazena os dados da sua aplicação (`config.json` e `sms_gateway.db`).

*   **Se estiver usando bind mount (`./config`)**: Faça backup do diretório `config` no seu host.
*   **Se estiver usando um volume nomeado (ex: `sms_gateway_data`)**:
    Você pode seguir as [estratégias de backup de volumes do Docker](https://docs.docker.com/storage/volumes/#backup-restore-or-migrate-data-volumes). Uma maneira comum é rodar um container temporário que monta o volume e cria um arquivo de backup:
    ```bash
    # Nome do volume: sms_gateway_data_sms-gateway-web (geralmente prefixado pelo nome do dir)
    # Verifique o nome exato com: docker volume ls
    docker run --rm -v sms_gateway_data_sms-gateway-web:/data -v $(pwd)/backup:/backup ubuntu tar cvf /backup/sms_config_backup.tar /data
    ```
    Isso criaria `sms_config_backup.tar` no subdiretório `backup` do seu diretório atual no host.

Este guia fornece uma base sólida para deployar a aplicação `sms-gateway-web` usando Docker. Para configurações mais avançadas com HTTPS e gerenciamento facilitado, consulte os guias para [Coolify](./coolify.md) ou [VPS com Portainer + Traefik](./vps-portainer-traefik.md).
