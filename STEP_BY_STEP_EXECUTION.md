# ⚡ Step-by-Step Execution Guide
## From .gitignore to Running Code - Copy & Paste Edition

**Time to complete:** 4-6 hours for full basic system  
**Current status:** .gitignore created ✅

---

## 📍 STEP 1: Complete Project Setup (30 minutes)

### 1.1: Populate .gitignore

Open `.gitignore` and add:

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/
.venv

# IDEs
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# Project specific
ml_models/*.pkl
logs/*.log
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# Frontend
frontend/dashboard/node_modules/
frontend/dashboard/build/

# Docker
docker-compose.override.yml

# Data
*.csv
*.log
!sample_logs/*.csv
!sample_logs/*.log
```

### 1.2: Create Directory Structure

Run these commands in PowerShell:

```powershell
# Create all directories at once
mkdir backend, backend/api, backend/parsers, backend/ingestion, backend/ml_engine, backend/correlation, backend/storage, backend/utils, tests, scripts, sample_logs, ml_models, docs

# Create __init__.py files
New-Item backend/__init__.py
New-Item backend/api/__init__.py
New-Item backend/parsers/__init__.py
New-Item backend/ingestion/__init__.py
New-Item backend/ml_engine/__init__.py
New-Item backend/correlation/__init__.py
New-Item backend/storage/__init__.py
New-Item backend/utils/__init__.py
New-Item tests/__init__.py
```

### 1.3: Create requirements.txt

```powershell
New-Item requirements.txt
```

Add this content:

```txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
confluent-kafka==2.3.0
elasticsearch==8.11.1
scikit-learn==1.4.0
pandas==2.2.0
numpy==1.26.3
pydantic==2.5.3
python-multipart==0.0.6
python-dotenv==1.0.0
aiofiles==23.2.1
pytest==7.4.4
httpx==0.26.0
joblib==1.3.2
```

### 1.4: Create Virtual Environment

```powershell
# Create venv
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

**✅ Checkpoint:** You should see all packages installing successfully.

---

## 📍 STEP 2: Create Configuration Files (15 minutes)

### 2.1: Create .env file

```powershell
New-Item .env
```

Add:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_AUTH_LOGS_TOPIC=auth_logs

# Elasticsearch Configuration
ES_HOST=localhost
ES_PORT=9200
ES_INDEX_NAME=security-logs

# ML Configuration
ML_MODEL_PATH=./ml_models/isolation_forest.pkl
ML_CONTAMINATION=0.1

# Logging
LOG_LEVEL=INFO
```

### 2.2: Create docker-compose.yml

```powershell
New-Item docker-compose.yml
```

Add:

```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    container_name: zookeeper
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.5.0
    container_name: kafka
    depends_on:
      - zookeeper
    ports:
      - "9092:9092"
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
      KAFKA_AUTO_CREATE_TOPICS_ENABLE: "true"

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.1
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data

volumes:
  es_data:
    driver: local
```

### 2.3: Start Docker Services

```powershell
# Start all services
docker-compose up -d

# Verify they're running
docker-compose ps

# Check Elasticsearch
curl http://localhost:9200
```

**✅ Checkpoint:** You should see Elasticsearch returning JSON with cluster info.

---

## 📍 STEP 3: Write Core Utility Code (20 minutes)

### 3.1: Create backend/utils/config.py

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application configuration"""
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_auth_logs_topic: str = "auth_logs"
    
    # Elasticsearch
    es_host: str = "localhost"
    es_port: int = 9200
    es_index_name: str = "security-logs"
    
    # ML
    ml_model_path: str = "./ml_models/isolation_forest.pkl"
    ml_contamination: float = 0.1
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 3.2: Create backend/utils/logger.py

```python
import logging
import sys

def setup_logger(name: str, level: str = "INFO"):
    """Setup application logger"""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

logger = setup_logger("ai_log_framework")
```

---

## 📍 STEP 4: Build Log Parser (30 minutes)

### 4.1: Create backend/parsers/log_parser.py

```python
import re
from datetime import datetime
from typing import Dict, Optional
from backend.utils.logger import logger

class LogParser:
    """Parse various log formats into normalized structure"""
    
    def __init__(self):
        # Syslog pattern: Jan 10 10:21:44 server1 sshd[12345]: message
        self.syslog_pattern = re.compile(
            r'(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+)\s+'
            r'(?P<host>\S+)\s+'
            r'(?P<service>\w+)\[(?P<pid>\d+)\]:\s+'
            r'(?P<message>.*)'
        )
    
    def parse_syslog(self, raw_log: str) -> Optional[Dict]:
        """Parse syslog format"""
        match = self.syslog_pattern.match(raw_log)
        if not match:
            logger.warning(f"Failed to parse log: {raw_log}")
            return None
        
        data = match.groupdict()
        
        # Build normalized log
        normalized = {
            "timestamp": self._normalize_timestamp(data['timestamp']),
            "host": data['host'],
            "service": data['service'],
            "event_type": self._classify_event(data['message']),
            "severity": self._calculate_severity(data['message']),
            "raw_log": raw_log
        }
        
        # Extract user if present
        user = self._extract_user(data['message'])
        if user:
            normalized['user'] = user
        
        # Extract IP if present
        ip = self._extract_ip(data['message'])
        if ip:
            normalized['source_ip'] = ip
        
        return normalized
    
    def _normalize_timestamp(self, ts: str) -> str:
        """Convert timestamp to ISO format"""
        try:
            dt = datetime.strptime(f"2026 {ts}", "%Y %b %d %H:%M:%S")
            return dt.isoformat() + "Z"
        except:
            return datetime.utcnow().isoformat() + "Z"
    
    def _classify_event(self, message: str) -> str:
        """Classify event type"""
        message_lower = message.lower()
        
        if "failed password" in message_lower or "authentication failure" in message_lower:
            return "LOGIN_FAILURE"
        elif "accepted password" in message_lower or "session opened" in message_lower:
            return "LOGIN_SUCCESS"
        elif "sudo" in message_lower or "su:" in message_lower:
            return "PRIVILEGE_ESCALATION"
        elif "connection closed" in message_lower:
            return "LOGOUT"
        else:
            return "UNKNOWN"
    
    def _calculate_severity(self, message: str) -> int:
        """Assign severity (1-10)"""
        message_lower = message.lower()
        
        if "failed" in message_lower or "error" in message_lower:
            return 7
        elif "sudo" in message_lower:
            return 8
        elif "accepted" in message_lower:
            return 3
        else:
            return 5
    
    def _extract_user(self, message: str) -> Optional[str]:
        """Extract username"""
        patterns = [
            r'for (\w+)',
            r'user=(\w+)',
            r'USER=(\w+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                return match.group(1)
        return None
    
    def _extract_ip(self, message: str) -> Optional[str]:
        """Extract IP address"""
        pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        match = re.search(pattern, message)
        return match.group(0) if match else None
```

### 4.2: Test the Parser

Create `tests/test_parser.py`:

```python
import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser

def test_parser():
    parser = LogParser()
    
    # Test case 1: Failed login
    log1 = "Jan 10 10:21:44 server1 sshd[12345]: Failed password for root from 192.168.1.10 port 45678 ssh2"
    result1 = parser.parse_syslog(log1)
    
    print("Test 1: Failed Login")
    print(f"  Event Type: {result1['event_type']}")
    print(f"  User: {result1.get('user', 'N/A')}")
    print(f"  IP: {result1.get('source_ip', 'N/A')}")
    print(f"  Severity: {result1['severity']}")
    
    assert result1['event_type'] == 'LOGIN_FAILURE'
    assert result1['user'] == 'root'
    assert result1['source_ip'] == '192.168.1.10'
    print("  ✅ PASSED\n")
    
    # Test case 2: Successful login
    log2 = "Jan 10 10:25:00 server1 sshd[12350]: Accepted password for admin from 192.168.1.5 port 45679 ssh2"
    result2 = parser.parse_syslog(log2)
    
    print("Test 2: Successful Login")
    print(f"  Event Type: {result2['event_type']}")
    print(f"  User: {result2.get('user', 'N/A')}")
    print(f"  Severity: {result2['severity']}")
    
    assert result2['event_type'] == 'LOGIN_SUCCESS'
    print("  ✅ PASSED\n")
    
    print("🎉 All tests passed!")

if __name__ == '__main__':
    test_parser()
```

Run the test:

```powershell
python tests/test_parser.py
```

**✅ Checkpoint:** You should see "All tests passed!"

---

## 📍 STEP 5: Create Sample Logs (10 minutes)

### 5.1: Create sample_logs/auth_logs.txt

```text
Jan 10 10:21:44 server1 sshd[12345]: Failed password for root from 192.168.1.10 port 45678 ssh2
Jan 10 10:21:50 server1 sshd[12346]: Failed password for root from 192.168.1.10 port 45679 ssh2
Jan 10 10:21:56 server1 sshd[12347]: Failed password for root from 192.168.1.10 port 45680 ssh2
Jan 10 10:22:02 server1 sshd[12348]: Failed password for root from 192.168.1.10 port 45681 ssh2
Jan 10 10:22:08 server1 sshd[12349]: Failed password for root from 192.168.1.10 port 45682 ssh2
Jan 10 10:22:14 server1 sshd[12350]: Failed password for root from 192.168.1.10 port 45683 ssh2
Jan 10 10:22:20 server1 sshd[12351]: Failed password for root from 192.168.1.10 port 45684 ssh2
Jan 10 10:22:26 server1 sshd[12352]: Failed password for root from 192.168.1.10 port 45685 ssh2
Jan 10 10:22:32 server1 sshd[12353]: Failed password for root from 192.168.1.10 port 45686 ssh2
Jan 10 10:22:38 server1 sshd[12354]: Failed password for root from 192.168.1.10 port 45687 ssh2
Jan 10 10:22:44 server1 sshd[12355]: Accepted password for root from 192.168.1.10 port 45688 ssh2
Jan 10 10:22:50 server1 sudo[12356]: root : TTY=pts/0 ; PWD=/root ; USER=admin ; COMMAND=/bin/bash
Jan 10 14:15:22 server1 sshd[13001]: Accepted password for alice from 192.168.1.20 port 50001 ssh2
Jan 10 14:30:10 server1 sshd[13045]: Failed password for bob from 192.168.1.30 port 50100 ssh2
Jan 10 03:00:00 server1 sshd[14000]: Accepted password for admin from 192.168.1.40 port 60000 ssh2
```

---

## 📍 STEP 6: Build Kafka Integration (30 minutes)

### 6.1: Create backend/ingestion/kafka_producer.py

```python
from confluent_kafka import Producer
import json
from typing import Dict
from backend.utils.logger import logger
from backend.utils.config import settings

class LogProducer:
    """Send logs to Kafka"""
    
    def __init__(self):
        self.config = {
            'bootstrap.servers': settings.kafka_bootstrap_servers,
            'client.id': 'log-producer'
        }
        self.producer = Producer(self.config)
        logger.info(f"Kafka Producer initialized: {settings.kafka_bootstrap_servers}")
    
    def send_log(self, topic: str, log_data: Dict):
        """Send a single log to Kafka"""
        try:
            message = json.dumps(log_data)
            self.producer.produce(
                topic=topic,
                value=message.encode('utf-8'),
                callback=self._delivery_report
            )
            self.producer.flush()
        except Exception as e:
            logger.error(f"Error sending log: {e}")
    
    def _delivery_report(self, err, msg):
        """Callback for delivery confirmation"""
        if err:
            logger.error(f"Delivery failed: {err}")
        else:
            logger.debug(f"Log delivered to {msg.topic()}")
```

### 6.2: Create backend/ingestion/kafka_consumer.py

```python
from confluent_kafka import Consumer, KafkaError
import json
from typing import Callable
from backend.utils.logger import logger
from backend.utils.config import settings

class LogConsumer:
    """Receive logs from Kafka"""
    
    def __init__(self, topics: list, group_id: str = 'log-consumer-group'):
        self.config = {
            'bootstrap.servers': settings.kafka_bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(self.config)
        self.consumer.subscribe(topics)
        logger.info(f"Kafka Consumer subscribed to: {topics}")
    
    def consume_logs(self, callback: Callable):
        """Continuously consume logs"""
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        logger.error(f"Consumer error: {msg.error()}")
                        break
                
                # Decode and process
                log_data = json.loads(msg.value().decode('utf-8'))
                callback(log_data)
                
        except KeyboardInterrupt:
            logger.info("Consumer stopped by user")
        finally:
            self.consumer.close()
```

### 6.3: Test Kafka Flow

Create `scripts/test_kafka.py`:

```python
import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser
from backend.ingestion.kafka_producer import LogProducer
from backend.ingestion.kafka_consumer import LogConsumer
import time

def test_kafka_flow():
    """Test: Parse -> Produce -> Consume"""
    
    parser = LogParser()
    producer = LogProducer()
    
    # Parse and send a log
    raw_log = "Jan 10 10:21:44 server1 sshd[12345]: Failed password for root from 192.168.1.10"
    parsed = parser.parse_syslog(raw_log)
    
    print("📤 Sending log to Kafka...")
    producer.send_log('auth_logs', parsed)
    print("✅ Log sent!")
    
    # Now consume it
    print("\n📥 Starting consumer (press Ctrl+C to stop)...")
    consumer = LogConsumer(['auth_logs'])
    
    def process_log(log_data):
        print(f"\n🔔 Received log:")
        print(f"   Event: {log_data['event_type']}")
        print(f"   User: {log_data.get('user', 'N/A')}")
        print(f"   Time: {log_data['timestamp']}")
    
    consumer.consume_logs(process_log)

if __name__ == '__main__':
    test_kafka_flow()
```

Run the test:

```powershell
python scripts/test_kafka.py
```

**✅ Checkpoint:** You should see the log being sent and received. Press Ctrl+C to stop.

---

## 📍 STEP 7: Build Elasticsearch Storage (25 minutes)

### 7.1: Create backend/storage/es_client.py

```python
from elasticsearch import Elasticsearch
from typing import Dict, List
from backend.utils.logger import logger
from backend.utils.config import settings

class LogStorage:
    """Store and retrieve logs from Elasticsearch"""
    
    def __init__(self):
        self.es = Elasticsearch([f'http://{settings.es_host}:{settings.es_port}'])
        self.index_name = settings.es_index_name
        self._create_index()
        logger.info(f"Elasticsearch client initialized: {settings.es_host}")
    
    def _create_index(self):
        """Create index with mappings"""
        if not self.es.indices.exists(index=self.index_name):
            mappings = {
                "mappings": {
                    "properties": {
                        "timestamp": {"type": "date"},
                        "host": {"type": "keyword"},
                        "service": {"type": "keyword"},
                        "event_type": {"type": "keyword"},
                        "user": {"type": "keyword"},
                        "source_ip": {"type": "ip"},
                        "severity": {"type": "integer"},
                        "is_anomaly": {"type": "boolean"},
                        "anomaly_score": {"type": "float"},
                        "raw_log": {"type": "text"}
                    }
                }
            }
            self.es.indices.create(index=self.index_name, body=mappings)
            logger.info(f"Created index: {self.index_name}")
    
    def store_log(self, log_data: Dict):
        """Store a single log"""
        try:
            self.es.index(index=self.index_name, document=log_data)
            logger.debug("Log stored successfully")
        except Exception as e:
            logger.error(f"Failed to store log: {e}")
    
    def search_logs(self, query: Dict, size: int = 100) -> List[Dict]:
        """Search logs"""
        try:
            result = self.es.search(index=self.index_name, query=query, size=size)
            return [hit['_source'] for hit in result['hits']['hits']]
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def get_recent_logs(self, hours: int = 24) -> List[Dict]:
        """Get logs from last N hours"""
        query = {
            "range": {
                "timestamp": {
                    "gte": f"now-{hours}h",
                    "lte": "now"
                }
            }
        }
        return self.search_logs(query)
    
    def get_failed_logins(self) -> List[Dict]:
        """Get all failed login attempts"""
        query = {
            "term": {"event_type": "LOGIN_FAILURE"}
        }
        return self.search_logs(query)
```

### 7.2: Test Elasticsearch

Create `scripts/test_elasticsearch.py`:

```python
import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser
from backend.storage.es_client import LogStorage

def test_elasticsearch():
    """Test: Parse -> Store -> Retrieve"""
    
    parser = LogParser()
    storage = LogStorage()
    
    # Parse and store logs
    logs = [
        "Jan 10 10:21:44 server1 sshd[12345]: Failed password for root from 192.168.1.10",
        "Jan 10 10:25:00 server1 sshd[12350]: Accepted password for admin from 192.168.1.5"
    ]
    
    print("📝 Storing logs...")
    for raw_log in logs:
        parsed = parser.parse_syslog(raw_log)
        if parsed:
            storage.store_log(parsed)
            print(f"  ✅ Stored: {parsed['event_type']}")
    
    # Wait a bit for indexing
    import time
    time.sleep(2)
    
    # Retrieve failed logins
    print("\n🔍 Searching for failed logins...")
    failed = storage.get_failed_logins()
    print(f"  Found {len(failed)} failed login(s)")
    
    for log in failed:
        print(f"    - User: {log.get('user', 'N/A')}, IP: {log.get('source_ip', 'N/A')}")
    
    print("\n✅ Elasticsearch test complete!")

if __name__ == '__main__':
    test_elasticsearch()
```

Run the test:

```powershell
python scripts/test_elasticsearch.py
```

**✅ Checkpoint:** Logs should be stored and retrieved successfully.

---

## 📍 STEP 8: Build Simple API (30 minutes)

### 8.1: Create backend/api/main.py

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser
from backend.storage.es_client import LogStorage
from backend.utils.logger import logger

app = FastAPI(title="AI Log Investigation API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
log_parser = LogParser()
log_storage = LogStorage()

# Pydantic models
class LogEntry(BaseModel):
    raw_log: str

class LogResponse(BaseModel):
    event_type: str
    user: str = None
    source_ip: str = None
    severity: int
    timestamp: str

@app.get("/")
async def root():
    """Health check"""
    return {"status": "running", "service": "AI Log Investigation API"}

@app.post("/api/logs/ingest")
async def ingest_log(log: LogEntry):
    """Ingest a single log"""
    try:
        # Parse
        parsed = log_parser.parse_syslog(log.raw_log)
        if not parsed:
            raise HTTPException(status_code=400, detail="Invalid log format")
        
        # Store
        log_storage.store_log(parsed)
        
        return {"status": "success", "parsed": parsed}
    
    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs/failed-logins", response_model=List[dict])
async def get_failed_logins():
    """Get all failed login attempts"""
    try:
        logs = log_storage.get_failed_logins()
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs/recent", response_model=List[dict])
async def get_recent_logs(hours: int = 24):
    """Get recent logs"""
    try:
        logs = log_storage.get_recent_logs(hours)
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    """Get basic statistics"""
    try:
        failed = log_storage.get_failed_logins()
        recent = log_storage.get_recent_logs(24)
        
        return {
            "total_logs_24h": len(recent),
            "failed_logins": len(failed),
            "unique_users": len(set(log.get('user') for log in recent if log.get('user')))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 8.2: Start the API

```powershell
# Start the API server
cd backend
python -m uvicorn api.main:app --reload
```

### 8.3: Test the API

Open a new PowerShell window and test:

```powershell
# Test health check
curl http://localhost:8000/

# Test log ingestion
curl -X POST "http://localhost:8000/api/logs/ingest" -H "Content-Type: application/json" -d '{\"raw_log\": \"Jan 10 10:21:44 server1 sshd[12345]: Failed password for root from 192.168.1.10\"}'

# Get failed logins
curl http://localhost:8000/api/logs/failed-logins

# Get stats
curl http://localhost:8000/api/stats
```

Or open http://localhost:8000/docs for interactive API docs!

**✅ Checkpoint:** API should respond to all endpoints.

---

## 📍 STEP 9: Create Complete Ingestion Script (20 minutes)

### 9.1: Create scripts/ingest_sample_logs.py

```python
import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser
from backend.ingestion.kafka_producer import LogProducer
from backend.storage.es_client import LogStorage
from pathlib import Path
import time

def ingest_logs():
    """Read sample logs and ingest them into the system"""
    
    parser = LogParser()
    producer = LogProducer()
    storage = LogStorage()
    
    # Read sample logs
    log_file = Path(__file__).parent.parent / "sample_logs" / "auth_logs.txt"
    
    if not log_file.exists():
        print(f"❌ Log file not found: {log_file}")
        return
    
    print(f"📖 Reading logs from: {log_file}")
    print("=" * 60)
    
    with open(log_file, 'r') as f:
        logs = f.readlines()
    
    print(f"Found {len(logs)} log entries\n")
    
    for i, raw_log in enumerate(logs, 1):
        if not raw_log.strip():
            continue
        
        # Parse
        parsed = parser.parse_syslog(raw_log.strip())
        
        if parsed:
            # Send to Kafka
            producer.send_log('auth_logs', parsed)
            
            # Store in Elasticsearch
            storage.store_log(parsed)
            
            # Display
            print(f"✅ [{i}/{len(logs)}] {parsed['event_type']}")
            print(f"   User: {parsed.get('user', 'N/A')}")
            print(f"   IP: {parsed.get('source_ip', 'N/A')}")
            print(f"   Severity: {parsed['severity']}/10")
            print()
            
            time.sleep(0.5)  # Simulate real-time
        else:
            print(f"❌ [{i}/{len(logs)}] Failed to parse")
    
    print("=" * 60)
    print("🎉 Ingestion complete!")
    print(f"\n📊 Summary:")
    print(f"   Total logs processed: {len(logs)}")
    print(f"\n🔗 View API docs: http://localhost:8000/docs")
    print(f"🔍 Check stats: http://localhost:8000/api/stats")

if __name__ == '__main__':
    ingest_logs()
```

### 9.2: Run Complete Ingestion

```powershell
# Make sure API is running in another terminal, then:
python scripts/ingest_sample_logs.py
```

**✅ Checkpoint:** All logs should be ingested and visible through API.

---

## 📍 STEP 10: Verify Everything Works (10 minutes)

### 10.1: Check All Services

```powershell
# Check Docker services
docker-compose ps

# Should see: zookeeper, kafka, elasticsearch all "Up"
```

### 10.2: Test Complete Flow

```powershell
# 1. Check API is running
curl http://localhost:8000/

# 2. Get statistics
curl http://localhost:8000/api/stats

# 3. Get failed logins
curl http://localhost:8000/api/logs/failed-logins

# 4. Get recent logs
curl http://localhost:8000/api/logs/recent?hours=1
```

### 10.3: Visual Verification

Open in browser: http://localhost:8000/docs

You should see:
- ✅ Interactive API documentation
- ✅ All endpoints listed
- ✅ Can test endpoints directly

---

## 🎉 CONGRATULATIONS!

You now have a working system with:

✅ **Log Parser** - Converts raw logs to structured data  
✅ **Kafka Integration** - Message streaming  
✅ **Elasticsearch** - Log storage and search  
✅ **REST API** - Query interface  
✅ **Sample Data** - 15 test logs  

---

## 🚀 What's Working Right Now

```
Sample Logs → Parser → Kafka → Elasticsearch
                              ↓
                           REST API
                              ↓
                    http://localhost:8000
```

---

## 📈 Next Steps (Optional - Add Later)

1. **Add ML Anomaly Detection** (1-2 hours)
2. **Add Correlation Engine** (1-2 hours)
3. **Build React Dashboard** (3-4 hours)
4. **Add Real-time WebSocket** (1 hour)

But for now, celebrate! You have a functional log investigation system! 🎊

---

## 🐛 Troubleshooting

### Docker containers not starting?
```powershell
docker-compose down
docker-compose up -d
```

### Kafka connection errors?
```powershell
# Wait 30 seconds after starting containers
timeout 30
```

### Elasticsearch not responding?
```powershell
# Check logs
docker logs elasticsearch

# Restart it
docker restart elasticsearch
```

### Python import errors?
```powershell
# Make sure venv is activated
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📊 Quick Commands Reference

```powershell
# Start everything
docker-compose up -d
.\venv\Scripts\activate
cd backend
python -m uvicorn api.main:app --reload

# In another terminal
.\venv\Scripts\activate
python scripts/ingest_sample_logs.py

# Check API
curl http://localhost:8000/api/stats

# Stop everything
docker-compose down
```

---

**You're now ready to add AI/ML features!** 🤖

Check IMPLEMENTATION_GUIDE.md Phase 4 for ML implementation.
