# 🎓 Step-by-Step Implementation Guide
## AI-Based Log Investigation Framework

This guide will walk you through building the project from scratch, explaining each concept like a teacher.

---

## 📚 PHASE 0: Understanding the Fundamentals

### What is a SIEM?
**SIEM = Security Information and Event Management**

Think of it like a security guard monitoring all cameras in a building:
- **Logs** = Camera footage (events happening in your system)
- **SIEM** = The security room where all cameras are monitored
- **AI** = Smart system that notices unusual patterns (like someone entering at 3 AM)

### Why Do We Need This?
Imagine a hospital with 1000 servers generating 100,000 log entries per minute. A human can't read them all. We need automation to:
1. Collect logs automatically
2. Understand them (parsing)
3. Find suspicious activity (AI)
4. Alert security teams

---

## 🚀 PHASE 1: Project Setup (Day 1)

### Step 1.1: Create Project Structure

```bash
# Create the main project directory structure
mkdir -p ai_log_framework
cd ai_log_framework

# Create subdirectories
mkdir -p {backend,frontend,kafka,elasticsearch,tests,sample_logs,ml_models,docs}
mkdir -p backend/{api,parsers,ml_engine,correlation,ingestion}
```

**Explanation:**
- `backend/` = All Python code (brain of the system)
- `frontend/` = Dashboard UI (what investigators see)
- `kafka/` = Message queue configurations
- `elasticsearch/` = Database for logs
- `tests/` = Quality assurance code
- `sample_logs/` = Test data
- `ml_models/` = AI models storage

### Step 1.2: Initialize Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
.\venv\Scripts\activate

# Activate it (Linux/Mac)
source venv/bin/activate

# Create requirements.txt
touch requirements.txt
```

**Explanation:**
Virtual environments isolate your project dependencies. Think of it as a separate workspace where you install only what this project needs.

### Step 1.3: Install Core Dependencies

```txt
# Add to requirements.txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
confluent-kafka==2.3.0
elasticsearch==8.11.1
scikit-learn==1.4.0
pandas==2.2.0
numpy==1.26.3
pydantic==2.5.3
python-multipart==0.0.6
aiofiles==23.2.1
pytest==7.4.4
httpx==0.26.0
```

```bash
# Install all packages
pip install -r requirements.txt
```

**Explanation of Key Libraries:**
- **FastAPI** = Modern web framework (creates APIs easily)
- **Kafka** = Message queue (handles millions of logs/second)
- **Elasticsearch** = Fast search database (finds logs in milliseconds)
- **scikit-learn** = AI/ML library (detects anomalies)
- **pandas** = Data manipulation (like Excel for programmers)

---

## 🔧 PHASE 2: Log Ingestion System (Day 2-3)

### Step 2.1: Understanding Log Formats

**Example 1: SSH Login Log (Syslog)**
```
Jan 10 10:21:44 server1 sshd[12345]: Failed password for root from 192.168.1.10 port 45678 ssh2
```

**What does this mean?**
- Timestamp: Jan 10 10:21:44
- Source: server1
- Service: sshd (SSH daemon)
- Event: Failed password attempt
- User: root
- IP: 192.168.1.10

**Example 2: Firewall Log (CSV)**
```csv
timestamp,src_ip,dst_ip,src_port,dst_port,action,protocol
2026-01-10T10:21:44Z,192.168.1.10,10.0.0.5,45678,22,DENY,TCP
```

### Step 2.2: Create Log Parser

**File:** `backend/parsers/log_parser.py`

```python
import re
from datetime import datetime
from typing import Dict, Optional

