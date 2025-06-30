from db import operaciones
from datetime import datetime

def prueba():
    zonas = operaciones.ver_zonas()
    for zona in zonas:
        print(f"ID: {zona['id_zona']}, Nombre: {zona['nombre']}, Lat: {zona['latitud']}, Long: {zona['longitud']}")



def motor_inferencia_alertas():
    zonas = operaciones.ver_zonas()
    for zona in zonas:
        id_zona = zona['id_zona']
        nombre_zona = zona['nombre']
        historico = operaciones.consultar_historico_inundaciones(id_zona)
        pronosticos = operaciones.consultar_pronostico_hoy_manana(id_zona)
        # Determinar si hay riesgo de inundación
        riesgo = False
        for pronostico in pronosticos:
            if pronostico['precipitacion_mm'] and pronostico['precipitacion_mm'] > 10:  # umbral ejemplo
                if historico:
                    riesgo = True
        if riesgo:
            print(f"ALERTA: Posible inundación en {nombre_zona}")
            # Aquí podrías insertar una alerta en la base de datos
            # operaciones.insertar_alerta(id_zona, datetime.now(), nivel_riesgo, 'Generada por motor de inferencia')
        else:
            print(f"Zona {nombre_zona} sin riesgo de inundación")