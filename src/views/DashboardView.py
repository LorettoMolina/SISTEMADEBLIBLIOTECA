import flet as ft
from src.controllers.LibroController import LibroController


class DashboardView:

    def __init__(self, page):
        self.page = page
        self.tabla = ft.Column()

    def cargar(self):

        self.tabla.controls.clear()

        libros = LibroController.listar()

        for libro in libros:
            self.tabla.controls.append(
                ft.Text(f"{libro[1]} - {libro[2]} - {libro[3]}")
            )

        self.page.update()

    def build(self):

        self.cargar()

        return ft.Column(
            controls=[
                ft.Text("Dashboard", size=30),
                self.tabla
            ]
        )