class LogParser:
    """
    Converts raw logs into a standardized format.
    Think of it as a translator that understands different log languages.
    """
    
    def __init__(self):
        # Regex patterns for different log types
        self.syslog_pattern = re.compile(
            r'(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+)\s+'
            r'(?P<host>\S+)\s+'
            r'(?P<service>\w+)\[(?P<pid>\d+)\]:\s+'
            r'(?P<message>.*)'
        )
    
    def parse_syslog(self, raw_log: str) -> Optional[Dict]:
        """
        Parse a syslog entry.
        
        Example input:
        "Jan 10 10:21:44 server1 sshd[12345]: Failed password for root"
        
        Example output:
        {
            "timestamp": "2026-01-10T10:21:44Z",
            "host": "server1",
            "service": "sshd",
            "event_type": "LOGIN_FAILURE",
            "user": "root",
            "raw_log": "..."
        }
        """
        match = self.syslog_pattern.match(raw_log)
        if not match:
            return None
        
        data = match.groupdict()
        
        # Normalize the log
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
        
        return normalized
    
    def _normalize_timestamp(self, ts: str) -> str:
        """Convert various timestamp formats to ISO 8601 UTC"""
        # Implementation depends on format
        # For now, assume current year
        dt = datetime.strptime(f"2026 {ts}", "%Y %b %d %H:%M:%S")
        return dt.isoformat() + "Z"
    
    def _classify_event(self, message: str) -> str:
        """Classify the event type"""
        if "Failed password" in message:
            return "LOGIN_FAILURE"
        elif "Accepted password" in message:
            return "LOGIN_SUCCESS"
        elif "sudo" in message:
            return "PRIVILEGE_ESCALATION"
        return "UNKNOWN"
    
    def _extract_user(self, message: str) -> Optional[str]:
        """Extract username from message"""
        match = re.search(r'for (\w+)', message)
        return match.group(1) if match else None
    
    def _calculate_severity(self, message: str) -> int:
        """Assign severity level (1-10)"""
        if "Failed" in message:
            return 7
        elif "Accepted" in message:
            return 3
        return 5
```

**Explanation:**
1. **Regex patterns** = Instructions to find specific patterns in text
2. **Normalization** = Converting different formats to ONE standard format
3. **Classification** = Labeling what type of event it is

---

## 🎯 PHASE 3: Kafka Integration (Day 4-5)

### Step 3.1: Understanding Kafka

**Analogy:** Kafka is like a post office:
- **Producer** = Person sending letters (log sources)
- **Topic** = Mailbox category (e.g., "auth_logs", "firewall_logs")
- **Consumer** = Person receiving letters (your parser)

**Why Kafka?**
- Handles 1 million+ messages per second
- Never loses data (persistence)
- Decouples producers from consumers

### Step 3.2: Setup Kafka with Docker

**File:** `docker-compose.yml`

```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:7.5.0
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_TICK_TIME: 2000
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:7.5.0
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

```bash
# Start all services
docker-compose up -d

# Check if running
docker-compose ps
```

**Explanation:**
- **Zookeeper** = Kafka's coordinator (keeps track of brokers)
- **Kafka** = Message broker
- **Elasticsearch** = Log storage

### Step 3.3: Create Kafka Producer

**File:** `backend/ingestion/kafka_producer.py`

```python
from confluent_kafka import Producer
import json
from typing import Dict

class LogProducer:
    """
    Sends logs to Kafka.
    Think of it as dropping letters in a mailbox.
    """
    
    def __init__(self, bootstrap_servers: str = 'localhost:9092'):
        self.config = {
            'bootstrap.servers': bootstrap_servers,
            'client.id': 'log-producer'
        }
        self.producer = Producer(self.config)
    
    def send_log(self, topic: str, log_data: Dict):
        """
        Send a single log entry to Kafka
        
        Args:
            topic: Category of log (e.g., 'auth_logs')
            log_data: Normalized log dictionary
        """
        try:
            # Convert dict to JSON string
            message = json.dumps(log_data)
            
            # Send to Kafka
            self.producer.produce(
                topic=topic,
                value=message.encode('utf-8'),
                callback=self._delivery_report
            )
            
            # Wait for message to be sent
            self.producer.flush()
            
        except Exception as e:
            print(f"Error sending log: {e}")
    
    def _delivery_report(self, err, msg):
        """Callback to confirm delivery"""
        if err:
            print(f"Delivery failed: {err}")
        else:
            print(f"Log delivered to {msg.topic()} [{msg.partition()}]")
```

