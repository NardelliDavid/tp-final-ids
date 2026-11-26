# puente entre python y MySQL
from dotenv import load_dotenv
import os
import mysql.connector

# Busca el archivo oculto .env en el proyecto y carga sus claves (DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE) como variables de entorno en la memoria del sistema
load_dotenv()

def conexion():
    conexion = mysql.connector.connect(
# os.getenv("DB_PASSWORD") da seguridad y permite que cada compañero pueda tener una contraseña distinta en su XAMPP/MySQL local sin tener que modificar el código compartido
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_DATABASE")
    )
    return conexion