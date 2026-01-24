from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict
from backend.utils.logger import logger

class IncidentCorrelator:
    """Correlate events into incidents"""
    
    def __init__(self):
        self.event_buffer = defaultdict(list)
        self.incidents = []
    
    def add_event(self, log_data: dict):
        """Add event and check for patterns"""
        source_key = log_data.get('source_ip', 'unknown')
        self.event_buffer[source_key].append(log_data)
        
        # Check patterns
        self._check_brute_force(source_key)
        self._check_privilege_escalation(source_key)
        
        # Cleanup old events
        self._cleanup_old_events()
    
    def _check_brute_force(self, source_ip: str):
        """Detect brute force: Multiple failures + success"""
        events = self.event_buffer[source_ip]
        
        # Get recent events (last 5 minutes)
        now = datetime.utcnow().replace(tzinfo=None)
        recent = [
            e for e in events
            if (now - datetime.fromisoformat(e['timestamp'].replace('Z', '')))
            < timedelta(minutes=5)
        ]
        
        # Count failures and successes
        failures = [e for e in recent if e['event_type'] == 'LOGIN_FAILURE']
        successes = [e for e in recent if e['event_type'] == 'LOGIN_SUCCESS']
        
        # Brute force detected!
        if len(failures) >= 5 and len(successes) >= 1:
            self._create_incident(
                incident_type='BRUTE_FORCE_ATTACK',
                source_ip=source_ip,
                events=recent,
                severity=9,
                description=f"{len(failures)} failed logins followed by successful login"
            )
    
    def _check_privilege_escalation(self, source_ip: str):
        """Detect privilege escalation after login"""
        events = self.event_buffer[source_ip]
        
        for i in range(len(events) - 1):
            if (events[i]['event_type'] == 'LOGIN_SUCCESS' and
                events[i+1]['event_type'] == 'PRIVILEGE_ESCALATION'):
                
                time_diff = (
                    datetime.fromisoformat(events[i+1]['timestamp'].replace('Z', '')) -
                    datetime.fromisoformat(events[i]['timestamp'].replace('Z', ''))
                )
                
                if time_diff < timedelta(minutes=2):
                    self._create_incident(
                        incident_type='PRIVILEGE_ESCALATION',
                        source_ip=source_ip,
                        events=[events[i], events[i+1]],
                        severity=8,
                        description="Suspicious privilege escalation after login"
                    )
    
    def _create_incident(self, incident_type: str, source_ip: str,
                        events: List[dict], severity: int, description: str):
        """Create incident record"""
        incident = {
            'incident_id': f"INC-{datetime.utcnow().timestamp()}",
            'type': incident_type,
            'source_ip': source_ip,
            'severity': severity,
            'description': description,
            'event_count': len(events),
            'first_seen': events[0]['timestamp'],
            'last_seen': events[-1]['timestamp'],
            'events': events,
            'status': 'OPEN'
        }
        
        self.incidents.append(incident)
        logger.warning(f"🚨 INCIDENT: {incident_type} from {source_ip}")
    
    def _cleanup_old_events(self):
        """Remove events older than 1 hour"""
        cutoff = datetime.utcnow().replace(tzinfo=None) - timedelta(hours=1)
        
        for source_ip in list(self.event_buffer.keys()):
            self.event_buffer[source_ip] = [
                e for e in self.event_buffer[source_ip]
                if datetime.fromisoformat(e['timestamp'].replace('Z', '')) > cutoff
            ]
    
    def get_open_incidents(self) -> List[dict]:
        """Return all open incidents"""
        return [i for i in self.incidents if i['status'] == 'OPEN']
