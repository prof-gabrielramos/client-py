# Interface Web: Instalação e Execução

Existem duas maneiras principais de instalar e executar a interface web `sms-gateway-web`. O uso de Docker é fortemente recomendado para simplicidade e consistência do ambiente.

## Método 1: Usando Docker e Docker Compose (Recomendado)

Esta é a maneira mais fácil e recomendada para a maioria dos usuários e para deploy.

**Pré-requisitos:**

*   [Docker](https://docs.docker.com/get-docker/) instalado.
*   [Docker Compose](https://docs.docker.com/compose/install/) instalado.

**Passos:**

1.  **Clone o repositório** (se ainda não o fez):
    ```bash
    git clone https://github.com/prof-gabrielramos/client-py.git
    cd client-py
    ```

2.  **Navegue até o diretório `sms-gateway-web`**:
    ```bash
    cd sms-gateway-web
    ```
    Este diretório contém o `Dockerfile` e o `docker-compose.yml` necessários.

3.  **Construa e execute os containers**:
    ```bash
    docker-compose up --build
    ```
    *   O comando `--build` garante que a imagem Docker seja construída (ou reconstruída se houver alterações no `Dockerfile` ou no código).
    *   Isso iniciará a aplicação web. Você verá logs no seu terminal.

4.  **Acesse a interface web**:
    Abra seu navegador e vá para [http://localhost:5000](http://localhost:5000).

**Comandos Úteis do Docker Compose:**

*   **Executar em segundo plano (detached mode)**:
    ```bash
    docker-compose up --build -d
    ```
*   **Ver logs (se estiver rodando em detached mode)**:
    ```bash
    docker-compose logs -f
    ```
*   **Parar a aplicação**:
    ```bash
    docker-compose down
    ```
    Isso irá parar e remover os containers. Seus dados de configuração e histórico de mensagens persistirão no diretório `sms-gateway-web/config` do seu host, pois ele está montado como um volume.
*   **Parar e remover volumes (CUIDADO: remove dados persistidos se não houver backup)**:
    ```bash
    docker-compose down -v
    ```
*   **Forçar reconstrução da imagem**:
    ```bash
    docker-compose build --no-cache
    docker-compose up -d --force-recreate
    ```

### Detalhes da Configuração Docker

*   **`Dockerfile`**: Define como a imagem da aplicação Python/Flask é construída.
    *   Usa `python:3.9-slim` como imagem base.
    *   Copia `requirements.txt` e instala as dependências.
    *   Copia o código da aplicação.
    *   Expõe a porta `5000`.
    *   Define `python run.py` como comando de execução.
*   **`docker-compose.yml`**: Orquestra o serviço `web`.
    *   `build: .`: Constrói a imagem a partir do `Dockerfile` no diretório atual.
    *   `image: sms-gateway-web:latest`: Nomeia a imagem construída.
    *   `container_name: sms-gateway-web`: Define um nome para o container.
    *   `ports: - "5000:5000"`: Mapeia a porta `5000` do host para a porta `5000` do container.
    *   `volumes: - ./config:/root/.sms-gateway-web`: **Importante para persistência de dados**. Mapeia o subdiretório `config` (que será criado no seu diretório `sms-gateway-web` no host) para `/root/.sms-gateway-web` dentro do container. É aqui que a aplicação armazena seu arquivo `config.json` e o banco de dados `sms_gateway.db`.
    *   `environment: - FLASK_ENV=production`: Define o ambiente Flask para produção.
    *   `restart: unless-stopped`: Garante que o container reinicie automaticamente a menos que seja parado manualmente.

## Método 2: Instalação Manual (Sem Docker)

Este método requer que você tenha Python 3.9+ e pip configurados no seu sistema.

**Pré-requisitos:**

*   Python 3.9 ou superior.
*   Pip (gerenciador de pacotes Python).

**Passos:**

1.  **Clone o repositório** (se ainda não o fez):
    ```bash
    git clone https://github.com/prof-gabrielramos/client-py.git
    cd client-py
    ```

2.  **Crie e ative um ambiente virtual** (recomendado):
    ```bash
    python3 -m venv venv_web
    source venv_web/bin/activate  # Linux/macOS
    # ou
    # venv_web\Scripts\activate    # Windows
    ```

3.  **Navegue até o diretório `sms-gateway-web`**:
    ```bash
    cd sms-gateway-web
    ```

4.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```
    Isso instalará Flask e outras bibliotecas necessárias.

5.  **Execute a aplicação**:
    ```bash
    python run.py
    ```
    Por padrão, a aplicação rodará em `http://localhost:5000`. Você pode especificar host e porta:
    ```bash
    python run.py --host 0.0.0.0 --port 8080
    ```

6.  **Acesse a interface web**:
    Abra seu navegador e vá para o endereço exibido no terminal (normalmente [http://localhost:5000](http://localhost:5000)).

**Para parar a aplicação manual**: Pressione `Ctrl+C` no terminal onde ela está rodando.

**Local da Configuração Manual**:
Quando executada manualmente, a aplicação criará um diretório de configuração no seu diretório home do usuário: `~/.sms-gateway-web/`. Este diretório conterá `config.json` e `sms_gateway.db`.

---

Independentemente do método escolhido, após a execução, você precisará configurar a conexão com sua instância do SMS Gateway for Android™ através da interface web. Veja a seção [Configuração](./configuration.md).
