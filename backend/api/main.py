from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser
from backend.storage.memory_storage import MemoryStorage as LogStorage
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
