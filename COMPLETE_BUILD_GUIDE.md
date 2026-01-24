# 🚀 Complete Project Build Guide
## AI-Based Log Investigation Framework - Phase by Phase

---

## 📁 COMPLETE PROJECT STRUCTURE

```
D:\AI-based_log\project\
│
├── .gitignore                          ✅ Created
├── .env                                ✅ Created
├── requirements.txt                    ✅ Created
├── docker-compose.yml                  ✅ Created
├── README.md
│
├── backend/
│   ├── __init__.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py                   # Configuration management
│   │   └── logger.py                   # Logging setup
│   │
│   ├── parsers/
│   │   ├── __init__.py
│   │   └── log_parser.py               # Parse raw logs
│   │
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── kafka_producer.py           # Send to Kafka
│   │   └── kafka_consumer.py           # Receive from Kafka
│   │
│   ├── ml_engine/
│   │   ├── __init__.py
│   │   ├── feature_extractor.py        # Extract ML features
│   │   └── anomaly_detector.py         # ML anomaly detection
│   │
│   ├── correlation/
│   │   ├── __init__.py
│   │   └── correlator.py               # Event correlation
│   │
│   ├── storage/
│   │   ├── __init__.py
│   │   └── es_client.py                # Elasticsearch operations
│   │
│   └── api/
│       ├── __init__.py
│       └── main.py                     # FastAPI application
│
├── tests/
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_ml.py
│   └── test_api.py
│
├── scripts/
│   ├── ingest_sample_logs.py           # Load sample data
│   ├── train_model.py                  # Train ML model
│   └── demo.py                         # Demo scenarios
│
├── sample_logs/
│   └── auth_logs.txt                   # Sample log data
│
└── ml_models/
    └── (trained models saved here)
```

---

## 🎯 IMPLEMENTATION ROADMAP

### ✅ Phase 0: Environment Setup (DONE)
- [x] Create .gitignore
- [x] Create requirements.txt
- [x] Create .env
- [x] Create docker-compose.yml
- [x] Install dependencies

### 📝 Phase 1: Core Utilities (20 min)
- [ ] Create directory structure
- [ ] Config management
- [ ] Logger setup

### 🔍 Phase 2: Log Parsing (30 min)
- [ ] Log parser implementation
- [ ] Test parser

### 📨 Phase 3: Kafka Integration (30 min)
- [ ] Kafka producer
- [ ] Kafka consumer
- [ ] Test messaging

### 💾 Phase 4: Elasticsearch Storage (25 min)
- [ ] ES client
- [ ] Store & retrieve logs
- [ ] Test storage

### 🤖 Phase 5: ML Engine (45 min)
- [ ] Feature extraction
- [ ] Anomaly detection model
- [ ] Train & test model

### 🔗 Phase 6: Correlation Engine (30 min)
- [ ] Event correlation logic
- [ ] Incident detection
- [ ] Test correlation

### ⚡ Phase 7: REST API (40 min)
- [ ] FastAPI setup
- [ ] All endpoints
- [ ] Test API

### 🧪 Phase 8: Testing & Demo (30 min)
- [ ] Create sample logs
- [ ] Integration tests
- [ ] Demo script

**Total Time: ~4-5 hours**

---

# 📦 PHASE 1: CORE UTILITIES

## Step 1.1: Create Directory Structure

```powershell
# Run this command
mkdir backend, backend/api, backend/parsers, backend/ingestion, backend/ml_engine, backend/correlation, backend/storage, backend/utils, tests, scripts, sample_logs, ml_models

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

## Step 1.2: Create backend/utils/config.py

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application configuration from .env"""
    
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

## Step 1.3: Create backend/utils/logger.py

```python
import logging
import sys

def setup_logger(name: str, level: str = "INFO"):
    """Setup application logger"""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    
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

# 🔍 PHASE 2: LOG PARSING

## Step 2.1: Create backend/parsers/log_parser.py

