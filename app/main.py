from api import clima
from telegram import Bot
from db import operaciones

clima.obtener_datos_climaticos(19.372385, -98.913537)

zonas = operaciones.ver_zonas()
for zona in zonas:
    print(f"ID: {zona['id_zona']}, Nombre: {zona['nombre']}, Lat: {zona['latitud']}, Long: {zona['longitud']}")
