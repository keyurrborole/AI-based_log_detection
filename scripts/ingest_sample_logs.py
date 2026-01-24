import sys
sys.path.append('..')

from backend.parsers.log_parser import LogParser
from backend.storage.memory_storage import MemoryStorage as LogStorage
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
