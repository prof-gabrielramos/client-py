#!/bin/bash
# System monitoring script

# Check service status
echo "=== Service Status ==="
docker-compose -f docker-compose.prod.yml ps

# Check resource usage
echo -e "\n=== Resource Usage ==="
docker stats --no-stream

# Check logs for errors
echo -e "\n=== Recent Errors ==="
docker-compose -f docker-compose.prod.yml logs --tail=50 | grep -i error

# Check disk space
echo -e "\n=== Disk Usage ==="
df -h

# Check database connections
echo -e "\n=== Database Status ==="
docker-compose -f docker-compose.prod.yml exec db psql -U user -d sms_gateway -c "SELECT count(*) as active_connections FROM pg_stat_activity;"

# Application health check
echo -e "\n=== Application Health ==="
curl -s http://localhost/api/health | jq .