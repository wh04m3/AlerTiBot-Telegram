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