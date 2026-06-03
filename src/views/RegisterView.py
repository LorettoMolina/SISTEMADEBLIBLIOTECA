import flet as ft
from src.controllers.UserController import UserController


class RegisterView:

    def __init__(self, page):
        self.page = page

        self.nombre = ft.TextField(label="Nombre")
        self.correo = ft.TextField(label="Correo")
        self.password = ft.TextField(label="Contraseña", password=True)

        self.msg = ft.Text()

    def registrar(self, e):

        try:
            UserController.registrar(
                self.nombre.value,
                "",  # apellido (puedes quitarlo en DB si no lo usas)
                "",  # telefono
                self.correo.value,
                self.password.value
            )

            self.msg.value = "Usuario registrado correctamente"
            self.msg.color = "green"

        except Exception as ex:
            print("ERROR REGISTRO:", ex)
            self.msg.value = "Error al registrar usuario"
            self.msg.color = "red"

        self.page.update()

    def go_login(self, e):
        self.page.clean()

        from src.views.LoginView import LoginView
        login = LoginView(self.page)

        self.page.add(login.build())

    def build(self):

        return ft.Column(
            controls=[
                ft.Text("Registro", size=30),

                self.nombre,
                self.correo,
                self.password,

                ft.ElevatedButton(
                    "Registrarse",
                    on_click=self.registrar
                ),

                ft.TextButton(
                    "Volver al login",
                    on_click=self.go_login
                ),

                self.msg
            ]
        )