### Step 3.4: Create Kafka Consumer

**File:** `backend/ingestion/kafka_consumer.py`

```python
from confluent_kafka import Consumer, KafkaError
import json

class LogConsumer:
    """
    Receives logs from Kafka.
    Think of it as checking your mailbox.
    """
    
    def __init__(self, topics: list, group_id: str = 'log-consumer-group'):
        self.config = {
            'bootstrap.servers': 'localhost:9092',
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(self.config)
        self.consumer.subscribe(topics)
    
    def consume_logs(self, callback_function):
        """
        Continuously read logs and process them
        
        Args:
            callback_function: Function to call for each log
        """
        try:
            while True:
                # Poll for new messages
                msg = self.consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    else:
                        print(f"Consumer error: {msg.error()}")
                        break
                
                # Decode message
                log_data = json.loads(msg.value().decode('utf-8'))
                
                # Process log
                callback_function(log_data)
                
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()
```

---

## 🤖 PHASE 4: AI/ML Anomaly Detection (Day 6-8)

### Step 4.1: Understanding Anomaly Detection

**What is an anomaly?**
Something that's different from normal behavior.

**Examples:**
- **Normal:** User logs in Monday-Friday, 9 AM - 5 PM
- **Anomaly:** Same user logs in Sunday, 3 AM

**How does AI detect this?**
1. Learn what "normal" looks like from historical data
2. When new log arrives, check if it's similar to normal
3. If very different → Flag as suspicious

### Step 4.2: Feature Engineering

**File:** `backend/ml_engine/feature_extractor.py`

```python
import pandas as pd
from datetime import datetime

class FeatureExtractor:
    """
    Converts logs into numbers that AI can understand.
    
    Think of it like converting colors to numbers:
    Red = 1, Green = 2, Blue = 3
    """
    
    def extract_features(self, log_data: dict) -> dict:
        """
        Convert log attributes to numerical features
        
        Example:
        Input: {"timestamp": "2026-01-10T03:00:00Z", "event_type": "LOGIN_FAILURE"}
        Output: {"hour": 3, "is_weekend": 1, "is_failure": 1}
        """
        features = {}
        
        # Time-based features
        timestamp = datetime.fromisoformat(log_data['timestamp'].replace('Z', '+00:00'))
        features['hour'] = timestamp.hour
        features['day_of_week'] = timestamp.weekday()
        features['is_weekend'] = 1 if timestamp.weekday() >= 5 else 0
        features['is_night'] = 1 if timestamp.hour < 6 or timestamp.hour > 22 else 0
        
        # Event type features
        features['is_failure'] = 1 if 'FAILURE' in log_data.get('event_type', '') else 0
        features['is_escalation'] = 1 if 'ESCALATION' in log_data.get('event_type', '') else 0
        
        # Severity
        features['severity'] = log_data.get('severity', 5)
        
        return features
    
    def aggregate_features(self, logs_df: pd.DataFrame, window_minutes: int = 5) -> pd.DataFrame:
        """
        Create aggregate features over time windows
        
        Example: Count of failed logins in last 5 minutes
        """
        # Group by time windows
        logs_df['timestamp'] = pd.to_datetime(logs_df['timestamp'])
        logs_df = logs_df.set_index('timestamp')
        
        # Rolling statistics
        agg_features = logs_df.rolling(f'{window_minutes}min').agg({
            'is_failure': 'sum',  # Total failures in window
            'severity': 'mean',   # Average severity
            'hour': 'first'       # Time of day
        })
        
        return agg_features
```

### Step 4.3: Anomaly Detection Model

**File:** `backend/ml_engine/anomaly_detector.py`

