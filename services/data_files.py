"""Excel persistence protected against concurrent reader/writer operations."""
from pathlib import Path
from threading import RLock
import os
import tempfile
import pandas as pd
from config import AppConfig

LOCK = RLock()
COLUMNS = ['place', 'temp', 'feels_like', 'wind', 'timestamp', 'sunrise', 'sunset']


def read_records():
    with LOCK:
        path = Path(AppConfig.WEATHER_FILE)
        if not path.exists():
            return []
        frame = pd.read_excel(path, dtype={'place': str})
        if frame.empty:
            return []
        frame = frame.where(pd.notna(frame), None)
        records = frame.to_dict(orient='records')
        return sorted(records, key=lambda row: str(row.get('timestamp') or ''), reverse=True)


def append(data):
    with LOCK:
        path = Path(AppConfig.WEATHER_FILE)
        path.parent.mkdir(parents=True, exist_ok=True)
        existing = pd.read_excel(path) if path.exists() else pd.DataFrame(columns=COLUMNS)
        updated = pd.concat([existing, pd.DataFrame(data)], ignore_index=True)
        # A temp file + atomic replace prevents a request reading a half-written workbook.
        fd, temp_path = tempfile.mkstemp(prefix='.weather-', suffix='.xlsx', dir=path.parent)
        os.close(fd)
        try:
            updated.to_excel(temp_path, index=False)
            os.replace(temp_path, path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
