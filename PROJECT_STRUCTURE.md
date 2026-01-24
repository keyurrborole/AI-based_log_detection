# 🗂️ Project File Structure & Templates
## Complete Directory Layout with File Purposes

---

## 📁 Complete Directory Structure

```
ai_log_framework/
│
├── 📄 README.md                          # Project overview
├── 📄 requirements.txt                   # Python dependencies
├── 📄 docker-compose.yml                 # Docker services config
├── 📄 .gitignore                         # Git ignore patterns
├── 📄 .env                               # Environment variables
│
├── 📁 backend/                           # Python backend code
│   ├── 📄 __init__.py
│   │
│   ├── 📁 api/                          # FastAPI application
│   │   ├── 📄 __init__.py
│   │   ├── 📄 main.py                   # Main API entry point
│   │   ├── 📄 models.py                 # Pydantic models
│   │   └── 📄 routes.py                 # API route handlers
│   │
│   ├── 📁 parsers/                      # Log parsing modules
│   │   ├── 📄 __init__.py
│   │   ├── 📄 log_parser.py             # Main parser class
│   │   ├── 📄 syslog_parser.py          # Syslog specific
│   │   ├── 📄 csv_parser.py             # CSV logs
│   │   └── 📄 json_parser.py            # JSON logs
│   │
│   ├── 📁 ingestion/                    # Kafka integration
│   │   ├── 📄 __init__.py
│   │   ├── 📄 kafka_producer.py         # Send to Kafka
│   │   └── 📄 kafka_consumer.py         # Receive from Kafka
│   │
│   ├── 📁 ml_engine/                    # AI/ML components
│   │   ├── 📄 __init__.py
│   │   ├── 📄 feature_extractor.py      # Feature engineering
│   │   ├── 📄 anomaly_detector.py       # Isolation Forest model
│   │   ├── 📄 model_trainer.py          # Training scripts
│   │   └── 📄 explainer.py              # XAI (explainability)
│   │
│   ├── 📁 correlation/                  # Event correlation
│   │   ├── 📄 __init__.py
│   │   ├── 📄 correlator.py             # Main correlation engine
│   │   ├── 📄 rules.py                  # Correlation rules
│   │   └── 📄 incident_manager.py       # Incident lifecycle
│   │
│   ├── 📁 storage/                      # Database interactions
│   │   ├── 📄 __init__.py
│   │   ├── 📄 es_client.py              # Elasticsearch client
│   │   └── 📄 schemas.py                # Index schemas
│   │
│   └── 📁 utils/                        # Utility functions
│       ├── 📄 __init__.py
│       ├── 📄 config.py                 # Configuration
│       ├── 📄 logger.py                 # Logging setup
│       └── 📄 helpers.py                # Helper functions
│
├── 📁 frontend/                          # React dashboard
│   └── 📁 dashboard/
│       ├── 📄 package.json
│       ├── 📄 tsconfig.json
│       │
│       ├── 📁 public/
│       │   └── 📄 index.html
│       │
│       └── 📁 src/
│           ├── 📄 App.tsx               # Main app component
│           ├── 📄 index.tsx             # Entry point
│           │
│           ├── 📁 components/           # React components
│           │   ├── 📄 Dashboard.tsx     # Main dashboard
│           │   ├── 📄 IncidentTable.tsx # Incidents view
│           │   ├── 📄 StatsCards.tsx    # Statistics
│           │   ├── 📄 Charts.tsx        # Chart components
│           │   └── 📄 AlertPanel.tsx    # Real-time alerts
│           │
│           ├── 📁 services/             # API calls
│           │   └── 📄 api.ts            # API client
│           │
│           ├── 📁 types/                # TypeScript types
│           │   └── 📄 index.ts
│           │
│           └── 📁 styles/               # CSS files
│               └── 📄 App.css
│
├── 📁 tests/                             # Test files
│   ├── 📄 __init__.py
│   ├── 📄 test_parser.py                # Parser tests
│   ├── 📄 test_ml_engine.py             # ML tests
│   ├── 📄 test_correlation.py           # Correlation tests
│   ├── 📄 test_api.py                   # API tests
│   └── 📄 test_integration.py           # Integration tests
│
├── 📁 scripts/                           # Utility scripts
│   ├── 📄 ingest_sample_logs.py         # Load sample data
│   ├── 📄 train_model.py                # Train ML model
│   ├── 📄 generate_sample_data.py       # Create test logs
│   └── 📄 demo.py                       # Demo scenario
│
├── 📁 sample_logs/                       # Test data
│   ├── 📄 auth_logs.txt                 # SSH logs
│   ├── 📄 firewall_logs.csv             # Firewall logs
│   ├── 📄 application_logs.json         # App logs
│   └── 📄 attack_scenarios.txt          # Attack simulations
│
├── 📁 ml_models/                         # Saved models
│   ├── 📄 isolation_forest.pkl          # Trained model
│   └── 📄 scaler.pkl                    # Feature scaler
│
├── 📁 docs/                              # Documentation
│   ├── 📄 API.md                        # API documentation
│   ├── 📄 ARCHITECTURE.md               # System architecture
│   ├── 📄 DEPLOYMENT.md                 # Deployment guide
│   └── 📄 USER_GUIDE.md                 # User manual
│
└── 📁 kafka/                             # Kafka configs
    └── 📄 topics.txt                     # Topic definitions
```

