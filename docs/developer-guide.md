# Guia do Desenvolvedor

Este guia fornece informações essenciais para desenvolvedores que trabalham neste projeto (`android-sms-gateway` e `sms-gateway-web`).

Ele é uma cópia adaptada do `DEVELOPER_GUIDE.md` da raiz do projeto, formatado para MkDocs.

## Índice (Conteúdo Original do `DEVELOPER_GUIDE.md`)

*   [Instruções de configuração](#instrucoes-de-configuracao)
*   [Visão geral da estrutura do projeto](#visao-geral-da-estrutura-do-projeto)
*   [Fluxo de trabalho de desenvolvimento](#fluxo-de-trabalho-de-desenvolvimento)
*   [Abordagem de teste](#abordagem-de-teste)
*   [Etapas comuns de solução de problemas](#etapas-comuns-de-solucao-de-problemas)

## Instruções de configuração

Existem duas maneiras principais de configurar o ambiente de desenvolvimento:

**1. Usando Docker (Recomendado para a Interface Web `sms-gateway-web`)**

Esta é a forma recomendada para trabalhar com a `sms-gateway-web`, pois garante um ambiente consistente.

*   **Pré-requisitos:**
    *   Docker instalado: [Instalar Docker](https://docs.docker.com/get-docker/)
    *   Docker Compose instalado: [Instalar Docker Compose](https://docs.docker.com/compose/install/)
*   **Passos:**
    1.  Clone o repositório:
        ```bash
        git clone https://github.com/prof-gabrielramos/client-py.git # Ou a URL do seu fork
        cd client-py/sms-gateway-web
        ```
    2.  Inicie os serviços com Docker Compose:
        ```bash
        docker-compose up --build
        ```
        Isso irá construir a imagem Docker (se ainda não existir) e iniciar o container da aplicação web.
    3.  A interface web estará acessível em `http://localhost:5000`.
    4.  O diretório `sms-gateway-web/config` no seu host é mapeado para `/root/.sms-gateway-web` no container, persistindo a configuração e o banco de dados SQLite.
    5.  Para parar os serviços:
        ```bash
        docker-compose down
        ```

**2. Configuração Manual (Principalmente para a biblioteca `android-sms-gateway`)**

Para desenvolver ou testar a biblioteca cliente Python (`android-sms-gateway`) diretamente, ou se você não quiser usar Docker para a interface web.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/prof-gabrielramos/client-py.git # Ou a URL do seu fork
    cd client-py
    ```

2.  **Crie e ative um ambiente virtual Python:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Windows: venv\Scripts\activate
    ```

3.  **Instale as dependências:**
    *   Para a biblioteca cliente e desenvolvimento geral:
        ```bash
        pip install -e ".[dev,requests,encryption]"
        ```
    *   Se for trabalhar na interface web (`sms-gateway-web`) manualmente:
        ```bash
        pip install -r sms-gateway-web/requirements.txt
        ```

4.  **Variáveis de Ambiente (para a biblioteca cliente):**
    Para usar os exemplos ou testes da biblioteca cliente que se comunicam com a API real do SMS Gateway, configure:
    ```bash
    export ANDROID_SMS_GATEWAY_LOGIN="seu_usuario_api"
    export ANDROID_SMS_GATEWAY_PASSWORD="sua_senha_api"
    export ANDROID_SMS_GATEWAY_BASE_URL="http://<IP_DO_CELULAR>:<PORTA>"
    ```
    Considere usar um arquivo `.env` com `python-dotenv` para gerenciar isso localmente (não comite o arquivo `.env`).

5.  **Executando a Interface Web Manualmente (sem Docker):**
    Se você instalou as dependências da `sms-gateway-web` manualmente:
    ```bash
    cd sms-gateway-web
    python run.py
    ```
    Acesse em `http://localhost:5000`.

**Ferramentas Adicionais Importantes:**

*   **Linters e Formatadores (Black, Flake8, iSort):**
    Estão configurados no `Pipfile` e `pyproject.toml`. Use-os para manter a qualidade do código.
    ```bash
    pip install black flake8 isort
    black .
    flake8 .
    isort .
    ```
    Ou, se estiver usando o ambiente `dev` do `Pipfile`: `pipenv run black .`, etc.
    Recomenda-se configurar seu editor para usar essas ferramentas automaticamente.

*   **Pytest para Testes:**
    ```bash
    pip install pytest pytest-cov
    pytest
    ```

*   **MkDocs para Documentação:**
    ```bash
    pip install mkdocs mkdocs-material
    ```
    Para construir e servir a documentação localmente (execute na raiz do projeto):
    ```bash
    mkdocs serve
    ```
    Acesse em `http://localhost:8000`.

**Verificando a Configuração:**
*   Para a biblioteca cliente: Execute `pytest` na raiz do projeto.
*   Para a interface web (Docker): Após `docker-compose up --build` em `sms-gateway-web/`, acesse `http://localhost:5000`.
*   Para a interface web (Manual): Em `sms-gateway-web/`, após `python run.py`, acesse `http://localhost:5000`.
*   Para documentação: Após `mkdocs serve` na raiz, acesse `http://localhost:8000`.

Certifique-se de que todas as ferramentas e versões de linguagem especificadas no projeto (Python 3.9+) sejam respeitadas.

## Visão geral da estrutura do projeto

Entender a organização do projeto é crucial para navegar e contribuir efetivamente.

```
client-py/
├── .github/             # Configurações do GitHub, como workflows de CI/CD
├── android_sms_gateway/ # Código fonte da biblioteca cliente Python
│   ├── __init__.py
│   ├── client.py        # Contém APIClient e AsyncAPIClient
│   ├── domain.py        # Modelos Pydantic (Message, MessageState, etc.)
│   ├── encryption.py    # Lógica de criptografia
│   ├── http.py          # Clientes HTTP síncronos
│   ├── ahttp.py         # Clientes HTTP assíncronos
│   └── constants.py     # Constantes
├── docs/                # Arquivos fonte da documentação MkDocs
│   ├── index.md
│   ├── api-client/
│   ├── deployment/
│   └── web-interface/
├── sms-gateway-web/     # Código fonte da interface web Flask
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── app.py           # Aplicação Flask principal
│   ├── run.py           # Script para executar o servidor Flask
│   ├── requirements.txt # Dependências da interface web
│   └── templates/       # Templates HTML Jinja2
├── tests/               # Testes para a biblioteca cliente Python
├── .env.example         # Exemplo de arquivo de variáveis de ambiente
├── .gitignore
├── DEVELOPER_GUIDE.md   # Guia do desenvolvedor (este arquivo, na raiz)
├── LICENSE
├── Makefile             # Contém comandos úteis (test, lint, etc.)
├── mkdocs.yml           # Configuração do MkDocs
├── Pipfile              # Definições de dependências para Pipenv
├── Pipfile.lock
├── pyproject.toml       # Configurações do projeto Python (Black, iSort, MyPy)
└── README.md            # README principal do projeto
```

**Principais Componentes:**

*   **`README.md` (raiz)**: Visão geral do projeto, instalação rápida da biblioteca, como rodar a interface web com Docker.
*   **`android_sms_gateway/`**: Pacote Python da biblioteca cliente.
*   **`sms-gateway-web/`**: Aplicação Flask para a interface web.
    *   **`Dockerfile` & `docker-compose.yml`**: Para containerizar a interface web.
    *   **`app.py`**: Lógica principal da aplicação Flask (rotas, views).
*   **`tests/`**: Testes unitários e de integração para a biblioteca `android_sms_gateway`.
*   **`docs/`**: Onde esta documentação (MkDocs) reside.
*   **`mkdocs.yml`**: Arquivo de configuração para o site de documentação MkDocs.
*   **`DEVELOPER_GUIDE.md` (raiz)**: Orientações gerais para desenvolvedores.
*   **`Pipfile`, `pyproject.toml`**: Gerenciamento de dependências e configuração de ferramentas de qualidade de código.

## Fluxo de trabalho de desenvolvimento

Seguimos um fluxo de trabalho baseado em Git para garantir colaboração eficiente e manutenção da qualidade do código.

1.  **Sincronize sua Branch Principal:**
    Antes de iniciar qualquer novo trabalho, certifique-se de que sua branch principal local (geralmente `main` ou `master`) está atualizada com o repositório remoto.
    ```bash
    git checkout main
    git pull origin main
    ```

2.  **Crie uma Nova Branch:**
    Crie uma branch a partir da principal para sua nova feature, correção de bug ou tarefa. Use um nome de branch descritivo.
    ```bash
    git checkout -b feature/nome-da-feature
    # ou
    git checkout -b bugfix/descricao-do-bug
    ```

3.  **Desenvolva na sua Branch:**
    *   Faça as alterações de código necessárias.
    *   Escreva ou atualize testes para cobrir suas alterações.
    *   Siga as convenções de codificação e estilo do projeto (Black, Flake8, iSort).
        ```bash
        # Exemplo de formatação e linting
        black .
        isort .
        flake8 .
        mypy android_sms_gateway # Se estiver trabalhando na lib
        ```
    *   Faça commits atômicos e com mensagens claras e descritivas (siga [Conventional Commits](https://www.conventionalcommits.org/)).
        ```bash
        git add .
        git commit -m "feat: Adiciona nova funcionalidade X"
        ```

4.  **Mantenha sua Branch Atualizada (Rebase):**
    Periodicamente, atualize sua branch de feature com as últimas alterações da branch principal.
    ```bash
    git fetch origin
    git rebase origin/main # ou a branch principal que você usa
    ```
    Resolva quaisquer conflitos que surgirem.

5.  **Execute Testes e Linters:**
    Antes de submeter suas alterações, execute todos os testes e ferramentas de linting/formatação.
    ```bash
    pytest
    # (comandos de linting como black --check, flake8, isort --check)
    make test # Se houver um Makefile com um target de teste
    make lint # Se houver
    ```

6.  **Envie sua Branch para o Repositório Remoto (Push):**
    ```bash
    git push origin feature/nome-da-feature
    ```
    Se você usou `rebase` e a branch já existe no remoto, pode ser necessário forçar o push (com cautela): `git push origin feature/nome-da-feature --force-with-lease`.

7.  **Crie um Pull Request (PR):**
    *   Vá para a interface do GitHub (ou GitLab, Bitbucket) do repositório.
    *   Crie um novo Pull Request da sua branch de feature para a branch principal.
    *   Descreva claramente as alterações.

8.  **Revisão de Código e Discussão.**

9.  **Merge do Pull Request.**

10. **Limpeza (Opcional):**
    ```bash
    git checkout main
    git pull origin main
    git branch -d feature/nome-da-feature
    git push origin --delete feature/nome-da-feature # Se permitido
    ```

## Abordagem de teste

Testes automatizados são fundamentais.

**Tipos de Testes (para `android-sms-gateway`):**

1.  **Testes Unitários:**
    *   **Objetivo:** Testar unidades de código isoladamente (funções, métodos).
    *   **Ferramenta:** `pytest`.
    *   **Localização:** `tests/`.
    *   **Princípios:** Rápidos, sem dependências externas (usar mocks/stubs, ex: para chamadas HTTP).

2.  **Testes de Integração:**
    *   **Objetivo:** Testar a interação entre componentes (ex: cliente API com um servidor HTTP mockado).
    *   **Ferramenta:** `pytest` com fixtures que podem simular um servidor API.
    *   **Localização:** `tests/`.

**Como Escrever Bons Testes:**

*   Clareza, AAA (Arrange, Act, Assert).
*   Testar casos de sucesso e falha.
*   Manter atualizados.

**Como Executar os Testes:**
Na raiz do projeto:
```bash
pytest
```
Para ver cobertura de testes (se configurado):
```bash
pytest --cov=android_sms_gateway
```

**Testes para `sms-gateway-web`:**
Atualmente, o foco dos testes automatizados está na biblioteca cliente. A interface web pode ser testada manualmente. Contribuições para adicionar testes automatizados para a interface web (ex: usando Selenium ou Playwright para testes E2E, ou testes unitários para a lógica Flask) são bem-vindas.

## Etapas comuns de solução de problemas

1.  **Problemas de Configuração do Ambiente:**
    *   **Docker**: Verifique se o Docker daemon está rodando. Erros de permissão?
    *   **Python Venv**: Ambiente virtual ativado? Dependências corretas instaladas (`pip install -r requirements.txt` ou `pip install -e ".[dev]"`)?
    *   **Variáveis de Ambiente**: `ANDROID_SMS_GATEWAY_LOGIN`, `PASSWORD`, `BASE_URL` estão definidas e corretas para testes da biblioteca ou uso da interface web?

2.  **Problemas com a API do SMS Gateway (Celular):**
    *   App SMS Gateway rodando no celular?
    *   Celular na mesma rede que o cliente (ou acessível publicamente se necessário)?
    *   IP e porta corretos na `BASE_URL`?
    *   Credenciais da API corretas?

3.  **Testes Falhando:**
    *   Leia a mensagem de erro do `pytest`.
    *   Execute testes individualmente: `pytest tests/test_meu_modulo.py::test_minha_funcao`.
    *   Use o debugger (`pdb` ou do seu IDE).

4.  **Problemas de Linting/Formatação:**
    *   Execute `black .`, `isort .`, `flake8 .` para corrigir/identificar problemas.
    *   Configure seu editor para formatar ao salvar.

5.  **Conflitos de Merge:**
    *   Resolva manualmente ou com uma ferramenta de merge.
    *   Peça ajuda se não tiver certeza.

**Onde Procurar Ajuda:**
*   Mensagens de erro.
*   Esta documentação e o `README.md`.
*   Documentação das ferramentas (Flask, Docker, MkDocs, etc.).
*   Stack Overflow, Google.
*   Issues do GitHub do projeto.
*   Colegas de equipe.

Lembre-se de fornecer contexto ao pedir ajuda.