```python
import re
from datetime import datetime
from typing import Dict, Optional
from backend.utils.logger import logger

class LogParser:
    """Parse various log formats into normalized structure"""
    
    def __init__(self):
        # Syslog: Jan 10 10:21:44 server1 sshd[12345]: message
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
            logger.warning(f"Failed to parse: {raw_log[:50]}")
            return None
        
        data = match.groupdict()
        
        normalized = {
            "timestamp": self._normalize_timestamp(data['timestamp']),
            "host": data['host'],
            "service": data['service'],
            "event_type": self._classify_event(data['message']),
            "severity": self._calculate_severity(data['message']),
            "raw_log": raw_log
        }
        
        # Extract optional fields
        user = self._extract_user(data['message'])
        if user:
            normalized['user'] = user
        
        ip = self._extract_ip(data['message'])
        if ip:
            normalized['source_ip'] = ip
        
        return normalized
    
    def _normalize_timestamp(self, ts: str) -> str:
        """Convert to ISO format"""
        try:
            dt = datetime.strptime(f"2026 {ts}", "%Y %b %d %H:%M:%S")
            return dt.isoformat() + "Z"
        except:
            return datetime.utcnow().isoformat() + "Z"
    
    def _classify_event(self, message: str) -> str:
        """Classify event type"""
        msg = message.lower()
        
        if "failed password" in msg or "authentication failure" in msg:
            return "LOGIN_FAILURE"
        elif "accepted password" in msg or "session opened" in msg:
            return "LOGIN_SUCCESS"
        elif "sudo" in msg or "su:" in msg:
            return "PRIVILEGE_ESCALATION"
        elif "connection closed" in msg:
            return "LOGOUT"
        return "UNKNOWN"
    
    def _calculate_severity(self, message: str) -> int:
        """Severity 1-10"""
        msg = message.lower()
        
        if "failed" in msg or "error" in msg:
            return 7
        elif "sudo" in msg:
            return 8
        elif "accepted" in msg:
            return 3
        return 5
    
    def _extract_user(self, message: str) -> Optional[str]:
        """Extract username"""
        patterns = [r'for (\w+)', r'user=(\w+)', r'USER=(\w+)']
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                return match.group(1)
        return None
    
    def _extract_ip(self, message: str) -> Optional[str]:
        """Extract IP address"""
        match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', message)
        return match.group(0) if match else None
```

## Step 2.2: Create tests/test_parser.py

```python
import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser

def test_parser():
    parser = LogParser()
    
    # Test 1: Failed login
    log1 = "Jan 10 10:21:44 server1 sshd[12345]: Failed password for root from 192.168.1.10"
    result1 = parser.parse_syslog(log1)
    
    print("✅ Test 1: Failed Login")
    assert result1['event_type'] == 'LOGIN_FAILURE'
    assert result1['user'] == 'root'
    assert result1['source_ip'] == '192.168.1.10'
    
    # Test 2: Successful login
    log2 = "Jan 10 10:25:00 server1 sshd[12350]: Accepted password for admin"
    result2 = parser.parse_syslog(log2)
    
    print("✅ Test 2: Successful Login")
    assert result2['event_type'] == 'LOGIN_SUCCESS'
    assert result2['user'] == 'admin'
    
    print("\n🎉 All parser tests passed!")

if __name__ == '__main__':
    test_parser()
```

**Run test:**
```powershell
python tests/test_parser.py
```

---

# 📨 PHASE 3: KAFKA INTEGRATION

## Step 3.1: Start Docker Services

```powershell
docker-compose up -d
timeout 15
docker-compose ps
```

## Step 3.2: Create backend/ingestion/kafka_producer.py

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
        logger.info(f"Kafka Producer ready: {settings.kafka_bootstrap_servers}")
    
    def send_log(self, topic: str, log_data: Dict):
        """Send log to Kafka topic"""
        try:
            message = json.dumps(log_data)
            self.producer.produce(
                topic=topic,
                value=message.encode('utf-8'),
                callback=self._delivery_report
            )
            self.producer.flush()
        except Exception as e:
            logger.error(f"Send failed: {e}")
    
    def _delivery_report(self, err, msg):
        if err:
            logger.error(f"Delivery failed: {err}")
        else:
            logger.debug(f"Delivered to {msg.topic()}")
```

## Step 3.3: Create backend/ingestion/kafka_consumer.py

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
        logger.info(f"Kafka Consumer subscribed: {topics}")
    
    def consume_logs(self, callback: Callable):
        """Continuously consume logs"""
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() != KafkaError._PARTITION_EOF:
                        logger.error(f"Error: {msg.error()}")
                    continue
                
                log_data = json.loads(msg.value().decode('utf-8'))
                callback(log_data)
                
        except KeyboardInterrupt:
            logger.info("Consumer stopped")
        finally:
            self.consumer.close()
```

---

# 💾 PHASE 4: ELASTICSEARCH STORAGE

## Step 4.1: Create backend/storage/es_client.py

