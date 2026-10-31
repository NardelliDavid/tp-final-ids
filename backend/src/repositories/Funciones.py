from backend.db.conexion_db import conexion

# GET /funciones/{id}/butacas
def obtener_datos_butacas(funcion_id):
    respuesta = None

    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    # Obtiene las filas y columnas de la sala de la función.
    consulta = """
        SELECT salas.filas, salas.columnas
        FROM funciones
        INNER JOIN salas ON funciones.sala_id = salas.id
        WHERE funciones.id = %s
    """

    cursor.execute(consulta, (funcion_id,))
    sala = cursor.fetchone()

    if sala is not None:

        # Busca las butacas que pertenecen a compras no canceladas.
        consulta = """
            SELECT entradas.fila, entradas.columna
            FROM entradas
            INNER JOIN compras ON entradas.compra_id = compras.id
            WHERE entradas.funcion_id = %s
            AND compras.estado != 'cancelada'
            AND entradas.estado != 'cancelada'
        """

        cursor.execute(consulta, (funcion_id,))
        ocupadas = cursor.fetchall()

        respuesta = {
            "filas": sala["filas"],
            "columnas": sala["columnas"],
            "ocupadas": ocupadas
        }

    cursor.close()
    conn.close()

    return respuesta