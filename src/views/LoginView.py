import flet as ft
from src.controllers.UserController import UserController

class LoginView:

    def __init__(self, page):
        self.page = page

        self.correo = ft.TextField(label="Correo")
        self.password = ft.TextField(label="Contraseña", password=True)
        self.msg = ft.Text()

    def login(self, e):

        usuario = UserController.login(
            self.correo.value,
            self.password.value
        )

        if usuario:
            self.msg.value = "Bienvenido"
            self.msg.color = "green"
        else:
            self.msg.value = "Datos incorrectos"
            self.msg.color = "red"

        self.page.update()

    def go_register(self, e):
        self.page.go("/register")

    def build(self):
        return ft.Column(
            controls=[
                ft.Text("Sistema Biblioteca", size=30),

                self.correo,
                self.password,

                ft.ElevatedButton("Ingresar", on_click=self.login),

                ft.TextButton(
                    "¿No tienes cuenta? Regístrate",
                    on_click=self.go_register
                ),

                self.msg
            ]
        )