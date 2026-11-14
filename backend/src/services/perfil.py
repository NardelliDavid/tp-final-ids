from werkzeug.security import check_password_hash, generate_password_hash
from db.conexion_db import conexion


# Lógica del endpoint GET /usuarios/me (Obtener los datos del perfil del usuario actual)
def consultar_datos_perfil(email_usuario):
    try:
        conn = conexion()
        cursor = conn.cursor()

        # Busca en la BD los datos del dueño de ese email
        query = "SELECT id, nombre, email, rol FROM usuarios WHERE email = %s"
        cursor.execute(query, (email_usuario,))
        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario:
            db_id, db_nombre, db_email, db_rol = usuario
            # Retorna la estructura exacta que te pide la captura (Salida 200)
            return {
                "id": db_id,
                "nombre": db_nombre,
                "email": db_email,
                "rol": db_rol
            }, 200

        return {"mensaje": "Usuario no encontrado"}, 404
    except Exception:
        return {"mensaje": "Hubo un error al conectar con la base de datos"}, 500


# Lógica del endpoint PATCH /usuarios/me (Modificar campos editables: nombre o contraseña)
def actualizar_datos_perfil(email_usuario, nombre_nuevo, pwd_actual, pwd_nueva):
    try:
        conn = conexion()
        cursor = conn.cursor()

        # Obtiene primero los datos actuales guardados en la BD
        query_select = "SELECT id, password_hash FROM usuarios WHERE email = %s"
        cursor.execute(query_select, (email_usuario,))
        usuario = cursor.fetchone()

        if not usuario:
            cursor.close()
            conn.close()
            return {"mensaje": "Usuario no encontrado"}, 404

        db_id, db_password_hash = usuario

        # CASO A: El usuario quiere actualizar su Contraseña
        if pwd_nueva:
            # Regla estricta del enunciado: Para cambiarla obliga a enviar la actual
            if not pwd_actual:
                cursor.close()
                conn.close()
                return {"mensaje": "Para cambiar la contraseña hay que enviar la actual"}, 400

            # Verifica si la contraseña actual escrita coincide con el hash almacenado
            if not check_password_hash(db_password_hash, pwd_actual):
                cursor.close()
                conn.close()
                return {"mensaje": "la contraseña actual es incorrecta"}, 401

            # Si es válida, encriptamos la nueva de forma segura
            nuevo_hash = generate_password_hash(pwd_nueva)
            query_update = "UPDATE usuarios SET password_hash = %s WHERE id = %s"
            cursor.execute(query_update, (nuevo_hash, db_id))

        # CASO B: El usuario quiere actualizar solo su Nombre
        if nombre_nuevo:
            query_update = "UPDATE usuarios SET nombre = %s WHERE id = %s"
            cursor.execute(query_update, (nombre_nuevo, db_id))

        conn.commit()
        cursor.close()
        conn.close()

        return {"mensaje": "el usuario actualizado."}, 200
    except Exception:
        return {"mensaje": "datos inválidos."}, 400


# Lógica del endpoint GET /usuarios/me/historial (Reunir compras y películas vistas)
def consultar_historial_usuario(email_usuario):
    try:
        conn = conexion()
        # Indica dictionary=True para que devuelva las filas estructuradas como JSON nativo
        cursor = conn.cursor(dictionary=True)

        # Primero localiza el ID numérico de nuestro usuario mediante su email
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email_usuario,))
        user_res = cursor.fetchone()
        if not user_res:
            cursor.close()
            conn.close()
            return {"mensaje": "Usuario no encontrado"}, 404

        usuario_id = user_res['id']

        # Une las tablas necesarias usando JOINs para armar el mapa del enunciado
        query_compras = """
            SELECT 
                c.id, c.fecha, c.estado, c.total,
                p.titulo AS pelicula, s.local, s.nombre AS sala, f.inicio
            FROM compras c
            JOIN entradas e ON c.id = e.compra_id
            JOIN funciones f ON e.funcion_id = f.id
            JOIN peliculas p ON f.pelicula_id = p.id
            JOIN salas s ON f.sala_id = s.id
            WHERE c.usuario_id = %s
            GROUP BY c.id
        """
        cursor.execute(query_compras, (usuario_id,))
        compras_raw = cursor.fetchall()

        lista_compras_final = []
        for c in compras_raw:
            compra_id = c['id']

            # Busca qué butacas se compraron asociadas a este número de compra
            cursor.execute("SELECT fila, columna FROM entradas WHERE compra_id = %s", (compra_id,))
            entradas = cursor.fetchall()
            # Las formateamos como pide tu captura: ["c7", "c8"]
            butacas = [f"c{e['columna']}" for e in entradas]

            # Busca qué servicios adicionales (Combos/Comida) se compraron
            query_servicios = """
                SELECT s.nombre, cs.cantidad 
                FROM compra_servicios cs
                JOIN servicios s ON cs.servicio_id = s.id
                WHERE cs.compra_id = %s
            """
            cursor.execute(query_servicios, (compra_id,))
            servicios = cursor.fetchall()

            # Estructura de la compra individual idéntica a tu guía de salida
            lista_compras_final.append({
                "id": compra_id,
                "fecha": c['fecha'].isoformat() if c['fecha'] else "",
                "estado": c['estado'],
                "pelicula": c['pelicula'],
                "local": c['local'],
                "sala": c['sala'],
                "inicio": c['inicio'].isoformat() if c['inicio'] else "",
                "butacas": butacas,
                "servicios": servicios,
                "total": float(c['total'])
            })

        # Una película figura como "vista" si el QR de la compra está validado (estado = 'utilizada')
        query_vistas = """
            SELECT DISTINCT p.id AS pelicula_id, p.titulo, p.poster_url, f.inicio AS fecha_funcion
            FROM compras c
            JOIN entradas e ON c.id = e.compra_id
            JOIN funciones f ON e.funcion_id = f.id
            JOIN peliculas p ON f.pelicula_id = p.id
            WHERE c.usuario_id = %s AND c.estado = 'utilizada'
        """
        cursor.execute(query_vistas, (usuario_id,))
        peliculas_vistas = cursor.fetchall()

        for p in peliculas_vistas:
            if p['fecha_funcion']:
                p['fecha_funcion'] = p['fecha_funcion'].isoformat()

        cursor.close()
        conn.close()

        # Devolvemos la salida estructurada completa requerida
        return {
            "compras": lista_compras_final,
            "peliculas_vistas": peliculas_vistas
        }, 200

    except Exception:
        return {"mensaje": "Hubo un error al procesar el historial en la base de datos"}, 500
