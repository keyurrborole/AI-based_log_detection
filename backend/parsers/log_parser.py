import re
from datetime import datetime
from typing import Dict, Optional
from backend.utils.logger import logger

class LogParser:
    """Parse various log formats into normalized structure"""
    
    def __init__(self):
        # Syslog: Jan 10 10:21:44 server1 sshd[12345]: message
        self.syslog_pattern = re.compile(
            r'(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+)\s+'
            r'(?P<host>\S+)\s+'
            r'(?P<service>\w+)\[(?P<pid>\d+)\]:\s+'
            r'(?P<message>.*)'
        )
    
    def parse_syslog(self, raw_log: str) -> Optional[Dict]:
        """Parse syslog format"""
        match = self.syslog_pattern.match(raw_log)
        if not match:
            logger.warning(f"Failed to parse: {raw_log[:50]}")
            return None
        
        data = match.groupdict()
        
        normalized = {
            "timestamp": self._normalize_timestamp(data['timestamp']),
            "host": data['host'],
            "service": data['service'],
            "event_type": self._classify_event(data['message']),
            "severity": self._calculate_severity(data['message']),
            "raw_log": raw_log
        }
        
        # Extract optional fields
        user = self._extract_user(data['message'])
        if user:
            normalized['user'] = user
        
        ip = self._extract_ip(data['message'])
        if ip:
            normalized['source_ip'] = ip
        
        return normalized
    
    def _normalize_timestamp(self, ts: str) -> str:
        """Convert to ISO format"""
        try:
            dt = datetime.strptime(f"2026 {ts}", "%Y %b %d %H:%M:%S")
            return dt.isoformat() + "Z"
        except:
            return datetime.utcnow().isoformat() + "Z"
    
    def _classify_event(self, message: str) -> str:
        """Classify event type"""
        msg = message.lower()
        
        if "failed password" in msg or "authentication failure" in msg:
            return "LOGIN_FAILURE"
        elif "accepted password" in msg or "session opened" in msg:
            return "LOGIN_SUCCESS"
        elif "sudo" in msg or "su:" in msg:
            return "PRIVILEGE_ESCALATION"
        elif "connection closed" in msg:
            return "LOGOUT"
        return "UNKNOWN"
    
    def _calculate_severity(self, message: str) -> int:
        """Severity 1-10"""
        msg = message.lower()
        
        if "failed" in msg or "error" in msg:
            return 7
        elif "sudo" in msg:
            return 8
        elif "accepted" in msg:
            return 3
        return 5
    
    def _extract_user(self, message: str) -> Optional[str]:
        """Extract username"""
        patterns = [r'for (\w+)', r'user=(\w+)', r'USER=(\w+)']
        for pattern in patterns:
            match = re.search(pattern, message)
            if match:
                return match.group(1)
        return None
    
    def _extract_ip(self, message: str) -> Optional[str]:
        """Extract IP address"""
        match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', message)
        return match.group(0) if match else None
