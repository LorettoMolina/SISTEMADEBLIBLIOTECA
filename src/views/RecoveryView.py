import flet as ft
from src.services.recovery_service import enviar_codigo


class RecoveryView:

    def __init__(self, page):
        self.page = page

        self.correo = ft.TextField(label="Correo")
        self.codigo = ft.TextField(label="Código recibido")
        self.msg = ft.Text()

    def enviar(self, e):

        codigo = enviar_codigo(self.correo.value)

        if codigo:
            self.msg.value = "Código enviado al correo"
            self.msg.color = "green"
        else:
            self.msg.value = "Error al enviar código"
            self.msg.color = "red"

        self.page.update()

    def validar(self, e):

        from src.services.recovery_service import codigo_recuperacion

        if self.codigo.value == codigo_recuperacion:
            self.msg.value = "Código correcto"
            self.msg.color = "green"
        else:
            self.msg.value = "Código incorrecto"
            self.msg.color = "red"

        self.page.update()

    def build(self):

        return ft.Column(
            controls=[
                ft.Text("Recuperar contraseña", size=30),

                self.correo,
                ft.ElevatedButton("Enviar código", on_click=self.enviar),

                self.codigo,
                ft.ElevatedButton("Validar código", on_click=self.validar),

                self.msg
            ]
        )