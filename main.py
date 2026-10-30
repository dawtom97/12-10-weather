"""Start: python main.py — dashboard and background weather collection."""
import logging
import threading

from config import AppConfig
from services.dashboard import create_app
from services.data_files import append
from services.openweather_api import get_weather

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


def collect_weather(stop_event):
    """Run independently of HTTP requests; failure never stops dashboard."""
    from services.mysql_db import insert_record

    while not stop_event.is_set():
        try:
            weather = get_weather(AppConfig.API_CITY)
            append([weather])
            logger.info('Zapisano pomiar: %s, %s °C', weather['place'], weather['temp'])
            if AppConfig.DB_ENABLED:
                insert_record(weather)
        except Exception:
            logger.exception('Nie udało się pobrać lub zapisać pogody; ponowię próbę')
        stop_event.wait(AppConfig.UPDATE_INTERVAL)


def main():
    if AppConfig.DB_ENABLED:
        try:
            from services.mysql_db import initialize_db
            initialize_db()
        except Exception:
            logger.exception('Nie udało się zainicjalizować MySQL; dashboard nadal działa')

    stop_event = threading.Event()
    worker = threading.Thread(target=collect_weather, args=(stop_event,), daemon=True, name='weather-collector')
    worker.start()
    try:
        create_app().run(host=AppConfig.HOST, port=AppConfig.PORT, debug=False, use_reloader=False)
    finally:
        stop_event.set()
        worker.join(timeout=3)


if __name__ == '__main__':
    main()
