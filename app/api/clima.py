import requests
import json
import config

# API de OpenWeatherMap
WEATHER_API_KEY = config.OPENWEATHER_TOKEN
CIUDAD = 'Chicoloapan,mx'

# === FUNCIONES ===

def obtener_datos_climaticos(lat, long):
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={long}&lang=esunits=metric&appid=9fa883a0584496cc0625733033f37b62'
    response = requests.get(url)
   # print(response.json())  # falla
    datos = response.json()

    # Guardarlos en un archivo local
    with open("datos_climaticos.json", "w", encoding='utf-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

    print("✅ Datos guardados en 'datos_climaticos.json'")
    return response.json()
