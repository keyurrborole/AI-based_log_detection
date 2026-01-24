from confluent_kafka import Consumer, KafkaError
import json
from typing import Callable
from backend.utils.logger import logger
from backend.utils.config import settings

class LogConsumer:
    """Receive logs from Kafka"""
    
    def __init__(self, topics: list, group_id: str = 'log-consumer-group'):
        self.config = {
            'bootstrap.servers': settings.kafka_bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest'
        }
        self.consumer = Consumer(self.config)
        self.consumer.subscribe(topics)
        logger.info(f"Kafka Consumer subscribed: {topics}")
    
    def consume_logs(self, callback: Callable):
        """Continuously consume logs"""
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                
                if msg is None:
                    continue
                
                if msg.error():
                    if msg.error().code() != KafkaError._PARTITION_EOF:
                        logger.error(f"Error: {msg.error()}")
                    continue
                
                log_data = json.loads(msg.value().decode('utf-8'))
                callback(log_data)
                
        except KeyboardInterrupt:
            logger.info("Consumer stopped")
        finally:
            self.consumer.close()
