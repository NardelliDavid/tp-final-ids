from datetime import datetime
from secrets import token_urlsafe
from mysql.connector import Error
from db.conexion_db import conexion
from datetime import timedelta


def obtener_funcion(funcion_id):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
            SELECT f.id, f.precio, f.inicio, s.filas, s.columnas
            FROM funciones f
            INNER JOIN salas s ON f.sala_id = s.id
            WHERE f.id = %s
        """
        cursor.execute(sql, (funcion_id,))
        funcion = cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

    return funcion


def butaca_esta_ocupada(funcion_id, fila, columna):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    ocupada = False

    try:
        sql = """
            SELECT id
            FROM entradas
            WHERE funcion_id = %s
              AND fila = %s
              AND columna = %s
              AND estado != 'cancelada'
            LIMIT 1
        """
        cursor.execute(sql, (funcion_id, fila, columna))

        if cursor.fetchone() is not None:
            ocupada = True
    finally:
        cursor.close()
        conn.close()

    return ocupada


def registrar_compra(email_usuario, funcion_id, butacas, servicios):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    mensaje = "No se pudo registrar la compra"
    respuesta = None
    codigo = 500

    try:
        conn.start_transaction() #conn.start_transaction(): Inicia una transacción que agrupa varias operaciones SQL, permitiendo confirmar todos los cambios juntos con commit() o deshacerlos con rollback() si ocurre un error, evitando que la compra quede registrada parcialmente.

        # Bloquea esta función hasta confirmar o cancelar la compra.
        cursor.execute("""
            SELECT id, precio, inicio
            FROM funciones
            WHERE id = %s
            FOR UPDATE
        """, (funcion_id,))
        funcion = cursor.fetchone()

        if funcion is None:
            mensaje = "Función no encontrada"
            codigo = 404

        elif funcion["inicio"] <= datetime.now():
            mensaje = "La función ya comenzó"
            codigo = 422

        else:
            cursor.execute(
                "SELECT id, rol FROM usuarios WHERE email = %s",
                (email_usuario,)
            )
            usuario = cursor.fetchone()

            if usuario is None:
                mensaje = "Usuario no encontrado"
                codigo = 401

            elif usuario["rol"] != "cliente":
                mensaje = "No tenés permiso para comprar entradas"
                codigo = 403

            else:
                # Segunda comprobación de ocupación, dentro de la transacción.
                ocupada = False

                for fila, columna in butacas:
                    cursor.execute("""
                        SELECT id FROM entradas
                        WHERE funcion_id = %s
                          AND fila = %s
                          AND columna = %s
                          AND estado != 'cancelada'
                        LIMIT 1
                    """, (funcion_id, fila, columna))

                    if cursor.fetchone() is not None:
                        ocupada = True

                if ocupada:
                    mensaje = "Una o más butacas están ocupadas"
                    codigo = 409

                else:
                    total = funcion["precio"] * len(butacas)
                    servicios_para_guardar = []
                    servicio_invalido = False

                    # Los precios se consultan en MySQL, no en el JSON.
                    for servicio in servicios:
                        cursor.execute("""
                            SELECT id, precio
                            FROM servicios
                            WHERE id = %s AND activo = 1
                            FOR UPDATE
                        """, (servicio["servicio_id"],))
                        info = cursor.fetchone()

                        if info is None:
                            servicio_invalido = True
                        else:
                            cantidad = servicio["cantidad"]
                            total += info["precio"] * cantidad
                            servicios_para_guardar.append(
                                (info["id"], cantidad, info["precio"])
                            )

                    if servicio_invalido:
                        mensaje = "Uno o más servicios no existen o están inactivos"
                        codigo = 422

                    else:
                        # Token que luego se representará como imagen QR.
                        codigo_qr = token_urlsafe(32)

                        cursor.execute("""
                            INSERT INTO compras (usuario_id, total, codigo_qr, estado)
                            VALUES (%s, %s, %s, 'activa')
                        """, (usuario["id"], total, codigo_qr))
                        compra_id = cursor.lastrowid

                        for fila, columna in butacas:
                            cursor.execute("""
                                INSERT INTO entradas
                                    (compra_id, funcion_id, fila, columna, precio)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (
                                compra_id, funcion_id, fila, columna, funcion["precio"]
                            ))

                        for servicio_id, cantidad, precio_unitario in servicios_para_guardar:
                            cursor.execute("""
                                INSERT INTO compra_servicios
                                    (compra_id, servicio_id, cantidad, precio_unitario)
                                VALUES (%s, %s, %s, %s)
                            """, (compra_id, servicio_id, cantidad, precio_unitario))

                        respuesta = {
                            "mensaje": "Compra creada correctamente",
                            "id": compra_id,
                            "estado": "activa",
                            "total": float(total),
                            "codigo_qr": codigo_qr,
                        }
                        codigo = 201

        if codigo == 201:
            conn.commit()
        else:
            conn.rollback()

    except Error:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()

    if respuesta is None:
        respuesta = {"mensaje": mensaje}

    return respuesta, codigo

