from db import operaciones

def prueba():
    zonas = operaciones.ver_zonas()
    for zona in zonas:
        print(f"ID: {zona['id_zona']}, Nombre: {zona['nombre']}, Lat: {zona['latitud']}, Long: {zona['longitud']}")
