import requests
from telegram import Bot
import json

# === CONFIGURACIÓN ===

# Token de tu bot de Telegram (cámbialo por el tuyo)
TELEGRAM_TOKEN = '7627891801:AAEoV04-jl0SDDIkHiqWKl2UpQRfv9l4QdA'
CHAT_ID = '862103430'  # Puede ser tu usuario o grupo

# API de OpenWeatherMap
WEATHER_API_KEY = '9fa883a0584496cc0625733033f37b62'
CIUDAD = 'Chicoloapan,mx'

# === FUNCIONES ===

def obtener_datos_climaticos():
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={CIUDAD}&appid={WEATHER_API_KEY}&units=metric&lang=es'
    response = requests.get(url)
   # print(response.json())  # 👈 Añade esta línea para ver qué está fallando
    datos = response.json()

    # Guardarlos en un archivo local
    with open("datos_climaticos.json", "w", encoding='utf-8') as archivo:
        json.dump(datos, archivo, ensure_ascii=False, indent=4)

    print("✅ Datos guardados en 'datos_climaticos.json'")
    return response.json()


def evaluar_riesgo(datos):
    for pronostico in datos['list'][:8]:  # Próximas 24 horas (8 bloques de 3h)
        if 'rain' in pronostico and pronostico['rain'].get('3h', 0) > 50:
            return True
    return False

def enviar_alerta():
    bot = Bot(token=TELEGRAM_TOKEN)
    bot.send_message(
        chat_id=CHAT_ID,
        text='🚨 *ALERTA DE INUNDACIÓN* 🚨\nSe esperan lluvias intensas en las próximas horas en Chicoloapan. Toma precauciones.',
        parse_mode='Markdown'
    )

# === PROGRAMA PRINCIPAL ===

def main():
    clima = obtener_datos_climaticos()
    if evaluar_riesgo(clima):
        enviar_alerta()
    else:
        print("No se detectó riesgo de inundación.")

if __name__ == "__main__":
    main()
