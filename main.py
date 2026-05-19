import flet as ft
import mysql.connector
import random
import smtplib
from email.mime.text import MIMEText


conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="biblioteca"
)

cursor = conexion.cursor()




CORREO_SISTEMA = "23308060610601@cetis61.edu.mx"


PASSWORD_CORREO = "fpot ykuc ebut gsuk"

codigo_recuperacion = ""


def main(page: ft.Page):

    global codigo_recuperacion

    page.title = "Sistema Biblioteca"

    page.window.width = 450
    page.window.height = 700

    page.theme_mode = ft.ThemeMode.DARK

    page.bgcolor = "#0f172a"

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    

    correo_login = ft.TextField(
        label="Correo",
        width=320,
        border_radius=15
    )

    password_login = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=320,
        border_radius=15
    )

    mensaje = ft.Text()

    def iniciar_sesion(e):

        sql = """
        SELECT * FROM usuarios
        WHERE correo=%s AND contrasena=%s
        """

        cursor.execute(
            sql,
            (
                correo_login.value,
                password_login.value
            )
        )

        usuario = cursor.fetchone()

        if usuario:

            mensaje.value = f"Bienvenido {usuario[1]}"
            mensaje.color = "green"

        else:

            mensaje.value = "Correo o contraseña incorrectos"
            mensaje.color = "red"

        page.update()

    # 

    def abrir_registro(e):

        page.clean()

        nombre = ft.TextField(
            label="Nombre",
            width=320,
            border_radius=15
        )

        apellido = ft.TextField(
            label="Apellido",
            width=320,
            border_radius=15
        )

        telefono = ft.TextField(
            label="Teléfono",
            width=320,
            border_radius=15
        )

        correo = ft.TextField(
            label="Correo",
            width=320,
            border_radius=15
        )

        password = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=320,
            border_radius=15
        )

        mensaje_registro = ft.Text()

        def registrar(e):

            sql = """
            INSERT INTO usuarios
            (nombre, apellido, telefono, correo, contrasena)
            VALUES (%s,%s,%s,%s,%s)
            """

            try:

                cursor.execute(
                    sql,
                    (
                        nombre.value,
                        apellido.value,
                        telefono.value,
                        correo.value,
                        password.value
                    )
                )

                conexion.commit()

                mensaje_registro.value = "Usuario registrado"
                mensaje_registro.color = "green"

            except Exception as error:

                mensaje_registro.value = str(error)
                mensaje_registro.color = "red"

            page.update()

        page.add(

            ft.Column(

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    ft.Icon(
                        ft.Icons.BOOK,
                        size=90,
                        color="cyan"
                    ),

                    ft.Text(
                        "REGISTRO",
                        size=35,
                        weight=ft.FontWeight.BOLD,
                        color="cyan"
                    ),

                    nombre,
                    apellido,
                    telefono,
                    correo,
                    password,

                    ft.ElevatedButton(
                        "Registrarse",
                        width=320,
                        height=50,
                        bgcolor="cyan",
                        color="black",
                        on_click=registrar
                    ),

                    mensaje_registro,

                    ft.TextButton(
                        "Volver al Login",
                        on_click=volver_login
                    )
                ]
            )
        )

    

    def recuperar_password(e):

        page.clean()

        correo = ft.TextField(
            label="Correo",
            width=320,
            border_radius=15
        )

        codigo = ft.TextField(
            label="Código",
            width=320,
            border_radius=15
        )

        nueva_password = ft.TextField(
            label="Nueva contraseña",
            password=True,
            can_reveal_password=True,
            width=320,
            border_radius=15
        )

        mensaje_rec = ft.Text()

        # ======================================
        # ENVIAR CODIGO
        # ======================================

        def enviar_codigo(e):

            global codigo_recuperacion

            cursor.execute(
                "SELECT * FROM usuarios WHERE correo=%s",
                (correo.value,)
            )

            usuario = cursor.fetchone()

            if usuario:

                codigo_recuperacion = str(
                    random.randint(100000, 999999)
                )

                msg = MIMEText(
                    f"Tu código de recuperación es: {codigo_recuperacion}"
                )

                msg["Subject"] = "Recuperar contraseña"
                msg["From"] = CORREO_SISTEMA
                msg["To"] = correo.value

                try:

                    server = smtplib.SMTP(
                        "smtp.gmail.com",
                        587
                    )

                    server.starttls()

                    server.login(
                        CORREO_SISTEMA,
                        PASSWORD_CORREO
                    )

                    server.send_message(msg)

                    server.quit()

                    mensaje_rec.value = "Código enviado correctamente"
                    mensaje_rec.color = "green"

                except Exception as error:

                    mensaje_rec.value = str(error)
                    mensaje_rec.color = "red"

            else:

                mensaje_rec.value = "Correo no encontrado"
                mensaje_rec.color = "red"

            page.update()

        # ======================================
        # CAMBIAR PASSWORD
        # ======================================

        def cambiar_password(e):

            global codigo_recuperacion

            if codigo.value == codigo_recuperacion:

                cursor.execute(
                    """
                    UPDATE usuarios
                    SET contrasena=%s
                    WHERE correo=%s
                    """,
                    (
                        nueva_password.value,
                        correo.value
                    )
                )

                conexion.commit()

                mensaje_rec.value = "Contraseña actualizada"
                mensaje_rec.color = "green"

            else:

                mensaje_rec.value = "Código incorrecto"
                mensaje_rec.color = "red"

            page.update()

        page.add(

            ft.Column(

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    ft.Icon(
                        ft.Icons.LOCK,
                        size=90,
                        color="cyan"
                    ),

                    ft.Text(
                        "RECUPERAR",
                        size=35,
                        weight=ft.FontWeight.BOLD,
                        color="cyan"
                    ),

                    correo,

                    ft.ElevatedButton(
                        "Enviar código",
                        width=320,
                        height=50,
                        bgcolor="cyan",
                        color="black",
                        on_click=enviar_codigo
                    ),

                    codigo,
                    nueva_password,

                    ft.ElevatedButton(
                        "Cambiar contraseña",
                        width=320,
                        height=50,
                        bgcolor="cyan",
                        color="black",
                        on_click=cambiar_password
                    ),

                    mensaje_rec,

                    ft.TextButton(
                        "Volver al Login",
                        on_click=volver_login
                    )
                ]
            )
        )

    # ==========================================
    # LOGIN SCREEN
    # ==========================================

    def volver_login(e=None):

        page.clean()

        page.add(

            ft.Column(

                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    ft.Icon(
                        ft.Icons.BOOK,
                        size=100,
                        color="cyan"
                    ),

                    ft.Text(
                        "SISTEMA BIBLIOTECA",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color="cyan"
                    ),

                    correo_login,
                    password_login,

                    ft.ElevatedButton(
                        "Iniciar Sesión",
                        width=320,
                        height=50,
                        bgcolor="cyan",
                        color="black",
                        on_click=iniciar_sesion
                    ),

                    mensaje,

                    ft.TextButton(
                        "¿No tienes cuenta? Registrarse",
                        on_click=abrir_registro
                    ),

                    ft.TextButton(
                        "¿Olvidaste tu contraseña?",
                        on_click=recuperar_password
                    )
                ]
            )
        )

    volver_login()

ft.app(target=main)