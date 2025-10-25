import requests
from config import Config
from datetime import datetime, timedelta
import json
import os

class WeatherService:
    
    BASE_URL = 'https://api.openweathermap.org/data/2.5'
    CACHE_DIR = 'data/cache/weather'
    CACHE_TTL = 1800  # 30min
    
    def __init__(self, api_key=None):
        self.api_key = api_key or Config.OPENWEATHER_API_KEY
        os.makedirs(self.CACHE_DIR, exist_ok=True)
    
    def _get_cache_path(self, lat, lon):
        return os.path.join(self.CACHE_DIR, f'{lat}_{lon}.json')
    
    def _is_cache_valid(self, cache_path):
        if not os.path.exists(cache_path):
            return False
        
        mod_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        return (datetime.now() - mod_time).seconds < self.CACHE_TTL
    
    def get_weather(self, latitude, longitude):
        cache_path = self._get_cache_path(latitude, longitude)
        
        if self._is_cache_valid(cache_path):
            with open(cache_path, 'r') as f:
                return json.load(f)
        
        if not self.api_key:
            return self._get_mock_weather(latitude, longitude)
        
        try:
            url = f'{self.BASE_URL}/weather'
            params = {
                'lat': latitude,
                'lon': longitude,
                'appid': self.api_key,
                'units': 'metric'  
            }
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            weather_data = {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
                'clouds': data['clouds']['all'],
                'timestamp': datetime.now().isoformat()
            }
            
            with open(cache_path, 'w') as f:
                json.dump(weather_data, f)
            
            return weather_data
            
        except requests.exceptions.RequestException as e:
            print(f'Weather API error: {e}')
            return self._get_mock_weather(latitude, longitude)
    
    def _get_mock_weather(self, latitude, longitude):
        import random
        
        descriptions = [
            'clear sky', 'few clouds', 'scattered clouds', 
            'broken clouds', 'light rain', 'moderate rain'
        ]
        
        base_temp = 30 - abs(latitude) * 0.5
        
        return {
            'temperature': round(base_temp + random.uniform(-5, 5), 1),
            'feels_like': round(base_temp + random.uniform(-3, 3), 1),
            'humidity': random.randint(40, 90),
            'pressure': random.randint(1000, 1020),
            'description': random.choice(descriptions),
            'icon': '01d',
            'wind_speed': round(random.uniform(0, 10), 1),
            'clouds': random.randint(0, 100),
            'timestamp': datetime.now().isoformat(),
            'source': 'simulated'
        }
    
    def get_forecast(self, latitude, longitude, days=5):
        forecast = []
        base_temp = 25
        
        for i in range(days):
            date = datetime.now() + timedelta(days=i)
            forecast.append({
                'date': date.strftime('%Y-%m-%d'),
                'temp_max': round(base_temp + random.uniform(-3, 5), 1),
                'temp_min': round(base_temp + random.uniform(-8, 0), 1),
                'description': random.choice(['sunny', 'cloudy', 'rainy']),
                'humidity': random.randint(40, 90)
            })
        
        return forecast