#!/bin/bash
# Script de validação automática para deploy

set -e

echo "🚀 Iniciando validação de deploy..."

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
PASSED=0
FAILED=0
WARNINGS=0

# Função para log
log_test() {
    local status=$1
    local message=$2
    
    case $status in
        "PASS")
            echo -e "${GREEN}✅ PASS${NC}: $message"
            ((PASSED++))
            ;;
        "FAIL")
            echo -e "${RED}❌ FAIL${NC}: $message"
            ((FAILED++))
            ;;
        "WARN")
            echo -e "${YELLOW}⚠️  WARN${NC}: $message"
            ((WARNINGS++))
            ;;
    esac
}

# Função para testar URL
test_url() {
    local url=$1
    local expected_status=$2
    local description=$3
    
    if curl -s -o /dev/null -w "%{http_code}" "$url" | grep -q "$expected_status"; then
        log_test "PASS" "$description"
    else
        log_test "FAIL" "$description"
    fi
}

# Função para testar comando
test_command() {
    local command=$1
    local description=$2
    
    if eval "$command" > /dev/null 2>&1; then
        log_test "PASS" "$description"
    else
        log_test "FAIL" "$description"
    fi
}

echo "📋 Executando testes de validação..."

# 1. Testes de Infraestrutura
echo -e "\n🏗️  Testando Infraestrutura..."

test_command "docker-compose -f docker-compose.prod.yml ps | grep -q 'Up'" "Containers estão rodando"
test_command "docker-compose -f docker-compose.prod.yml exec -T db pg_isready" "Banco de dados está acessível"
test_command "docker-compose -f docker-compose.prod.yml exec -T redis redis-cli ping | grep -q PONG" "Redis está acessível"

# 2. Testes de Conectividade
echo -e "\n🌐 Testando Conectividade..."

BASE_URL="https://sms.yourdomain.com"
test_url "$BASE_URL" "200" "Página principal acessível"
test_url "$BASE_URL/api/health" "200" "Health check funcionando"
test_url "http://sms.yourdomain.com" "301" "HTTP redirect para HTTPS"

# 3. Testes de Segurança
echo -e "\n🔒 Testando Segurança..."

# Verificar headers de segurança
HEADERS=$(curl -s -I "$BASE_URL")
if echo "$HEADERS" | grep -q "Strict-Transport-Security"; then
    log_test "PASS" "HSTS header presente"
else
    log_test "FAIL" "HSTS header ausente"
fi

if echo "$HEADERS" | grep -q "X-Frame-Options"; then
    log_test "PASS" "X-Frame-Options header presente"
else
    log_test "FAIL" "X-Frame-Options header ausente"
fi

# Testar rate limiting (deve falhar após várias tentativas)
echo "Testando rate limiting..."
RATE_LIMIT_TEST=0
for i in {1..6}; do
    if curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/auth/login" | grep -q "429"; then
        RATE_LIMIT_TEST=1
        break
    fi
    sleep 1
done

if [ $RATE_LIMIT_TEST -eq 1 ]; then
    log_test "PASS" "Rate limiting funcionando"
else
    log_test "WARN" "Rate limiting não testado adequadamente"
fi

# 4. Testes de Performance
echo -e "\n⚡ Testando Performance..."

# Teste de tempo de resposta
RESPONSE_TIME=$(curl -s -o /dev/null -w "%{time_total}" "$BASE_URL")
if (( $(echo "$RESPONSE_TIME < 2.0" | bc -l) )); then
    log_test "PASS" "Tempo de resposta aceitável ($RESPONSE_TIME s)"
else
    log_test "WARN" "Tempo de resposta alto ($RESPONSE_TIME s)"
fi

# Teste de compressão
if curl -s -H "Accept-Encoding: gzip" -I "$BASE_URL" | grep -q "Content-Encoding: gzip"; then
    log_test "PASS" "Compressão gzip habilitada"
else
    log_test "WARN" "Compressão gzip não detectada"
fi

