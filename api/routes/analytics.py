"""Analyze API endpoints"""
from flask import Blueprint, jsonify, request
from api.services.analytics_service import AnalyticsService
from datetime import datetime
import json
import os

bp = Blueprint('analytics', __name__, url_prefix='/api/v1/analytics')

analytics_service = AnalyticsService()

@bp.route('/summary', methods=['GET'])
def get_global_summary():
    """
    get summary
    """
    try:
        summary = analytics_service.get_global_summary()
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/region/<region>', methods=['GET'])
def get_region_analytics(region):
    """
    get regional info

    """
    try:
        analytics = analytics_service.get_region_analytics(region)
        
        if not analytics:
            return jsonify({
                'error': 'Region not found or has no data',
                'available_regions': ['Africa', 'Asia-Pacific', 'Europe-CIS', 'Latin America']
            }), 404
        
        return jsonify(analytics), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/alerts', methods=['GET'])
def get_alerts():
    """
    get warnings
    """
    try:
        severity = request.args.get('severity')  # critical, warning, info
        limit = int(request.args.get('limit', 50))
        
        if severity and severity not in ['critical', 'warning', 'info']:
            return jsonify({
                'error': 'Invalid severity parameter',
                'valid_values': ['critical', 'warning', 'info']
            }), 400
        
        if limit > 100:
            limit = 100
        
        alerts = analytics_service.get_alerts(severity, limit)
        return jsonify(alerts), 200
    except ValueError:
        return jsonify({'error': 'Invalid limit parameter - must be a number'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/trends', methods=['GET'])
def get_performance_trends():
    """
    get trends
    """
    try:
        days = int(request.args.get('days', 7))
        
        if days < 1:
            return jsonify({'error': 'Days parameter must be at least 1'}), 400
        
        if days > 30:
            return jsonify({'error': 'Maximum 30 days allowed'}), 400
        
        trends = analytics_service.get_performance_trends(days)
        return jsonify(trends), 200
    except ValueError:
        return jsonify({'error': 'Invalid days parameter - must be a number'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/top-performers', methods=['GET'])
def get_top_performers():
    """
    get device list
    """
    try:
        limit = int(request.args.get('limit', 10))
        
        if limit < 1:
            limit = 1
        if limit > 50:
            limit = 50
        
        performers = analytics_service.get_top_performers(limit)
        return jsonify({
            'total': len(performers),
            'limit': limit,
            'performers': performers
        }), 200
    except ValueError:
        return jsonify({'error': 'Invalid limit parameter - must be a number'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/device-distribution', methods=['GET'])
def get_device_distribution():
    """get distribution analytics"""
    try:
        distribution = analytics_service.get_device_type_distribution()
        return jsonify(distribution), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/health-score', methods=['GET'])
def get_health_score():
    """
    get scores
    """
    try:
        health_data = analytics_service.calculate_health_score()
        return jsonify(health_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reports/generate', methods=['POST'])
def generate_report():
   
    try:
        data = request.get_json() or {}
        
        report_type = data.get('type', 'summary')
        user = data.get('user', 'system')
        include_trends = data.get('include_trends', True)
        include_alerts = data.get('include_alerts', True)
        
        report_id = f'RPT-{datetime.now().strftime("%Y%m%d%H%M%S")}'
        
        report_data = {
            'id': report_id,
            'type': report_type,
            'generated_at': datetime.now().isoformat(),
            'generated_by': user,
            'summary': analytics_service.get_global_summary()
        }
        
        if include_trends:
            report_data['trends'] = analytics_service.get_performance_trends(days=7)
        
        if include_alerts:
            report_data['alerts'] = analytics_service.get_alerts(limit=20)
        
        # score
        report_data['health_score'] = analytics_service.calculate_health_score()
        
        # distribution
        report_data['device_distribution'] = analytics_service.get_device_type_distribution()
        
        # save report
        reports_dir = 'data/cache/reports'
        os.makedirs(reports_dir, exist_ok=True)
        
        report_path = os.path.join(reports_dir, f'report_{report_id}.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        return jsonify({
            'message': 'Report generated successfully',
            'report_id': report_id,
            'download_url': f"/api/v1/analytics/reports/{report_id}",
            'generated_at': report_data['generated_at']
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reports/<report_id>', methods=['GET'])
def get_report(report_id):

    try:
        report_path = f"data/cache/reports/report_{report_id}.json"
        
        if not os.path.exists(report_path):
            return jsonify({'error': 'Report not found'}), 404
        
        with open(report_path, 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        return jsonify(report), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/reports', methods=['GET'])
def list_reports():
    try:
        reports_dir = 'data/cache/reports'
        
        if not os.path.exists(reports_dir):
            return jsonify({'reports': []}), 200
        
        reports = []
        for filename in os.listdir(reports_dir):
            if filename.startswith('report_') and filename.endswith('.json'):
                report_id = filename.replace('report_', '').replace('.json', '')
                file_path = os.path.join(reports_dir, filename)
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    report_data = json.load(f)
                
                reports.append({
                    'id': report_id,
                    'type': report_data.get('type', 'unknown'),
                    'generated_at': report_data.get('generated_at'),
                    'generated_by': report_data.get('generated_by', 'unknown'),
                    'url': f"/api/v1/analytics/reports/{report_id}"
                })
        
        # sort by time
        reports.sort(key=lambda x: x.get('generated_at', ''), reverse=True)
        
        return jsonify({
            'total': len(reports),
            'reports': reports
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500