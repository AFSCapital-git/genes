# 🚀 Deploy Genes Agora - Instruções Rápidas

## Opção 1: Script Automatizado (RECOMENDADO)

**Execute estes comandos no VPS:**

```bash
# 1. SSH no VPS
ssh root@187.127.24.128

# 2. Baixar e executar script de deployment
curl -fsSL https://raw.githubusercontent.com/AFSCapital-git/genes/main/deploy.sh -o deploy.sh
chmod +x deploy.sh
./deploy.sh
```

**Pronto!** O script faz tudo automaticamente:
- ✅ Instala Docker e Docker Compose (se necessário)
- ✅ Clona o repositório
- ✅ Configura .env com secrets seguros
- ✅ Faz build e deploy de todos os serviços
- ✅ Verifica saúde de todos os componentes

---

## Opção 2: Passo a Passo Manual

Se preferir ter controle total:

### 1. Conectar no VPS
```bash
ssh root@187.127.24.128
```

### 2. Instalar Docker (se não tiver)
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
apt-get install -y docker-compose-plugin
```

### 3. Clone do repositório
```bash
cd /opt
git clone https://github.com/AFSCapital-git/genes.git
cd genes
```

### 4. Configurar ambiente
```bash
cp .env.example .env

# Gerar secrets seguros
SECRET_KEY=$(openssl rand -hex 32)
POSTGRES_PASSWORD=$(openssl rand -base64 24)

# Editar .env com os valores gerados
nano .env
```

### 5. Deploy
```bash
docker compose up -d --build
```

### 6. Verificar
```bash
# Status dos serviços
docker compose ps

# Health check
curl http://localhost:8000/health

# Logs (se necessário)
docker compose logs -f agente_constructor
```

---

## ✅ Verificação de Sucesso

Quando tudo estiver funcionando, você verá:

```
$ curl http://localhost:8000/health
{
  "status": "healthy",
  "timestamp": "2026-05-25T16:47:00Z"
}

$ docker compose ps
NAME                    STATUS              PORTS
genes_agente_constructor   Up (healthy)      0.0.0.0:8000->8000/tcp
genes_postgres             Up (healthy)      0.0.0.0:5432->5432/tcp
genes_redis                Up (healthy)      0.0.0.0:6379->6379/tcp
```

---

## 🔍 Acessar a API

**URL da API:** http://187.127.24.128:8000

**Documentação interativa:** http://187.127.24.128:8000/docs

**Endpoints principais:**
- `GET /` - Info da plataforma
- `GET /health` - Health check
- `GET /api/v1/agents/` - Listar agentes (em desenvolvimento)
- `POST /api/v1/agents/create` - Criar agente (em desenvolvimento)

---

## 🆘 Troubleshooting

### Serviço não inicia
```bash
# Ver logs
docker compose logs agente_constructor

# Verificar se portas estão livres
netstat -tulpn | grep -E '8000|5432|6379'

# Reiniciar serviços
docker compose restart
```

### Erro de permissão do Docker
```bash
# Dar permissão ao usuário
usermod -aG docker $USER

# Ou executar como root
```

### Banco de dados não conecta
```bash
# Verificar PostgreSQL
docker exec genes_postgres pg_isready -U genes

# Ver logs
docker compose logs postgres
```

---

## 🎯 Depois do Deploy

1. **Testar API:**
   ```bash
   curl http://187.127.24.128:8000/
   ```

2. **Ver documentação interativa:**
   - Abrir no navegador: http://187.127.24.128:8000/docs

3. **Próximo passo:**
   - Implementar endpoint de criação de agentes
   - Criar o primeiro agente via API

---

## 📞 Suporte

Qualquer problema:
1. Verificar logs: `docker compose logs -f`
2. Status: `docker compose ps`
3. Reiniciar: `docker compose restart`

---

**Pronto para construir o futuro!** 🧬🦞

Built by AFS Capital
