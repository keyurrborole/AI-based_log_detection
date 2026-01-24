from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from typing import Dict
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
