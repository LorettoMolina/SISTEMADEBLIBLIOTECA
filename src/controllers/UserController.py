from src.models.UserModel import UserModel

class UserController:

    @staticmethod
    def login(correo,password):
        return UserModel.login(
            correo,
            password
        )

    @staticmethod
    def registrar(
        nombre,
        apellido,
        telefono,
        correo,
        password
    ):

        UserModel.registrar(
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
    def cambiar_password(
        correo,
        nueva_password
    ):
        UserModel.cambiar_password(
            correo,
            nueva_password
        )