"""Device API endpoints"""
from flask import Blueprint, jsonify, request
from api.models.device import Device
from datetime import datetime, timedelta
import json
import random

bp = Blueprint('devices', __name__, url_prefix='/api/v1/devices')

def load_devices():
    with open('data/seed_data.json', 'r') as f:
        data = json.load(f)
    return [Device(**d) for d in data['devices']]

@bp.route('', methods=['GET'])
def get_all_devices():
    devices = load_devices()
    
    device_type = request.args.get('type')
    if device_type:
        devices = [d for d in devices if d.device_type == device_type]
    
    status = request.args.get('status')
    if status:
        devices = [d for d in devices if d.status == status]
    
    office_id = request.args.get('office_id')
    if office_id:
        devices = [d for d in devices if d.office_id == office_id]
    
    return jsonify({
        'total': len(devices),
        'devices': [d.to_dict() for d in devices]
    })

@bp.route('/<device_id>', methods=['GET'])
def get_device(device_id):
    devices = load_devices()
    device = next((d for d in devices if d.id == device_id), None)
    
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    device_info = device.to_dict()
    device_info['current_metrics'] = device.get_metrics()
    
    return jsonify(device_info)

@bp.route('/<device_id>/metrics', methods=['GET'])
def get_device_metrics(device_id):
    devices = load_devices()
    device = next((d for d in devices if d.id == device_id), None)
    
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    hours = int(request.args.get('hours', 24))
    
    # moch historical data
    metrics_history = []
    now = datetime.now()
    
    for i in range(hours):
        timestamp = now - timedelta(hours=hours-i)
        metrics = device.get_metrics()
        metrics['timestamp'] = timestamp.isoformat()
        metrics_history.append(metrics)
    
    return jsonify({
        'device_id': device_id,
        'device_name': device.name,
        'period': f'{hours} hours',
        'data_points': len(metrics_history),
        'metrics': metrics_history
    })

@bp.route('/<device_id>/status', methods=['GET'])
def get_device_status(device_id):
    devices = load_devices()
    device = next((d for d in devices if d.id == device_id), None)
    
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    metrics = device.get_metrics()
    
    # get health status
    health_status = 'healthy'
    warnings = []
    
    if metrics['cpu_usage'] > 80:
        health_status = 'warning'
        warnings.append('High CPU usage')
    
    if metrics['memory_usage'] > 85:
        health_status = 'warning'
        warnings.append('High memory usage')
    
    if metrics['temperature'] > 60:
        health_status = 'warning'
        warnings.append('High temperature')
    
    if metrics['packet_loss'] > 1:
        health_status = 'warning'
        warnings.append('Packet loss detected')
    
    # critical warnings
    if len(warnings) >= 3:
        health_status = 'critical'
    
    return jsonify({
        'device_id': device_id,
        'device_name': device.name,
        'status': device.status,
        'health_status': health_status,
        'warnings': warnings,
        'metrics': metrics,
        'last_updated': datetime.now().isoformat()
    })

@bp.route('/<device_id>/alerts', methods=['GET'])
def get_device_alerts(device_id):
    """获取设备告警历史"""
    devices = load_devices()
    device = next((d for d in devices if d.id == device_id), None)
    
    if not device:
        return jsonify({'error': 'Device not found'}), 404
    
    # mock warning data
    alerts = []
    alert_types = [
        'High CPU Usage',
        'Memory Threshold Exceeded',
        'High Temperature',
        'Packet Loss Detected',
        'Interface Down',
        'Connection Timeout'
    ]
    
    num_alerts = random.randint(5, 10)
    now = datetime.now()
    
    for i in range(num_alerts):
        alert_time = now - timedelta(hours=random.randint(1, 72))
        severity = random.choice(['warning', 'critical', 'info'])
        
        alerts.append({
            'id': f'ALERT-{device_id}-{i+1}',
            'timestamp': alert_time.isoformat(),
            'severity': severity,
            'type': random.choice(alert_types),
            'message': f'{random.choice(alert_types)} on {device.name}',
            'acknowledged': random.choice([True, False])
        })
    
    # sort by time
    alerts.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return jsonify({
        'device_id': device_id,
        'total_alerts': len(alerts),
        'alerts': alerts
    })