```python
from elasticsearch import Elasticsearch
from typing import Dict, List
from backend.utils.logger import logger
from backend.utils.config import settings

class LogStorage:
    """Elasticsearch operations"""
    
    def __init__(self):
        self.es = Elasticsearch([f'http://{settings.es_host}:{settings.es_port}'])
        self.index_name = settings.es_index_name
        self._create_index()
        logger.info(f"Elasticsearch ready: {settings.es_host}")
    
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
        """Store single log"""
        try:
            self.es.index(index=self.index_name, document=log_data)
        except Exception as e:
            logger.error(f"Store failed: {e}")
    
    def search_logs(self, query: Dict, size: int = 100) -> List[Dict]:
        """Search with query"""
        try:
            result = self.es.search(index=self.index_name, query=query, size=size)
            return [hit['_source'] for hit in result['hits']['hits']]
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def get_failed_logins(self) -> List[Dict]:
        """Get all failed logins"""
        query = {"term": {"event_type": "LOGIN_FAILURE"}}
        return self.search_logs(query)
    
    def get_anomalies(self) -> List[Dict]:
        """Get all anomalies"""
        query = {"term": {"is_anomaly": True}}
        return self.search_logs(query)
    
    def get_stats(self) -> Dict:
        """Get basic statistics"""
        try:
            total = self.es.count(index=self.index_name)['count']
            failed = len(self.get_failed_logins())
            anomalies = len(self.get_anomalies())
            
            return {
                "total_logs": total,
                "failed_logins": failed,
                "anomalies": anomalies
            }
        except:
            return {"total_logs": 0, "failed_logins": 0, "anomalies": 0}
```

---

# 🤖 PHASE 5: ML ENGINE

## Step 5.1: Create backend/ml_engine/feature_extractor.py

```python
from datetime import datetime
from typing import Dict
import pandas as pd

class FeatureExtractor:
    """Extract ML features from logs"""
    
    def extract_features(self, log_data: Dict) -> Dict:
        """Convert log to ML features"""
        features = {}
        
        # Time features
        try:
            ts = datetime.fromisoformat(log_data['timestamp'].replace('Z', '+00:00'))
            features['hour'] = ts.hour
            features['day_of_week'] = ts.weekday()
            features['is_weekend'] = 1 if ts.weekday() >= 5 else 0
            features['is_night'] = 1 if ts.hour < 6 or ts.hour > 22 else 0
        except:
            features['hour'] = 0
            features['day_of_week'] = 0
            features['is_weekend'] = 0
            features['is_night'] = 0
        
        # Event features
        features['is_failure'] = 1 if 'FAILURE' in log_data.get('event_type', '') else 0
        features['is_escalation'] = 1 if 'ESCALATION' in log_data.get('event_type', '') else 0
        features['severity'] = log_data.get('severity', 5)
        
        return features
    
    def features_to_array(self, features: Dict) -> list:
        """Convert to array for ML"""
        return [
            features['hour'],
            features['day_of_week'],
            features['is_weekend'],
            features['is_night'],
            features['is_failure'],
            features['is_escalation'],
            features['severity']
        ]
```

## Step 5.2: Create backend/ml_engine/anomaly_detector.py

```python
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib
from pathlib import Path
from backend.utils.logger import logger

class AnomalyDetector:
    """ML-based anomaly detection"""
    
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train(self, features: np.ndarray):
        """Train on normal logs"""
        if len(features) < 10:
            logger.warning("Need at least 10 samples to train")
            return
        
        features_scaled = self.scaler.fit_transform(features)
        self.model.fit(features_scaled)
        self.is_trained = True
        logger.info(f"Model trained on {len(features)} samples")
    
    def predict(self, features: np.ndarray) -> Dict:
        """Detect if anomaly"""
        if not self.is_trained:
            return {'is_anomaly': False, 'anomaly_score': 0.0}
        
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        prediction = self.model.predict(features_scaled)[0]
        score = self.model.score_samples(features_scaled)[0]
        
        # Convert to probability
        anomaly_score = 1 / (1 + np.exp(score))
        
        return {
            'is_anomaly': prediction == -1,
            'anomaly_score': float(anomaly_score),
            'label': 'SUSPICIOUS' if prediction == -1 else 'NORMAL'
        }
    
    def save_model(self, filepath: str):
        """Save trained model"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump({'model': self.model, 'scaler': self.scaler}, filepath)
        logger.info(f"Model saved: {filepath}")
    
    def load_model(self, filepath: str):
        """Load trained model"""
        data = joblib.load(filepath)
        self.model = data['model']
        self.scaler = data['scaler']
        self.is_trained = True
        logger.info(f"Model loaded: {filepath}")
```

