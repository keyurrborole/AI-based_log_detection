# ⚡ Quick Command Cheatsheet

## Copy-Paste These Commands in Order

---

## 🔧 Initial Setup (Run Once)

```powershell
# 1. Create directory structure
mkdir backend, backend/api, backend/parsers, backend/ingestion, backend/ml_engine, backend/correlation, backend/storage, backend/utils, tests, scripts, sample_logs, ml_models, docs

# 2. Create __init__.py files
New-Item backend/__init__.py
New-Item backend/api/__init__.py
New-Item backend/parsers/__init__.py
New-Item backend/ingestion/__init__.py
New-Item backend/ml_engine/__init__.py
New-Item backend/correlation/__init__.py
New-Item backend/storage/__init__.py
New-Item backend/utils/__init__.py
New-Item tests/__init__.py

# 3. Create files
New-Item requirements.txt
New-Item .env
New-Item docker-compose.yml

# 4. Create virtual environment
python -m venv venv

# 5. Activate venv
.\venv\Scripts\activate

# 6. Install dependencies
pip install -r requirements.txt

# 7. Start Docker services
docker-compose up -d
```

---

## 🚀 Daily Startup

```powershell
# 1. Start Docker (if not running)
docker-compose up -d

# 2. Activate Python venv
.\venv\Scripts\activate

# 3. Start API (Terminal 1)
cd backend
python -m uvicorn api.main:app --reload

# 4. Run ingestion (Terminal 2 - after API is up)
cd ..
python scripts/ingest_sample_logs.py
```

---

## 🧪 Testing Commands

```powershell
# Test parser
python tests/test_parser.py

# Test Kafka
python scripts/test_kafka.py

# Test Elasticsearch
python scripts/test_elasticsearch.py

# Test API
curl http://localhost:8000/
curl http://localhost:8000/api/stats
```

---

## 📊 Monitoring Commands

```powershell
# Check Docker services
docker-compose ps

# Check logs
docker logs kafka
docker logs elasticsearch

# Check Elasticsearch health
curl http://localhost:9200

# View API docs
start http://localhost:8000/docs
```

---

## 🛑 Shutdown Commands

```powershell
# Stop API (Ctrl+C in API terminal)

# Stop Docker services
docker-compose down

# Deactivate venv
deactivate
```

---

## 🔄 Restart Commands

```powershell
# Restart Docker services
docker-compose restart

# Restart specific service
docker restart elasticsearch
docker restart kafka
```

---

## 🐛 Troubleshooting Commands

```powershell
# Clean restart Docker
docker-compose down
docker-compose up -d

# View container logs
docker logs elasticsearch --tail 50
docker logs kafka --tail 50

# Check if ports are in use
netstat -ano | findstr :9200
netstat -ano | findstr :9092
netstat -ano | findstr :8000

# Reinstall Python packages
pip install -r requirements.txt --force-reinstall
```

---

## 📦 API Endpoints (curl)

```powershell
# Health check
curl http://localhost:8000/

# Ingest log
curl -X POST http://localhost:8000/api/logs/ingest -H "Content-Type: application/json" -d '{\"raw_log\": \"Jan 10 10:21:44 server1 sshd[12345]: Failed password for root\"}'

# Get failed logins
curl http://localhost:8000/api/logs/failed-logins

# Get recent logs
curl http://localhost:8000/api/logs/recent?hours=24

# Get statistics
curl http://localhost:8000/api/stats
```

---

## 🎯 Complete Workflow (Copy All)

```powershell
# Full startup sequence
docker-compose up -d
timeout 10
.\venv\Scripts\activate
cd backend
start python -m uvicorn api.main:app --reload
timeout 5
cd ..
python scripts/ingest_sample_logs.py
start http://localhost:8000/docs
```

---

## 📝 File Creation Order

```powershell
# 1. Config files
# Edit: .gitignore, requirements.txt, .env, docker-compose.yml

# 2. Utility modules
# Create: backend/utils/config.py, backend/utils/logger.py

# 3. Core modules
# Create: backend/parsers/log_parser.py

# 4. Integration modules
# Create: backend/ingestion/kafka_producer.py
# Create: backend/ingestion/kafka_consumer.py
# Create: backend/storage/es_client.py

# 5. API
# Create: backend/api/main.py

# 6. Scripts
# Create: scripts/test_kafka.py
# Create: scripts/test_elasticsearch.py
# Create: scripts/ingest_sample_logs.py

# 7. Tests
# Create: tests/test_parser.py

# 8. Sample data
# Create: sample_logs/auth_logs.txt
```

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Setup directories & files | 10 min |
| Create config files | 15 min |
| Write utility code | 20 min |
| Write parser | 30 min |
| Kafka integration | 30 min |
| Elasticsearch | 25 min |
| API | 30 min |
| Testing | 20 min |
| **Total** | **~3 hours** |

---

## 🎓 Learning Checkpoints

After each step, verify:

### Step 1-3: Setup ✅
- [ ] Directories created
- [ ] Dependencies installed
- [ ] Docker running

### Step 4: Parser ✅
- [ ] Parser test passes
- [ ] Logs normalized correctly

### Step 6: Kafka ✅
- [ ] Can send to Kafka
- [ ] Can receive from Kafka

### Step 7: Elasticsearch ✅
- [ ] Can store logs
- [ ] Can search logs

### Step 8: API ✅
- [ ] API responds
- [ ] All endpoints work
- [ ] Swagger UI accessible

### Step 9-10: Integration ✅
- [ ] Complete flow works
- [ ] Logs visible in API
- [ ] Stats accurate

---

## 🆘 Emergency Commands

```powershell
# Kill all Python processes
taskkill /F /IM python.exe

# Kill process on port 8000
netstat -ano | findstr :8000
# Note the PID, then:
taskkill /F /PID <PID>

# Remove all Docker containers and volumes
docker-compose down -v

# Clean Python cache
Get-ChildItem -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
```

---

## 📋 Status Check Command

```powershell
# Run this to check everything
echo "=== Docker Services ==="
docker-compose ps
echo "`n=== Python Environment ==="
python --version
pip list | Select-String "fastapi|kafka|elastic"
echo "`n=== Ports ==="
netstat -ano | findstr ":8000 :9092 :9200"
echo "`n=== API Status ==="
curl http://localhost:8000/
```

---

**Save this file for quick reference!** 📌
