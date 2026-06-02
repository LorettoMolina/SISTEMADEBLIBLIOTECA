import flet as ft

class RegisterView:

    def __init__(self, page):
        self.page = page

        self.nombre = ft.TextField(label="Nombre")
        self.correo = ft.TextField(label="Correo")
        self.password = ft.TextField(label="Contraseña", password=True)

    def go_login(self, e):
        self.page.go("/")

    def registrar(self, e):
        print("Registrar usuario")

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
                )
            ]
        )