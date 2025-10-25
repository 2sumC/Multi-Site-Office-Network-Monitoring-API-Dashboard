from datetime import datetime, timedelta
import json
import random
from collections import defaultdict

class AnalyticsService:
    
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        try:
            with open('data/seed_data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.offices = data.get('offices', [])
            self.devices = data.get('devices', [])
            
            print(f"✅ Loaded {len(self.offices)} offices and {len(self.devices)} devices")
            
        except FileNotFoundError:
            print("⚠️ seed_data.json not found, using empty data")
            self.offices = []
            self.devices = []
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            self.offices = []
            self.devices = []
    
    def get_global_summary(self):
        total_devices = len(self.devices)
        online_rate = random.uniform(0.90, 0.98)
        online_devices = int(total_devices * online_rate)
        
        total_offices = len(self.offices)
        active_rate = random.uniform(0.95, 1.0)
        active_offices = int(total_offices * active_rate)
        
        regions = defaultdict(lambda: {'offices': 0, 'devices': 0})
        
        for office in self.offices:
            region = office.get('region', 'Unknown')
            regions[region]['offices'] += 1
        
        for device in self.devices:
            office_id = device.get('office_id')
            office = next((o for o in self.offices if o['id'] == office_id), None)
            if office:
                region = office.get('region', 'Unknown')
                regions[region]['devices'] += 1
        
        critical_alerts = random.randint(0, 5)
        warning_alerts = random.randint(5, 20)
        info_alerts = random.randint(10, 50)
        
        avg_uptime = round(random.uniform(98.0, 99.9), 2)
        avg_response_time = round(random.uniform(20, 80), 1)
        avg_cpu = round(random.uniform(30, 60), 1)
        avg_memory = round(random.uniform(40, 70), 1)
        
        return {
            'timestamp': datetime.now().isoformat(),
            'global_health': {
                'total_offices': total_offices,
                'active_offices': active_offices,
                'office_health': round(active_offices / total_offices * 100, 1) if total_offices > 0 else 0,
                'total_devices': total_devices,
                'online_devices': online_devices,
                'device_health': round(online_devices / total_devices * 100, 1) if total_devices > 0 else 0
            },
            'performance_metrics': {
                'average_uptime_pct': avg_uptime,
                'average_response_time_ms': avg_response_time,
                'average_cpu_usage_pct': avg_cpu,
                'average_memory_usage_pct': avg_memory
            },
            'alerts': {
                'critical': critical_alerts,
                'warning': warning_alerts,
                'info': info_alerts,
                'total': critical_alerts + warning_alerts + info_alerts
            },
            'regional_breakdown': [
                {
                    'region': region,
                    'offices': stats['offices'],
                    'devices': stats['devices'],
                    'health_score': round(random.uniform(85, 98), 1)
                }
                for region, stats in regions.items()
            ]
        }
    
    def get_region_analytics(self, region):
      
        region_offices = [o for o in self.offices if o.get('region') == region]
        
        if not region_offices:
            return None
        
        office_ids = [o['id'] for o in region_offices]
        region_devices = [d for d in self.devices if d.get('office_id') in office_ids]
        
        online_rate = random.uniform(0.90, 0.98)
        online_devices = int(len(region_devices) * online_rate)
        
        return {
            'region': region,
            'summary': {
                'total_offices': len(region_offices),
                'total_devices': len(region_devices),
                'online_devices': online_devices,
                'avg_devices_per_office': round(len(region_devices) / len(region_offices), 1) if len(region_offices) > 0 else 0
            },
            'performance': {
                'average_uptime_pct': round(random.uniform(95, 99.5), 2),
                'average_latency_ms': round(random.uniform(30, 100), 1),
                'packet_loss_pct': round(random.uniform(0.1, 2), 2)
            },
            'offices': [
                {
                    'id': o['id'],
                    'name': o['name'],
                    'country': o['country'],
                    'city': o['city'],
                    'status': 'active',
                    'health_score': round(random.uniform(85, 99), 1),
                    'devices_count': len([d for d in region_devices if d.get('office_id') == o['id']])
                }
                for o in region_offices
            ]
        }
    
    def get_alerts(self, severity=None, limit=50):
        """mock data"""
        alert_types = [
            'High CPU Usage',
            'Memory Threshold Exceeded',
            'Device Offline',
            'High Temperature',
            'Packet Loss Detected',
            'Interface Down',
            'Configuration Changed',
            'Security Event',
            'Backup Failed',
            'License Expiring',
            'Disk Space Low',
            'Fan Speed Warning'
        ]
        
        severities = ['critical', 'warning', 'info']
        alerts = []
        
        num_alerts = min(limit, random.randint(20, 100))
        
        for i in range(num_alerts):
            if severity:
                alert_severity = severity
            else:
                alert_severity = random.choices(
                    severities,
                    weights=[0.1, 0.3, 0.6],  # 10% critical, 30% warning, 60% info
                    k=1
                )[0]
            
            if not self.devices:
                break
                
            device = random.choice(self.devices)
            
            office = next((o for o in self.offices if o['id'] == device.get('office_id')), None)
            
            if not office:
                continue
            
            hours_ago = random.randint(0, 72)
            minutes_ago = random.randint(0, 59)
            alert_time = datetime.now() - timedelta(hours=hours_ago, minutes=minutes_ago)
            
            alert_type = random.choice(alert_types)
            
            alerts.append({
                'id': f'ALERT-{i+1:05d}',
                'timestamp': alert_time.isoformat(),
                'severity': alert_severity,
                'type': alert_type,
                'device_id': device['id'],
                'device_name': device['name'],
                'office_id': office['id'],
                'office_name': office['name'],
                'country': office['country'],
                'message': f"{alert_type} detected on {device['name']} at {office['name']}",
                'acknowledged': random.choice([True, False, False, False]),  # 25% 已确认
                'resolved': random.choice([True, False, False, False])  # 25% 已解决
            })
        
        alerts.sort(key=lambda x: x['timestamp'], reverse=True)
        
        alerts = alerts[:limit]
        
        return {
            'total': len(alerts),
            'severity_filter': severity,
            'critical_count': len([a for a in alerts if a['severity'] == 'critical']),
            'warning_count': len([a for a in alerts if a['severity'] == 'warning']),
            'info_count': len([a for a in alerts if a['severity'] == 'info']),
            'alerts': alerts
        }
    
    def get_performance_trends(self, days=7):
        
        trends = []
        
        total_hours = days * 24
        
        for i in range(total_hours):
            timestamp = datetime.now() - timedelta(hours=total_hours - i)
            
            hour_of_day = timestamp.hour
            
            base_cpu = 45
            if 8 <= hour_of_day <= 18:
                base_cpu = 60
            cpu_usage = base_cpu + random.uniform(-10, 10)
            
            base_memory = 50 + (i / total_hours) * 10
            memory_usage = base_memory + random.uniform(-5, 5)
            
            base_bandwidth = 20
            if 8 <= hour_of_day <= 18:
                base_bandwidth = 40
            bandwidth = base_bandwidth + random.uniform(-10, 10)
            
            latency = random.uniform(20, 80)
            
            packet_loss = random.uniform(0, 0.5) if random.random() > 0.9 else random.uniform(0, 2)
            
            total_devices = len(self.devices)
            devices_online = total_devices - random.randint(0, int(total_devices * 0.05))
            
            trends.append({
                'timestamp': timestamp.isoformat(),
                'avg_cpu_usage': round(cpu_usage, 2),
                'avg_memory_usage': round(memory_usage, 2),
                'avg_bandwidth_mbps': round(bandwidth, 2),
                'avg_latency_ms': round(latency, 2),
                'packet_loss_pct': round(packet_loss, 3),
                'devices_online': devices_online
            })
        
        return {
            'period_days': days,
            'data_points': len(trends),
            'start_time': trends[0]['timestamp'] if trends else None,
            'end_time': trends[-1]['timestamp'] if trends else None,
            'trends': trends
        }
    
    def get_top_performers(self, limit=10):
        if not self.devices:
            return []
        
        performers = []
        
        eval_count = min(limit * 2, len(self.devices))
        eval_devices = random.sample(self.devices, eval_count)
        
        for device in eval_devices:
            office = next((o for o in self.offices if o['id'] == device.get('office_id')), None)
            
            if not office:
                continue
            
            uptime = round(random.uniform(99, 99.99), 2)
            response_time = round(random.uniform(5, 30), 2)
            reliability = round(random.uniform(95, 100), 1)
            
            performers.append({
                'device_id': device['id'],
                'device_name': device['name'],
                'device_type': device.get('device_type', 'unknown'),
                'office_name': office['name'],
                'country': office['country'],
                'region': office.get('region', 'Unknown'),
                'uptime_pct': uptime,
                'avg_response_time_ms': response_time,
                'reliability_score': reliability,
                'combined_score': round((uptime + reliability) / 2, 2)
            })
        
        performers.sort(key=lambda x: x['combined_score'], reverse=True)
        
        return performers[:limit]
    
    def get_device_type_distribution(self):
        """获取设备类型分布统计"""
        if not self.devices:
            return {
                'total_devices': 0,
                'distribution': []
            }
        
        type_counts = defaultdict(int)
        for device in self.devices:
            device_type = device.get('device_type', 'unknown')
            type_counts[device_type] += 1
        
        total = sum(type_counts.values())
        
        distribution = [
            {
                'type': device_type.capitalize(),
                'count': count,
                'percentage': round(count / total * 100, 1) if total > 0 else 0
            }
            for device_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True)
        ]
        
        return {
            'total_devices': total,
            'types_count': len(distribution),
            'distribution': distribution
        }
    
    def calculate_health_score(self):
        """计算整体健康评分"""
        summary = self.get_global_summary()
        
        device_health = summary['global_health']['device_health']
        office_health = summary['global_health']['office_health']
        avg_uptime = summary['performance_metrics']['average_uptime_pct']
        
        health_score = (
            device_health * 0.4 +      
            office_health * 0.3 +     
            avg_uptime * 0.3          
        )
        
    
        if health_score >= 95:
            status = 'excellent'
            status_color = 'green'
            status_icon = '🟢'
        elif health_score >= 85:
            status = 'good'
            status_color = 'blue'
            status_icon = '🔵'
        elif health_score >= 70:
            status = 'fair'
            status_color = 'yellow'
            status_icon = '🟡'
        else:
            status = 'poor'
            status_color = 'red'
            status_icon = '🔴'
        
        
        recommendations = self._generate_recommendations(health_score, summary)
        
        return {
            'health_score': round(health_score, 2),
            'status': status,
            'status_color': status_color,
            'status_icon': status_icon,
            'components': {
                'device_health': device_health,
                'office_health': office_health,
                'avg_uptime': avg_uptime
            },
            'recommendations': recommendations,
            'timestamp': datetime.now().isoformat()
        }
    
    def _generate_recommendations(self, health_score, summary):
        
        recommendations = []
        
        
        if summary['alerts']['critical'] > 0:
            recommendations.append({
                'priority': 'high',
                'category': 'alerts',
                'icon': '🚨',
                'message': f"{summary['alerts']['critical']} critical alerts require immediate attention",
                'action': 'Review and resolve critical alerts in the alerts panel'
            })
        
        if summary['global_health']['device_health'] < 95:
            offline = summary['global_health']['total_devices'] - summary['global_health']['online_devices']
            recommendations.append({
                'priority': 'medium',
                'category': 'availability',
                'icon': '⚠️',
                'message': f"{offline} devices are offline and need investigation",
                'action': 'Check device connectivity and perform diagnostics'
            })
        
        if summary['performance_metrics']['average_cpu_usage_pct'] > 70:
            recommendations.append({
                'priority': 'medium',
                'category': 'performance',
                'icon': '📊',
                'message': "High CPU usage detected across multiple devices",
                'action': 'Consider capacity upgrade or load balancing'
            })
        
        if summary['performance_metrics']['average_memory_usage_pct'] > 75:
            recommendations.append({
                'priority': 'medium',
                'category': 'performance',
                'icon': '💾',
                'message': "High memory usage may impact performance",
                'action': 'Review memory allocation and optimize applications'
            })
        
        if summary['performance_metrics']['average_response_time_ms'] > 100:
            recommendations.append({
                'priority': 'low',
                'category': 'network',
                'icon': '🌐',
                'message': "Network latency is higher than optimal",
                'action': 'Investigate network connectivity and routing'
            })
        
        if not recommendations:
            recommendations.append({
                'priority': 'info',
                'category': 'general',
                'icon': '✅',
                'message': "System is operating normally - maintain current monitoring schedule",
                'action': 'Continue regular monitoring and maintenance'
            })
        
        priority_order = {'high': 0, 'medium': 1, 'low': 2, 'info': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))
        
        return recommendations