---

## 📄 Essential File Templates

### 1. requirements.txt

```txt
# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6

# Message Queue
confluent-kafka==2.3.0

# Database
elasticsearch==8.11.1
redis==5.0.1

# Machine Learning
scikit-learn==1.4.0
pandas==2.2.0
numpy==1.26.3
joblib==1.3.2

# Utilities
python-dotenv==1.0.0
aiofiles==23.2.1
python-dateutil==2.8.2

# Testing
pytest==7.4.4
pytest-asyncio==0.21.1
httpx==0.26.0
pytest-cov==4.1.0

# Monitoring
prometheus-client==0.19.0

# Security
cryptography==42.0.0
```

---

### 2. docker-compose.yml

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
    networks:
      - log_network

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
      KAFKA_LOG_RETENTION_HOURS: 168
    networks:
      - log_network

  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.11.1
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
      - "ES_JAVA_OPTS=-Xms1g -Xmx1g"
    ports:
      - "9200:9200"
      - "9300:9300"
    volumes:
      - es_data:/usr/share/elasticsearch/data
    networks:
      - log_network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:9200 || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    networks:
      - log_network

volumes:
  es_data:
    driver: local
  redis_data:
    driver: local

networks:
  log_network:
    driver: bridge
```

---

### 3. .env (Environment Variables)

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_AUTH_LOGS_TOPIC=auth_logs
KAFKA_FIREWALL_LOGS_TOPIC=firewall_logs
KAFKA_APP_LOGS_TOPIC=app_logs

# Elasticsearch Configuration
ES_HOST=localhost
ES_PORT=9200
ES_INDEX_NAME=security-logs

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379

# ML Configuration
ML_MODEL_PATH=./ml_models/isolation_forest.pkl
ML_CONTAMINATION=0.1
ML_TRAIN_INTERVAL_HOURS=24

# Logging
LOG_LEVEL=INFO
LOG_FILE=./logs/app.log

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 4. .gitignore

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
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
ml_models/*.pkl
logs/*.log
sample_logs/large_*.txt
.env.local

# Testing
.pytest_cache/
.coverage
htmlcov/

# Frontend
frontend/dashboard/node_modules/
frontend/dashboard/build/
frontend/dashboard/.env.local

# Docker
docker-compose.override.yml

# Data
*.csv
*.log
!sample_logs/*.csv
!sample_logs/*.log
```

---

### 5. backend/utils/config.py

```python
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application configuration"""
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 4
    
    # Kafka
    kafka_bootstrap_servers: str = "localhost:9092"
    kafka_auth_logs_topic: str = "auth_logs"
    kafka_firewall_logs_topic: str = "firewall_logs"
    
    # Elasticsearch
    es_host: str = "localhost"
    es_port: int = 9200
    es_index_name: str = "security-logs"
    
    # ML
    ml_model_path: str = "./ml_models/isolation_forest.pkl"
    ml_contamination: float = 0.1
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings()
```

---

### 6. backend/utils/logger.py

```python
import logging
import sys
from pathlib import Path

def setup_logger(name: str, log_file: str = None, level: str = "INFO"):
    """Setup application logger"""
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# Create default logger
logger = setup_logger("ai_log_framework")
```

---

### 7. README.md Template

