#!/bin/bash
# Genes Platform Deployment Script
# Run this script on the VPS as root

set -e  # Exit on error

echo "🧬 Starting Genes Platform Deployment..."

# 1. Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "📦 Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    echo "✅ Docker installed"
else
    echo "✅ Docker already installed"
fi

# 2. Check if Docker Compose is installed
if ! docker compose version &> /dev/null; then
    echo "📦 Installing Docker Compose plugin..."
    apt-get update
    apt-get install -y docker-compose-plugin
    echo "✅ Docker Compose installed"
else
    echo "✅ Docker Compose already installed"
fi

# 3. Navigate to /opt
cd /opt

# 4. Clone repository if not exists
if [ ! -d "genes" ]; then
    echo "📥 Cloning Genes repository..."
    git clone https://github.com/AFSCapital-git/genes.git
    echo "✅ Repository cloned"
else
    echo "📥 Updating Genes repository..."
    cd genes
    git pull origin main
    cd ..
    echo "✅ Repository updated"
fi

# 5. Enter genes directory
cd genes

# 6. Create .env file if not exists
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    
    # Generate secure secret key
    SECRET_KEY=$(openssl rand -hex 32)
    POSTGRES_PASSWORD=$(openssl rand -base64 24)
    
    # Update .env with generated secrets
    sed -i "s/genes_secure_password_change_this/$POSTGRES_PASSWORD/" .env
    sed -i "s/generate_a_secure_random_key_here/$SECRET_KEY/" .env
    
    echo "✅ Environment configured with secure secrets"
    echo "📝 Secrets saved to /opt/genes/.env"
else
    echo "✅ .env already exists"
fi

# 7. Create necessary directories
mkdir -p logs agents/generated

# 8. Pull base images
echo "🐳 Pulling Docker images..."
docker pull postgres:15
docker pull redis:7-alpine
docker pull python:3.11-slim
echo "✅ Images pulled"

# 9. Build and start services
echo "🚀 Building and starting Genes platform..."
docker compose up -d --build

# 10. Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 15

# 11. Check service status
echo "📊 Service Status:"
docker compose ps

# 12. Health check
echo ""
echo "🏥 Running health checks..."

# Check PostgreSQL
if docker exec genes_postgres pg_isready -U genes &> /dev/null; then
    echo "✅ PostgreSQL is healthy"
else
    echo "❌ PostgreSQL is not responding"
fi

# Check Redis
if docker exec genes_redis redis-cli ping &> /dev/null; then
    echo "✅ Redis is healthy"
else
    echo "❌ Redis is not responding"
fi

# Check Agente_Constructor API
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ Agente_Constructor API is healthy"
    echo ""
    echo "🎉 DEPLOYMENT SUCCESSFUL!"
    echo ""
    echo "🔗 API URL: http://187.127.24.128:8000"
    echo "📚 API Docs: http://187.127.24.128:8000/docs"
    echo ""
    echo "📋 Next steps:"
    echo "  - Test API: curl http://localhost:8000/health"
    echo "  - View logs: docker compose logs -f"
    echo "  - Check status: docker compose ps"
else
    echo "⚠️ Agente_Constructor API is not responding yet"
    echo "Check logs with: docker compose logs agente_constructor"
fi

echo ""
echo "🧬 Genes Platform deployed to /opt/genes"
echo "Built with 🦞 by AFS Capital"
