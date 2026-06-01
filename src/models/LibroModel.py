from src.models.databaseModel import cursor, conexion

class LibroModel:

    @staticmethod
    def obtener_todos():

        cursor.execute(
            "SELECT * FROM libros"
        )

        return cursor.fetchall()

    @staticmethod
    def agregar(
        titulo,
        autor,
        categoria,
        stock
    ):

        cursor.execute(
            """
            INSERT INTO libros
            (titulo,autor,categoria,stock)
            VALUES (%s,%s,%s,%s)
            """,
            (
                titulo,
                autor,
                categoria,
                stock
            )
        )

        conexion.commit()

    @staticmethod
    def actualizar(
        id_libro,
        titulo,
        autor,
        categoria,
        stock
    ):

        cursor.execute(
            """
            UPDATE libros
            SET titulo=%s,
                autor=%s,
                categoria=%s,
                stock=%s
            WHERE id=%s
            """,
            (
                titulo,
                autor,
                categoria,
                stock,
                id_libro
            )
        )

        conexion.commit()

    @staticmethod
    def eliminar(id_libro):

        cursor.execute(
            "DELETE FROM libros WHERE id=%s",
            (id_libro,)
        )

        conexion.commit()