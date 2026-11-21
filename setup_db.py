from werkzeug.security import generate_password_hash
from backend.db.conexion_db import conexion

# Usuarios de prueba para el sistema
USUARIOS = [
    ("Admin", "admin@cineparadiso.com", "admin123", "administrador"),
    ("Juan", "juan@test.com", "juan123", "cliente"),
    ("Ana", "ana@test.com", "ana123", "cliente"),
]

SQL_INSERT = """
    INSERT INTO usuarios (nombre, email, password_hash, rol)
    VALUES (%s, %s, %s, %s)
"""

# Prepara los datos de los usuarios en la constante
def preparar_datos(usuarios):
    datos = []
    for nombre, email, clave, rol in usuarios:
        clave_hash = generate_password_hash(clave)
        datos.append((nombre, email, clave_hash, rol))
    return datos

# Funcion para ejecutar el codigo SQL en los archivos datos_ejemplo.sql y init_db.sql
def ejecutar_script(cur, ruta):
    with open(ruta, "r", encoding="utf-8") as archivo:
        script_sql = archivo.read()
    for sentencia in script_sql.split(";"):
        sentencia = sentencia.strip()
        if sentencia:
            cur.execute(sentencia)

def main():
    con = conexion()
    cur = con.cursor()
    try:
        ejecutar_script(cur, "backend/db/init_db.sql")
        con.commit()
        print("Se creó la base de datos exitosamente.")

        cur.executemany(SQL_INSERT, preparar_datos(USUARIOS))
        con.commit()
        print(f"{cur.rowcount} usuarios insertados.")

        ejecutar_script(cur, "backend/db/datos_ejemplo.sql")
        con.commit()
        print("Se insertaron datos de ejemplo para testeo.")
    except Exception:
        con.rollback()
        raise
    finally:
        cur.close()
        con.close()


if __name__ == "__main__":
    main()