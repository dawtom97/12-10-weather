import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / '.env')


class AppConfig:
    API_KEY = os.getenv('API_KEY', '')
    API_CITY = os.getenv('API_CITY', 'Cairo')
    WEATHER_FILE = str(ROOT / os.getenv('WEATHER_FILE', 'weather.xlsx')) if not Path(os.getenv('WEATHER_FILE', 'weather.xlsx')).is_absolute() else os.getenv('WEATHER_FILE')
    UPDATE_INTERVAL = max(60, int(os.getenv('UPDATE_INTERVAL', '600')))
    HOST = os.getenv('HOST', '127.0.0.1')
    PORT = int(os.getenv('PORT', '5000'))
    DB_ENABLED = os.getenv('DB_ENABLED', 'false').lower() in ('true', '1', 'yes')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME')
    DB_PORT = int(os.getenv('DB_PORT', '3306'))
