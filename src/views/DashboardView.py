import flet as ft
from src.controllers.LibrosController import LibrosController

class DashboardView:

    def __init__(self, page):

        self.page = page
        self.tabla = ft.Column()

    def cargar(self):

        self.tabla.controls.clear()

        for libro in LibrosController.listar():

            self.tabla.controls.append(
                ft.Text(libro[1])
            )

    def build(self):

        self.cargar()

        return ft.Column(
            controls=[
                ft.Text("Dashboard"),
                self.tabla
            ]
        )