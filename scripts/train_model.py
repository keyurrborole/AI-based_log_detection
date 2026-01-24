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
