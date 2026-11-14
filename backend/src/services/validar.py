from werkzeug.security import generate_password_hash, check_password_hash  # encripta la contraseña
from itsdangerous import URLSafeTimedSerializer  # crea el token de seguridad
from db.conexion_db import conexion  # Importa la función que conecta a MySQL

serializador = URLSafeTimedSerializer("mi_clave_segura")


# Lógica del Endpoint de Registro (POST /auth/registro)
def registrar_usuario(nombre, email, password):
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

        return {"id": nuevo_id, "nombre": nombre, "email": email}, 201
    except Exception:
        return {"mensaje": "El email ya se encuentra registrado o hubo un error en la BD"}, 400


# Lógica del Endpoint de Login (POST /auth/login)
def autenticar_usuario(email, password):
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

                return {
                    "mensaje": "Inicio de sesión exitoso",
                    "token": token_real,  # <-- Aquí devolvemos el token real que pide el enunciado
                    "usuario": {
                        "id": db_id,
                        "nombre": db_nombre,
                        "email": db_email,
                        "rol": db_rol
                    }
                }, 200

        return {"mensaje": "Email o contraseña incorrectos"}, 401
    except Exception:
        return {"mensaje": "Hubo un error en el servidor al intentar iniciar sesión"}, 500


# Función de seguridad (Guardia) que antes estaba en perfil.py
def verificar_token(auth_header):
    """
    Lee la cabecera 'Authorization', extrae el token y lo desencripta
    para obtener el email del usuario que tiene la sesión activa.
    """
    if not auth_header:
        return None

    try:
        # Saca la palabra Bearer si viene en la cabecera para quedarnos solo con el token
        if "Bearer " in auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = auth_header

        # Desencripta usando la misma clave y sal del login
        email = serializador.loads(token, salt="auth-salt")
        return email
    except Exception:
        return None  # Si el token es inválido o expiró, rebota la petición
