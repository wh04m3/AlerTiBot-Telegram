from api import clima
from telegram import Bot
from db import operaciones
from config import TELEGRAM_TOKEN


from telegram.ext import ApplicationBuilder
from telegram_bot.comandos import registrar_comandos


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Registra todos los comandos y callbacks
    registrar_comandos(app)

    # Ejecuta el bot (ya maneja el loop interno)
    app.run_polling()

if __name__ == "__main__":
    main()



# clima.obtener_datos_climaticos(19.372385, -98.913537)

# zonas = operaciones.ver_zonas()
# for zona in zonas:
#     print(f"ID: {zona['id_zona']}, Nombre: {zona['nombre']}, Lat: {zona['latitud']}, Long: {zona['longitud']}")
