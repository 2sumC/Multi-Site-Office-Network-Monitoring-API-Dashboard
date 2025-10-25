from datetime import datetime
import random

class Device:
    """Internet Device"""
    
    DEVICE_TYPES = ['router', 'switch', 'firewall', 'access_point']
    
    def __init__(self, id, office_id, name, device_type, 
                 ip_address, status='online'):
        self.id = id
        self.office_id = office_id
        self.name = name
        self.device_type = device_type
        self.ip_address = ip_address
        self.status = status  # online, offline, warning
        self.last_seen = datetime.now()
    
    def get_metrics(self, simulate=True):
        """Device Metrics"""
        if simulate:
            # simulate data
            return {
                'cpu_usage': round(random.uniform(10, 90), 2),
                'memory_usage': round(random.uniform(20, 80), 2),
                'bandwidth_in': round(random.uniform(0.5, 10), 2),  # Mbps
                'bandwidth_out': round(random.uniform(0.3, 8), 2),
                'temperature': round(random.uniform(35, 65), 1),  # Celsius
                'uptime': random.randint(100000, 9999999),  # seconds
                'packet_loss': round(random.uniform(0, 2), 2),  # percentage
                'latency': round(random.uniform(1, 50), 2),  # ms
                'timestamp': datetime.now().isoformat()
            }
        else:
            # Real data
            pass
    
    def to_dict(self):
        return {
            'id': self.id,
            'office_id': self.office_id,
            'name': self.name,
            'type': self.device_type,
            'ip_address': self.ip_address,
            'status': self.status,
            'last_seen': self.last_seen.isoformat()
        }