"""OpenWeather current conditions (one request, with validation and timeout)."""
from datetime import datetime, timedelta, timezone
import requests
from config import AppConfig


def get_weather(city=None):
    if not AppConfig.API_KEY:
        raise RuntimeError('Brak API_KEY w pliku .env')
    city = (city or AppConfig.API_CITY).strip()
    if not city:
        raise ValueError('Podaj nazwę miasta')
    response = requests.get(
        'https://api.openweathermap.org/data/2.5/weather',
        params={'q': city, 'appid': AppConfig.API_KEY, 'units': 'metric', 'lang': 'pl'},
        timeout=12,
    )
    response.raise_for_status()
    data = response.json()
    main = data['main']
    wind = data['wind']
    sys = data['sys']
    local_timezone = timezone(timedelta(seconds=data.get('timezone', 0)))

    def local_time(ts):
        return datetime.fromtimestamp(ts, local_timezone).strftime('%H:%M:%S')

    return {
        'place': data['name'],
        'temp': round(main['temp'], 2),
        'feels_like': round(main['feels_like'], 2),
        'wind': round(wind['speed'], 2),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'sunrise': local_time(sys['sunrise']),
        'sunset': local_time(sys['sunset']),
    }
