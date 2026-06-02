import mysql.connector

conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="biblioteca1"
)

cursor = conexion.cursor()