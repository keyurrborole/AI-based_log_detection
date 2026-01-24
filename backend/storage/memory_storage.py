from typing import Dict, List
from datetime import datetime
from backend.utils.logger import logger

class MemoryStorage:
    """In-memory log storage (no Elasticsearch needed)"""
    
    def __init__(self):
        self.logs = []
        logger.info("Memory storage initialized (no Elasticsearch)")
    
    def store_log(self, log_data: Dict):
        """Store log in memory"""
        self.logs.append(log_data)
    
    def search_logs(self, query: Dict, size: int = 100) -> List[Dict]:
        """Search logs with simple filtering"""
        results = self.logs
        
        # Simple term matching
        if "term" in query:
            for field, value in query["term"].items():
                results = [log for log in results if log.get(field) == value]
        
        return results[:size]
    
    def get_failed_logins(self) -> List[Dict]:
        """Get all failed logins"""
        return [log for log in self.logs if log.get('event_type') == 'LOGIN_FAILURE']
    
    def get_anomalies(self) -> List[Dict]:
        """Get all anomalies"""
        return [log for log in self.logs if log.get('is_anomaly') == True]
    
    def get_stats(self) -> Dict:
        """Get basic statistics"""
        return {
            "total_logs": len(self.logs),
            "failed_logins": len(self.get_failed_logins()),
            "anomalies": len(self.get_anomalies())
        }
    
    def clear(self):
        """Clear all logs"""
        self.logs = []
        logger.info("Storage cleared")