---

# 🔗 PHASE 6: CORRELATION ENGINE

## Step 6.1: Create backend/correlation/correlator.py

```python
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict
from backend.utils.logger import logger

class IncidentCorrelator:
    """Correlate events into incidents"""
    
    def __init__(self):
        self.event_buffer = defaultdict(list)
        self.incidents = []
    
    def add_event(self, log_data: dict):
        """Add event and check for patterns"""
        source_key = log_data.get('source_ip', 'unknown')
        self.event_buffer[source_key].append(log_data)
        
        # Check patterns
        self._check_brute_force(source_key)
        self._check_privilege_escalation(source_key)
        
        # Cleanup old events
        self._cleanup_old_events()
    
    def _check_brute_force(self, source_ip: str):
        """Detect brute force: Multiple failures + success"""
        events = self.event_buffer[source_ip]
        
        # Get recent events (last 5 minutes)
        now = datetime.utcnow()
        recent = [
            e for e in events
            if (now - datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00')))
            < timedelta(minutes=5)
        ]
        
        # Count failures and successes
        failures = [e for e in recent if e['event_type'] == 'LOGIN_FAILURE']
        successes = [e for e in recent if e['event_type'] == 'LOGIN_SUCCESS']
        
        # Brute force detected!
        if len(failures) >= 5 and len(successes) >= 1:
            self._create_incident(
                incident_type='BRUTE_FORCE_ATTACK',
                source_ip=source_ip,
                events=recent,
                severity=9,
                description=f"{len(failures)} failed logins followed by successful login"
            )
    
    def _check_privilege_escalation(self, source_ip: str):
        """Detect privilege escalation after login"""
        events = self.event_buffer[source_ip]
        
        for i in range(len(events) - 1):
            if (events[i]['event_type'] == 'LOGIN_SUCCESS' and
                events[i+1]['event_type'] == 'PRIVILEGE_ESCALATION'):
                
                time_diff = (
                    datetime.fromisoformat(events[i+1]['timestamp'].replace('Z', '+00:00')) -
                    datetime.fromisoformat(events[i]['timestamp'].replace('Z', '+00:00'))
                )
                
                if time_diff < timedelta(minutes=2):
                    self._create_incident(
                        incident_type='PRIVILEGE_ESCALATION',
                        source_ip=source_ip,
                        events=[events[i], events[i+1]],
                        severity=8,
                        description="Suspicious privilege escalation after login"
                    )
    
    def _create_incident(self, incident_type: str, source_ip: str,
                        events: List[dict], severity: int, description: str):
        """Create incident record"""
        incident = {
            'incident_id': f"INC-{datetime.utcnow().timestamp()}",
            'type': incident_type,
            'source_ip': source_ip,
            'severity': severity,
            'description': description,
            'event_count': len(events),
            'first_seen': events[0]['timestamp'],
            'last_seen': events[-1]['timestamp'],
            'events': events,
            'status': 'OPEN'
        }
        
        self.incidents.append(incident)
        logger.warning(f"🚨 INCIDENT: {incident_type} from {source_ip}")
    
    def _cleanup_old_events(self):
        """Remove events older than 1 hour"""
        cutoff = datetime.utcnow() - timedelta(hours=1)
        
        for source_ip in list(self.event_buffer.keys()):
            self.event_buffer[source_ip] = [
                e for e in self.event_buffer[source_ip]
                if datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00')) > cutoff
            ]
    
    def get_open_incidents(self) -> List[dict]:
        """Return all open incidents"""
        return [i for i in self.incidents if i['status'] == 'OPEN']
```

---

# ⚡ PHASE 7: REST API

## Step 7.1: Create backend/api/main.py

