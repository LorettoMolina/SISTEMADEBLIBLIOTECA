import flet as ft
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="biblioteca"
)

cursor = conexion.cursor()

def main(page: ft.Page):

    page.title = "Sistema Biblioteca"

    page.window_width = 400
    page.window_height = 600

    mensaje_registro = ft.Text("")
    mensaje_login = ft.Text("")

    nombre = ft.TextField(label="Nombre")
    apellido = ft.TextField(label="Apellido")
    telefono = ft.TextField(label="Teléfono")
    correo_reg = ft.TextField(label="Correo")

    contrasena_reg = ft.TextField(
        label="Contraseña",
        password=True
    )

    def registrar(e):

        sql = """
        INSERT INTO usuarios
        (nombre, apellido, telefono, correo, contrasena)
        VALUES (%s,%s,%s,%s,%s)
        """

        valores = (
            nombre.value,
            apellido.value,
            telefono.value,
            correo_reg.value,
            contrasena_reg.value
        )

        try:

            cursor.execute(sql, valores)
            conexion.commit()

            mensaje_registro.value = "Usuario registrado correctamente"
            mensaje_registro.color = "green"

        except mysql.connector.Error as error:

            mensaje_registro.value = f"Error: {error}"
            mensaje_registro.color = "red"

        page.update()

    correo_login = ft.TextField(label="Correo")

    contrasena_login = ft.TextField(
        label="Contraseña",
        password=True
    )

    def login(e):

        sql = """
        SELECT * FROM usuarios
        WHERE correo=%s AND contrasena=%s
        """

        valores = (
            correo_login.value,
            contrasena_login.value
        )

        cursor.execute(sql, valores)

        usuario = cursor.fetchone()

        if usuario:

            mensaje_login.value = f"Bienvenido {usuario[1]}"
            mensaje_login.color = "green"

        else:

            mensaje_login.value = "Correo o contraseña incorrectos"
            mensaje_login.color = "red"

        page.update()

    registro_tab = ft.Column([

        ft.Text(
            "REGISTRO",
            size=25,
            weight="bold"
        ),

        nombre,
        apellido,
        telefono,
        correo_reg,
        contrasena_reg,

        ft.ElevatedButton(
            "Registrarse",
            on_click=registrar
        ),

        mensaje_registro

    ])

    login_tab = ft.Column([

        ft.Text(
            "INICIO DE SESIÓN",
            size=25,
            weight="bold"
        ),

        correo_login,
        contrasena_login,

        ft.ElevatedButton(
            "Iniciar Sesión",
            on_click=login
        ),

        mensaje_login

    ])

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[

            ft.Tab(
                text="Registro",
                content=registro_tab
            ),

            ft.Tab(
                text="Login",
                content=login_tab
            )

        ]

    )

    page.add(tabs)

ft.app(target=main)