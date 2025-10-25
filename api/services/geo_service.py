import requests
import json
import os
from datetime import datetime, timedelta

class GeoService:
    
    IPAPI_BASE = 'http://ip-api.com/json'
    COUNTRIES_BASE = 'https://restcountries.com/v3.1'
    CACHE_DIR = 'data/cache/geo'
    CACHE_TTL = 86400  #
    
    def __init__(self):
        os.makedirs(self.CACHE_DIR, exist_ok=True)
    
    def get_ip_location(self, ip_address):
        cache_path = os.path.join(self.CACHE_DIR, f'ip_{ip_address}.json')
        
        if self._is_cache_valid(cache_path):
            with open(cache_path, 'r') as f:
                return json.load(f)
        
        try:
            url = f'{self.IPAPI_BASE}/{ip_address}'
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] == 'success':
                location_data = {
                    'ip': ip_address,
                    'country': data['country'],
                    'country_code': data['countryCode'],
                    'region': data['regionName'],
                    'city': data['city'],
                    'latitude': data['lat'],
                    'longitude': data['lon'],
                    'timezone': data['timezone'],
                    'isp': data['isp'],
                    'timestamp': datetime.now().isoformat()
                }
                
                with open(cache_path, 'w') as f:
                    json.dump(location_data, f)
                
                return location_data
            
        except requests.exceptions.RequestException as e:
            print(f'IP API error: {e}')
        
        return None
    
    def get_country_info(self, country_code):
        cache_path = os.path.join(self.CACHE_DIR, f'country_{country_code}.json')
        
        if self._is_cache_valid(cache_path):
            with open(cache_path, 'r') as f:
                return json.load(f)
        
        try:
            url = f'{self.COUNTRIES_BASE}/alpha/{country_code}'
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()[0]
            
            country_info = {
                'name': data['name']['common'],
                'official_name': data['name']['official'],
                'capital': data.get('capital', ['N/A'])[0],
                'region': data['region'],
                'subregion': data.get('subregion', 'N/A'),
                'population': data.get('population', 0),
                'languages': list(data.get('languages', {}).values()),
                'currencies': list(data.get('currencies', {}).keys()),
                'timezones': data.get('timezones', []),
                'flag': data['flags']['png'],
                'timestamp': datetime.now().isoformat()
            }
            
            with open(cache_path, 'w') as f:
                json.dump(country_info, f)
            
            return country_info
            
        except requests.exceptions.RequestException as e:
            print(f'Countries API error: {e}')
        
        return None
    
    def _is_cache_valid(self, cache_path):
        if not os.path.exists(cache_path):
            return False
        
        mod_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        return (datetime.now() - mod_time).seconds < self.CACHE_TTL
    
    def get_distance(self, lat1, lon1, lat2, lon2):
        from math import radians, cos, sin, asin, sqrt
        
        # Haversine
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # earth
        
        return round(c * r, 2)