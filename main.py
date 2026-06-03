import flet as ft
from src.views.LoginView import LoginView

def main(page: ft.Page):
    page.title = "Sistema Biblioteca"
    page.theme_mode = ft.ThemeMode.LIGHT

    login = LoginView(page)

    page.add(login.build())

ft.run(main)