from elasticsearch import Elasticsearch
from typing import Dict, List
from backend.utils.logger import logger
from backend.utils.config import settings

class LogStorage:
    """Elasticsearch operations"""
    
    def __init__(self):
        self.es = Elasticsearch([f'http://{settings.es_host}:{settings.es_port}'])
        self.index_name = settings.es_index_name
        self._create_index()
        logger.info(f"Elasticsearch ready: {settings.es_host}")
    
    def _create_index(self):
        """Create index with mappings"""
        if not self.es.indices.exists(index=self.index_name):
            mappings = {
                "mappings": {
                    "properties": {
                        "timestamp": {"type": "date"},
                        "host": {"type": "keyword"},
                        "service": {"type": "keyword"},
                        "event_type": {"type": "keyword"},
                        "user": {"type": "keyword"},
                        "source_ip": {"type": "ip"},
                        "severity": {"type": "integer"},
                        "is_anomaly": {"type": "boolean"},
                        "anomaly_score": {"type": "float"},
                        "raw_log": {"type": "text"}
                    }
                }
            }
            self.es.indices.create(index=self.index_name, body=mappings)
            logger.info(f"Created index: {self.index_name}")
    
    def store_log(self, log_data: Dict):
        """Store single log"""
        try:
            self.es.index(index=self.index_name, document=log_data)
        except Exception as e:
            logger.error(f"Store failed: {e}")
    
    def search_logs(self, query: Dict, size: int = 100) -> List[Dict]:
        """Search with query"""
        try:
            result = self.es.search(index=self.index_name, query=query, size=size)
            return [hit['_source'] for hit in result['hits']['hits']]
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def get_failed_logins(self) -> List[Dict]:
        """Get all failed logins"""
        query = {"term": {"event_type": "LOGIN_FAILURE"}}
        return self.search_logs(query)
    
    def get_anomalies(self) -> List[Dict]:
        """Get all anomalies"""
        query = {"term": {"is_anomaly": True}}
        return self.search_logs(query)
    
    def get_stats(self) -> Dict:
        """Get basic statistics"""
        try:
            total = self.es.count(index=self.index_name)['count']
            failed = len(self.get_failed_logins())
            anomalies = len(self.get_anomalies())
            
            return {
                "total_logs": total,
                "failed_logins": failed,
                "anomalies": anomalies
            }
        except:
            return {"total_logs": 0, "failed_logins": 0, "anomalies": 0}
