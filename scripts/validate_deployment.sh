#!/bin/bash
# Comprehensive SMS Gateway Deployment Validation Script
# Performs security, functionality, performance, and infrastructure checks

set -e

# Script configuration
SCRIPT_NAME="SMS Gateway Deployment Validator"
VERSION="1.0.0"
LOG_FILE="validation_$(date +%Y%m%d_%H%M%S).log"
REPORT_FILE="validation_report_$(date +%Y%m%d_%H%M%S).html"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Test counters
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
WARNING_TESTS=0
CRITICAL_FAILURES=0

# Configuration variables (can be overridden by environment)
BASE_URL="${BASE_URL:-https://sms.yourdomain.com}"
HTTP_URL="${HTTP_URL:-http://sms.yourdomain.com}"
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.prod.yml}"
TIMEOUT="${TIMEOUT:-30}"
MAX_RESPONSE_TIME="${MAX_RESPONSE_TIME:-2.0}"
MAX_CPU_USAGE="${MAX_CPU_USAGE:-70}"
MAX_MEMORY_USAGE="${MAX_MEMORY_USAGE:-80}"
MAX_DISK_USAGE="${MAX_DISK_USAGE:-85}"

# Required environment variables
REQUIRED_ENV_VARS=(
    "SECRET_KEY"
    "DATABASE_URL"
    "GATEWAY_URL"
)

# Initialize log file
init_logging() {
    echo "=== $SCRIPT_NAME v$VERSION ===" | tee "$LOG_FILE"
    echo "Validation started at: $(date)" | tee -a "$LOG_FILE"
    echo "Base URL: $BASE_URL" | tee -a "$LOG_FILE"
    echo "Compose file: $COMPOSE_FILE" | tee -a "$LOG_FILE"
    echo "========================================" | tee -a "$LOG_FILE"
}

# Logging functions
log_test() {
    local status=$1
    local category=$2
    local message=$3
    local details="${4:-}"
    
    ((TOTAL_TESTS++))
    
    local timestamp=$(date '+%H:%M:%S')
    local log_entry="[$timestamp] [$category] $message"
    
    case $status in
        "PASS")
            echo -e "${GREEN}✅ PASS${NC} [$category] $message" | tee -a "$LOG_FILE"
            ((PASSED_TESTS++))
            ;;
        "FAIL")
            echo -e "${RED}❌ FAIL${NC} [$category] $message" | tee -a "$LOG_FILE"
            if [ -n "$details" ]; then
                echo -e "   ${RED}Details: $details${NC}" | tee -a "$LOG_FILE"
            fi
            ((FAILED_TESTS++))
            ;;
        "CRITICAL")
            echo -e "${RED}🚨 CRITICAL${NC} [$category] $message" | tee -a "$LOG_FILE"
            if [ -n "$details" ]; then
                echo -e "   ${RED}Details: $details${NC}" | tee -a "$LOG_FILE"
            fi
            ((FAILED_TESTS++))
            ((CRITICAL_FAILURES++))
            ;;
        "WARN")
            echo -e "${YELLOW}⚠️  WARN${NC} [$category] $message" | tee -a "$LOG_FILE"
            if [ -n "$details" ]; then
                echo -e "   ${YELLOW}Details: $details${NC}" | tee -a "$LOG_FILE"
            fi
            ((WARNING_TESTS++))
            ;;
        "INFO")
            echo -e "${BLUE}ℹ️  INFO${NC} [$category] $message" | tee -a "$LOG_FILE"
            ;;
    esac
}

# Utility functions
check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_test "CRITICAL" "PREREQ" "Required command '$1' not found"
        return 1
    fi
    return 0
}

