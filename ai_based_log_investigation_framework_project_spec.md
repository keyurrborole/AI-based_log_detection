# AI-Based Log Investigation Framework (Enterprise-Scale SIEM)

> **Domain:** Cyber Forensics  \
> **Difficulty:** Easy → Medium  \
> **Goal:** Build an enterprise-grade, real-time, AI-powered log investigation system for cyber incident response.

---

## 1. Problem Overview

Modern systems generate massive volumes of logs (servers, endpoints, applications, IoT). Manual analysis is slow, error-prone, and unsuitable for incident response. This project builds a **SIEM-like framework** that ingests logs in real time, normalizes them, applies **AI/ML for anomaly detection or classification**, correlates events, and visualizes security insights for investigators.

---

## 2. High-Level Architecture

```
┌────────────┐     ┌──────────────┐     ┌──────────────┐
│ Log Sources│ --> │ Ingestion     │ --> │ Parsing &    │
│ (Syslog,   │     │ (Kafka / API) │     │ Normalization│
│ CSV, JSON) │     └──────────────┘     └──────────────┘
└────────────┘                                   │
                                                  v
                                         ┌────────────────┐
                                         │ Storage Layer  │
                                         │ (Elastic / DB) │
                                         └────────────────┘
                                                  │
                                                  v
                                      ┌─────────────────────┐
                                      │ AI / ML Engine      │
                                      │ (Anomaly Detection) │
                                      └─────────────────────┘
                                                  │
                                                  v
                                     ┌──────────────────────┐
                                     │ Correlation Engine   │
                                     │ (Rules + Context)   │
                                     └──────────────────────┘
                                                  │
                                                  v
                                      ┌─────────────────────┐
                                      │ Visualization &     │
                                      │ Alert Dashboard     │
                                      └─────────────────────┘
```

---

## 3. Core Modules (What to Build)

### 3.1 Log Ingestion Module

**Purpose:** Collect logs from multiple sources in real time.

**Supported Formats:**
- Syslogs (Linux auth.log, SSH logs)
- CSV (firewall, proxy logs)
- JSON (cloud, app, IDS logs)

**Tech Suggestions:**
- Apache Kafka (mandatory for enterprise-scale streaming)
- Logstash / Fluentd (optional)
- REST API for manual upload

**Output:** Raw logs forwarded to parser

---

### 3.2 Log Parsing & Normalization

**Purpose:** Convert heterogeneous logs into a unified schema.

**Normalized Fields (Example):**
```json
{
  "timestamp": "2026-01-10T10:21:44Z",
  "source_ip": "192.168.1.10",
  "destination_ip": "10.0.0.5",
  "user": "root",
  "event_type": "LOGIN_FAILURE",
  "status": "FAILED",
  "raw_log": "..."
}
```

**Key Tasks:**
- Timestamp standardization (UTC)
- Field extraction using regex / JSON parsing
- Tagging event types

---

### 3.3 AI / ML Engine (Core Intelligence)

#### Option A: Anomaly Detection (Recommended)

**Why:** Logs are usually unlabeled in forensics.

**Models:**
- Isolation Forest
- One-Class SVM
- Autoencoders (advanced)

**Features Used:**
- Failed login count
- Request frequency per IP
- Time-of-day access
- Unique destination count

**Output:**
```json
{
  "event_id": "abc123",
  "anomaly_score": 0.92,
  "label": "SUSPICIOUS"
}
```

#### Explainability (XAI)
- Feature importance (why flagged?)
- Threshold-based reasoning

---

### 3.4 Correlation Logic

**Purpose:** Connect isolated suspicious events into incidents.

**Correlation Rules Examples:**
- Same IP + multiple failed logins within 5 minutes
- Login failure → success → privilege escalation
- Same user accessing from different geolocations

**Implementation:**
- Rule engine (Python)
- Sliding time windows
- Graph-based correlation (advanced)

**Output:** Incident timelines

---

### 3.5 Storage Layer

**Requirements:**
- Tamper-proof storage (forensics-ready)
- Fast querying

**Tech Options:**
- Elasticsearch (recommended)
- PostgreSQL / MongoDB

**Security:**
- Hashing logs for integrity
- Role-based access control

---

### 3.6 Visualization Dashboard

**Purpose:** Investigator-friendly UI

**Dashboard Features:**
- Real-time alerts
- Incident timelines
- Top suspicious IPs/users
- Anomaly heatmaps

**Tech Stack:**
- Backend: FastAPI / Flask
- Frontend: React + Chart.js
- Optional: Kibana-like UI

---

## 4. Realistic Use Cases (Must Demonstrate)

### Use Case 1: Brute Force Attack
- 100+ failed SSH logins
- Same IP
- Detected by anomaly model
- Correlated into one incident

### Use Case 2: Insider Threat
- Access at unusual time
- Multiple sensitive file reads

### Use Case 3: Malware Beaconing
- Periodic outbound traffic
- Same destination

---

## 5. Demo Requirements

**Working Demo Must Include:**
- Sample logs (auth.log, firewall.csv)
- Real-time ingestion via Kafka
- ML anomaly detection output
- Alert visible on dashboard

---

## 6. Enterprise SIEM Expectations (IMPORTANT)

✔ Real-time streaming (Kafka mandatory)  \
✔ Scalable ingestion  \
✔ Correlation across sources  \
✔ Explainable AI decisions  \
✔ Incident-response-ready UI

---

## 7. Project Milestones

### Phase 1
- Log ingestion + parsing

### Phase 2
- Storage + anomaly detection

### Phase 3
- Correlation engine + dashboard

### Phase 4
- Reporting + benchmarking

---

## 8. Future Enhancements

- SOAR integration
- LLM-based log querying
- Cloud-native deployment
- Threat intelligence feeds

---

## 9. Recommended Tech Stack (Complete)

### Backend
- **Language:** Python 3.10+
- **Framework:** FastAPI (modern, async, production-ready)
- **Message Queue:** Apache Kafka + Confluent Kafka Python Client
- **ML Libraries:** scikit-learn, pandas, numpy
- **Storage:** Elasticsearch 8.x + PostgreSQL (metadata)

### Frontend
- **Framework:** React 18+ with TypeScript
- **UI Library:** Material-UI (MUI) or Ant Design
- **Charts:** Recharts / Chart.js / Apache ECharts
- **Real-time:** WebSocket (Socket.io or native)

### Infrastructure
- **Containerization:** Docker + Docker Compose
- **Orchestration:** Kubernetes (optional for production)
- **Monitoring:** Prometheus + Grafana
- **Logging:** ELK Stack integration

### Development Tools
- **Version Control:** Git
- **Testing:** pytest, unittest
- **Linting:** black, flake8, mypy
- **Documentation:** Swagger UI (auto-generated by FastAPI)

---

## 10. Final Deliverables Checklist

- [ ] Real-time ingestion pipeline (Kafka)
- [ ] Normalized log schema
- [ ] AI anomaly detection model
- [ ] Correlation logic
- [ ] Visualization dashboard
- [ ] Sample incident demo
- [ ] Docker containerization
- [ ] API documentation
- [ ] Unit tests (>70% coverage)
- [ ] Performance benchmarks

---

> **This README is designed to be fed directly to GitHub Copilot to scaffold the full project.**

