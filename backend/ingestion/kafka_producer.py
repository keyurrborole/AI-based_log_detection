from confluent_kafka import Producer
import json
from typing import Dict
from backend.utils.logger import logger
from backend.utils.config import settings

class LogProducer:
    """Send logs to Kafka"""
    
    def __init__(self):
        self.config = {
            'bootstrap.servers': settings.kafka_bootstrap_servers,
            'client.id': 'log-producer'
        }
        self.producer = Producer(self.config)
        logger.info(f"Kafka Producer ready: {settings.kafka_bootstrap_servers}")
    
    def send_log(self, topic: str, log_data: Dict):
        """Send log to Kafka topic"""
        try:
            message = json.dumps(log_data)
            self.producer.produce(
                topic=topic,
                value=message.encode('utf-8'),
                callback=self._delivery_report
            )
            self.producer.flush()
        except Exception as e:
            logger.error(f"Send failed: {e}")
    
    def _delivery_report(self, err, msg):
        if err:
            logger.error(f"Delivery failed: {err}")
        else:
            logger.debug(f"Delivered to {msg.topic()}")