test_url() {
    local url=$1
    local expected_status=$2
    local description=$3
    local timeout=${4:-$TIMEOUT}
    
    local response
    response=$(curl -s -o /dev/null -w "%{http_code}:%{time_total}" --max-time "$timeout" "$url" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        local status_code=$(echo "$response" | cut -d: -f1)
        local response_time=$(echo "$response" | cut -d: -f2)
        
        if [ "$status_code" = "$expected_status" ]; then
            log_test "PASS" "HTTP" "$description (${response_time}s)"
        else
            log_test "FAIL" "HTTP" "$description" "Expected $expected_status, got $status_code"
        fi
    else
        log_test "FAIL" "HTTP" "$description" "Connection failed or timeout"
    fi
}

test_command() {
    local command=$1
    local description=$2
    local category="${3:-SYSTEM}"
    
    if eval "$command" > /dev/null 2>&1; then
        log_test "PASS" "$category" "$description"
        return 0
    else
        log_test "FAIL" "$category" "$description"
        return 1
    fi
}

# Check prerequisites
check_prerequisites() {
    echo -e "\n${PURPLE}🔍 Checking Prerequisites...${NC}"
    
    local required_commands=("curl" "docker" "docker-compose" "jq" "bc")
    
    for cmd in "${required_commands[@]}"; do
        check_command "$cmd"
    done
    
    # Check if compose file exists
    if [ ! -f "$COMPOSE_FILE" ]; then
        log_test "CRITICAL" "PREREQ" "Docker compose file not found: $COMPOSE_FILE"
    else
        log_test "PASS" "PREREQ" "Docker compose file found"
    fi
}

# Environment variables validation
validate_environment() {
    echo -e "\n${PURPLE}🌍 Validating Environment Variables...${NC}"
    
    for var in "${REQUIRED_ENV_VARS[@]}"; do
        if [ -z "${!var}" ]; then
            log_test "CRITICAL" "ENV" "Required environment variable $var is not set"
        else
            log_test "PASS" "ENV" "Environment variable $var is set"
        fi
    done
    
    # Check for sensitive data exposure
    if [ -n "$SECRET_KEY" ] && [ ${#SECRET_KEY} -lt 32 ]; then
        log_test "WARN" "ENV" "SECRET_KEY appears to be too short (< 32 characters)"
    fi
    
    # Validate URLs
    if [[ "$DATABASE_URL" =~ ^postgresql:// ]] || [[ "$DATABASE_URL" =~ ^sqlite:// ]]; then
        log_test "PASS" "ENV" "DATABASE_URL format is valid"
    else
        log_test "WARN" "ENV" "DATABASE_URL format may be invalid"
    fi
}

# Infrastructure tests
test_infrastructure() {
    echo -e "\n${PURPLE}🏗️  Testing Infrastructure...${NC}"
    
    # Check if Docker daemon is running
    test_command "docker info" "Docker daemon is running" "DOCKER"
    
    # Check container status
    if docker-compose -f "$COMPOSE_FILE" ps | grep -q "Up"; then
        log_test "PASS" "DOCKER" "Containers are running"
        
        # Get detailed container status
        local containers
        containers=$(docker-compose -f "$COMPOSE_FILE" ps --services)
        
        for container in $containers; do
            if docker-compose -f "$COMPOSE_FILE" ps "$container" | grep -q "Up"; then
                log_test "PASS" "DOCKER" "Container $container is healthy"
            else
                log_test "FAIL" "DOCKER" "Container $container is not running"
            fi
        done
    else
        log_test "CRITICAL" "DOCKER" "No containers are running"
    fi
    
    # Test database connectivity
    if docker-compose -f "$COMPOSE_FILE" exec -T db pg_isready 2>/dev/null; then
        log_test "PASS" "DATABASE" "PostgreSQL is ready"
        
        # Test database connection with query
        if docker-compose -f "$COMPOSE_FILE" exec -T db psql -U user -d sms_gateway -c "SELECT 1;" > /dev/null 2>&1; then
            log_test "PASS" "DATABASE" "Database query execution successful"
        else
            log_test "FAIL" "DATABASE" "Database query execution failed"
        fi
    else
        log_test "CRITICAL" "DATABASE" "Database is not accessible"
    fi
    
    # Test Redis connectivity
    if docker-compose -f "$COMPOSE_FILE" exec -T redis redis-cli ping 2>/dev/null | grep -q "PONG"; then
        log_test "PASS" "CACHE" "Redis is responding"
    else
        log_test "WARN" "CACHE" "Redis is not responding (may not be required)"
    fi
}

# Network connectivity tests
test_connectivity() {
    echo -e "\n${PURPLE}🌐 Testing Network Connectivity...${NC}"
    
    # Test main application
    test_url "$BASE_URL" "200" "Main application is accessible"
    test_url "$BASE_URL/api/health" "200" "Health check endpoint"
    
    # Test HTTPS redirect
    test_url "$HTTP_URL" "301" "HTTP to HTTPS redirect"
    
    # Test static assets
    test_url "$BASE_URL/static/css/app.min.css" "200" "Static CSS assets"
    test_url "$BASE_URL/static/js/app.min.js" "200" "Static JS assets"
    
    # Test API endpoints
    test_url "$BASE_URL/api/health" "200" "API health endpoint"
    
    # Test authentication endpoints
    test_url "$BASE_URL/auth/login" "200" "Login page accessible"
}

# Security validation
validate_security() {
    echo -e "\n${PURPLE}🔒 Validating Security Configuration...${NC}"
    
    # Check security headers
    local headers
    headers=$(curl -s -I "$BASE_URL" 2>/dev/null)
    
    if echo "$headers" | grep -qi "strict-transport-security"; then
        log_test "PASS" "SECURITY" "HSTS header present"
    else
        log_test "FAIL" "SECURITY" "HSTS header missing"
    fi
    
    if echo "$headers" | grep -qi "x-frame-options"; then
        log_test "PASS" "SECURITY" "X-Frame-Options header present"
    else
        log_test "FAIL" "SECURITY" "X-Frame-Options header missing"
    fi
    
    if echo "$headers" | grep -qi "x-content-type-options"; then
        log_test "PASS" "SECURITY" "X-Content-Type-Options header present"
    else
        log_test "FAIL" "SECURITY" "X-Content-Type-Options header missing"
    fi
    
    if echo "$headers" | grep -qi "x-xss-protection"; then
        log_test "PASS" "SECURITY" "X-XSS-Protection header present"
    else
        log_test "WARN" "SECURITY" "X-XSS-Protection header missing"
    fi
    
    # Test SSL/TLS certificate
    local ssl_info
    ssl_info=$(echo | openssl s_client -servername "$(echo "$BASE_URL" | sed 's|https://||')" -connect "$(echo "$BASE_URL" | sed 's|https://||'):443" 2>/dev/null | openssl x509 -noout -dates 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        log_test "PASS" "SECURITY" "SSL certificate is valid"
        
        # Check certificate expiration
        local expiry_date
        expiry_date=$(echo "$ssl_info" | grep "notAfter" | cut -d= -f2)
        local expiry_epoch
        expiry_epoch=$(date -d "$expiry_date" +%s 2>/dev/null)
        local current_epoch
        current_epoch=$(date +%s)
        local days_until_expiry=$(( (expiry_epoch - current_epoch) / 86400 ))
        
        if [ "$days_until_expiry" -gt 30 ]; then
            log_test "PASS" "SECURITY" "SSL certificate expires in $days_until_expiry days"
        elif [ "$days_until_expiry" -gt 7 ]; then
            log_test "WARN" "SECURITY" "SSL certificate expires in $days_until_expiry days"
        else
            log_test "CRITICAL" "SECURITY" "SSL certificate expires in $days_until_expiry days"
        fi
    else
        log_test "FAIL" "SECURITY" "SSL certificate validation failed"
    fi
    
    # Test rate limiting
    log_test "INFO" "SECURITY" "Testing rate limiting (this may take a moment)..."
    local rate_limit_triggered=false
    
    for i in {1..8}; do
        local response_code
        response_code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/auth/login" \
            -H "Content-Type: application/json" \
            -d '{"username":"test","password":"test"}' 2>/dev/null)
        
        if [ "$response_code" = "429" ]; then
            rate_limit_triggered=true
            break
        fi
        sleep 1
    done
    
    if [ "$rate_limit_triggered" = true ]; then
        log_test "PASS" "SECURITY" "Rate limiting is working"
    else
        log_test "WARN" "SECURITY" "Rate limiting not triggered (may need adjustment)"
    fi
}

# SMS functionality tests
test_sms_functionality() {
    echo -e "\n${PURPLE}📱 Testing SMS Gateway Functionality...${NC}"
    
    # Test gateway connection (mock test)
    local gateway_url
    gateway_url=$(echo "$GATEWAY_URL" | sed 's|/$||')
    
    if [ -n "$gateway_url" ]; then
        # Test if gateway URL is reachable
        if curl -s --max-time 10 "$gateway_url" > /dev/null 2>&1; then
            log_test "PASS" "SMS" "SMS Gateway is reachable"
        else
            log_test "WARN" "SMS" "SMS Gateway may not be reachable" "Check if the Android device is online"
        fi
    else
        log_test "WARN" "SMS" "Gateway URL not configured"
    fi
    
    # Test API endpoints that don't require authentication
    test_url "$BASE_URL/api/health" "200" "API health endpoint responds"
    
    # Test that protected endpoints require authentication
    local auth_test_response
    auth_test_response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/send" 2>/dev/null)
    
    if [ "$auth_test_response" = "401" ] || [ "$auth_test_response" = "403" ]; then
        log_test "PASS" "SMS" "Protected endpoints require authentication"
    else
        log_test "FAIL" "SMS" "Protected endpoints may not require authentication"
    fi
}

# Authentication and authorization tests
test_authentication() {
    echo -e "\n${PURPLE}🔐 Testing Authentication & Authorization...${NC}"
    
    # Test login page accessibility
    test_url "$BASE_URL/auth/login" "200" "Login page is accessible"
    
    # Test that dashboard requires authentication
    local dashboard_response
    dashboard_response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/" 2>/dev/null)
    
    if [ "$dashboard_response" = "302" ] || [ "$dashboard_response" = "401" ]; then
        log_test "PASS" "AUTH" "Dashboard requires authentication"
    else
        log_test "WARN" "AUTH" "Dashboard may not require authentication"
    fi
    
    # Test invalid login attempt
    local invalid_login_response
    invalid_login_response=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE_URL/auth/login" \
        -H "Content-Type: application/json" \
        -d '{"username":"invalid","password":"invalid"}' 2>/dev/null)
    
    if [ "$invalid_login_response" = "401" ] || [ "$invalid_login_response" = "200" ]; then
        log_test "PASS" "AUTH" "Invalid login attempts are handled properly"
    else
        log_test "WARN" "AUTH" "Invalid login response unexpected: $invalid_login_response"
    fi
}

# Performance monitoring
monitor_performance() {
    echo -e "\n${PURPLE}⚡ Monitoring System Performance...${NC}"
    
    # Test response times
    local response_time
    response_time=$(curl -s -o /dev/null -w "%{time_total}" "$BASE_URL" 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        if (( $(echo "$response_time < $MAX_RESPONSE_TIME" | bc -l) )); then
            log_test "PASS" "PERF" "Response time acceptable (${response_time}s)"
        else
            log_test "WARN" "PERF" "Response time high (${response_time}s)"
        fi
    else
        log_test "FAIL" "PERF" "Could not measure response time"
    fi
    
    # Check system resources
    if command -v docker &> /dev/null; then
        # CPU usage
        local cpu_usage
        cpu_usage=$(docker stats --no-stream --format "table {{.CPUPerc}}" 2>/dev/null | tail -n +2 | head -1 | sed 's/%//' | cut -d. -f1)
        
        if [ -n "$cpu_usage" ] && [ "$cpu_usage" -lt "$MAX_CPU_USAGE" ]; then
            log_test "PASS" "PERF" "CPU usage acceptable (${cpu_usage}%)"
        elif [ -n "$cpu_usage" ]; then
            log_test "WARN" "PERF" "CPU usage high (${cpu_usage}%)"
        else
            log_test "WARN" "PERF" "Could not measure CPU usage"
        fi
        
        # Memory usage
        local memory_usage
        memory_usage=$(docker stats --no-stream --format "table {{.MemPerc}}" 2>/dev/null | tail -n +2 | head -1 | sed 's/%//' | cut -d. -f1)
        
        if [ -n "$memory_usage" ] && [ "$memory_usage" -lt "$MAX_MEMORY_USAGE" ]; then
            log_test "PASS" "PERF" "Memory usage acceptable (${memory_usage}%)"
        elif [ -n "$memory_usage" ]; then
            log_test "WARN" "PERF" "Memory usage high (${memory_usage}%)"
        else
            log_test "WARN" "PERF" "Could not measure memory usage"
        fi
    fi
    
    # Disk usage
    local disk_usage
    disk_usage=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ "$disk_usage" -lt "$MAX_DISK_USAGE" ]; then
        log_test "PASS" "PERF" "Disk usage acceptable (${disk_usage}%)"
    else
        log_test "WARN" "PERF" "Disk usage high (${disk_usage}%)"
    fi
    
    # Test compression
    if curl -s -H "Accept-Encoding: gzip" -I "$BASE_URL" | grep -qi "content-encoding: gzip"; then
        log_test "PASS" "PERF" "Gzip compression enabled"
    else
        log_test "WARN" "PERF" "Gzip compression not detected"
    fi
}

# Logging configuration validation
validate_logging() {
    echo -e "\n${PURPLE}📝 Validating Logging Configuration...${NC}"
    
    # Check if log files exist and are being written
    local log_dirs=("logs" "logs/nginx")
    
    for log_dir in "${log_dirs[@]}"; do
        if [ -d "$log_dir" ]; then
            log_test "PASS" "LOGGING" "Log directory $log_dir exists"
            
            # Check if logs are being written
            if find "$log_dir" -name "*.log" -mtime -1 2>/dev/null | grep -q .; then
                log_test "PASS" "LOGGING" "Recent logs found in $log_dir"
            else
                log_test "WARN" "LOGGING" "No recent logs in $log_dir"
            fi
        else
            log_test "WARN" "LOGGING" "Log directory $log_dir not found"
        fi
    done
    
    # Check application logs
    if docker-compose -f "$COMPOSE_FILE" logs --tail=10 web 2>/dev/null | grep -q .; then
        log_test "PASS" "LOGGING" "Application logs are being generated"
    else
        log_test "WARN" "LOGGING" "No application logs detected"
    fi
}

# Backup validation
validate_backups() {
    echo -e "\n${PURPLE}💾 Validating Backup Configuration...${NC}"
    
    # Check if backup script exists
    if [ -f "scripts/backup.sh" ]; then
        log_test "PASS" "BACKUP" "Backup script exists"
        
        # Check if script is executable
        if [ -x "scripts/backup.sh" ]; then
            log_test "PASS" "BACKUP" "Backup script is executable"
        else
            log_test "WARN" "BACKUP" "Backup script is not executable"
        fi
    else
        log_test "WARN" "BACKUP" "Backup script not found"
    fi
    
    # Check for existing backups
    if [ -d "backups" ]; then
        log_test "PASS" "BACKUP" "Backup directory exists"
        
        if find backups/ -name "*.sql.gz" -mtime -7 2>/dev/null | grep -q .; then
            log_test "PASS" "BACKUP" "Recent backups found"
        else
            log_test "WARN" "BACKUP" "No recent backups found"
        fi
    else
        log_test "WARN" "BACKUP" "Backup directory not found"
    fi
}

# Generate HTML report
generate_html_report() {
    cat > "$REPORT_FILE" << EOF
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMS Gateway Deployment Validation Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .summary { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .metric { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }
        .metric h3 { margin: 0 0 10px 0; }
        .metric .value { font-size: 2em; font-weight: bold; }
        .pass { color: #28a745; }
        .fail { color: #dc3545; }
        .warn { color: #ffc107; }
        .critical { color: #dc3545; font-weight: bold; }
        .log-entry { padding: 8px; margin: 2px 0; border-radius: 4px; font-family: monospace; }
        .log-pass { background-color: #d4edda; }
        .log-fail { background-color: #f8d7da; }
        .log-warn { background-color: #fff3cd; }
        .log-critical { background-color: #f5c6cb; }
        .status-badge { padding: 10px 20px; border-radius: 20px; font-weight: bold; text-align: center; margin: 20px 0; }
        .status-approved { background-color: #d4edda; color: #155724; }
        .status-rejected { background-color: #f8d7da; color: #721c24; }
        .status-conditional { background-color: #fff3cd; color: #856404; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>SMS Gateway Deployment Validation Report</h1>
            <p>Generated on: $(date)</p>
            <p>Base URL: $BASE_URL</p>
        </div>
        
        <div class="summary">
            <div class="metric">
                <h3>Total Tests</h3>
                <div class="value">$TOTAL_TESTS</div>
            </div>
            <div class="metric">
                <h3>Passed</h3>
                <div class="value pass">$PASSED_TESTS</div>
            </div>
            <div class="metric">
                <h3>Failed</h3>
                <div class="value fail">$FAILED_TESTS</div>
            </div>
            <div class="metric">
                <h3>Warnings</h3>
                <div class="value warn">$WARNING_TESTS</div>
            </div>
            <div class="metric">
                <h3>Critical</h3>
                <div class="value critical">$CRITICAL_FAILURES</div>
            </div>
        </div>
EOF

    # Determine overall status
    if [ $CRITICAL_FAILURES -gt 0 ]; then
        echo '<div class="status-badge status-rejected">❌ DEPLOYMENT REJECTED - Critical failures detected</div>' >> "$REPORT_FILE"
    elif [ $FAILED_TESTS -gt 0 ]; then
        echo '<div class="status-badge status-rejected">❌ DEPLOYMENT REJECTED - Test failures detected</div>' >> "$REPORT_FILE"
    elif [ $WARNING_TESTS -gt 0 ]; then
        echo '<div class="status-badge status-conditional">⚠️ DEPLOYMENT APPROVED WITH CONDITIONS - Warnings present</div>' >> "$REPORT_FILE"
    else
        echo '<div class="status-badge status-approved">✅ DEPLOYMENT APPROVED - All tests passed</div>' >> "$REPORT_FILE"
    fi

    cat >> "$REPORT_FILE" << EOF
        
        <h2>Detailed Test Results</h2>
        <div class="test-results">
EOF

    # Add log entries to HTML report
    while IFS= read -r line; do
        if [[ $line == *"PASS"* ]]; then
            echo "<div class=\"log-entry log-pass\">$line</div>" >> "$REPORT_FILE"
        elif [[ $line == *"FAIL"* ]]; then
            echo "<div class=\"log-entry log-fail\">$line</div>" >> "$REPORT_FILE"
        elif [[ $line == *"CRITICAL"* ]]; then
            echo "<div class=\"log-entry log-critical\">$line</div>" >> "$REPORT_FILE"
        elif [[ $line == *"WARN"* ]]; then
            echo "<div class=\"log-entry log-warn\">$line</div>" >> "$REPORT_FILE"
        fi
    done < "$LOG_FILE"

    cat >> "$REPORT_FILE" << EOF
        </div>
    </div>
</body>
</html>
EOF
}

# Main execution
main() {
    echo -e "${CYAN}🚀 Starting SMS Gateway Deployment Validation${NC}"
    echo -e "${CYAN}Version: $VERSION${NC}"
    echo -e "${CYAN}Timestamp: $(date)${NC}\n"
    
    init_logging
    
    # Run all validation tests
    check_prerequisites
    validate_environment
    test_infrastructure
    test_connectivity
    validate_security
    test_sms_functionality
    test_authentication
    monitor_performance
    validate_logging
    validate_backups
    
    # Generate reports
    echo -e "\n${PURPLE}📊 Generating Reports...${NC}"
    generate_html_report
    
    # Final summary
    echo -e "\n${CYAN}========================================${NC}"
    echo -e "${CYAN}VALIDATION SUMMARY${NC}"
    echo -e "${CYAN}========================================${NC}"
    echo -e "Total Tests: ${BLUE}$TOTAL_TESTS${NC}"
    echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
    echo -e "Failed: ${RED}$FAILED_TESTS${NC}"
    echo -e "Warnings: ${YELLOW}$WARNING_TESTS${NC}"
    echo -e "Critical Failures: ${RED}$CRITICAL_FAILURES${NC}"
    
    echo -e "\nReports generated:"
    echo -e "  📄 Log file: $LOG_FILE"
    echo -e "  🌐 HTML report: $REPORT_FILE"
    
    # Determine exit code
    if [ $CRITICAL_FAILURES -gt 0 ]; then
        echo -e "\n🚫 ${RED}DEPLOYMENT REJECTED${NC} - Critical failures detected"
        exit 2
    elif [ $FAILED_TESTS -gt 0 ]; then
        echo -e "\n🚫 ${RED}DEPLOYMENT REJECTED${NC} - Test failures detected"
        exit 1
    elif [ $WARNING_TESTS -gt 0 ]; then
        echo -e "\n⚠️  ${YELLOW}DEPLOYMENT APPROVED WITH CONDITIONS${NC} - Warnings present"
        exit 0
    else
        echo -e "\n🎉 ${GREEN}DEPLOYMENT APPROVED${NC} - All tests passed!"
        exit 0
    fi
}

# Handle script interruption
trap 'echo -e "\n${RED}Validation interrupted${NC}"; exit 130' INT TERM

# Execute main function
main "$@"