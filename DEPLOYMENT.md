# 🚀 Genes Deployment Guide

## Prerequisites

- VPS with Docker and Docker Compose installed
- SSH access to VPS
- GitHub repository access
- Port 8000 available (or configure different port)

## VPS Setup

### 1. Clone Repository

```bash
cd /opt
git clone https://github.com/AFSCapital-git/genes.git
cd genes
```

### 2. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit with secure values
nano .env
```

**Important:** Change these values in `.env`:
- `POSTGRES_PASSWORD` - Strong database password
- `SECRET_KEY` - Generate with: `openssl rand -hex 32`

### 3. Deploy with Docker Compose

```bash
# Build and start services
docker-compose up -d

# Check logs
docker-compose logs -f agente_constructor

# Verify all services are running
docker-compose ps
```

### 4. Verify Deployment

```bash
# Test API health
curl http://localhost:8000/health

# Check database connection
docker exec genes_postgres psql -U genes -c "\l"

# Check Redis
docker exec genes_redis redis-cli ping
```

## Service Management

### Start/Stop Services

```bash
# Start all services
docker-compose start

# Stop all services
docker-compose stop

# Restart Agente_Constructor
docker-compose restart agente_constructor
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f agente_constructor

# Last 100 lines
docker-compose logs --tail=100
```

### Update Code

```bash
cd /opt/genes
git pull origin main
docker-compose build agente_constructor
docker-compose up -d agente_constructor
```

## CI/CD with GitHub Actions

GitHub Actions workflow will be configured for:
- ✅ Automated testing on pull requests
- ✅ Automated deployment on push to `main`
- ✅ Security scanning
- ✅ Docker image building

## Monitoring

### Health Checks

All services have health checks:
- Agente_Constructor: `http://localhost:8000/health`
- PostgreSQL: `docker exec genes_postgres pg_isready`
- Redis: `docker exec genes_redis redis-cli ping`

### Logs Location

- Application logs: `/opt/genes/logs/`
- Docker logs: `docker-compose logs`

## Security Checklist

- [ ] Strong passwords in `.env`
- [ ] Firewall configured (allow only port 8000 from trusted IPs)
- [ ] SSL/TLS configured (use nginx reverse proxy)
- [ ] Regular backups of PostgreSQL data
- [ ] Docker socket access restricted
- [ ] Regular security updates

## Backup & Recovery

### Database Backup

```bash
# Backup
docker exec genes_postgres pg_dump -U genes genes > backup.sql

# Restore
docker exec -i genes_postgres psql -U genes genes < backup.sql
```

### Volume Backup

```bash
# Backup volumes
docker run --rm -v genes_postgres_data:/data -v $(pwd):/backup \
  alpine tar czf /backup/postgres-backup.tar.gz /data
```

## Troubleshooting

### Agente_Constructor won't start

1. Check logs: `docker-compose logs agente_constructor`
2. Verify database is healthy: `docker-compose ps postgres`
3. Check environment variables: `docker-compose config`

### Can't connect to Docker socket

Ensure user has Docker permissions:
```bash
usermod -aG docker $USER
```

### Port already in use

Change port in `docker-compose.yml`:
```yaml
ports:
  - "9000:8000"  # Use port 9000 instead
```

## Next Steps

After deployment:
1. Test API endpoints
2. Create first agent via API
3. Configure monitoring/alerts
4. Set up automated backups
5. Configure SSL certificate

---

Built with 🧬 by AFS Capital
