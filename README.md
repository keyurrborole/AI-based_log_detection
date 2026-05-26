# AI-Based Log Investigation Framework

An AI-powered log investigation and threat detection system built to support cyber incident analysis using real-time log processing, machine learning, and event correlation.

## Overview

This project is a SIEM-style framework that collects logs from different sources, processes them in real time, detects suspicious activity using machine learning, and presents important alerts through a dashboard.

It was developed as a group project for the DSCI CSIC Competition 2026, organized by the Government of India.

The main goal of this project is to show how security teams can use automation, log analysis, and AI-based detection techniques to identify possible cyber threats more effectively.

## Key Features

- Real-time log ingestion from multiple sources
- AI-based anomaly detection using machine learning
- Event correlation to identify multi-step attacks
- Fast log storage and searching
- Dashboard for alerts and investigation
- Docker-based setup
- One-click project execution using `run.bat`
- Test suite for validating core functionality

## Tech Stack

### Backend

- Python
- FastAPI
- Apache Kafka
- Elasticsearch
- scikit-learn

### Frontend

- React
- TypeScript
- Material UI
- Recharts

### Infrastructure

- Docker
- Docker Compose
- Redis
- Prometheus

## Architecture

```text
Log Sources -> Kafka -> Parser -> AI Detection -> Correlation -> Dashboard
                            |
                      Elasticsearch
```

## What This Project Demonstrates

This project demonstrates how a security monitoring system can detect and investigate:

1. Brute force login attempts
2. Privilege escalation activity
3. Insider threat behavior
4. Suspicious outbound network activity
5. Malware-like beaconing patterns

## Learning Outcomes

Through this project, we explored:

- How SIEM systems work
- Real-time stream processing using Kafka
- Log parsing and normalization
- Machine learning-based anomaly detection
- Backend API development with FastAPI
- Dashboard development with React
- Elasticsearch-based log search
- Docker-based application setup
- Cybersecurity investigation workflows

## Prerequisites

Before running the project, make sure the following requirements:

- Python 3.10 or above
- Docker Desktop
- Node.js 18 or above
- Git
- At least 8 GB RAM

## How to Run the Project

This project includes a `run.bat` file to start the complete project easily on Windows.

### Method 1: Run using `run.bat`

1. Open the project folder:

```text
D:\projects\AI-based_log\project
```

2. Double-click:

```text
run.bat
```

3. Wait for all required services to start.

4. Open the dashboard in your browser using the URL shown in the terminal.

### Method 2: Run from Command Prompt

Open Command Prompt and run:

```bat
cd /d "D:\projects\AI-based_log\project"
run.bat
```

### Method 3: Run manually

If you do not want to use `run.bat`, you can start the services manually by following the setup instructions in the documentation files.

## Documentation

Start with these files in order:

1. `START_HERE.md`  
   Main navigation guide for the project.

2. `HOW_TO_PROCEED.md`  
   Explains the learning path and how to approach the project.

3. `ai_based_log_investigation_framework_project_spec.md`  
   Contains the complete project specification.

4. `IMPLEMENTATION_GUIDE.md`  
   Step-by-step implementation guide.

5. `PROJECT_STRUCTURE.md`  
   Explains the folder structure and file organization.

6. `CHECKLIST.md`  
   Helps track progress while building or reviewing the project.

## Project Timeline

Estimated duration: 20 days  
Recommended effort: 3 to 5 hours per day

Suggested structure:

- Week 1: Core setup and log pipeline
- Week 2: Detection, storage, and correlation
- Week 3: Dashboard, integration, and testing

For a detailed plan, refer to `QUICK_START_ROADMAP.md`.

## Folder Structure

The project includes folders for:

- Backend services
- Machine learning models
- Sample logs
- Scripts
- Tests
- Documentation

Refer to `PROJECT_STRUCTURE.md` for the complete structure.

## Project Value

This project is useful for:

- Cybersecurity portfolios
- College projects
- Competition submissions
- Learning SIEM concepts
- Understanding log analysis
- Practicing full-stack development
- Building practical machine learning experience

## License

This project is for educational and competition purposes only.

## Support

If you get stuck:

- Read `HOW_TO_PROCEED.md`
- Check the troubleshooting sections in the documentation
- Review the implementation guide step by step

## Last Updated

January 24, 2026
