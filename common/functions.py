from datetime import datetime

temp_c = lambda temp: round(temp - 273.15, 2)

km_h = lambda wind: round(wind * 3.6, 2)

timestamp = lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S")

time_dt = lambda time: datetime.fromtimestamp(time).strftime("%H:%M:%S")