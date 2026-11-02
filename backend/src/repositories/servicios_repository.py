from db.conexion_db import conexion

def obtener_servicios_activos():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM servicios WHERE activo = 1"
        )
        servicios = cursor.fetchall()
        return servicios
    finally:
        cursor.close()
        conn.close()
