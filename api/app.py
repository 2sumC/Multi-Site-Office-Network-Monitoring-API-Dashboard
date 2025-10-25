import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()  

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object(config_class)
    
    CORS(app)
    
    os.makedirs('data/cache/weather', exist_ok=True)
    os.makedirs('data/cache/geo', exist_ok=True)
    os.makedirs('data/cache/reports', exist_ok=True)
    os.makedirs('data/db', exist_ok=True)
    
    from api.routes import offices, devices, analytics, external
    
    app.register_blueprint(offices.bp)
    app.register_blueprint(devices.bp)
    app.register_blueprint(analytics.bp)
    app.register_blueprint(external.bp)
    
    try:
        from api.routes import snmp
        app.register_blueprint(snmp.bp)
        print("✅ SNMP monitoring enabled")
    except ImportError:
        print("⚠️  SNMP monitoring not available (optional feature)")
    
    @app.route('/')
    def index():
        return render_template('dashboard.html')
    
    @app.route('/health')
    def health_check():
        """API健康检查"""
        from datetime import datetime
        return jsonify({
            'status': 'healthy',
            'api_version': app.config['API_VERSION'],
            'timestamp': datetime.now().isoformat(),
            'environment': 'development' if app.config['DEBUG'] else 'production'
        })
    
    @app.route('/api')
    @app.route(app.config['API_PREFIX'])
    def api_root():
        return jsonify({
            'message': 'UNDP ICT Infrastructure Dashboard API',
            'version': app.config['API_VERSION'],
            'documentation': 'See README.md for full API documentation',
            'base_url': app.config['API_PREFIX'],
            'endpoints': {
                'offices': {
                    'list_all': f"{app.config['API_PREFIX']}/offices",
                    'get_one': f"{app.config['API_PREFIX']}/offices/{{id}}",
                    'devices': f"{app.config['API_PREFIX']}/offices/{{id}}/devices"
                },
                'devices': {
                    'list_all': f"{app.config['API_PREFIX']}/devices",
                    'get_one': f"{app.config['API_PREFIX']}/devices/{{id}}",
                    'metrics': f"{app.config['API_PREFIX']}/devices/{{id}}/metrics",
                    'status': f"{app.config['API_PREFIX']}/devices/{{id}}/status",
                    'alerts': f"{app.config['API_PREFIX']}/devices/{{id}}/alerts"
                },
                'analytics': {
                    'summary': f"{app.config['API_PREFIX']}/analytics/summary",
                    'region': f"{app.config['API_PREFIX']}/analytics/region/{{region}}",
                    'alerts': f"{app.config['API_PREFIX']}/analytics/alerts",
                    'trends': f"{app.config['API_PREFIX']}/analytics/trends",
                    'health': f"{app.config['API_PREFIX']}/analytics/health-score"
                },
                'external': {
                    'weather': f"{app.config['API_PREFIX']}/external/weather/{{office_id}}",
                    'time': f"{app.config['API_PREFIX']}/external/time/{{office_id}}",
                    'country': f"{app.config['API_PREFIX']}/external/country/{{country_code}}",
                    'news': f"{app.config['API_PREFIX']}/external/news"
                },
                'snmp': {
                    'device_info': f"{app.config['API_PREFIX']}/snmp/device/{{host}}/info",
                    'cpu': f"{app.config['API_PREFIX']}/snmp/device/{{host}}/cpu",
                    'memory': f"{app.config['API_PREFIX']}/snmp/device/{{host}}/memory",
                    'interface': f"{app.config['API_PREFIX']}/snmp/device/{{host}}/interface/{{index}}",
                    'all_metrics': f"{app.config['API_PREFIX']}/snmp/device/{{host}}/metrics"
                }
            },
            'examples': [
                f"GET {app.config['API_PREFIX']}/analytics/summary",
                f"GET {app.config['API_PREFIX']}/offices",
                f"GET {app.config['API_PREFIX']}/devices?status=online",
                f"GET {app.config['API_PREFIX']}/analytics/alerts?severity=critical",
                f"GET {app.config['API_PREFIX']}/snmp/device/192.168.1.1/info"
            ]
        })
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not found',
            'message': 'The requested resource was not found',
            'status': 404
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred',
            'status': 500
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad request',
            'message': 'Invalid request parameters',
            'status': 400
        }), 400
    
    @app.cli.command()
    def init_data():
        print("Initializing data...")
        print("✅ Data initialization complete")
    
    @app.cli.command()
    def clear_cache():
        import shutil
        cache_dirs = ['data/cache/weather', 'data/cache/geo', 'data/cache/reports']
        for cache_dir in cache_dirs:
            if os.path.exists(cache_dir):
                shutil.rmtree(cache_dir)
                os.makedirs(cache_dir)
        print("✅ Cache cleared")
    
    return app

app = create_app()

if __name__ == '__main__':
    PORT = 8000
    print("=" * 60)
    print("🌍 ICT Infrastructure Dashboard")
    print("=" * 60)
    print(f"Dashboard: http://localhost:{PORT}")
    print(f"API: http://localhost:{PORT}/api/v1")
    print(f"Health: http://localhost:{PORT}/health")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=PORT)