def obtener_detalle_compra(id_compra, email_usuario):

    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT c.id, c.fecha, c.estado, c.total, c.codigo_qr,
                   u.email AS email_duenio
            FROM compras c
            INNER JOIN usuarios u ON u.id = c.usuario_id
            WHERE c.id = %s
        """, (id_compra,))

        compra = cursor.fetchone()

        if compra is None:
            return {"mensaje": "Compra no encontrada"}, 404

        if compra["email_duenio"] != email_usuario:
            return {"mensaje": "No tenés permiso para consultar esta compra"}, 403

        cursor.execute("""
            SELECT e.fila, e.columna, e.precio, e.estado,
                   f.id AS funcion_id, f.inicio, f.fin,
                   p.titulo AS pelicula,
                   s.local, s.nombre AS sala
            FROM entradas e
            INNER JOIN funciones f ON f.id = e.funcion_id
            INNER JOIN peliculas p ON p.id = f.pelicula_id
            INNER JOIN salas s ON s.id = f.sala_id
            WHERE e.compra_id = %s
            ORDER BY e.fila, e.columna
        """, (id_compra,))

        filas_entradas = cursor.fetchall()

        entradas = []
        funcion = None

        for entrada in filas_entradas:

            entradas.append({
                "butaca": f'{entrada["fila"]}{entrada["columna"]}',
                "precio": float(entrada["precio"]),
                "estado": entrada["estado"]
            })

            if funcion is None:
                funcion = {
                    "id": entrada["funcion_id"],
                    "pelicula": entrada["pelicula"],
                    "local": entrada["local"],
                    "sala": entrada["sala"],
                    "inicio": entrada["inicio"].isoformat(),
                    "fin": entrada["fin"].isoformat()
                }

        cursor.execute("""
            SELECT cs.servicio_id, s.nombre, cs.cantidad, cs.precio_unitario
            FROM compra_servicios cs
            INNER JOIN servicios s ON s.id = cs.servicio_id
            WHERE cs.compra_id = %s
            ORDER BY cs.id
        """, (id_compra,))

        filas_servicios = cursor.fetchall()

        servicios = []

        for servicio in filas_servicios:

            precio_unitario = float(servicio["precio_unitario"])
            cantidad = servicio["cantidad"]

            servicios.append({
                "servicio_id": servicio["servicio_id"],
                "nombre": servicio["nombre"],
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "subtotal": round(precio_unitario * cantidad, 2)
            })

        respuesta = {
            "id": compra["id"],
            "estado": compra["estado"],
            "fecha": compra["fecha"].isoformat(),
            "funcion": funcion,
            "entradas": entradas,
            "servicios": servicios,
            "total": float(compra["total"]),
            "codigo_qr": compra["codigo_qr"]
        }

        return respuesta, 200

    finally:
        cursor.close()
        conn.close()

def cancelar_compra(id_compra, email_usuario):

    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    try:
        conn.start_transaction()

        cursor.execute("""
            SELECT c.id, c.estado, u.email AS email_duenio
            FROM compras c
            INNER JOIN usuarios u ON u.id = c.usuario_id
            WHERE c.id = %s
            FOR UPDATE
        """, (id_compra,))

        compra = cursor.fetchone()

        if compra is None:
            respuesta = {"mensaje": "Compra no encontrada"}
            codigo = 404

        elif compra["email_duenio"] != email_usuario:
            respuesta = {"mensaje": "No tenés permiso para cancelar esta compra"}
            codigo = 403

        elif compra["estado"] != "activa":
            respuesta = {"mensaje": "La compra ya fue cancelada o utilizada"}
            codigo = 409

        else:
            cursor.execute("""
                SELECT MIN(f.inicio) AS inicio,
                       COUNT(*) AS cantidad_entradas,
                       SUM(e.estado != 'activa') AS entradas_no_activas
                FROM entradas e
                INNER JOIN funciones f ON f.id = e.funcion_id
                WHERE e.compra_id = %s
            """, (id_compra,))

            datos_funcion = cursor.fetchone()

            if datos_funcion["cantidad_entradas"] == 0:
                respuesta = {"mensaje": "La compra no tiene entradas"}
                codigo = 409

            elif datos_funcion["entradas_no_activas"]:
                respuesta = {"mensaje": "La compra tiene entradas que ya no están activas"}
                codigo = 409

            elif datos_funcion["inicio"] < datetime.now() + timedelta(hours=2):
                respuesta = {
                    "mensaje": "No se puede cancelar con menos de 2 horas de anticipación"
                }
                codigo = 422

            else:
                cursor.execute("""
                    UPDATE compras
                    SET estado = 'cancelada'
                    WHERE id = %s
                """, (id_compra,))

                cursor.execute("""
                    UPDATE entradas
                    SET estado = 'cancelada'
                    WHERE compra_id = %s
                """, (id_compra,))

                respuesta = {
                    "mensaje": "Compra cancelada correctamente",
                    "id": id_compra,
                    "estado": "cancelada"
                }

                codigo = 200

        if codigo == 200:
            conn.commit()
        else:
            conn.rollback()

        return respuesta, codigo

    except Exception:
        conn.rollback()
        raise

    finally:
        cursor.close()
        conn.close()