```python
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import numpy as np
import joblib

class AnomalyDetector:
    """
    AI model that learns normal behavior and detects outliers.
    
    Algorithm: Isolation Forest
    - Idea: Anomalies are easier to isolate (separate) from normal data
    - Like finding the one red ball in a box of 1000 blue balls
    """
    
    def __init__(self, contamination=0.1):
        """
        Args:
            contamination: Expected percentage of anomalies (0.1 = 10%)
        """
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def train(self, features: np.ndarray):
        """
        Train the model on normal logs
        
        Args:
            features: 2D array of numerical features
                     Shape: (num_logs, num_features)
        """
        # Normalize features (make them same scale)
        features_scaled = self.scaler.fit_transform(features)
        
        # Train model
        self.model.fit(features_scaled)
        self.is_trained = True
        
        print(f"Model trained on {len(features)} samples")
    
    def predict(self, features: np.ndarray) -> dict:
        """
        Detect if new log is anomaly
        
        Returns:
            {
                'is_anomaly': True/False,
                'anomaly_score': 0.0 to 1.0 (higher = more suspicious)
            }
        """
        if not self.is_trained:
            raise Exception("Model not trained yet!")
        
        # Normalize
        features_scaled = self.scaler.transform(features)
        
        # Predict
        prediction = self.model.predict(features_scaled)[0]
        score = self.model.score_samples(features_scaled)[0]
        
        # Convert score to 0-1 range
        anomaly_score = self._normalize_score(score)
        
        return {
            'is_anomaly': prediction == -1,  # -1 = anomaly, 1 = normal
            'anomaly_score': anomaly_score,
            'label': 'SUSPICIOUS' if prediction == -1 else 'NORMAL'
        }
    
    def _normalize_score(self, score: float) -> float:
        """Convert isolation score to 0-1 probability"""
        # Isolation Forest scores are negative
        # More negative = more anomalous
        return 1 / (1 + np.exp(score))
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        joblib.dump({
            'model': self.model,
            'scaler': self.scaler
        }, filepath)
    
    def load_model(self, filepath: str):
        """Load pre-trained model"""
        data = joblib.load(filepath)
        self.model = data['model']
        self.scaler = data['scaler']
        self.is_trained = True
```

**Explanation of Isolation Forest:**
1. Randomly selects features
2. Randomly splits data points
3. Anomalies need fewer splits to isolate
4. Normal points need many splits

---

## 🔗 PHASE 5: Correlation Engine (Day 9-10)

### Step 5.1: Understanding Correlation

**Scenario:** Brute Force Attack Detection

Single suspicious events:
- 10:00 AM - Login failure from IP 1.2.3.4
- 10:01 AM - Login failure from IP 1.2.3.4
- 10:02 AM - Login failure from IP 1.2.3.4
- ...
- 10:05 AM - Login success from IP 1.2.3.4

**Correlation Rule:**
IF (same IP + 10+ failures within 5 min + 1 success) THEN "Brute Force Attack"

### Step 5.2: Create Correlation Engine

**File:** `backend/correlation/correlator.py`

