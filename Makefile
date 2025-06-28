# Makefile para o projeto SMS Gateway Client & Web

.PHONY: all clean install-dev install-web-manual lint format test coverage docs serve-docs build-docs build-docker run-docker stop-docker logs-docker help clean-pycache clean-build clean-venv clean-docs clean-docker-config

# ==============================================================================
# Variáveis
# ==============================================================================
PYTHON_INTERPRETER := python3 # Ou apenas python, dependendo do seu sistema
VENV_DIR := venv
# Tenta usar pipenv run se pipenv estiver disponível, caso contrário executa diretamente
PIPENV_EXISTS := $(shell command -v pipenv 2> /dev/null)
ifdef PIPENV_EXISTS
	PIPENV_RUN := pipenv run
else
	PIPENV_RUN :=
endif

# ==============================================================================
# Alvos Principais
# ==============================================================================

all: help

help:
	@echo "Comandos disponíveis:"
	@echo "  make install-dev         Instala dependências de desenvolvimento da biblioteca (Pipenv)."
	@echo "  make install-web-manual  Instala dependências da interface web manualmente (requirements.txt)."
	@echo "  make lint                Executa linters (black, flake8, isort, mypy)."
	@echo "  make format              Formata o código com Black e iSort."
	@echo "  make test                Executa testes com pytest."
	@echo "  make coverage            Executa testes e gera relatório de cobertura."
	@echo "  make docs                Constrói a documentação com MkDocs (alias para build-docs)."
	@echo "  make build-docs          Constrói a documentação com MkDocs."
	@echo "  make serve-docs          Serve a documentação localmente com MkDocs (http://localhost:8000)."
	@echo ""
	@echo "Docker (para sms-gateway-web):"
	@echo "  make build-docker        Constrói a imagem Docker para a interface web."
	@echo "  make run-docker          Executa a interface web usando Docker Compose (em background)."
	@echo "  make stop-docker         Para os containers Docker da interface web."
	@echo "  make logs-docker         Mostra os logs do container da interface web."
	@echo ""
	@echo "Limpeza:"
	@echo "  make clean               Remove arquivos temporários e de build (pycache, build artifacts, docs site)."
	@echo "  make clean-pycache       Remove arquivos __pycache__ e .pyc."
	@echo "  make clean-build         Remove artefatos de build (dist, build, .egg-info)."
	@echo "  make clean-venv          Remove o ambiente virtual Pipenv (se 'pipenv --rm' funcionar) ou o diretório ./venv."
	@echo "  make clean-docs          Remove o site MkDocs construído (./site)."
	@echo "  make clean-docker-config Remove o diretório de configuração local do Docker (./sms-gateway-web/config)."


# ==============================================================================
# Instalação e Ambiente
# ==============================================================================

install-dev:
	@echo ">>> Instalando dependências de desenvolvimento com Pipenv (inclui mkdocs, mkdocs-material)..."
	pipenv install --dev

install-web-manual:
	@echo ">>> Instalando dependências da interface web (sms-gateway-web/requirements.txt)..."
	$(PYTHON_INTERPRETER) -m pip install -r sms-gateway-web/requirements.txt

# ==============================================================================
# Qualidade de Código e Testes
# ==============================================================================

lint:
	@echo ">>> Verificando estilo com Black..."
	$(PIPENV_RUN) black --check .
	@echo ">>> Verificando com Flake8..."
	$(PIPENV_RUN) flake8 .
	@echo ">>> Verificando importações com iSort..."
	$(PIPENV_RUN) isort --check-only .
	@echo ">>> Verificando tipos com MyPy (para a biblioteca android_sms_gateway)..."
	$(PIPENV_RUN) mypy android_sms_gateway

format:
	@echo ">>> Formatando com Black..."
	$(PIPENV_RUN) black .
	@echo ">>> Formatando importações com iSort..."
	$(PIPENV_RUN) isort .

test:
	@echo ">>> Executando testes com Pytest..."
	$(PIPENV_RUN) pytest

coverage:
	@echo ">>> Executando testes e gerando relatório de cobertura..."
	$(PIPENV_RUN) pytest --cov=android_sms_gateway --cov-report=html --cov-report=term
	@echo "Relatório HTML de cobertura em: htmlcov/index.html"

# ==============================================================================
# Documentação (MkDocs)
# ==============================================================================

docs: build-docs

build-docs:
	@echo ">>> Construindo documentação com MkDocs (output em ./site)..."
	$(PIPENV_RUN) mkdocs build

serve-docs:
	@echo ">>> Servindo documentação localmente em http://localhost:8000 (Pressione Ctrl+C para parar)..."
	$(PIPENV_RUN) mkdocs serve

# ==============================================================================
# Docker (para sms-gateway-web)
# ==============================================================================

build-docker:
	@echo ">>> Construindo imagem Docker para sms-gateway-web..."
	cd sms-gateway-web && docker-compose build

run-docker:
	@echo ">>> Executando sms-gateway-web com Docker Compose em background..."
	cd sms-gateway-web && docker-compose up -d
	@echo "Interface web deve estar disponível em http://localhost:5000"

stop-docker:
	@echo ">>> Parando containers Docker de sms-gateway-web..."
	cd sms-gateway-web && docker-compose down

logs-docker:
	@echo ">>> Mostrando logs do container sms-gateway-web (Pressione Ctrl+C para parar)..."
	cd sms-gateway-web && docker-compose logs -f


# ==============================================================================
# Limpeza
# ==============================================================================

clean-pycache:
	@echo ">>> Removendo arquivos __pycache__ e .pyc..."
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

clean-build:
	@echo ">>> Removendo artefatos de build Python..."
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-venv:
	@echo ">>> Tentando remover ambiente virtual Pipenv..."
	-$(PIPENV_RUN) pipenv --rm # O '-' ignora erros se o ambiente não existir ou pipenv não estiver configurado
	@echo ">>> Removendo diretório $(VENV_DIR) (se existir)..."
	rm -rf $(VENV_DIR)

clean-docs:
	@echo ">>> Removendo site MkDocs construído (./site)..."
	rm -rf site

clean-docker-config:
	@echo ">>> Removendo diretório de configuração local do Docker (./sms-gateway-web/config)..."
	@echo "AVISO: Isso removerá o banco de dados e configurações da interface web local."
	rm -rf ./sms-gateway-web/config

clean: clean-pycache clean-build clean-docs
	@echo "Limpeza básica concluída (pycache, build artifacts, docs site)."
	@echo "Use 'make clean-venv' para remover o ambiente virtual."
	@echo "Use 'make clean-docker-config' para remover a configuração local do Docker da web."

# ==============================================================================
# Comandos de Release (Exemplo - requer twine, build do Pipenv)
# ==============================================================================
# .PHONY: build-package release-test release
# build-package: clean-build
# 	@echo ">>> Construindo pacote wheel e sdist..."
# 	$(PIPENV_RUN) python -m build # ou `pipenv run python setup.py sdist bdist_wheel` se usar setup.py
#
# release-test: build-package
# 	@echo ">>> Fazendo upload para TestPyPI..."
# 	$(PIPENV_RUN) twine upload --repository testpypi dist/*
#
# release: build-package
# 	@echo ">>> Fazendo upload para PyPI..."
# 	$(PIPENV_RUN) twine upload dist/*
