# Guia de Deploy em Produção

## Pré-requisitos

### Sistema
- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM mínimo
- 20GB espaço em disco
- SSL/TLS certificados

### Variáveis de Ambiente
Copie `.env.example` para `.env` e configure:

```bash
cp .env.example .env
# Edite .env com suas configurações
```

## Deploy Passo a Passo

### 1. Preparação do Ambiente

```bash
# Clone o repositório
git clone https://github.com/your-repo/sms-gateway.git
cd sms-gateway/sms-gateway-web

# Configure permissões
chmod +x scripts/*.sh

# Crie diretórios necessários
mkdir -p logs backups ssl
```

### 2. Configuração SSL

```bash
# Coloque seus certificados em:
# ssl/cert.pem
# ssl/key.pem

# Ou use Let's Encrypt
certbot certonly --standalone -d sms.yourdomain.com
cp /etc/letsencrypt/live/sms.yourdomain.com/fullchain.pem ssl/cert.pem
cp /etc/letsencrypt/live/sms.yourdomain.com/privkey.pem ssl/key.pem
```

### 3. Deploy da Aplicação

```bash
# Deploy inicial
./scripts/deploy.sh

# Verificar status
docker-compose -f docker-compose.prod.yml ps
```

### 4. Configuração Inicial

```bash
# Criar usuário admin
docker-compose -f docker-compose.prod.yml exec web flask create-admin

# Verificar saúde da aplicação
curl https://sms.yourdomain.com/api/health
```

## Monitoramento

### Health Checks
```bash
# Verificar status dos serviços
./scripts/monitor.sh

# Logs em tempo real
docker-compose -f docker-compose.prod.yml logs -f
```

### Métricas
- **CPU/Memory**: Disponível em `/api/metrics`
- **Application**: Logs em `logs/app.log`
- **Nginx**: Logs em `logs/nginx/`

## Backup e Recovery

### Backup Automático
```bash
# Configurar cron para backup diário
echo "0 2 * * * /path/to/scripts/backup.sh" | crontab -
```

### Recovery
```bash
# Restaurar backup
gunzip backup_file.sql.gz
docker-compose -f docker-compose.prod.yml exec db psql -U user -d sms_gateway < backup_file.sql
```

## Troubleshooting

### Problemas Comuns

#### Aplicação não inicia
```bash
# Verificar logs
docker-compose -f docker-compose.prod.yml logs web

# Verificar configuração
docker-compose -f docker-compose.prod.yml config
```

#### Banco de dados não conecta
```bash
# Verificar status do PostgreSQL
docker-compose -f docker-compose.prod.yml exec db pg_isready

# Verificar logs do banco
docker-compose -f docker-compose.prod.yml logs db
```

#### SSL/HTTPS problemas
```bash
# Verificar certificados
openssl x509 -in ssl/cert.pem -text -noout

# Testar configuração Nginx
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

## Atualizações

### Deploy de Nova Versão
```bash
# Backup antes da atualização
./scripts/backup.sh

# Deploy nova versão
git pull origin main
./scripts/deploy.sh
```

### Rollback
```bash
# Voltar para versão anterior
git checkout previous-version-tag
./scripts/deploy.sh
```

## Segurança

### Checklist de Segurança
- [ ] HTTPS configurado e funcionando
- [ ] Firewall configurado (apenas portas 80, 443 abertas)
- [ ] Senhas fortes configuradas
- [ ] Backup funcionando
- [ ] Logs sendo coletados
- [ ] Rate limiting ativo
- [ ] Headers de segurança configurados

### Monitoramento de Segurança
```bash
# Verificar tentativas de login
grep "Failed login" logs/app.log

# Verificar rate limiting
grep "Rate limit" logs/nginx/access.log
```