```python
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict

class IncidentCorrelator:
    """
    Connects related suspicious events into incidents.
    Think of it as a detective connecting clues.
    """
    
    def __init__(self):
        # Store recent events grouped by source
        self.event_buffer = defaultdict(list)
        self.incidents = []
    
    def add_event(self, log_data: dict):
        """Add a new log event to correlation buffer"""
        source_key = log_data.get('source_ip', 'unknown')
        self.event_buffer[source_key].append(log_data)
        
        # Check for patterns
        self._check_brute_force(source_key)
        self._check_privilege_escalation(source_key)
        
        # Clean old events
        self._cleanup_old_events()
    
    def _check_brute_force(self, source_ip: str):
        """
        Detect brute force attack pattern
        
        Pattern: Multiple failed logins followed by success
        """
        events = self.event_buffer[source_ip]
        
        # Get events from last 5 minutes
        now = datetime.utcnow()
        recent_events = [
            e for e in events
            if (now - datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00')))
            < timedelta(minutes=5)
        ]
        
        # Count failures and successes
        failures = [e for e in recent_events if e['event_type'] == 'LOGIN_FAILURE']
        successes = [e for e in recent_events if e['event_type'] == 'LOGIN_SUCCESS']
        
        # Trigger condition
        if len(failures) >= 10 and len(successes) >= 1:
            self._create_incident(
                incident_type='BRUTE_FORCE_ATTACK',
                source_ip=source_ip,
                events=recent_events,
                severity=9,
                description=f"Detected {len(failures)} failed logins followed by successful login"
            )
    
    def _check_privilege_escalation(self, source_ip: str):
        """
        Detect privilege escalation attempt
        
        Pattern: Login followed by sudo/admin commands
        """
        events = self.event_buffer[source_ip]
        
        # Look for login -> escalation sequence
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
        """Create and store an incident"""
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
        print(f"🚨 INCIDENT DETECTED: {incident_type} from {source_ip}")
    
    def _cleanup_old_events(self):
        """Remove events older than 1 hour"""
        cutoff_time = datetime.utcnow() - timedelta(hours=1)
        
        for source_ip in list(self.event_buffer.keys()):
            self.event_buffer[source_ip] = [
                e for e in self.event_buffer[source_ip]
                if datetime.fromisoformat(e['timestamp'].replace('Z', '+00:00')) > cutoff_time
            ]
    
    def get_open_incidents(self) -> List[dict]:
        """Return all open incidents"""
        return [i for i in self.incidents if i['status'] == 'OPEN']
```

---

## 💾 PHASE 6: Storage with Elasticsearch (Day 11-12)

### Step 6.1: Understanding Elasticsearch

**Analogy:** Elasticsearch is like a library with a super-smart index system.
- Traditional DB: You ask for a specific book (ID)
- Elasticsearch: You ask "find books about cybersecurity from 2026" (search)

**Why Elasticsearch?**
- Search millions of logs in milliseconds
- Full-text search (find logs containing "failed password")
- Aggregations (count how many attacks per hour)

### Step 6.2: Create Elasticsearch Client

**File:** `backend/storage/es_client.py`

```python
from elasticsearch import Elasticsearch
from datetime import datetime
from typing import Dict, List

class LogStorage:
    """
    Stores and retrieves logs from Elasticsearch
    """
    
    def __init__(self, es_host: str = 'localhost:9200'):
        self.es = Elasticsearch([f'http://{es_host}'])
        self.index_name = 'security-logs'
        self._create_index()
    
    def _create_index(self):
        """Create index with proper mappings"""
        if not self.es.indices.exists(index=self.index_name):
            mappings = {
                "mappings": {
                    "properties": {
                        "timestamp": {"type": "date"},
                        "source_ip": {"type": "ip"},
                        "destination_ip": {"type": "ip"},
                        "event_type": {"type": "keyword"},
                        "severity": {"type": "integer"},
                        "is_anomaly": {"type": "boolean"},
                        "anomaly_score": {"type": "float"},
                        "raw_log": {"type": "text"}
                    }
                }
            }
            self.es.indices.create(index=self.index_name, body=mappings)
    
    def store_log(self, log_data: Dict):
        """Store a single log entry"""
        self.es.index(index=self.index_name, document=log_data)
    
    def search_logs(self, query: Dict, size: int = 100) -> List[Dict]:
        """
        Search logs with Elasticsearch query DSL
        
        Example query:
        {
            "match": {
                "event_type": "LOGIN_FAILURE"
            }
        }
        """
        result = self.es.search(index=self.index_name, query=query, size=size)
        return [hit['_source'] for hit in result['hits']['hits']]
    
    def get_anomalies(self, hours: int = 24) -> List[Dict]:
        """Get all anomalies from last N hours"""
        query = {
            "bool": {
                "must": [
                    {"term": {"is_anomaly": True}},
                    {"range": {
                        "timestamp": {
                            "gte": f"now-{hours}h",
                            "lte": "now"
                        }
                    }}
                ]
            }
        }
        return self.search_logs(query)
    
    def get_top_attackers(self, limit: int = 10) -> List[Dict]:
        """Get IPs with most anomalies"""
        query = {
            "aggs": {
                "top_ips": {
                    "terms": {
                        "field": "source_ip",
                        "size": limit,
                        "order": {"_count": "desc"}
                    },
                    "aggs": {
                        "avg_severity": {
                            "avg": {"field": "severity"}
                        }
                    }
                }
            },
            "size": 0
        }
        
        result = self.es.search(index=self.index_name, body=query)
        return result['aggregations']['top_ips']['buckets']
```

