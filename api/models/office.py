
class Office:
    
    def __init__(self, id, name, country, region, city, 
                 latitude, longitude, timezone, status='active'):
        self.id = id
        self.name = name
        self.country = country
        self.region = region  # Africa, Asia, Europe, Americas
        self.city = city
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.status = status
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'region': self.region,
            'city': self.city,
            'coordinates': {
                'lat': self.latitude,
                'lng': self.longitude
            },
            'timezone': self.timezone,
            'status': self.status
        }
    
    @staticmethod
    def from_dict(data):
        return Office(
            id=data.get('id'),
            name=data.get('name'),
            country=data.get('country'),
            region=data.get('region'),
            city=data.get('city'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            timezone=data.get('timezone'),
            status=data.get('status', 'active')
        )