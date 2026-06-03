from src.models.UserModel import UserModel


class UserController:

    @staticmethod
    def login(correo, password):
        return UserModel.login(correo, password)

    @staticmethod
    def registrar(nombre, apellido, telefono, correo, password):
        return UserModel.registrar(
            nombre,
            apellido,
            telefono,
            correo,
            password
        )

    @staticmethod
    def buscar_correo(correo):
        return UserModel.buscar_correo(correo)

    @staticmethod
    def cambiar_password(correo, nueva_password):
        return UserModel.cambiar_password(correo, nueva_password)