---

## 🌐 PHASE 7: API Backend with FastAPI (Day 13-14)

### Step 7.1: Create Main API

**File:** `backend/api/main.py`

```python
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import asyncio

app = FastAPI(title="AI Log Investigation API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import our modules
from backend.parsers.log_parser import LogParser
from backend.ml_engine.anomaly_detector import AnomalyDetector
from backend.storage.es_client import LogStorage
from backend.correlation.correlator import IncidentCorrelator

# Initialize components
log_parser = LogParser()
anomaly_detector = AnomalyDetector()
log_storage = LogStorage()
correlator = IncidentCorrelator()

# Pydantic models for API
class LogEntry(BaseModel):
    raw_log: str
    log_type: str  # 'syslog', 'csv', 'json'

class IncidentResponse(BaseModel):
    incident_id: str
    type: str
    severity: int
    description: str
    event_count: int

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "running", "service": "AI Log Investigation Framework"}

@app.post("/api/logs/ingest")
async def ingest_log(log: LogEntry):
    """
    Endpoint to manually ingest a single log
    
    Example:
    POST /api/logs/ingest
    {
        "raw_log": "Jan 10 10:21:44 server1 sshd[12345]: Failed password",
        "log_type": "syslog"
    }
    """
    try:
        # 1. Parse log
        parsed_log = log_parser.parse_syslog(log.raw_log)
        if not parsed_log:
            raise HTTPException(status_code=400, detail="Invalid log format")
        
        # 2. Extract features and detect anomaly
        # (Simplified - in reality use feature_extractor)
        parsed_log['is_anomaly'] = False
        parsed_log['anomaly_score'] = 0.0
        
        # 3. Store in Elasticsearch
        log_storage.store_log(parsed_log)
        
        # 4. Correlate events
        correlator.add_event(parsed_log)
        
        return {"status": "success", "parsed_log": parsed_log}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logs/anomalies", response_model=List[dict])
async def get_anomalies(hours: int = 24):
    """Get all anomalies from last N hours"""
    return log_storage.get_anomalies(hours)

@app.get("/api/incidents", response_model=List[IncidentResponse])
async def get_incidents():
    """Get all open incidents"""
    return correlator.get_open_incidents()

@app.get("/api/stats/top-attackers")
async def get_top_attackers(limit: int = 10):
    """Get top suspicious IPs"""
    return log_storage.get_top_attackers(limit)

@app.post("/api/logs/upload")
async def upload_log_file(file: UploadFile):
    """
    Upload a log file for batch processing
    """
    content = await file.read()
    lines = content.decode('utf-8').split('\n')
    
    results = []
    for line in lines:
        if line.strip():
            parsed = log_parser.parse_syslog(line)
            if parsed:
                log_storage.store_log(parsed)
                results.append(parsed)
    
    return {
        "status": "success",
        "processed": len(results),
        "total_lines": len(lines)
    }

# WebSocket for real-time updates
from fastapi import WebSocket

@app.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket):
    """
    WebSocket endpoint for real-time alert streaming
    """
    await websocket.accept()
    try:
        while True:
            # Check for new incidents
            incidents = correlator.get_open_incidents()
            if incidents:
                await websocket.send_json({"incidents": incidents})
            await asyncio.sleep(2)  # Check every 2 seconds
    except Exception as e:
        print(f"WebSocket error: {e}")
```

