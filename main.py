import flet as ft

from src.views.LoginView import LoginView

def main(page: ft.Page):

    page.title = "Biblioteca"

    page.window_width = 450
    page.window_height = 750

    login = LoginView(page)

    page.add(
        login.build()
    )

ft.app(target=main)