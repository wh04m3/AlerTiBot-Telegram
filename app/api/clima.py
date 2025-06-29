import requests
import json
import config

# API de OpenWeatherMap
WEATHER_API_KEY = config.OPENWEATHER_TOKEN

# === FUNCIONES ===

def obtener_datos_climaticos(lat, long):
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={long}&lang=esunits=metric&appid={WEATHER_API_KEY}'
    response = requests.get(url)
   # print(response.json())  # falla
    datos = response.json()

    # Guardarlos en un archivo local
    with open("datos_climaticos.json", "w", encoding='utf-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

    print("✅ Datos guardados en 'datos_climaticos.json'")
    return response.json()

def resumen_clima_actual():
    try:
        with open("datos_climaticos.json", "r", encoding="utf-8") as f:
            datos = json.load(f)

        clima = datos["current"]
        clima_main = clima["weather"][0]["main"]
        descripcion = clima["weather"][0]["description"].capitalize()
        temp = clima["temp"] - 273.15  # Kelvin a Celsius
        humedad = clima["humidity"]
        viento = clima["wind_speed"]
        lluvia = clima.get("rain", {}).get("1h", 0)

        estado = "☁️ Estado del clima: " + descripcion
        detalles = (
            f"🌡 Temperatura: {temp:.1f} °C | 💧 Humedad: {humedad}%\n"
            f"🌬 Viento: {viento:.1f} km/h"
        )

        if lluvia > 0:
            detalles += f"\n🌧 Lluvia en la última hora: {lluvia:.2f} mm"

        return f"{estado}\n{detalles}"

    except Exception as e:
        return f"⚠️ Error al leer los datos del clima: {e}"