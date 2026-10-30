"""Optional MySQL sink. Errors are logged and do not break the collector."""
import logging
from config import AppConfig

logger = logging.getLogger(__name__)


def create_connection():
    import mysql.connector
    return mysql.connector.connect(
        host=AppConfig.DB_HOST,
        user=AppConfig.DB_USER,
        password=AppConfig.DB_PASSWORD,
        database=AppConfig.DB_NAME,
        port=AppConfig.DB_PORT,
        connection_timeout=5,
    )


def initialize_db():
    conn = create_connection()
    try:
        cursor = conn.cursor()
        try:
            cursor.execute('''CREATE TABLE IF NOT EXISTS records (
                id CHAR(36) NOT NULL DEFAULT (UUID()) PRIMARY KEY,
                place VARCHAR(255) NOT NULL,
                temp FLOAT NOT NULL,
                feel FLOAT NOT NULL,
                wind FLOAT NOT NULL,
                timestamp TIMESTAMP NOT NULL,
                sunrise TIME NOT NULL,
                sunset TIME NOT NULL
            )''')
            conn.commit()
        finally:
            cursor.close()
    finally:
        conn.close()


def insert_record(data):
    try:
        conn = create_connection()
        try:
            cursor = conn.cursor()
            try:
                cursor.execute('''INSERT INTO records
                    (place, temp, feel, wind, timestamp, sunrise, sunset)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)''', (
                    data['place'], data['temp'], data['feels_like'], data['wind'],
                    data['timestamp'], data['sunrise'], data['sunset']
                ))
                conn.commit()
            finally:
                cursor.close()
        finally:
            conn.close()
    except Exception:
        logger.exception('Zapis do MySQL nie powiódł się')


def read_record():
    conn = create_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM records ORDER BY timestamp DESC')
            return cursor.fetchall()
        finally:
            cursor.close()
    finally:
        conn.close()
