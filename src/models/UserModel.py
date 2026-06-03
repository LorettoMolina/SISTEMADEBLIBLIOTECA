import bcrypt
from src.models.databaseModel import cursor, conexion


class UserModel:

    @staticmethod
    def registrar(nombre, apellido, telefono, correo, password):

        password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        cursor.execute(
            """
            INSERT INTO usuarios
            (nombre, apellido, telefono, correo, contrasena)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (nombre, apellido, telefono, correo, password_hash)
        )

        conexion.commit()

    @staticmethod
    def login(correo, password):

        cursor.execute(
            "SELECT * FROM usuarios WHERE correo=%s",
            (correo,)
        )

        usuario = cursor.fetchone()

        if not usuario:
            return None

        try:
            password_db = usuario[5]

            # 🔥 FIX ROBUSTO
            if bcrypt.checkpw(
                password.encode('utf-8'),
                password_db.encode('utf-8')
            ):
                return usuario

        except ValueError as e:
            print("ERROR BCRYPT:", e)

        return None

    @staticmethod
    def buscar_correo(correo):

        cursor.execute(
            "SELECT * FROM usuarios WHERE correo=%s",
            (correo,)
        )

        return cursor.fetchone()

    @staticmethod
    def cambiar_password(correo, nueva_password):

        hash_password = bcrypt.hashpw(
            nueva_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        cursor.execute(
            """
            UPDATE usuarios
            SET contrasena=%s
            WHERE correo=%s
            """,
            (hash_password, correo)
        )

        conexion.commit()