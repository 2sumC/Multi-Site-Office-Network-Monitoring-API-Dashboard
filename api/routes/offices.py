"""Office API endpoints"""
from flask import Blueprint, jsonify, request
from api.models.office import Office
import json
import os

bp = Blueprint('offices', __name__, url_prefix='/api/v1/offices')


def load_offices():
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    seed_path = os.path.join(base_dir, 'data', 'seed_data.json')
    
    try:
        if not os.path.exists(seed_path):
            print(f"⚠️ seed_data.json not found at {seed_path}")
            return []
        
        with open(seed_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return [Office.from_dict(o) for o in data.get('offices', [])]
    except Exception as e:
        print(f"❌ Error loading offices: {e}")
        return []


def load_devices():
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    seed_path = os.path.join(base_dir, 'data', 'seed_data.json')
    
    try:
        if not os.path.exists(seed_path):
            return []
        
        with open(seed_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return data.get('devices', [])
    except Exception as e:
        print(f"❌ Error loading devices: {e}")
        return []


@bp.route('', methods=['GET'])
def get_all_offices():
    offices = load_offices()
    
    region = request.args.get('region')
    if region:
        offices = [o for o in offices if o.region == region]
    
    status = request.args.get('status')
    if status:
        offices = [o for o in offices if o.status == status]
    
    return jsonify({
        'total': len(offices),
        'offices': [o.to_dict() for o in offices]
    })


@bp.route('/<office_id>', methods=['GET'])
def get_office(office_id):
    offices = load_offices()
    office = next((o for o in offices if o.id == office_id), None)
    
    if not office:
        return jsonify({'error': 'Office not found'}), 404
    
    return jsonify(office.to_dict())


@bp.route('/<office_id>/devices', methods=['GET'])
def get_office_devices(office_id):
    offices = load_offices()
    office = next((o for o in offices if o.id == office_id), None)
    
    if not office:
        return jsonify({'error': 'Office not found'}), 404
    
    from api.models.device import Device
    devices_data = load_devices()
    
    devices = [Device(**d) for d in devices_data if d.get('office_id') == office_id]
    
    return jsonify({
        'office_id': office_id,
        'office_name': office.name,
        'total_devices': len(devices),
        'devices': [d.to_dict() for d in devices]
    })


@bp.route('', methods=['POST'])
def create_office():
    data = request.get_json()
    
    required_fields = ['name', 'country', 'region', 'city', 'latitude', 'longitude']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    import uuid
    data['id'] = f"CO-{data['region'][:2].upper()}-{str(uuid.uuid4())[:3].upper()}"
    
    office = Office.from_dict(data)
        
    return jsonify({
        'message': 'Office created successfully',
        'office': office.to_dict()
    }), 201