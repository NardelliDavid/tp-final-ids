import mysql.connector

def conexion():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="david",
        database="cine_paradiso"
    )
    return conexion

def consultar_db(consulta_sql):
    conn = conexion()
    cursor = conn.cursor()

    cursor.execute(consulta_sql)
    consulta = cursor.fetchall()

    cursor.close()
    conn.close()

    return consulta

def insertar_datos(consulta_sql, valores):
    try:
        conn = conexion()
        cursor = conn.cursor()

        cursor.execute(consulta_sql, valores)
        conn.commit()

        cursor.close()
        conn.close()

        return {"OK": "Datos insertados correctamente"}, 200

    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()

        return {"Error": str(e)}, 400

def eliminar_datos(consulta_sql, valores):
    try:
        conn = conexion()
        cursor = conn.cursor()

        cursor.execute(consulta_sql, valores)
        conn.commit()

        cursor.close()
        conn.close()

        return {"OK": "Datos eliminados correctamente"}, 200

    except Exception as e:
        conn.rollback()
        cursor.close()
        conn.close()

        return {"Error": str(e)}, 400