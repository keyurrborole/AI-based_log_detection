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
