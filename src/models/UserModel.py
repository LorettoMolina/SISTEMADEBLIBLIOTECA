import bcrypt

from src.models.databaseModel import cursor, conexion

class UserModel:

    @staticmethod
    def registrar(nombre, apellido, telefono, correo, password):

        password_hash = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        cursor.execute(
            """
            INSERT INTO usuarios
            (nombre, apellido, telefono, correo, contrasena)
            VALUES (%s,%s,%s,%s,%s)
            """,
            (
                nombre,
                apellido,
                telefono,
                correo,
                password_hash
            )
        )

        conexion.commit()

    @staticmethod
    def login(correo, password):

        cursor.execute(
            "SELECT * FROM usuarios WHERE correo=%s",
            (correo,)
        )

        usuario = cursor.fetchone()

        if usuario:

            password_db = usuario[5]

            if bcrypt.checkpw(
                password.encode(),
                password_db.encode()
            ):
                return usuario

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
            nueva_password.encode(),
            bcrypt.gensalt()
        ).decode()

        cursor.execute(
            """
            UPDATE usuarios
            SET contrasena=%s
            WHERE correo=%s
            """,
            (
                hash_password,
                correo
            )
        )

        conexion.commit()