---

## 🎨 PHASE 8: Frontend Dashboard (Day 15-17)

### Step 8.1: Create React App

```bash
cd frontend
npx create-react-app dashboard --template typescript
cd dashboard
npm install recharts axios @mui/material @emotion/react @emotion/styled
```

### Step 8.2: Create Dashboard Component

**File:** `frontend/dashboard/src/Dashboard.tsx`

```typescript
import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, LineChart, Line, PieChart, Pie,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend
} from 'recharts';
import { Card, CardContent, Typography, Grid } from '@mui/material';

interface Incident {
  incident_id: string;
  type: string;
  severity: number;
  description: string;
  source_ip: string;
}

interface Stats {
  total_logs: number;
  total_anomalies: number;
  open_incidents: number;
}

const Dashboard: React.FC = () => {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [stats, setStats] = useState<Stats>({
    total_logs: 0,
    total_anomalies: 0,
    open_incidents: 0
  });

  useEffect(() => {
    // Fetch data every 5 seconds
    const fetchData = async () => {
      try {
        const incidentsRes = await axios.get('http://localhost:8000/api/incidents');
        setIncidents(incidentsRes.data);
        
        const anomaliesRes = await axios.get('http://localhost:8000/api/logs/anomalies');
        setStats(prev => ({
          ...prev,
          total_anomalies: anomaliesRes.data.length,
          open_incidents: incidentsRes.data.length
        }));
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '20px', backgroundColor: '#1a1a1a', minHeight: '100vh' }}>
      <Typography variant="h3" style={{ color: '#fff', marginBottom: '20px' }}>
        🔐 AI Log Investigation Dashboard
      </Typography>

      {/* Stats Cards */}
      <Grid container spacing={3}>
        <Grid item xs={4}>
          <Card style={{ backgroundColor: '#2a2a2a' }}>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Logs Processed
              </Typography>
              <Typography variant="h4" style={{ color: '#4caf50' }}>
                {stats.total_logs.toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={4}>
          <Card style={{ backgroundColor: '#2a2a2a' }}>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Anomalies Detected
              </Typography>
              <Typography variant="h4" style={{ color: '#ff9800' }}>
                {stats.total_anomalies}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={4}>
          <Card style={{ backgroundColor: '#2a2a2a' }}>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Open Incidents
              </Typography>
              <Typography variant="h4" style={{ color: '#f44336' }}>
                {stats.open_incidents}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Incidents Table */}
      <Card style={{ marginTop: '20px', backgroundColor: '#2a2a2a' }}>
        <CardContent>
          <Typography variant="h5" style={{ color: '#fff', marginBottom: '10px' }}>
            🚨 Active Incidents
          </Typography>
          <table style={{ width: '100%', color: '#fff' }}>
            <thead>
              <tr>
                <th>ID</th>
                <th>Type</th>
                <th>Source IP</th>
                <th>Severity</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {incidents.map(incident => (
                <tr key={incident.incident_id}>
                  <td>{incident.incident_id}</td>
                  <td>{incident.type}</td>
                  <td>{incident.source_ip}</td>
                  <td>
                    <span style={{
                      color: incident.severity >= 8 ? '#f44336' : '#ff9800'
                    }}>
                      {incident.severity}/10
                    </span>
                  </td>
                  <td>{incident.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;
```

---

## 🧪 PHASE 9: Testing & Sample Data (Day 18-19)

### Step 9.1: Create Sample Logs

**File:** `sample_logs/auth_logs.txt`

```
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
```

### Step 9.2: Create Test Script

**File:** `tests/test_integration.py`

