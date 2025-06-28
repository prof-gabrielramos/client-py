# Guia do Desenvolvedor

Este guia fornece informações essenciais para desenvolvedores que trabalham neste projeto.

## Índice

- [Instruções de configuração](#instruções-de-configuração)
- [Visão geral da estrutura do projeto](#visão-geral-da-estrutura-do-projeto)
- [Fluxo de trabalho de desenvolvimento](#fluxo-de-trabalho-de-desenvolvimento)
- [Abordagem de teste](#abordagem-de-teste)
- [Etapas comuns de solução de problemas](#etapas-comuns-de-solução-de-problemas)

## Instruções de configuração

Existem duas maneiras principais de configurar o ambiente de desenvolvimento:

**1. Usando Docker (Recomendado para a Interface Web)**

Esta é a forma recomendada para trabalhar com a `sms-gateway-web`, pois garante um ambiente consistente.

*   **Pré-requisitos:**
    *   Docker instalado: [Instalar Docker](https://docs.docker.com/get-docker/)
    *   Docker Compose instalado: [Instalar Docker Compose](https://docs.docker.com/compose/install/)
*   **Passos:**
    1.  Clone o repositório:
        ```bash
        git clone https://github.com/android-sms-gateway/client-py.git # Ou a URL do seu fork
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
    git clone https://github.com/android-sms-gateway/client-py.git # Ou a URL do seu fork
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

Entender a organização do projeto é crucial para navegar e contribuir efetivamente. Abaixo está uma visão geral das principais pastas e sua finalidade:

*(Adapte esta seção à estrutura real do seu projeto. O exemplo abaixo é genérico.)*

```
<NOME_DO_REPOSITORIO>/
├── .github/             # Configurações do GitHub, como workflows de CI/CD
├── .vscode/             # Configurações específicas do VSCode (opcional)
├── docs/                # Documentação do projeto (além deste guia)
├── <NOME_DA_APP_PRINCIPAL>/ # Código fonte principal da aplicação
│   ├── api/             # Endpoints da API (se aplicável)
│   ├── apps/            # Módulos ou aplicações Django/Flask (se aplicável)
│   ├── core/            # Lógica de negócios principal, modelos
│   ├── static/          # Arquivos estáticos (CSS, JavaScript, imagens) para a app principal
│   ├── templates/       # Templates HTML para a app principal
│   ├── tests/           # Testes específicos para a app principal
│   ├── urls.py          # Definições de URL (Django)
│   └── views.py         # Lógica de visualização (Django/Flask)
├── data/                # Scripts de migração, dados iniciais (não versionar dados sensíveis)
├── scripts/             # Scripts úteis (build, deploy, etc.)
├── tests/               # Testes de integração ou para todo o projeto
├── venv/                # Ambiente virtual Python (geralmente no .gitignore)
├── .env.example         # Exemplo de arquivo de variáveis de ambiente
├── .gitignore           # Especifica arquivos e pastas ignorados pelo Git
├── manage.py            # Utilitário de gerenciamento do Django (se aplicável)
├── requirements.txt     # Dependências Python
├── Dockerfile           # Instruções para construir uma imagem Docker (se aplicável)
├── docker-compose.yml   # Configuração para Docker Compose (se aplicável)
└── README.md            # Visão geral do projeto, instruções básicas de setup
```

**Principais Arquivos e Pastas:**

*   **`README.md`**: Fornece uma introdução ao projeto, como instalá-lo e executá-lo. É o primeiro arquivo que um novo desenvolvedor deve ler.
*   **`<NOME_DA_APP_PRINCIPAL>/` ou `src/`**: Contém o código fonte principal da aplicação. A estrutura interna pode variar dependendo do framework (por exemplo, Django, Flask, React, Angular, Node.js).
    *   **`core/` ou `lib/`**: Geralmente contém a lógica de negócios central, modelos de dados, serviços, etc.
    *   **`api/` ou `routes/`**: Define os endpoints da API.
    *   **`views/` ou `controllers/`**: Lida com as requisições HTTP e retorna as respostas.
    *   **`models/` ou `database/`**: Define os esquemas do banco de dados e interações.
    *   **`static/` ou `public/`**: Arquivos estáticos como CSS, JavaScript e imagens.
    *   **`templates/` ou `views/` (frontend)**: Arquivos de template HTML.
*   **`tests/`**: Contém os testes automatizados. É importante que esta pasta reflita a estrutura do código fonte para facilitar a localização dos testes.
*   **`scripts/`**: Scripts auxiliares para tarefas como deployment, build, ou outras operações de desenvolvimento.
*   **`docs/`**: Documentação adicional do projeto, como diagramas de arquitetura, decisões de design, etc.
*   **`requirements.txt` / `package.json` / `pom.xml` / `Gemfile`**: Define as dependências do projeto.
*   **`.env.example`**: Um template para o arquivo `.env` que armazena configurações específicas do ambiente (como chaves de API, credenciais de banco de dados). O arquivo `.env` real não deve ser versionado.
*   **`Dockerfile` e `docker-compose.yml` (se usados)**: Para containerização da aplicação.
*   **`.github/workflows/` (se usado)**: Define os pipelines de Integração Contínua/Entrega Contínua (CI/CD) usando GitHub Actions.

Compreender onde os diferentes tipos de código e configuração residem ajudará você a fazer alterações de forma mais eficiente e a seguir as convenções do projeto.

## Fluxo de trabalho de desenvolvimento

Seguimos um fluxo de trabalho baseado em Git para garantir colaboração eficiente e manutenção da qualidade do código.

1.  **Sincronize sua Branch Principal:**
    Antes de iniciar qualquer novo trabalho, certifique-se de que sua branch principal local (geralmente `main` ou `develop`) está atualizada com o repositório remoto.
    ```bash
    git checkout main  # ou develop
    git pull origin main
    ```

2.  **Crie uma Nova Branch:**
    Crie uma branch a partir da principal para sua nova feature, correção de bug ou tarefa. Use um nome de branch descritivo, por exemplo, prefixado com `feature/`, `bugfix/`, ou `chore/`.
    ```bash
    # Exemplo para uma nova feature
    git checkout -b feature/nome-da-feature

    # Exemplo para uma correção de bug
    git checkout -b bugfix/descricao-do-bug
    ```
    **Convenções de Nomenclatura de Branch (Exemplo):**
    *   `feature/<nome-da-feature>` (ex: `feature/user-authentication`)
    *   `bugfix/<issue-id>-<descricao-curta>` (ex: `bugfix/123-fix-login-error`)
    *   `hotfix/<descricao-curta>` (ex: `hotfix/critical-security-patch`)
    *   `chore/<descricao-tarefa>` (ex: `chore/update-dependencies`)

3.  **Desenvolva na sua Branch:**
    *   Faça as alterações de código necessárias.
    *   Escreva ou atualize testes para cobrir suas alterações.
    *   Siga as convenções de codificação e estilo do projeto (verifique se há um arquivo `CONTRIBUTING.md` ou guias de estilo).
    *   Faça commits atômicos e com mensagens claras e descritivas.
        ```bash
        git add .
        git commit -m "feat: Implementa autenticação de usuário"
        # ou para commits mais detalhados:
        # git commit -m "fix: Corrige erro de login ao usar caracteres especiais
        #
        # - O problema ocorria devido à falta de sanitização da entrada.
        # - Adicionada validação e sanitização para campos de nome de usuário."
        ```
    *   **Mensagens de Commit:** Siga convenções como [Conventional Commits](https://www.conventionalcommits.org/) se o projeto as utilizar.

4.  **Mantenha sua Branch Atualizada (Rebase):**
    Periodicamente, atualize sua branch de feature com as últimas alterações da branch principal para evitar grandes conflitos de merge mais tarde. Use `rebase` para manter um histórico de commits limpo.
    ```bash
    git checkout main
    git pull origin main
    git checkout feature/nome-da-feature
    git rebase main
    ```
    Resolva quaisquer conflitos que surgirem durante o rebase.

5.  **Execute Testes e Linters:**
    Antes de submeter suas alterações, execute todos os testes e ferramentas de linting/formatação para garantir que o código está correto e segue os padrões.
    ```bash
    # Exemplo (adapte aos comandos do seu projeto)
    pytest
    pylint <NOME_DA_APP_PRINCIPAL>/
    # ou
    npm test
    npm run lint
    ```

6.  **Envie sua Branch para o Repositório Remoto (Push):**
    ```bash
    git push origin feature/nome-da-feature
    ```
    Se você usou `rebase` e a branch já existe no remoto, pode ser necessário forçar o push (com cautela): `git push origin feature/nome-da-feature --force-with-lease`.

7.  **Crie um Pull Request (PR):**
    *   Vá para a interface do GitHub (ou GitLab, Bitbucket) do repositório.
    *   Crie um novo Pull Request da sua branch de feature para a branch principal (`main` ou `develop`).
    *   Preencha o template do PR, se houver. Descreva claramente as alterações feitas, o problema que resolvem e como testá-las.
    *   Referencie quaisquer issues relevantes (ex: "Closes #123").
    *   Adicione revisores apropriados.

8.  **Revisão de Código e Discussão:**
    *   Seu PR será revisado por outros membros da equipe.
    *   Responda aos comentários e faça as alterações solicitadas. Faça push dos commits adicionais para a mesma branch; o PR será atualizado automaticamente.
    *   Participe das discussões para garantir que a melhor solução seja implementada.

9.  **Merge do Pull Request:**
    *   Após a aprovação e a passagem de quaisquer verificações de CI, o PR será mergeado na branch principal por um mantenedor do projeto.
    *   Geralmente, usa-se "Squash and merge" ou "Rebase and merge" para manter o histórico da branch principal limpo.

10. **Limpeza (Opcional):**
    Após o merge do PR, você pode deletar sua branch local e remota.
    ```bash
    git checkout main
    git pull origin main
    git branch -d feature/nome-da-feature
    git push origin --delete feature/nome-da-feature
    ```

Este fluxo de trabalho ajuda a manter a qualidade do código, facilita a colaboração e permite um rastreamento claro das alterações.

## Abordagem de teste

Testes automatizados são fundamentais para garantir a qualidade, estabilidade e manutenibilidade do nosso código. Espera-se que todas as novas features e correções de bugs incluam testes apropriados.

**Tipos de Testes:**

*(Adapte esta seção aos tipos de teste e ferramentas específicas usadas no projeto.)*

1.  **Testes Unitários:**
    *   **Objetivo:** Testar a menor unidade de código isoladamente (funções, métodos, classes).
    *   **Ferramentas Comuns:**
        *   Python: `unittest`, `pytest`
        *   JavaScript: `Jest`, `Mocha`, `Jasmine`
        *   Java: `JUnit`, `TestNG`
        *   Ruby: `RSpec`, `Minitest`
    *   **Localização:** Geralmente em uma pasta `tests/unit` ou ao lado do código que testam (ex: `meu_modulo/tests/test_minha_funcao.py`).
    *   **Princípios:**
        *   Devem ser rápidos de executar.
        *   Não devem ter dependências externas (arquivos, bancos de dados, APIs). Use mocks e stubs para isolar unidades.
        *   Cada teste deve focar em um único aspecto ou comportamento.

2.  **Testes de Integração:**
    *   **Objetivo:** Testar a interação entre diferentes componentes ou módulos do sistema. Por exemplo, como diferentes partes da sua aplicação interagem com o banco de dados ou com serviços externos (mockados).
    *   **Ferramentas Comuns:** As mesmas dos testes unitários, mas com configuração para permitir interações limitadas (ex: um banco de dados de teste em memória).
    *   **Localização:** Geralmente em uma pasta `tests/integration`.
    *   **Princípios:**
        *   Podem ser mais lentos que testes unitários.
        *   Verificam se os "contratos" entre os módulos estão funcionando corretamente.

3.  **Testes End-to-End (E2E) / Testes de UI:**
    *   **Objetivo:** Testar o fluxo completo da aplicação do ponto de vista do usuário, simulando interações reais com a interface do usuário (se aplicável).
    *   **Ferramentas Comuns:**
        *   Web: `Selenium`, `Cypress`, `Playwright`, `Puppeteer`
        *   Mobile: `Appium`, `Espresso` (Android), `XCUITest` (iOS)
    *   **Localização:** Geralmente em uma pasta `tests/e2e` ou `tests/ui`.
    *   **Princípios:**
        *   São os mais lentos e, às vezes, os mais frágeis.
        *   Fornecem alta confiança de que a aplicação funciona como esperado para o usuário.
        *   Devem focar nos fluxos críticos do usuário.

**Como Escrever Bons Testes:**

*   **Clareza e Legibilidade:** Um teste deve ser fácil de entender. O nome do teste deve descrever o que ele está testando e qual o resultado esperado.
*   **ARRANGE, ACT, ASSERT (AAA):**
    *   **Arrange:** Configure as pré-condições e entradas necessárias para o teste.
    *   **Act:** Execute a unidade de código ou ação que está sendo testada.
    *   **Assert:** Verifique se o resultado ou o estado do sistema é o esperado.
*   **Testar Casos de Sucesso e Falha:** Não teste apenas o "caminho feliz". Inclua testes para entradas inválidas, condições de erro e casos extremos.
*   **Cobertura de Código (Code Coverage):**
    *   Monitore a cobertura de código para identificar partes do código que não estão sendo testadas.
    *   Ferramentas como `coverage.py` (Python) ou `Istanbul` (JavaScript) podem ajudar.
    *   Lembre-se que 100% de cobertura não garante ausência de bugs, mas é um bom indicador.
*   **Manter os Testes Atualizados:** Testes devem ser tratados como código de primeira classe. Se o código da aplicação muda, os testes correspondentes devem ser atualizados. Testes quebrados devem ser corrigidos imediatamente.
*   **Evitar Lógica Complexa nos Testes:** Testes devem ser simples e diretos. Se um teste é muito complexo, ele próprio pode conter bugs.

**Como Executar os Testes:**

*   **Localmente:**
    Forneça os comandos exatos para executar os diferentes tipos de testes.
    ```bash
    # Exemplo para Python com pytest
    pytest  # Executa todos os testes descobertos
    pytest tests/unit/ # Executa apenas testes unitários
    pytest -k "nome_especifico_do_teste" # Executa um teste específico

    # Exemplo para JavaScript com npm/Jest
    npm test
    npm run test:unit
    npm run test:integration
    ```
*   **Integração Contínua (CI):**
    *   Os testes são geralmente executados automaticamente em cada push e Pull Request através de um sistema de CI (ex: GitHub Actions, Jenkins, GitLab CI).
    *   Garanta que os PRs só possam ser mergeados se todos os testes passarem.

**Estratégia de Teste:**

*   **Pirâmide de Testes:** Priorize testes unitários (base larga), seguidos por testes de integração (meio) e, por fim, testes E2E (topo estreito).
*   **Test Driven Development (TDD) ou Behavior Driven Development (BDD):** Considere adotar essas práticas onde você escreve os testes *antes* de escrever o código da funcionalidade. Isso ajuda a definir claramente os requisitos e a garantir que o código seja testável desde o início.

Incentivamos todos os desenvolvedores a escreverem testes abrangentes para suas contribuições. Se você não tem certeza de como testar uma parte específica do código, peça ajuda!

## Etapas comuns de solução de problemas

Esta seção aborda alguns problemas comuns que você pode encontrar durante o desenvolvimento e como resolvê-los.

*(Adapte e expanda esta seção com problemas e soluções específicas do seu projeto.)*

1.  **Problemas de Configuração do Ambiente:**
    *   **Sintoma:** Erros ao instalar dependências, o servidor não inicia, comandos não são reconhecidos.
    *   **Soluções:**
        *   **Verifique as versões:** Certifique-se de que você está usando as versões corretas de Node.js, Python, Java, Ruby, etc., conforme especificado no projeto (geralmente no `README.md` ou em arquivos como `.nvmrc`, `.python-version`).
        *   **Ambiente Virtual:** Se estiver usando Python, Node.js (com nvm), ou Ruby (com rvm/rbenv), certifique-se de que seu ambiente virtual está ativado.
            ```bash
            # Python
            source venv/bin/activate
            # Node (com nvm)
            nvm use
            ```
        *   **Dependências:** Tente reinstalar as dependências:
            ```bash
            # Python
            rm -rf venv # Cuidado: remove o ambiente virtual
            python -m venv venv
            source venv/bin/activate
            pip install -r requirements.txt

            # Node.js
            rm -rf node_modules
            npm install # ou yarn install
            ```
        *   **Variáveis de Ambiente:** Verifique se todas as variáveis de ambiente necessárias estão definidas corretamente no seu arquivo `.env` (e se o arquivo `.env` existe e é carregado).
        *   **Caminhos (PATH):** Certifique-se de que os binários das suas ferramentas e linguagens estão no PATH do sistema.

2.  **Problemas com o Banco de Dados:**
    *   **Sintoma:** Erros de conexão com o banco de dados, tabelas não encontradas, dados inconsistentes.
    *   **Soluções:**
        *   **Serviço do BD:** Verifique se o serviço do seu banco de dados (PostgreSQL, MySQL, MongoDB, etc.) está em execução.
        *   **Credenciais:** Confirme se as credenciais do banco de dados (usuário, senha, host, porta, nome do banco) no seu arquivo `.env` ou configuração estão corretas.
        *   **Migrações:** Certifique-se de que todas as migrações do banco de dados foram executadas.
            ```bash
            # Exemplo Django
            python manage.py makemigrations
            python manage.py migrate
            # Exemplo Rails
            rails db:migrate
            ```
        *   **Banco de Dados de Teste:** Se os problemas ocorrem durante os testes, verifique a configuração do banco de dados de teste. Alguns frameworks criam e destroem bancos de dados de teste automaticamente.

3.  **Testes Falhando:**
    *   **Sintoma:** Testes unitários, de integração ou E2E estão vermelhos.
    *   **Soluções:**
        *   **Leia a Mensagem de Erro:** A saída do teste geralmente indica qual asserção falhou e por quê.
        *   **Execute Testes Individualmente:** Isole o teste problemático e execute-o individualmente para focar na depuração.
            ```bash
            # pytest
            pytest path/to/test_file.py::TestClassName::test_method_name
            # Jest
            jest -t "nome do teste"
            ```
        *   **Depure:** Use um depurador (`pdb` para Python, `debugger` no Chrome DevTools para JS, etc.) para percorrer o código do teste e o código que está sendo testado.
        *   **Dependências de Teste:** Certifique-se de que quaisquer mocks, stubs ou fixtures estão configurados corretamente.
        *   **Dados de Teste:** Verifique se os dados usados para o teste são apropriados e cobrem o cenário que você está tentando testar.
        *   **Alterações Recentes:** Se os testes estavam passando antes, reveja as alterações recentes no código ou nos próprios testes.

4.  **Problemas de Linting/Formatação:**
    *   **Sintoma:** O CI falha devido a erros de linting ou formatação, ou você vê avisos no seu editor.
    *   **Soluções:**
        *   **Execute o Linter/Formatador:** Execute as ferramentas de linting (ex: `pylint`, `eslint`, `rubocop`) e formatação (ex: `black`, `prettier`, `autopep8`) localmente.
            ```bash
            # Exemplo Python com Black e Pylint
            black .
            pylint meu_modulo/
            # Exemplo JavaScript com Prettier e ESLint
            npx prettier --write .
            npx eslint --fix .
            ```
        *   **Configuração do Editor:** Configure seu editor para usar os linters e formatadores do projeto, idealmente para formatar ao salvar.
        *   **Verifique as Regras:** Entenda as regras de linting do projeto (geralmente em arquivos como `.pylintrc`, `.eslintrc.js`, `.rubocop.yml`).

5.  **Conflitos de Merge:**
    *   **Sintoma:** O Git informa que há conflitos ao tentar fazer `merge` ou `rebase`.
    *   **Soluções:**
        *   **Inspecione os Conflitos:** Abra os arquivos listados pelo Git. Você verá marcadores `<<<<<<<`, `=======`, `>>>>>>>`.
        *   **Resolva Manualmente:** Edite os arquivos para manter as alterações desejadas de ambas as branches e remova os marcadores de conflito.
        *   **Use uma Ferramenta de Merge:** Ferramentas como `git mergetool` ou as integradas em IDEs podem ajudar a visualizar e resolver conflitos.
        *   **Adicione e Continue:** Após resolver os conflitos em um arquivo:
            ```bash
            git add <arquivo_resolvido>
            ```
            Quando todos os conflitos estiverem resolvidos e os arquivos adicionados:
            ```bash
            # Se estiver fazendo rebase
            git rebase --continue
            # Se estiver fazendo merge
            git commit
            ```
        *   **Peça Ajuda:** Se não tiver certeza de como resolver um conflito complexo, peça ajuda a outro membro da equipe.

6.  **"Funciona na Minha Máquina" (Mas Falha no CI ou para Outros):**
    *   **Sintoma:** O código funciona localmente, mas falha no ambiente de CI ou para outros desenvolvedores.
    *   **Soluções:**
        *   **Consistência do Ambiente:** Verifique se há diferenças entre seu ambiente local e o ambiente de CI (versões de dependências, variáveis de ambiente, sistema operacional). Docker pode ajudar a mitigar isso.
        *   **Dependências não Versionadas:** Certifique-se de que todas as dependências estão listadas no `requirements.txt`, `package.json`, etc., e que não há dependências globais das quais seu código depende implicitamente.
        *   **Estado Oculto:** Seu ambiente local pode ter algum estado (arquivos em cache, configurações locais do banco de dados) que não está presente no CI. Tente limpar caches ou reconstruir seu ambiente do zero.
        *   **Testes Específicos do SO:** Se o código interage com o sistema de arquivos ou processos, pode haver diferenças entre Windows, macOS e Linux.

**Onde Procurar Ajuda:**

*   **Mensagens de Erro:** Leia-as cuidadosamente. Muitas vezes, elas contêm a chave para a solução.
*   **Documentação do Projeto:** Releia este guia, o `README.md` e outras documentações.
*   **Documentação das Ferramentas/Frameworks:** Consulte a documentação oficial das linguagens, frameworks e bibliotecas que você está usando.
*   **Stack Overflow e Google:** Pesquise a mensagem de erro ou o problema. É provável que alguém já tenha passado por isso.
*   **Colegas de Equipe:** Não hesite em pedir ajuda a outros desenvolvedores do projeto.

Lembre-se de fornecer o máximo de contexto possível ao pedir ajuda (o que você estava tentando fazer, o que você esperava, o que aconteceu, mensagens de erro completas e etapas para reproduzir o problema).
