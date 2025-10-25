import requests
from datetime import datetime
import pytz

class TimeService:
    
    BASE_URL = 'http://worldtimeapi.org/api'
    
    def get_timezone_time(self, timezone):
        try:
            url = f'{self.BASE_URL}/timezone/{timezone}'
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            data = response.json()
            
            return {
                'timezone': timezone,
                'datetime': data['datetime'],
                'utc_offset': data['utc_offset'],
                'day_of_week': data['day_of_week'],
                'day_of_year': data['day_of_year'],
                'week_number': data['week_number']
            }
            
        except requests.exceptions.RequestException as e:
            print(f'Time API error: {e}')
            return self._get_local_timezone_time(timezone)
    
    def _get_local_timezone_time(self, timezone):
        try:
            tz = pytz.timezone(timezone)
            now = datetime.now(tz)
            
            return {
                'timezone': timezone,
                'datetime': now.isoformat(),
                'utc_offset': now.strftime('%z'),
                'day_of_week': now.weekday(),
                'source': 'local'
            }
        except:
            return None
    
    def get_all_timezones(self):
        try:
            url = f'{self.BASE_URL}/timezone'
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException:
            return pytz.all_timezones
    
    def convert_time(self, time_str, from_tz, to_tz):
        try:
            from_timezone = pytz.timezone(from_tz)
            to_timezone = pytz.timezone(to_tz)
            
            dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            
            if dt.tzinfo is None:
                dt = from_timezone.localize(dt)
            
            converted = dt.astimezone(to_timezone)
            
            return {
                'original': {
                    'time': time_str,
                    'timezone': from_tz
                },
                'converted': {
                    'time': converted.isoformat(),
                    'timezone': to_tz
                }
            }
            
        except Exception as e:
            print(f'Time conversion error: {e}')
            return None