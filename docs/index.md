# Bem-vindo ao SMS Gateway Client & Web Interface

Este projeto fornece um conjunto de ferramentas para interagir com o [SMS Gateway for Android™](https://sms-gate.app/), permitindo que você envie mensagens SMS programaticamente através dos seus dispositivos Android.

## Componentes Principais

O projeto é composto por duas partes principais:

1.  **`android-sms-gateway` (Biblioteca Cliente Python)**:
    Uma biblioteca Python robusta e moderna para integração com a API do SMS Gateway. Ela oferece:
    *   Clientes síncronos e assíncronos.
    *   Suporte a criptografia de ponta a ponta.
    *   Gerenciamento de webhooks.
    *   E muito mais!
    *   Ideal para integrar funcionalidades de SMS em suas aplicações Python.
    *   *Licença: Apache 2.0*

2.  **`sms-gateway-web` (Interface Web)**:
    Uma interface de usuário baseada na web, construída com Flask, que utiliza a biblioteca cliente Python. Ela fornece um dashboard para:
    *   Enviar SMS facilmente.
    *   Visualizar histórico de mensagens.
    *   Gerenciar contatos e configurações de conexão.
    *   Pode ser facilmente "deployada" usando Docker.
    *   *Licença: MIT*

## Navegação da Documentação

*   **[Guia de Início Rápido](./getting-started.md)**: Comece aqui! Visão geral e primeiros passos.
*   **Interface Web**:
    *   **[Visão Geral](./web-interface/index.md)**
    *   **[Instalação e Execução](./web-interface/installation.md)**
    *   **[Configuração](./web-interface/configuration.md)**
    *   **[Uso](./web-interface/usage.md)**
*   **Cliente Python API**:
    *   **[Visão Geral](./api-client/index.md)**
    *   **[Instalação](./api-client/installation.md)**
    *   **[Primeiros Passos](./api-client/first-steps.md)**
    *   **[Guia do Cliente](./api-client/client-guide.md)**
    *   **[Criptografia](./api-client/encryption.md)**
*   **Deployment**:
    *   **[Visão Geral](./deployment/index.md)**
    *   **[Docker (Geral)](./deployment/docker.md)**
    *   **[Coolify](./deployment/coolify.md)**
    *   **[VPS com Portainer + Traefik](./deployment/vps-portainer-traefik.md)**
*   **[Guia do Desenvolvedor](./developer-guide.md)**: Para quem deseja contribuir com o projeto.
*   **[Licença](./license.md)**: Informações sobre as licenças do projeto.

## Contribuições

Contribuições são bem-vindas! Por favor, consulte o [Guia do Desenvolvedor](./developer-guide.md) e o `README.md` principal do projeto no [repositório GitHub](https://github.com/prof-gabrielramos/client-py) para mais informações sobre como contribuir.

## Suporte e Issues

Se você encontrar algum problema, tiver dúvidas ou sugestões, por favor, abra uma [issue no GitHub](https://github.com/prof-gabrielramos/client-py/issues).

---

*Android é uma marca registrada da Google LLC. Este projeto não é afiliado nem endossado pela Google.*

*Esta documentação é gerada usando [MkDocs](https://www.mkdocs.org/) com o tema [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).*
