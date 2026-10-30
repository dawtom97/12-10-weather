# Pogodnik — dashboard + automatyczne pobieranie danych

## Uruchomienie

1. Zainstaluj Python 3.10+.
2. W folderze projektu wykonaj `python -m pip install -r requirements.txt`.
3. Skopiuj `.env.example` do `.env` i wpisz swój klucz `API_KEY` z OpenWeatherMap (Current Weather Data).
4. Wykonaj `python main.py`.
5. Otwórz http://127.0.0.1:5000/wyniki (lub stronę główną http://127.0.0.1:5000/).

Dashboard działa w serwerze Flask, a zbieranie danych odbywa się w oddzielnym wątku. Pierwsze pobranie rozpoczyna się przy starcie aplikacji, kolejne co `UPDATE_INTERVAL` sekund (minimum 60). Domyślnie to 10 minut; dane bieżącej pogody z OpenWeatherMap mogą nie zmieniać się co minutę. Widok sprawdza aktualizacje co 15 sekund i odświeża się, gdy pojawi się nowy pomiar.

Archiwum jest zapisywane do Excela (`WEATHER_FILE`), a zapis jest atomowy i chroniony blokadą. MySQL jest **opcjonalny**: ustaw `DB_ENABLED=true`, skonfiguruj parametry DB i utwórz bazę danych wskazaną przez `DB_NAME` (tabela `records` tworzy się automatycznie). Gdy MySQL jest niedostępny, pomiary nadal są zapisywane do Excela. Wyszukiwanie miasta jest jednorazowym zapytaniem i nie zmienia miasta cyklicznego zbierania; to ustawia `API_CITY` w `.env`.

## Adresy

- `/` — strona główna
- `/wyniki` — dashboard i historia pomiarów
- `/wyszukaj` — wyszukiwanie pogody innego miasta
- `/api/pomiary` — JSON z najnowszymi 100 pomiarami

## Bezpieczeństwo

Nie udostępniaj pliku `.env`: może zawierać klucz API i hasło bazy danych. Archiwum ZIP nie zawiera prawdziwego `.env`. Jeśli wcześniej udostępniłeś klucz API lub hasło, rozważ ich zmianę.

## Dalsze ulepszenia

Przy dużej liczbie pomiarów warto przenieść historię z Excela do SQLite/MySQL, zastosować paginację i uruchamiać harmonogram jako osobny proces (np. APScheduler/Celery), jeśli dashboard będzie działać na wielu instancjach.
