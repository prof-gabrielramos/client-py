# Runbook de Operações

## Visão Geral

Este runbook contém procedimentos operacionais para o SMS Gateway Web Interface em produção.

## Contatos de Emergência

- **DevOps**: devops@company.com
- **Segurança**: security@company.com
- **Suporte**: support@company.com

## Procedimentos de Emergência

### Aplicação Fora do Ar

#### Sintomas
- HTTP 502/503 errors
- Timeout nas requisições
- Health check falhando

#### Diagnóstico
```bash
# 1. Verificar status dos containers
docker-compose -f docker-compose.prod.yml ps

# 2. Verificar logs da aplicação
docker-compose -f docker-compose.prod.yml logs --tail=100 web

# 3. Verificar recursos do sistema
docker stats --no-stream

# 4. Verificar conectividade do banco
docker-compose -f docker-compose.prod.yml exec db pg_isready
```

#### Resolução
```bash
# 1. Restart da aplicação
docker-compose -f docker-compose.prod.yml restart web

# 2. Se não resolver, restart completo
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

# 3. Verificar health check
curl -f https://sms.yourdomain.com/api/health
```

### Banco de Dados Indisponível

#### Sintomas
- Erros de conexão com banco
- Timeout em queries
- Aplicação retornando 500 errors

#### Diagnóstico
```bash
# 1. Verificar status do PostgreSQL
docker-compose -f docker-compose.prod.yml exec db pg_isready

# 2. Verificar logs do banco
docker-compose -f docker-compose.prod.yml logs db

# 3. Verificar conexões ativas
docker-compose -f docker-compose.prod.yml exec db psql -U user -d sms_gateway -c "SELECT count(*) FROM pg_stat_activity;"

# 4. Verificar espaço em disco
df -h
```

#### Resolução
```bash
# 1. Restart do banco
docker-compose -f docker-compose.prod.yml restart db

# 2. Se não resolver, verificar corrupção
docker-compose -f docker-compose.prod.yml exec db pg_dump -U user sms_gateway > test_dump.sql

# 3. Restaurar backup se necessário
./scripts/backup.sh restore latest
```

### Alto Uso de Recursos

#### Sintomas
- CPU > 80%
- Memory > 80%
- Disk > 90%
- Aplicação lenta

#### Diagnóstico
```bash
# 1. Verificar uso de recursos
./scripts/monitor.sh

# 2. Verificar processos
docker-compose -f docker-compose.prod.yml exec web ps aux

# 3. Verificar logs de performance
grep "Slow request" logs/app.log

# 4. Verificar cache hit rate
docker-compose -f docker-compose.prod.yml exec redis redis-cli info stats
```

#### Resolução
```bash
# 1. Limpar cache se necessário
docker-compose -f docker-compose.prod.yml exec redis redis-cli FLUSHALL

# 2. Restart da aplicação
docker-compose -f docker-compose.prod.yml restart web

# 3. Verificar e limpar logs antigos
find logs/ -name "*.log" -mtime +7 -delete

# 4. Limpar imagens Docker antigas
docker image prune -f
```

## Manutenção Programada

### Backup Manual
```bash
# Criar backup completo
./scripts/backup.sh

# Verificar integridade do backup
gunzip -t backups/latest_backup.sql.gz
```

### Atualização de Dependências
```bash
# 1. Backup antes da atualização
./scripts/backup.sh

# 2. Atualizar imagens Docker
docker-compose -f docker-compose.prod.yml pull

# 3. Restart com novas imagens
docker-compose -f docker-compose.prod.yml up -d

# 4. Verificar funcionamento
curl -f https://sms.yourdomain.com/api/health
```

### Limpeza de Logs
```bash
# Rotacionar logs da aplicação
docker-compose -f docker-compose.prod.yml exec web logrotate /etc/logrotate.conf

# Limpar logs antigos do Nginx
find logs/nginx/ -name "*.log" -mtime +30 -delete

# Limpar logs antigos da aplicação
find logs/ -name "*.log" -mtime +30 -delete
```

## Monitoramento

### Métricas Críticas

#### Aplicação
- **Response Time**: < 200ms (95th percentile)
- **Error Rate**: < 1%
- **Availability**: > 99.9%

#### Sistema
- **CPU Usage**: < 70%
- **Memory Usage**: < 80%
- **Disk Usage**: < 85%

#### Banco de Dados
- **Connection Pool**: < 80% utilização
- **Query Time**: < 100ms (95th percentile)
- **Lock Waits**: < 5%

### Alertas Configurados

#### Críticos (Resposta Imediata)
- Aplicação fora do ar
- Banco de dados indisponível
- Disk usage > 90%
- Memory usage > 90%

#### Warnings (Resposta em 1 hora)
- Response time > 500ms
- Error rate > 5%
- CPU usage > 80%
- Memory usage > 80%

### Comandos de Monitoramento

```bash
# Status geral do sistema
./scripts/monitor.sh

# Métricas da aplicação
curl -s https://sms.yourdomain.com/api/metrics | jq .

# Status dos containers
docker-compose -f docker-compose.prod.yml ps

# Logs em tempo real
docker-compose -f docker-compose.prod.yml logs -f --tail=50

# Verificar performance do banco
docker-compose -f docker-compose.prod.yml exec db psql -U user -d sms_gateway -c "SELECT * FROM pg_stat_activity WHERE state = 'active';"
```

## Procedimentos de Segurança

### Incidente de Segurança

#### Detecção
- Múltiplas tentativas de login falhadas
- Tráfego anômalo
- Alertas de rate limiting

#### Resposta
```bash
# 1. Verificar logs de segurança
grep "Failed login" logs/app.log | tail -100

# 2. Verificar IPs suspeitos
grep "Rate limit exceeded" logs/nginx/access.log | awk '{print $1}' | sort | uniq -c | sort -nr

# 3. Bloquear IP se necessário (temporário)
docker-compose -f docker-compose.prod.yml exec nginx nginx -s reload

# 4. Notificar equipe de segurança
echo "Security incident detected" | mail -s "ALERT: Security Incident" security@company.com
```

### Auditoria de Segurança

```bash
# Verificar usuários ativos
docker-compose -f docker-compose.prod.yml exec web flask list-users

# Verificar configurações de segurança
docker-compose -f docker-compose.prod.yml exec web flask security-check

# Verificar certificados SSL
openssl x509 -in ssl/cert.pem -noout -dates
```

## Escalação

### Nível 1 - Suporte Técnico
- Problemas básicos de conectividade
- Reinicialização de serviços
- Verificação de status

### Nível 2 - DevOps
- Problemas de infraestrutura
- Performance issues
- Atualizações de sistema

### Nível 3 - Desenvolvimento
- Bugs na aplicação
- Problemas de código
- Mudanças arquiteturais

### Nível 4 - Arquitetura
- Problemas sistêmicos
- Decisões de arquitetura
- Planejamento de capacidade