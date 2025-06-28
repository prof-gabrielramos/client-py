# Guia de Segurança

## Visão Geral

Este documento descreve as medidas de segurança implementadas e as práticas recomendadas para manter a aplicação segura em produção.

## Medidas de Segurança Implementadas

### 1. Autenticação e Autorização

#### Autenticação
- **Método**: Session-based authentication
- **Proteção**: Rate limiting (5 tentativas por 5 minutos)
- **Senha**: Hashing com Werkzeug (PBKDF2)
- **Sessão**: Cookies seguros com HTTPOnly e SameSite

#### Autorização
- **Middleware**: Decorator `@require_auth`
- **Validação**: Verificação de sessão em cada request
- **Timeout**: Sessões expiram em 1 hora

### 2. Proteção contra Ataques

#### SQL Injection
- **Proteção**: SQLAlchemy ORM com prepared statements
- **Validação**: Sanitização de todos os inputs
- **Exemplo**:
```python
# SEGURO
user = User.query.filter_by(username=username).first()

# EVITAR
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
```

#### Cross-Site Scripting (XSS)
- **Proteção**: Sanitização com biblioteca `bleach`
- **Templates**: Auto-escape habilitado no Jinja2
- **Headers**: Content-Type validation

#### Cross-Site Request Forgery (CSRF)
- **Proteção**: Flask-WTF CSRF tokens
- **Validação**: Token em todos os formulários
- **Configuração**: Timeout de 1 hora para tokens

#### Rate Limiting
- **Implementação**: Flask-Limiter
- **Limites**:
  - Login: 5 tentativas por 5 minutos
  - API: 10 requests por minuto
  - SMS: 10 mensagens por minuto

### 3. Segurança de Dados

#### Criptografia
- **Em Trânsito**: HTTPS obrigatório (TLS 1.2+)
- **Em Repouso**: Senhas hasheadas
- **Sessões**: Cookies criptografados

#### Validação de Entrada
- **Sanitização**: Todos os inputs são sanitizados
- **Validação**: Tipos de dados e formatos
- **Limites**: Tamanho máximo de mensagens (1600 chars)

### 4. Headers de Segurança

```nginx
# Configuração Nginx
add_header X-Frame-Options DENY;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";
add_header Referrer-Policy "strict-origin-when-cross-origin";
```

## Configuração Segura

### 1. Variáveis de Ambiente

```bash
# Secrets (NUNCA commitar)
SECRET_KEY=your-super-secret-key-here
DB_PASSWORD=strong-database-password
REDIS_PASSWORD=strong-redis-password
GATEWAY_API_KEY=your-gateway-api-key

# Configurações de segurança
FORCE_HTTPS=true
SESSION_COOKIE_SECURE=true
WTF_CSRF_ENABLED=true
```

### 2. Configuração do Banco

```sql
-- Criar usuário com privilégios limitados
CREATE USER sms_app WITH PASSWORD 'strong_password';
GRANT CONNECT ON DATABASE sms_gateway TO sms_app;
GRANT USAGE ON SCHEMA public TO sms_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO sms_app;
```

### 3. Firewall

```bash
# Permitir apenas portas necessárias
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP (redirect para HTTPS)
ufw allow 443/tcp   # HTTPS
ufw enable
```

## Monitoramento de Segurança

### 1. Logs de Segurança

#### Eventos Monitorados
- Tentativas de login falhadas
- Rate limiting ativado
- Erros de validação
- Acessos a endpoints sensíveis

#### Exemplo de Log
```
2024-01-15 10:30:45 WARNING: Failed login attempt for user admin from 192.168.1.100
2024-01-15 10:31:00 WARNING: Rate limit exceeded for IP 192.168.1.100
```

### 2. Alertas Automáticos

```bash
# Script de monitoramento (cron job)
#!/bin/bash
FAILED_LOGINS=$(grep "Failed login" /app/logs/app.log | grep "$(date +%Y-%m-%d)" | wc -l)

if [ $FAILED_LOGINS -gt 10 ]; then
    echo "ALERT: $FAILED_LOGINS failed login attempts today" | \
    mail -s "Security Alert" security@company.com
fi
```

### 3. Métricas de Segurança

- **Failed Login Rate**: < 5% das tentativas
- **Rate Limit Hits**: < 1% das requests
- **SSL Certificate**: Válido e não expirando em 30 dias
- **Vulnerability Scan**: Sem vulnerabilidades críticas

## Procedimentos de Resposta a Incidentes

### 1. Detecção de Ataque

#### Indicadores
- Múltiplas tentativas de login de IPs diferentes
- Requests com payloads suspeitos
- Tráfego anômalo em horários incomuns

#### Resposta Imediata
```bash
# 1. Identificar IP atacante
grep "Failed login" logs/app.log | tail -100

# 2. Bloquear IP temporariamente
iptables -A INPUT -s ATTACKER_IP -j DROP

# 3. Notificar equipe
echo "Attack detected from $ATTACKER_IP" | mail -s "SECURITY ALERT" security@company.com
```

### 2. Comprometimento Suspeito

#### Ações Imediatas
1. **Isolar**: Desconectar da rede se necessário
2. **Preservar**: Fazer backup dos logs
3. **Investigar**: Analisar logs de acesso
4. **Comunicar**: Notificar stakeholders

#### Comandos de Investigação
```bash
# Verificar logins recentes
grep "Successful login" logs/app.log | tail -50

# Verificar ações de usuários
grep "user_id:" logs/app.log | tail -100

# Verificar mudanças de configuração
grep "Settings updated" logs/app.log
```

## Auditoria de Segurança

### 1. Checklist Mensal

- [ ] Atualizar dependências
- [ ] Verificar certificados SSL
- [ ] Revisar logs de segurança
- [ ] Testar backup e recovery
- [ ] Verificar configurações de firewall
- [ ] Validar rate limiting
- [ ] Testar procedimentos de resposta

### 2. Scan de Vulnerabilidades

```bash
# Scan de portas
nmap -sS -O target_host

# Scan de vulnerabilidades web
nikto -h https://sms.yourdomain.com

# Verificar headers de segurança
curl -I https://sms.yourdomain.com
```

### 3. Teste de Penetração

#### Testes Recomendados
- **Authentication Bypass**: Tentar contornar login
- **SQL Injection**: Testar inputs com payloads
- **XSS**: Testar campos de entrada
- **CSRF**: Verificar proteção de formulários
- **Rate Limiting**: Testar limites configurados

## Compliance e Regulamentações

### LGPD (Lei Geral de Proteção de Dados)

#### Medidas Implementadas
- **Minimização**: Coleta apenas dados necessários
- **Consentimento**: Usuário autoriza envio de SMS
- **Segurança**: Dados protegidos em trânsito e repouso
- **Retenção**: Logs mantidos por período limitado

#### Direitos dos Usuários
- **Acesso**: Usuário pode ver seus dados
- **Correção**: Usuário pode corrigir dados
- **Exclusão**: Usuário pode deletar conta

### Boas Práticas

1. **Princípio do Menor Privilégio**: Usuários têm apenas permissões necessárias
2. **Defesa em Profundidade**: Múltiplas camadas de segurança
3. **Fail Secure**: Sistema falha de forma segura
4. **Auditabilidade**: Todas as ações são logadas
5. **Atualizações**: Dependências mantidas atualizadas

## Contatos de Emergência

- **Equipe de Segurança**: security@company.com
- **DevOps**: devops@company.com
- **CERT.br**: cert@cert.br (incidentes nacionais)
- **Polícia Civil**: 197 (crimes cibernéticos)