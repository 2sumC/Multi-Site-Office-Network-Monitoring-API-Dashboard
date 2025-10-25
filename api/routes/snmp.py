"""SNMP API Endpoint"""
from flask import Blueprint, jsonify, request
from api.services.snmp_service import SNMPService

bp = Blueprint('snmp', __name__, url_prefix='/api/v1/snmp')

snmp_service = SNMPService()

@bp.route('/device/<host>/info', methods=['GET'])
def get_device_info(host):
   
    community = request.args.get('community', 'public')
    port = int(request.args.get('port', 161))
    
    info = snmp_service.get_device_info(host, community, port)
    
    if not info:
        return jsonify({
            'error': 'Unable to connect to device',
            'host': host
        }), 404
    
    return jsonify(info)


@bp.route('/device/<host>/cpu', methods=['GET'])
def get_cpu_usage(host):
  
    community = request.args.get('community', 'public')
    port = int(request.args.get('port', 161))
    
    cpu = snmp_service.get_cpu_usage(host, community, port)
    
    if not cpu:
        return jsonify({
            'error': 'Unable to retrieve CPU data',
            'host': host,
            'note': 'This may not be a Cisco device, or SNMP is not configured'
        }), 404
    
    return jsonify(cpu)


@bp.route('/device/<host>/memory', methods=['GET'])
def get_memory_usage(host):
   
    community = request.args.get('community', 'public')
    port = int(request.args.get('port', 161))
    
    memory = snmp_service.get_memory_usage(host, community, port)
    
    if not memory:
        return jsonify({
            'error': 'Unable to retrieve memory data',
            'host': host
        }), 404
    
    return jsonify(memory)


@bp.route('/device/<host>/interface/<int:interface_index>', methods=['GET'])
def get_interface_stats(host, interface_index):
   
    community = request.args.get('community', 'public')
    port = int(request.args.get('port', 161))
    
    stats = snmp_service.get_interface_stats(host, interface_index, community, port)
    
    if not stats:
        return jsonify({
            'error': 'Unable to retrieve interface data',
            'host': host,
            'interface_index': interface_index
        }), 404
    
    return jsonify(stats)


@bp.route('/device/<host>/metrics', methods=['GET'])
def get_all_metrics(host):
   
    community = request.args.get('community', 'public')
    port = int(request.args.get('port', 161))
    
    metrics = snmp_service.get_all_metrics(host, community, port)
    
    if not metrics:
        return jsonify({
            'error': 'Unable to retrieve device metrics',
            'host': host
        }), 404
    
    return jsonify(metrics)


@bp.route('/device/<host>/walk', methods=['GET'])
def snmp_walk(host):
   
    oid = request.args.get('oid', '1.3.6.1.2.1.1')
    community = request.args.get('community', 'public')
    port = int(request.args.get('port', 161))
    max_results = int(request.args.get('max_results', 10))
    
    results = snmp_service.walk_oid(host, oid, community, port, max_results)
    
    if not results:
        return jsonify({
            'error': 'SNMP walk failed',
            'host': host,
            'oid': oid
        }), 404
    
    return jsonify({
        'host': host,
        'oid': oid,
        'results': results,
        'count': len(results)
    })


@bp.route('/discover', methods=['POST'])
def discover_devices():
    
    data = request.get_json()
    network = data.get('network')
    community = data.get('community', 'public')
    
    if not network:
        return jsonify({'error': 'network parameter required'}), 400
    
    
    discovered = []
    
    test_ips = [
        f"{network.split('/')[0].rsplit('.', 1)[0]}.1",
        f"{network.split('/')[0].rsplit('.', 1)[0]}.254"
    ]
    
    for ip in test_ips:
        info = snmp_service.get_device_info(ip, community)
        if info:
            discovered.append({
                'ip': ip,
                'hostname': info.get('hostname', 'Unknown'),
                'description': info.get('description', 'N/A')[:100]
            })
    
    return jsonify({
        'network': network,
        'discovered_devices': discovered,
        'count': len(discovered)
    })