from werkzeug.security import generate_password_hash, check_password_hash  # Encripta y valida contraseñas
# itsdangerous: firma datos y estampa la fecha/hora de creación para que el token expire
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from db.conexion_db import conexion

serializador = URLSafeTimedSerializer("mi_clave_segura")  # Clave secreta para firmar los tokens
TIEMPO_EXPIRACION = 3600  # Duración del token en segundos (3600 = 1 hora)


# Registro de usuarios (POST /auth/registro)
def registrar_usuario(nombre, email, password):
    password_encriptada = generate_password_hash(password)

    try:
        conn = conexion()
        cursor = conn.cursor()
        query = "INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nombre, email, password_encriptada, "cliente"))

        conn.commit()
        nuevo_id = cursor.lastrowid
        cursor.close()
        conn.close()

        return {"id": nuevo_id, "nombre": nombre, "email": email}, 201
    except Exception:
        return {"mensaje": "El email ya se encuentra registrado o hubo un error en la BD"}, 400


# Login de usuarios (POST /auth/login)
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
                # Firma el email con la hora actual (dumps) y una sal específica para auth
                token_real = serializador.dumps(db_email, salt="auth-salt")

                return {
                    "mensaje": "Inicio de sesión exitoso",
                    "token": token_real,
                    "expira_en": TIEMPO_EXPIRACION,
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


# Guardia de seguridad: valida el token recibido en el header Authorization
def verificar_token(auth_header):
    if not auth_header:
        return None

    try:
        # Quita el prefijo "Bearer " si viene incluido
        token = auth_header.split(" ")[1] if "Bearer " in auth_header else auth_header

        # Verifica la firma y comprueba que no haya superado max_age (en segundos)
        email = serializador.loads(token, salt="auth-salt", max_age=TIEMPO_EXPIRACION)
        return email
    except (SignatureExpired, BadSignature, Exception):
        return None  # Token vencido o adulterado