```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser
from backend.storage.es_client import LogStorage
from backend.ml_engine.feature_extractor import FeatureExtractor
from backend.ml_engine.anomaly_detector import AnomalyDetector
from backend.correlation.correlator import IncidentCorrelator
from backend.utils.logger import logger
import numpy as np

app = FastAPI(title="AI Log Investigation API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
log_parser = LogParser()
log_storage = LogStorage()
feature_extractor = FeatureExtractor()
anomaly_detector = AnomalyDetector()
correlator = IncidentCorrelator()

# Try to load trained model
try:
    anomaly_detector.load_model('./ml_models/isolation_forest.pkl')
except:
    logger.warning("No trained model found - anomaly detection disabled")

# Models
class LogEntry(BaseModel):
    raw_log: str

@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "AI Log Investigation API",
        "version": "1.0.0"
    }

@app.post("/api/logs/ingest")
async def ingest_log(log: LogEntry):
    """Ingest a single log"""
    try:
        # Parse
        parsed = log_parser.parse_syslog(log.raw_log)
        if not parsed:
            raise HTTPException(status_code=400, detail="Invalid log format")
        
        # Extract ML features
        features = feature_extractor.extract_features(parsed)
        feature_array = np.array(feature_extractor.features_to_array(features))
        
        # Anomaly detection
        if anomaly_detector.is_trained:
            detection = anomaly_detector.predict(feature_array)
            parsed.update(detection)
        else:
            parsed['is_anomaly'] = False
            parsed['anomaly_score'] = 0.0
        
        # Store
        log_storage.store_log(parsed)
        
        # Correlate
        correlator.add_event(parsed)
        
        return {"status": "success", "log": parsed}
    
    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs/failed-logins")
async def get_failed_logins():
    """Get all failed login attempts"""
    return log_storage.get_failed_logins()

@app.get("/api/logs/anomalies")
async def get_anomalies():
    """Get all detected anomalies"""
    return log_storage.get_anomalies()

@app.get("/api/incidents")
async def get_incidents():
    """Get all open incidents"""
    return correlator.get_open_incidents()

@app.get("/api/stats")
async def get_stats():
    """Get statistics"""
    es_stats = log_storage.get_stats()
    incidents = correlator.get_open_incidents()
    
    return {
        **es_stats,
        "open_incidents": len(incidents),
        "model_trained": anomaly_detector.is_trained
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

# 🧪 PHASE 8: SAMPLE DATA & SCRIPTS

## Step 8.1: Create sample_logs/auth_logs.txt

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
Jan 10 09:15:00 server1 sshd[14100]: Accepted password for alice from 192.168.1.20 port 60100 ssh2
Jan 10 16:30:00 server1 sshd[14200]: Failed password for charlie from 10.0.0.50 port 60200 ssh2
```

## Step 8.2: Create scripts/train_model.py

```python
import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser
from backend.ml_engine.feature_extractor import FeatureExtractor
from backend.ml_engine.anomaly_detector import AnomalyDetector
from pathlib import Path
import numpy as np

def train_model():
    """Train anomaly detection model on normal logs"""
    
    parser = LogParser()
    extractor = FeatureExtractor()
    detector = AnomalyDetector(contamination=0.1)
    
    # Read sample logs
    log_file = Path(__file__).parent.parent / "sample_logs" / "auth_logs.txt"
    
    with open(log_file, 'r') as f:
        logs = f.readlines()
    
    print(f"📖 Reading {len(logs)} logs...")
    
    # Extract features
    features_list = []
    for raw_log in logs:
        if not raw_log.strip():
            continue
        
        parsed = parser.parse_syslog(raw_log.strip())
        if parsed:
            features = extractor.extract_features(parsed)
            feature_array = extractor.features_to_array(features)
            features_list.append(feature_array)
    
    # Train model
    features_array = np.array(features_list)
    print(f"\n🤖 Training model on {len(features_array)} samples...")
    detector.train(features_array)
    
    # Save model
    detector.save_model('./ml_models/isolation_forest.pkl')
    print("✅ Model trained and saved!")
    
    # Test predictions
    print("\n🧪 Testing predictions:")
    for i, features in enumerate(features_list[:5]):
        result = detector.predict(np.array(features))
        print(f"  Log {i+1}: {result['label']} (score: {result['anomaly_score']:.3f})")

if __name__ == '__main__':
    train_model()
```

## Step 8.3: Create scripts/ingest_sample_logs.py

