import flet as ft
from src.views.LoginView import LoginView

def main(page: ft.Page):

    page.title = "Sistema Biblioteca"
    page.theme_mode = ft.ThemeMode.LIGHT

    def route_change(route):
        page.views.clear()

        if page.route == "/":
            login = LoginView(page)
            page.views.append(
                ft.View(
                    "/",
                    controls=[login.build()]
                )
            )

        elif page.route == "/register":
            from src.views.RegisterView import RegisterView
            register = RegisterView(page)

            page.views.append(
                ft.View(
                    "/register",
                    controls=[register.build()]
                )
            )

        page.update()

    def go_back(e):
        page.go("/")

    page.on_route_change = route_change
    page.go("/")


ft.app(target=main)