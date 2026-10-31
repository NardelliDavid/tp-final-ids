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


# POST/funciones 
def obtener_duracion_pelicula(pelicula_id):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    consulta = """
        SELECT duracion_min
        FROM peliculas
        WHERE id = %s
    """

    cursor.execute(consulta, (pelicula_id,))
    pelicula = cursor.fetchone()

    cursor.close()
    conn.close()

    return pelicula


def existe_sala(sala_id):
    conn = conexion()
    cursor = conn.cursor()

    consulta = """
        SELECT id
        FROM salas
        WHERE id = %s
    """

    cursor.execute(consulta, (sala_id,))
    sala = cursor.fetchone()

    cursor.close()
    conn.close()

    return sala is not None


def existe_superposicion(sala_id, inicio, fin):
    conn = conexion()
    cursor = conn.cursor()

    consulta = """
        SELECT id
        FROM funciones
        WHERE sala_id = %s
        AND estado = 'activa'
        AND inicio < DATE_ADD(%s, INTERVAL 20 MINUTE)
        AND DATE_ADD(fin, INTERVAL 20 MINUTE) > %s
    """

    cursor.execute(consulta, (sala_id, fin, inicio))
    funcion = cursor.fetchone()

    cursor.close()
    conn.close()

    return funcion is not None


def crear_funcion(pelicula_id, sala_id, inicio, fin, precio):
    conn = conexion()
    cursor = conn.cursor()

    consulta = """
        INSERT INTO funciones (pelicula_id, sala_id, inicio, fin, precio)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(consulta, (pelicula_id, sala_id, inicio, fin, precio))
    conn.commit()

    funcion_id = cursor.lastrowid

    cursor.close()
    conn.close()

    return funcion_id


# PATCH	/funciones/{id}
def obtener_funcion_por_id(funcion_id):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    consulta = """
        SELECT id, pelicula_id, sala_id, inicio, fin, precio, estado
        FROM funciones
        WHERE id = %s
    """

    cursor.execute(consulta, (funcion_id,))
    funcion = cursor.fetchone()

    cursor.close()
    conn.close()

    return funcion


def actualizar_funcion(funcion_id, sala_id, inicio, fin, precio):
    conn = conexion()
    cursor = conn.cursor()

    consulta = """
        UPDATE funciones
        SET sala_id = %s,
            inicio = %s,
            fin = %s,
            precio = %s
        WHERE id = %s
    """

    cursor.execute(consulta, (sala_id, inicio, fin, precio, funcion_id))
    conn.commit()

    filas_modificadas = cursor.rowcount

    cursor.close()
    conn.close()

    return filas_modificadas

# DELETE/funciones/{id} 
def existe_funcion(funcion_id):
    conn = conexion()
    cursor = conn.cursor()

    consulta = """
        SELECT id
        FROM funciones
        WHERE id = %s
    """

    cursor.execute(consulta, (funcion_id,))
    funcion = cursor.fetchone()

    cursor.close()
    conn.close()

    return funcion is not None


def tiene_compras_activas(funcion_id):
    conn = conexion()
    cursor = conn.cursor()

    consulta = """
        SELECT compras.id
        FROM compras
        INNER JOIN entradas ON compras.id = entradas.compra_id
        WHERE entradas.funcion_id = %s
        AND compras.estado = 'activa'
        LIMIT 1
    """

    cursor.execute(consulta, (funcion_id,))
    compra = cursor.fetchone()

    cursor.close()
    conn.close()

    return compra is not None


def dar_de_baja_funcion(funcion_id):
    conn = conexion()
    cursor = conn.cursor()

    consulta = """
        UPDATE funciones
        SET estado = 'cancelada'
        WHERE id = %s
    """

    cursor.execute(consulta, (funcion_id,))
    conn.commit()

    cursor.close()
    conn.close()