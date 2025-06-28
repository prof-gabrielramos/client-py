#!/bin/bash
# Production deployment script

set -e

echo "Starting deployment..."

# Pull latest changes
git pull origin main

# Build and deploy with Docker Compose
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# Run database migrations
docker-compose -f docker-compose.prod.yml exec web flask db upgrade

# Health check
echo "Performing health check..."
if curl -f http://localhost/health; then
    echo "Deployment successful!"
else
    echo "Health check failed!"
    exit 1
fi

# Cleanup old images
docker image prune -f

echo "Deployment completed successfully!"