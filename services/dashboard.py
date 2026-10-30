from datetime import datetime
from flask import Flask, jsonify, render_template, request
from config import AppConfig
from services.data_files import read_records
from services.openweather_api import get_weather


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')

    @app.get('/')
    def index():
        return render_template('index.html', now=datetime.now())

    @app.get('/wyniki')
    def wyniki():
        records = read_records()
        latest = records[0] if records else None
        city = latest['place'] if latest else AppConfig.API_CITY
        return render_template('wyniki.html', df=records, latest=latest, city=city, now=datetime.now())

    @app.get('/api/pomiary')
    def api_pomiary():
        records = read_records()
        return jsonify({'latest': records[0] if records else None, 'count': len(records), 'records': records[:100]})

    @app.route('/wyszukaj', methods=['GET', 'POST'])
    def wyszukaj():
        weather = None
        error = None
        if request.method == 'POST':
            city = request.form.get('query', '').strip()
            try:
                weather = get_weather(city) if city else None
                if not city:
                    error = 'Wpisz nazwę miasta.'
            except Exception as exc:
                error = f'Nie udało się pobrać pogody: {exc}'
        return render_template('wyszukaj.html', weather=weather, error=error, now=datetime.now())

    return app
