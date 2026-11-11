import os
import mysql.connector

def conexion():
    conexion = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ.get("DB_NAME", "cine_paradiso")
    )
    return conexion