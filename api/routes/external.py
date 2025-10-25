"""External API endpoints"""
from flask import Blueprint, jsonify, request
from api.services.weather_service import WeatherService
from api.services.geo_service import GeoService
from api.services.time_service import TimeService
from api.services.news_service import NewsService

from api.models.office import Office
import json

bp = Blueprint('external', __name__, url_prefix='/api/v1/external')

weather_service = WeatherService()
geo_service = GeoService()
time_service = TimeService()

def load_offices():
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    seed_path = os.path.join(base_dir, 'data', 'seed_data.json')
    
    try:
        if not os.path.exists(seed_path):
            print(f"⚠️ seed_data.json not found, using empty data")
            return []
        
        with open(seed_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return [Office.from_dict(o) for o in data.get('offices', [])]
    except Exception as e:
        print(f"❌ Error loading offices: {e}")
        return []

@bp.route('/weather/<office_id>', methods=['GET'])
def get_office_weather(office_id):
    offices = load_offices()
    office = next((o for o in offices if o.id == office_id), None)
    
    if not office:
        return jsonify({'error': 'Office not found'}), 404
    
    # get weather
    weather = weather_service.get_weather(office.latitude, office.longitude)
    
    return jsonify({
        'office_id': office_id,
        'office_name': office.name,
        'location': {
            'city': office.city,
            'country': office.country,
            'coordinates': {
                'lat': office.latitude,
                'lng': office.longitude
            }
        },
        'weather': weather
    })

@bp.route('/weather/forecast/<office_id>', methods=['GET'])
def get_office_forecast(office_id):
    offices = load_offices()
    office = next((o for o in offices if o.id == office_id), None)
    
    if not office:
        return jsonify({'error': 'Office not found'}), 404
    
    days = int(request.args.get('days', 5))
    forecast = weather_service.get_forecast(office.latitude, office.longitude, days)
    
    return jsonify({
        'office_id': office_id,
        'office_name': office.name,
        'forecast': forecast
    })

@bp.route('/location/ip/<ip_address>', methods=['GET'])
def get_ip_location(ip_address):
    location = geo_service.get_ip_location(ip_address)
    
    if not location:
        return jsonify({'error': 'Unable to retrieve location'}), 404
    
    return jsonify(location)

@bp.route('/country/<country_code>', methods=['GET'])
def get_country_info(country_code):
    info = geo_service.get_country_info(country_code)
    
    if not info:
        return jsonify({'error': 'Country not found'}), 404
    
    return jsonify(info)

@bp.route('/time/<office_id>', methods=['GET'])
def get_office_time(office_id):
    offices = load_offices()
    office = next((o for o in offices if o.id == office_id), None)
    
    if not office:
        return jsonify({'error': 'Office not found'}), 404
    
    time_info = time_service.get_timezone_time(office.timezone)
    
    return jsonify({
        'office_id': office_id,
        'office_name': office.name,
        'local_time': time_info.get('datetime'),
        'timezone': time_info.get('timezone'),
        'utc_offset': time_info.get('utc_offset')
    })

@bp.route('/distance', methods=['GET'])
def calculate_distance():
    office1_id = request.args.get('office1')
    office2_id = request.args.get('office2')
    
    if not office1_id or not office2_id:
        return jsonify({'error': 'Both office1 and office2 parameters required'}), 400
    
    offices = load_offices()
    office1 = next((o for o in offices if o.id == office1_id), None)
    office2 = next((o for o in offices if o.id == office2_id), None)
    
    if not office1 or not office2:
        return jsonify({'error': 'One or both offices not found'}), 404
    
    distance = geo_service.get_distance(
        office1.latitude, office1.longitude,
        office2.latitude, office2.longitude
    )
    
    return jsonify({
        'office1': {
            'id': office1.id,
            'name': office1.name,
            'city': office1.city
        },
        'office2': {
            'id': office2.id,
            'name': office2.name,
            'city': office2.city
        },
        'distance_km': distance
    })

@bp.route('/connectivity/<country_code>', methods=['GET'])
def get_connectivity_info(country_code):
    import random
    
    # mock data
    connectivity = {
        'country_code': country_code,
        'average_speed_mbps': round(random.uniform(5, 100), 2),
        'reliability_score': round(random.uniform(60, 99), 1),
        'coverage_percentage': round(random.uniform(70, 99), 1),
        'providers_count': random.randint(3, 15),
        'fiber_availability': random.choice([True, False]),
        'satellite_availability': True,
        'estimated_latency_ms': round(random.uniform(20, 200), 1)
    }
    
    return jsonify(connectivity)

@bp.route('/news')
def get_latest_news():
    service = NewsService()
    news = service.get_latest_news()

    if not news:
        return jsonify({"news": []})

    return jsonify({"news": news})
