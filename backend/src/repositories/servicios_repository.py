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


def crear_servicio(nombre, descripcion, precio):

    conn = conexion()
    cursor = conn.cursor()

    try:
        
        sql = "INSERT INTO servicios (nombre, descripcion, precio) VALUES (%s, %s, %s)"
        valores = (nombre, descripcion, precio)
        cursor.execute(sql, valores)

        conn.commit()

        return cursor.lastrowid

    except Exception:
        conn.rollback()  #deshace los cambios pendientes de la transaccion
        raise        #vuelve a lanzar la excepción que ocurrió, para que otra parte del programa pueda manejarla.

    finally:
        cursor.close()
        conn.close()
        

def modificar_servicio(id_servicio, datos):

    conn = conexion()
    cursor = conn.cursor()
    modificado = False

    try:
        cursor.execute(
            "SELECT id FROM servicios WHERE id = %s",
            (id_servicio,)
        )

        if cursor.fetchone() is not None:

            campos = []
            valores = []

            for campo in ("nombre", "descripcion", "precio"):
                if campo in datos:
                    campos.append(campo + " = %s")
                    valores.append(datos[campo])

            sql = "UPDATE servicios SET " + ", ".join(campos) + " WHERE id = %s"

            valores.append(id_servicio)

            cursor.execute(sql, tuple(valores))
            conn.commit()

            modificado = True

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

    return modificado


def eliminar_servicio(id_servicio):

    conn = conexion()
    cursor = conn.cursor()
    eliminado = False

    try:
        cursor.execute("SELECT id FROM servicios WHERE id = %s",(id_servicio,))

        if cursor.fetchone() is not None:

            cursor.execute("UPDATE servicios SET activo = 0 WHERE id = %s",(id_servicio,))

            conn.commit()
            eliminado = True

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

    return eliminado


    