```markdown
# AI-Based Log Investigation Framework

> Enterprise-grade SIEM system powered by AI for real-time threat detection

## 🚀 Features

- ✅ Real-time log ingestion with Apache Kafka
- 🤖 AI-powered anomaly detection (Isolation Forest)
- 🔗 Intelligent event correlation
- 📊 Interactive dashboard with real-time alerts
- 🔍 Fast log search with Elasticsearch
- 📈 Advanced analytics and reporting

## 🏗️ Architecture

[Insert architecture diagram here]

## 📋 Prerequisites

- Python 3.10+
- Docker Desktop
- Node.js 18+
- 8GB RAM minimum

## 🔧 Installation

### 1. Clone Repository
\`\`\`bash
git clone https://github.com/yourusername/ai-log-framework.git
cd ai-log-framework
\`\`\`

### 2. Setup Backend
\`\`\`bash
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
\`\`\`

### 3. Start Services
\`\`\`bash
docker-compose up -d
\`\`\`

### 4. Run Application
\`\`\`bash
# Terminal 1: Backend
cd backend
uvicorn api.main:app --reload

# Terminal 2: Frontend
cd frontend/dashboard
npm install
npm start
\`\`\`

## 📖 Usage

### Ingest Sample Logs
\`\`\`bash
python scripts/ingest_sample_logs.py
\`\`\`

### Access Dashboard
Open http://localhost:3000

### API Documentation
Open http://localhost:8000/docs

## 🧪 Testing

\`\`\`bash
pytest tests/ -v --cov
\`\`\`

## 📊 Demo Scenarios

1. **Brute Force Attack Detection**
2. **Privilege Escalation**
3. **Insider Threat**

## 🤝 Contributing

Pull requests are welcome! See CONTRIBUTING.md

## 📄 License

MIT License

## 👨‍💻 Author

Your Name - [your-email@example.com](mailto:your-email@example.com)

## 🙏 Acknowledgments

- scikit-learn for ML algorithms
- Apache Kafka for stream processing
- Elastic for search capabilities
```

---

### 8. scripts/ingest_sample_logs.py

```python
#!/usr/bin/env python3
"""
Sample log ingestion script
Reads logs from sample_logs/ and sends them to the system
"""

import sys
import time
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from backend.parsers.log_parser import LogParser
from backend.ingestion.kafka_producer import LogProducer
from backend.utils.logger import logger

def main():
    """Main ingestion function"""
    
    parser = LogParser()
    producer = LogProducer()
    
    # Sample logs directory
    sample_dir = Path(__file__).parent.parent / "sample_logs"
    auth_logs = sample_dir / "auth_logs.txt"
    
    if not auth_logs.exists():
        logger.error(f"Sample log file not found: {auth_logs}")
        return
    
    logger.info("Starting log ingestion...")
    
    with open(auth_logs, 'r') as f:
        for i, line in enumerate(f, 1):
            if line.strip():
                # Parse log
                parsed = parser.parse_syslog(line.strip())
                
                if parsed:
                    # Send to Kafka
                    producer.send_log('auth_logs', parsed)
                    logger.info(f"✓ Sent log #{i}: {parsed['event_type']}")
                    time.sleep(0.5)  # Simulate real-time
                else:
                    logger.warning(f"✗ Failed to parse log #{i}")
    
    logger.info("Ingestion complete!")

if __name__ == '__main__':
    main()
```

---

### 9. tests/conftest.py (Pytest Configuration)

```python
import pytest
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def sample_syslog():
    """Sample syslog entry"""
    return "Jan 10 10:21:44 server1 sshd[12345]: Failed password for root"

@pytest.fixture
def sample_parsed_log():
    """Sample parsed log"""
    return {
        'timestamp': '2026-01-10T10:21:44Z',
        'host': 'server1',
        'service': 'sshd',
        'event_type': 'LOGIN_FAILURE',
        'user': 'root',
        'severity': 7
    }

@pytest.fixture
def kafka_config():
    """Kafka test configuration"""
    return {
        'bootstrap.servers': 'localhost:9092',
        'client.id': 'test-client'
    }
```

---

## 🎯 File Creation Order

### Phase 1: Core Setup
1. Create directory structure
2. Create `.gitignore`
3. Create `requirements.txt`
4. Create `.env`
5. Create `docker-compose.yml`

### Phase 2: Utilities
1. `backend/utils/config.py`
2. `backend/utils/logger.py`
3. `backend/utils/helpers.py`

### Phase 3: Core Logic
1. `backend/parsers/log_parser.py`
2. `backend/ingestion/kafka_producer.py`
3. `backend/ingestion/kafka_consumer.py`
4. `backend/ml_engine/feature_extractor.py`
5. `backend/ml_engine/anomaly_detector.py`
6. `backend/correlation/correlator.py`
7. `backend/storage/es_client.py`

### Phase 4: API
1. `backend/api/models.py`
2. `backend/api/main.py`
3. `backend/api/routes.py`

### Phase 5: Frontend
1. `frontend/dashboard/package.json`
2. `frontend/dashboard/src/types/index.ts`
3. `frontend/dashboard/src/services/api.ts`
4. `frontend/dashboard/src/components/*.tsx`
5. `frontend/dashboard/src/App.tsx`

### Phase 6: Testing & Scripts
1. `tests/conftest.py`
2. `tests/test_*.py`
3. `scripts/*.py`
4. `sample_logs/*.txt`

---

## 📝 Notes

- **Always create `__init__.py`** in Python directories
- **Test as you build** - don't wait until the end
- **Commit frequently** to Git
- **Document as you go** - future you will thank you!

---

**Next Step:** Start creating these files following IMPLEMENTATION_GUIDE.md!

