from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash # encripta la contraseña
from db.conexion_db import conexion # Importa la función que conecta a MySQL
from itsdangerous import URLSafeTimedSerializer # crea el token de seguridad

auth_bp = Blueprint('auth', __name__)
serializador = URLSafeTimedSerializer("mi_clave_segura")

# Endpoint de Registro
@auth_bp.route('/auth/registro', methods=['POST'])
def registro():
    datos = request.get_json()
    nombre = datos.get('nombre')
    email = datos.get('email')
    password = datos.get('password')
    
    if not nombre or not email or not password:
        return jsonify({"mensaje": "Faltan datos obligatorios"}), 400

    password_encriptada = generate_password_hash(password)

    try:
        conn = conexion()
        cursor = conn.cursor()
        query = "INSERT INTO usuarios (nombre, email, password_hash) VALUES (%s, %s, %s)"
        cursor.execute(query, (nombre, email, password_encriptada))
        conn.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        return jsonify({"id": nuevo_id, "nombre": nombre, "email": email}), 201
    except Exception as e:
        return jsonify({"mensaje": "El email ya se encuentra registrado o hubo un error en la BD"}), 400


# Endpoint de Login

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    datos = request.get_json()
    email = datos.get('email')
    password = datos.get('password')
    
    if not email or not password:
        return jsonify({"mensaje": "Faltan datos obligatorios"}), 400

    try:
        conn = conexion()
        cursor = conn.cursor()
        query = "SELECT id, nombre, email, password_hash, rol FROM usuarios WHERE email = %s"
        cursor.execute(query, (email,))
        usuario = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if usuario:
            db_id, db_nombre, db_email, db_password_hash, db_rol = usuario
            
            if check_password_hash(db_password_hash, password):
                # Genera un token encriptando el email del usuario 
                token_real = serializador.dumps(db_email, salt="auth-salt")
                
                return jsonify({
                    "mensaje": "Inicio de sesión exitoso",
                    "token": token_real, # <-- Aquí devolvemos el token real que pide el enunciado
                    "usuario": {
                        "id": db_id,
                        "nombre": db_nombre,
                        "email": db_email,
                        "rol": db_rol
                    }
                }), 200
        
        return jsonify({"mensaje": "Email o contraseña incorrectos"}), 401
    except Exception as e:
        return jsonify({"mensaje": "Hubo un error en el servidor al intentar iniciar sesión"}), 500
