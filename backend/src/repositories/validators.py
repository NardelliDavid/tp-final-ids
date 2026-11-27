from db.conexion_db import conexion

def buscar_usuario_por_mail(email):

    if email:
        con = conexion()
        cursor = con.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM usuarios WHERE email = %s",
            (email,)
        )
        usuario = cursor.fetchone()
        cursor.close()
        con.close()

    return usuario