```python
import pytest
import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser
from backend.ml_engine.feature_extractor import FeatureExtractor
from backend.correlation.correlator import IncidentCorrelator

def test_log_parsing():
    """Test if parser correctly extracts fields"""
    parser = LogParser()
    raw_log = "Jan 10 10:21:44 server1 sshd[12345]: Failed password for root"
    
    result = parser.parse_syslog(raw_log)
    
    assert result is not None
    assert result['event_type'] == 'LOGIN_FAILURE'
    assert result['user'] == 'root'
    assert result['service'] == 'sshd'

def test_feature_extraction():
    """Test feature engineering"""
    extractor = FeatureExtractor()
    log_data = {
        'timestamp': '2026-01-10T03:00:00Z',
        'event_type': 'LOGIN_FAILURE',
        'severity': 7
    }
    
    features = extractor.extract_features(log_data)
    
    assert features['hour'] == 3
    assert features['is_night'] == 1
    assert features['is_failure'] == 1

def test_brute_force_detection():
    """Test if correlator detects brute force"""
    correlator = IncidentCorrelator()
    
    # Simulate 15 failed logins
    for i in range(15):
        log = {
            'timestamp': f'2026-01-10T10:2{i:01d}:00Z',
            'source_ip': '192.168.1.10',
            'event_type': 'LOGIN_FAILURE'
        }
        correlator.add_event(log)
    
    # Add successful login
    success_log = {
        'timestamp': '2026-01-10T10:25:00Z',
        'source_ip': '192.168.1.10',
        'event_type': 'LOGIN_SUCCESS'
    }
    correlator.add_event(success_log)
    
    incidents = correlator.get_open_incidents()
    assert len(incidents) > 0
    assert incidents[0]['type'] == 'BRUTE_FORCE_ATTACK'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
```

---

## 🚀 PHASE 10: Running the Complete System (Day 20)

### Step 10.1: Start All Services

```bash
# Terminal 1: Start Kafka and Elasticsearch
docker-compose up -d

# Terminal 2: Start FastAPI backend
cd backend
uvicorn api.main:app --reload --port 8000

# Terminal 3: Start React frontend
cd frontend/dashboard
npm start

# Terminal 4: Start log ingestion script
python scripts/ingest_sample_logs.py
```

### Step 10.2: Create Ingestion Script

**File:** `scripts/ingest_sample_logs.py`

```python
import time
import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser
from backend.ingestion.kafka_producer import LogProducer

def main():
    parser = LogParser()
    producer = LogProducer()
    
    # Read sample logs
    with open('../sample_logs/auth_logs.txt', 'r') as f:
        logs = f.readlines()
    
    print("Starting log ingestion...")
    for raw_log in logs:
        if raw_log.strip():
            # Parse log
            parsed = parser.parse_syslog(raw_log)
            if parsed:
                # Send to Kafka
                producer.send_log('auth_logs', parsed)
                print(f"✓ Sent: {parsed['event_type']}")
                time.sleep(1)  # Simulate real-time
    
    print("Ingestion complete!")

if __name__ == '__main__':
    main()
```

---

## 📊 Summary: What You've Built

Congratulations! You've built an enterprise-grade SIEM system with:

1. **Real-time log ingestion** (Kafka) ✅
2. **Intelligent parsing** (converts messy logs to clean data) ✅
3. **AI anomaly detection** (finds suspicious patterns) ✅
4. **Event correlation** (connects the dots between attacks) ✅
5. **Fast storage** (Elasticsearch for millions of logs) ✅
6. **Beautiful dashboard** (React UI) ✅
7. **REST API** (for integration) ✅

---

## 🎯 Next Steps

1. **Train the ML model** with real historical data
2. **Add more correlation rules** (data exfiltration, lateral movement)
3. **Implement alerting** (email, Slack notifications)
4. **Add authentication** to dashboard
5. **Deploy to cloud** (AWS, Azure, GCP)

---

## 📚 Learning Resources

- Kafka: https://kafka.apache.org/documentation/
- Elasticsearch: https://www.elastic.co/guide/
- FastAPI: https://fastapi.tiangolo.com/
- Anomaly Detection: https://scikit-learn.org/stable/modules/outlier_detection.html

---

**Remember:** Cybersecurity is about layers. Each component adds a layer of defense!

