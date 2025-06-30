from db import conexion
def insertar_reporte(nivel, zona, usuario):
    conn = conexion.get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reportes (nivel, zona, usuario) VALUES (%s, %s, %s)", (nivel, zona, usuario))
    conn.commit()
    conn.close()
def ver_zonas():
    conn = conexion.get_connection()
    cursor = conn.cursor(dictionary=True)  # devuelve resultados como diccionario
    cursor.execute("SELECT * FROM zona")
    resultados = cursor.fetchall()         # recupera todos los resultados
    conn.close()
    return resultados



def consultar_historico_inundaciones(id_zona):
    conn = conexion.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM historico_inundaciones WHERE id_zona = %s", (id_zona,))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def consultar_pronostico_actual(id_zona):
    conn = conexion.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pronostico_clima WHERE id_zona = %s ORDER BY fecha DESC LIMIT 1", (id_zona,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def consultar_pronostico_hoy_manana(id_zona):
    from datetime import datetime, timedelta
    conn = conexion.get_connection()
    cursor = conn.cursor(dictionary=True)
    hoy = datetime.now().date()
    manana = hoy + timedelta(days=1)
    cursor.execute("SELECT * FROM pronostico_clima WHERE id_zona = %s AND (DATE(fecha) = %s OR DATE(fecha) = %s)", (id_zona, hoy, manana))
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def ver_zonas():
    conn = conexion.get_connection()
    cursor = conn.cursor(dictionary=True)  # devuelve resultados como diccionario
    cursor.execute("SELECT * FROM zona")
    resultados = cursor.fetchall()         # recupera todos los resultados
    conn.close()
    return resultados