```python
import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser
from backend.storage.es_client import LogStorage
from backend.ml_engine.feature_extractor import FeatureExtractor
from backend.ml_engine.anomaly_detector import AnomalyDetector
from backend.correlation.correlator import IncidentCorrelator
from pathlib import Path
import time
import numpy as np

def ingest_logs():
    """Complete ingestion pipeline"""
    
    parser = LogParser()
    storage = LogStorage()
    extractor = FeatureExtractor()
    detector = AnomalyDetector()
    correlator = IncidentCorrelator()
    
    # Load model
    try:
        detector.load_model('./ml_models/isolation_forest.pkl')
        print("✅ Model loaded")
    except:
        print("⚠️  No model found - train first with: python scripts/train_model.py")
    
    # Read logs
    log_file = Path(__file__).parent.parent / "sample_logs" / "auth_logs.txt"
    
    with open(log_file, 'r') as f:
        logs = f.readlines()
    
    print(f"\n📖 Processing {len(logs)} logs...")
    print("=" * 60)
    
    for i, raw_log in enumerate(logs, 1):
        if not raw_log.strip():
            continue
        
        # Parse
        parsed = parser.parse_syslog(raw_log.strip())
        if not parsed:
            continue
        
        # ML features & detection
        features = extractor.extract_features(parsed)
        feature_array = np.array(extractor.features_to_array(features))
        
        if detector.is_trained:
            detection = detector.predict(feature_array)
            parsed.update(detection)
        else:
            parsed['is_anomaly'] = False
            parsed['anomaly_score'] = 0.0
        
        # Store
        storage.store_log(parsed)
        
        # Correlate
        correlator.add_event(parsed)
        
        # Display
        status = "🚨" if parsed.get('is_anomaly') else "✅"
        print(f"{status} [{i}/{len(logs)}] {parsed['event_type']}")
        print(f"   User: {parsed.get('user', 'N/A')}, IP: {parsed.get('source_ip', 'N/A')}")
        if parsed.get('is_anomaly'):
            print(f"   ⚠️  ANOMALY: {parsed['anomaly_score']:.3f}")
        
        time.sleep(0.3)
    
    print("=" * 60)
    
    # Show incidents
    incidents = correlator.get_open_incidents()
    if incidents:
        print(f"\n🚨 DETECTED {len(incidents)} INCIDENT(S):")
        for inc in incidents:
            print(f"  - {inc['type']}: {inc['description']}")
    
    # Show stats
    stats = storage.get_stats()
    print(f"\n📊 STATISTICS:")
    print(f"  Total logs: {stats['total_logs']}")
    print(f"  Failed logins: {stats['failed_logins']}")
    print(f"  Anomalies: {stats['anomalies']}")
    print(f"  Open incidents: {len(incidents)}")
    
    print(f"\n🌐 View API: http://localhost:8000/docs")

if __name__ == '__main__':
    ingest_logs()
```

---

# 🚀 COMPLETE EXECUTION SEQUENCE

## Step-by-Step Commands

```powershell
# 1. Ensure Docker is running
docker-compose up -d
timeout 15

# 2. Activate venv (if not already)
.\venv\Scripts\activate

# 3. Train ML model
python scripts/train_model.py

# 4. Start API (in Terminal 1)
cd backend
python -m uvicorn api.main:app --reload

# 5. In new Terminal 2 - Ingest logs
.\venv\Scripts\activate
python scripts/ingest_sample_logs.py

# 6. Test API
curl http://localhost:8000/api/stats
curl http://localhost:8000/api/incidents

# 7. Open browser
start http://localhost:8000/docs
```

---

# ✅ VERIFICATION CHECKLIST

After completing all phases:

- [ ] Docker services running (kafka, elasticsearch)
- [ ] Parser test passes
- [ ] ML model trained
- [ ] API responds at http://localhost:8000
- [ ] Sample logs ingested
- [ ] Stats show correct counts
- [ ] Incidents detected (brute force)
- [ ] Swagger UI accessible

---

# 📊 PROJECT STATUS

**Current Status:** Phase 0 Complete ✅

**Next Action:** Run the directory creation commands from Phase 1

**Estimated Time to Complete:** 4-5 hours of focused work

**What You'll Have:**
- Full-stack log investigation system
- Real-time processing pipeline
- AI anomaly detection
- Event correlation
- REST API with Swagger docs
- Working demo with sample data

---

# 🎯 QUICK START COMMANDS

```powershell
# Complete setup (run once)
mkdir backend, backend/api, backend/parsers, backend/ingestion, backend/ml_engine, backend/correlation, backend/storage, backend/utils, tests, scripts, sample_logs, ml_models
New-Item backend/__init__.py, backend/api/__init__.py, backend/parsers/__init__.py, backend/ingestion/__init__.py, backend/ml_engine/__init__.py, backend/correlation/__init__.py, backend/storage/__init__.py, backend/utils/__init__.py, tests/__init__.py

# Daily startup
docker-compose up -d
.\venv\Scripts\activate
cd backend
python -m uvicorn api.main:app --reload
```

**Now start creating the Python files from each phase! Copy the code exactly as shown above.** 🚀
