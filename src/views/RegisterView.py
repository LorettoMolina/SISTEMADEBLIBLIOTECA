import flet as ft

class RegisterView:

    def __init__(self, page):
        self.page = page

    def build(self):
        return ft.Column(
            controls=[
                ft.Text("Registro")
            ]
        )