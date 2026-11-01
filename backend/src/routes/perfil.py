from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from db.conexion_db import conexion
# Importamos el serializador de tokens desde tu archivo de endpoints para compartir la clave secreta
from src.routes.validar import serializador 

# Crea el Blueprint exclusivo para el módulo de Perfil
perfil_bp = Blueprint('perfil', __name__)

def obtener_usuario_autenticado():
    """
    Función de seguridad (Guardia).
    Lee la cabecera 'Authorization', extrae el token y lo desencripta
    para obtener el email del usuario que tiene la sesión activa.
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
        
    try:
        # saca la palabra Bearer  si viene en la cabecera para quedarnos solo con el token
        if "Bearer " in auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = auth_header
            
        # Desencripta usando la misma clave y sal del login
        email = serializador.loads(token, salt="auth-salt")
        return email
    except Exception:
        return None # Si el token es inválido o expiro, rebota la petición


# endpoint GET/usuarios/me  Obtener los datos del perfil del usuario actual
@perfil_bp.route('/usuarios/me', methods=['GET'])
def obtener_perfil():
    # Valida que el cliente tenga un token real y activo
    email_usuario = obtener_usuario_autenticado()
    if not email_usuario:
        return jsonify({"mensaje": "Token inválido o inexistente. No autorizado."}), 401
        
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
            return jsonify({
                "id": db_id,
                "nombre": db_nombre,
                "email": db_email,
                "rol": db_rol
            }), 200
            
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    except Exception:
        return jsonify({"mensaje": "Hubo un error al conectar con la base de datos"}), 500


# endpoint PATCH/usuarios/me Modificar campos editables (nombre o contraseña)
@perfil_bp.route('/usuarios/me', methods=['PATCH'])
def modificar_perfil():
    # Verifica autenticación
    email_usuario = obtener_usuario_autenticado()
    if not email_usuario:
        return jsonify({"mensaje": "No autorizado"}), 401
        
    datos = request.get_json()
    nombre_nuevo = datos.get('nombre')
    pwd_actual = datos.get('password_actual')
    pwd_nueva = datos.get('password_nueva')
    
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
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
            
        db_id, db_password_hash = usuario

        # CASO A: El usuario quiere actualizar su Contraseña
        if pwd_nueva:
            # Regla estricta del enunciado: Para cambiarla obliga a enviar la actual
            if not pwd_actual:
                cursor.close()
                conn.close()
                return jsonify({"mensaje": "Para cambiar la contraseña hay que enviar la actual"}), 400
                
            # Verifica si la contraseña actual escrita coincide con el hash almacenado
            if not check_password_hash(db_password_hash, pwd_actual):
                cursor.close()
                conn.close()
                return jsonify({"mensaje": "la contraseña actual es incorrecta"}), 401
                
            # Si es valida, encriptamos la nueva de forma segura
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
        
        return jsonify({"mensaje": "el usuario actualizado."}), 200
    except Exception:
        return jsonify({"mensaje": "datos inválidos."}), 400


# endpoint GET/usuarios/me/historial Reunir compras y películas vistas
@perfil_bp.route('/usuarios/me/historial', methods=['GET'])
def obtener_historial():
    # Verificamos autenticación
    email_usuario = obtener_usuario_autenticado()
    if not email_usuario:
        return jsonify({"mensaje": "No autorizado"}), 401
        
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
            return jsonify({"mensaje": "Usuario no encontrado"}), 404
            
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
            
            # Busca que butacas se compraron asociadas a este número de compra
            cursor.execute("SELECT fila, columna FROM entradas WHERE compra_id = %s", (compra_id,))
            entradas = cursor.fetchall()
            # Las formateamos como pide tu captura: ["c7", "c8"]
            butacas = [f"c{e['columna']}" for e in entradas]
            
            # Busca que servicios adicionales (Combos/Comida) se compraron
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
        return jsonify({
            "compras": lista_compras_final,
            "peliculas_vistas": peliculas_vistas
        }), 200
        
    except Exception as e:
        return jsonify({"mensaje": "Hubo un error al procesar el historial en la base de datos"}), 500
