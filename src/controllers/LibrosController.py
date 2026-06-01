from src.models.LibroModel import LibroModel

class LibroController:

    @staticmethod
    def listar():
        return LibroModel.obtener_todos()

    @staticmethod
    def agregar(
        titulo,
        autor,
        categoria,
        stock
    ):
        LibroModel.agregar(
            titulo,
            autor,
            categoria,
            stock
        )

    @staticmethod
    def actualizar(
        id_libro,
        titulo,
        autor,
        categoria,
        stock
    ):
        LibroModel.actualizar(
            id_libro,
            titulo,
            autor,
            categoria,
            stock
        )

    @staticmethod
    def eliminar(id_libro):
        LibroModel.eliminar(id_libro)