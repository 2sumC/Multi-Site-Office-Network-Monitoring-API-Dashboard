import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    
    # Database
    DATABASE_PATH = 'data/db/undp_ict.db'
    
    # API Key
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY', '')
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')
    
    # API Configuration
    API_VERSION = 'v1'
    API_PREFIX = f'/api/{API_VERSION}'
    
    # Cache Configuration
    CACHE_DIR = 'data/cache'
    CACHE_TTL = 300  # 5分钟
    
    # Mock data
    SIMULATE_DEVICES = True  
    UPDATE_INTERVAL = 60     # 60s