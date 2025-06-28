# Guia de Início Rápido

Bem-vindo à documentação do SMS Gateway Client & Web Interface!

Este projeto consiste em duas partes principais:

1.  **`android-sms-gateway`**: Uma biblioteca cliente Python para interagir com a API do [SMS Gateway for Android™](https://sms-gate.app/).
2.  **`sms-gateway-web`**: Uma interface web construída com Flask que utiliza a biblioteca cliente Python para fornecer um dashboard para enviar e gerenciar mensagens SMS.

## Estrutura da Documentação

Esta documentação está organizada da seguinte forma:

*   **Guia de Início Rápido** (esta página): Uma visão geral e os primeiros passos.
*   **Interface Web**: Detalhes sobre a instalação, configuração e uso da aplicação web.
*   **Cliente Python API**: Informações aprofundadas sobre a biblioteca Python, incluindo instalação, como usar o cliente, criptografia, etc.
*   **Deployment**: Guias sobre como fazer deploy da interface web em várias plataformas.
*   **Guia do Desenvolvedor**: Informações para quem deseja contribuir com o desenvolvimento do projeto.
*   **Licença**: Detalhes da licença do projeto.

## Pré-requisitos

Antes de começar, você precisará ter o seguinte instalado, dependendo de como você pretende usar o projeto:

*   **Python 3.9+**: Necessário para a biblioteca cliente e para rodar a interface web manualmente.
*   **Pip**: Gerenciador de pacotes Python.
*   **Docker e Docker Compose**: Recomendado para rodar a interface web `sms-gateway-web`, pois simplifica a configuração e o deploy.
    *   [Instalar Docker](https://docs.docker.com/get-docker/)
    *   [Instalar Docker Compose](https://docs.docker.com/compose/install/)
*   **Git**: Para clonar o repositório.

## Obtendo o Código

Primeiro, clone o repositório do projeto:

```bash
git clone https://github.com/prof-gabrielramos/client-py.git
cd client-py
```

## Próximos Passos

### Para Usuários da Interface Web

Se você deseja apenas usar a interface web para enviar SMS:

1.  **Opção Recomendada: Usar Docker**
    *   Navegue até o diretório da interface web: `cd sms-gateway-web`
    *   Inicie a aplicação: `docker-compose up --build`
    *   Acesse em [http://localhost:5000](http://localhost:5000)
    *   Consulte a seção [Interface Web - Instalação e Execução](./web-interface/installation.md) para mais detalhes.

2.  **Opção Manual (sem Docker)**
    *   Certifique-se de ter Python 3.9+ e pip.
    *   Instale as dependências: `pip install -r sms-gateway-web/requirements.txt`
    *   Execute a aplicação: `cd sms-gateway-web && python run.py`
    *   Acesse em [http://localhost:5000](http://localhost:5000)

### Para Desenvolvedores da Biblioteca Cliente Python

Se você pretende usar ou desenvolver a biblioteca `android-sms-gateway`:

1.  **Crie um ambiente virtual e instale em modo editável**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # ou venv\Scripts\activate no Windows
    pip install -e ".[dev,requests,encryption]"
    ```
2.  Consulte a seção [Cliente Python API](./api-client/index.md) para detalhes sobre como usá-la.

### Para Contribuidores do Projeto

Se você deseja contribuir para qualquer parte do projeto:

1.  Leia o [Guia do Desenvolvedor](./developer-guide.md) para informações sobre o setup de desenvolvimento, fluxo de trabalho, testes, etc.
2.  Considere usar Docker para a interface web para um ambiente consistente.

## Navegando pela Documentação

Use o menu de navegação à esquerda para explorar os tópicos. Se você tiver alguma dúvida ou encontrar problemas, por favor, abra uma [issue no GitHub](https://github.com/prof-gabrielramos/client-py/issues).
