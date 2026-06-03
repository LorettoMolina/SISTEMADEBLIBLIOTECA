from src.models.LibroModel import LibroModel


class LibroController:

    @staticmethod
    def listar():
        return LibroModel.obtener_todos()

    @staticmethod
    def agregar(titulo, autor, categoria, stock):
        return LibroModel.agregar(
            titulo,
            autor,
            categoria,
            stock
        )

    @staticmethod
    def actualizar(id_libro, titulo, autor, categoria, stock):
        return LibroModel.actualizar(
            id_libro,
            titulo,
            autor,
            categoria,
            stock
        )

    @staticmethod
    def eliminar(id_libro):
        return LibroModel.eliminar(id_libro)