# 5. Testes de Funcionalidade
echo -e "\n🔧 Testando Funcionalidade..."

# Health check detalhado
HEALTH_RESPONSE=$(curl -s "$BASE_URL/api/health")
if echo "$HEALTH_RESPONSE" | grep -q '"status":"healthy"'; then
    log_test "PASS" "Health check retorna status healthy"
else
    log_test "FAIL" "Health check não retorna status healthy"
fi

# Verificar se a aplicação está servindo conteúdo correto
if curl -s "$BASE_URL" | grep -q "SMS Gateway"; then
    log_test "PASS" "Página principal carrega conteúdo correto"
else
    log_test "FAIL" "Página principal não carrega conteúdo esperado"
fi

# 6. Testes de Backup
echo -e "\n💾 Testando Backup..."

if [ -f "./scripts/backup.sh" ]; then
    if ./scripts/backup.sh > /dev/null 2>&1; then
        log_test "PASS" "Script de backup executa sem erros"
    else
        log_test "FAIL" "Script de backup falhou"
    fi
else
    log_test "WARN" "Script de backup não encontrado"
fi

# Verificar se existem backups recentes
if find backups/ -name "*.sql.gz" -mtime -1 2>/dev/null | grep -q .; then
    log_test "PASS" "Backup recente encontrado"
else
    log_test "WARN" "Nenhum backup recente encontrado"
fi

# 7. Testes de Logs
echo -e "\n📝 Testando Logs..."

if [ -f "logs/app.log" ]; then
    log_test "PASS" "Arquivo de log da aplicação existe"
    
    # Verificar se logs estão sendo escritos
    if [ -s "logs/app.log" ]; then
        log_test "PASS" "Logs estão sendo escritos"
    else
        log_test "WARN" "Arquivo de log está vazio"
    fi
else
    log_test "FAIL" "Arquivo de log da aplicação não encontrado"
fi

# 8. Testes de Recursos do Sistema
echo -e "\n💻 Testando Recursos do Sistema..."

# Verificar uso de CPU
CPU_USAGE=$(docker stats --no-stream --format "table {{.CPUPerc}}" | tail -n +2 | head -1 | sed 's/%//')
if (( $(echo "$CPU_USAGE < 70" | bc -l) )); then
    log_test "PASS" "Uso de CPU aceitável ($CPU_USAGE%)"
else
    log_test "WARN" "Uso de CPU alto ($CPU_USAGE%)"
fi

# Verificar uso de memória
MEMORY_USAGE=$(docker stats --no-stream --format "table {{.MemPerc}}" | tail -n +2 | head -1 | sed 's/%//')
if (( $(echo "$MEMORY_USAGE < 80" | bc -l) )); then
    log_test "PASS" "Uso de memória aceitável ($MEMORY_USAGE%)"
else
    log_test "WARN" "Uso de memória alto ($MEMORY_USAGE%)"
fi

# Verificar espaço em disco
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -lt 85 ]; then
    log_test "PASS" "Espaço em disco suficiente ($DISK_USAGE% usado)"
else
    log_test "WARN" "Espaço em disco baixo ($DISK_USAGE% usado)"
fi

# Resumo dos resultados
echo -e "\n📊 Resumo dos Resultados:"
echo -e "✅ Testes Passaram: ${GREEN}$PASSED${NC}"
echo -e "❌ Testes Falharam: ${RED}$FAILED${NC}"
echo -e "⚠️  Avisos: ${YELLOW}$WARNINGS${NC}"

# Determinar status final
if [ $FAILED -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "\n🎉 ${GREEN}DEPLOY APROVADO${NC} - Todos os testes passaram!"
        exit 0
    else
        echo -e "\n⚠️  ${YELLOW}DEPLOY APROVADO COM RESSALVAS${NC} - Alguns avisos encontrados"
        exit 0
    fi
else
    echo -e "\n🚫 ${RED}DEPLOY REPROVADO${NC} - Falhas críticas encontradas"
    exit 1
fi