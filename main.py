import flet as ft
import bcrypt
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
    page.window_width = 450
    page.window_height = 750
    page.bgcolor = "#2650b3"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    
    correo_login = ft.TextField(label="Correo", width=320)
    password_login = ft.TextField(label="Contraseña", password=True, width=320)
    mensaje = ft.Text()

    
    def volver_login(e=None):
        correo_login.value = ""
        password_login.value = ""
        mensaje.value = ""
        page.clean()

        page.add(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Icon(ft.Icons.BOOK, size=100, color="cyan"),
                    ft.Text("SISTEMA BIBLIOTECA", size=30, color="cyan"),
                    correo_login,
                    password_login,
                    ft.ElevatedButton(
                        "Iniciar Sesión",
                        width=320,
                        bgcolor="cyan",
                        color="black",
                        on_click=iniciar_sesion
                    ),
                    mensaje,
                    ft.TextButton("Registrarse", on_click=abrir_registro),
                    ft.TextButton("Recuperar contraseña", on_click=recuperar_password)
                ]
            )
        )

    def iniciar_sesion(e):
        try:
            cursor.execute(
                "SELECT * FROM usuarios WHERE correo=%s AND contrasena=%s",
                (correo_login.value, password_login.value)
            )
            usuario = cursor.fetchone()
            if usuario:
                abrir_sistema(usuario)
            else:
                mensaje.value = "Datos incorrectos"
                mensaje.color = "red"
            page.update()
        except Exception as error:
            mensaje.value = str(error)
            mensaje.color = "red"
            page.update()

    
    def abrir_registro(e):
        page.clean()
        nombre = ft.TextField(label="Nombre", width=320)
        apellido = ft.TextField(label="Apellido", width=320)
        telefono = ft.TextField(label="Teléfono", width=320)
        correo = ft.TextField(label="Correo", width=320)
        password = ft.TextField(label="Contraseña", password=True, width=320)
        msg = ft.Text()

        def registrar(e):
            try:
                cursor.execute(
                    "INSERT INTO usuarios (nombre, apellido, telefono, correo, contrasena) VALUES (%s,%s,%s,%s,%s)",
                    (nombre.value, apellido.value, telefono.value, correo.value, password.value)
                )
                conexion.commit()
                msg.value = "Usuario registrado"
                msg.color = "green"
            except Exception as error:
                msg.value = str(error)
                msg.color = "red"
            page.update()

        page.add(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("REGISTRO", size=30, color="cyan"),
                    nombre, apellido, telefono, correo, password,
                    ft.ElevatedButton("Registrar", width=320, on_click=registrar),
                    msg,
                    ft.TextButton("Volver", on_click=volver_login)
                ]
            )
        )

    
    def recuperar_password(e):
        page.clean()
        correo = ft.TextField(label="Correo", width=320)
        codigo = ft.TextField(label="Código", width=320)
        nueva = ft.TextField(label="Nueva contraseña", password=True, width=320)
        msg = ft.Text()

        def enviar(e):
            global codigo_recuperacion
            cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (correo.value,))
            user = cursor.fetchone()
            if user:
                codigo_recuperacion = str(random.randint(100000, 999999))
                msg_email = MIMEText(f"Tu código de recuperación es: {codigo_recuperacion}")
                msg_email["Subject"] = "Recuperación de contraseña"
                msg_email["From"] = CORREO_SISTEMA
                msg_email["To"] = correo.value
                try:
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(CORREO_SISTEMA, PASSWORD_CORREO)
                    server.send_message(msg_email)
                    server.quit()
                    msg.value = "Código enviado"
                    msg.color = "green"
                except Exception as error:
                    msg.value = str(error)
                    msg.color = "red"
            else:
                msg.value = "Correo no existe"
                msg.color = "red"
            page.update()

        def cambiar(e):
            if codigo.value == codigo_recuperacion:
                cursor.execute(
                    "UPDATE usuarios SET contrasena=%s WHERE correo=%s",
                    (nueva.value, correo.value)
                )
                conexion.commit()
                msg.value = "Contraseña cambiada"
                msg.color = "green"
            else:
                msg.value = "Código incorrecto"
                msg.color = "red"
            page.update()

        page.add(
            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("RECUPERAR", size=30, color="cyan"),
                    correo,
                    ft.ElevatedButton("Enviar código", on_click=enviar),
                    codigo, nueva,
                    ft.ElevatedButton("Cambiar contraseña", on_click=cambiar),
                    msg,
                    ft.TextButton("Volver", on_click=volver_login)
                ]
            )
        )

    
    def abrir_sistema(usuario):
        page.clean()
        t1 = ft.TextField(label="Título", width=300)
        t2 = ft.TextField(label="Autor", width=300)
        t3 = ft.TextField(label="Categoría", width=300)
        t4 = ft.TextField(label="Stock", width=300)
        tabla = ft.Column()
        libro_id = {"id": None}

        def cargar():
            tabla.controls.clear()
            cursor.execute("SELECT * FROM libros")
            for l in cursor.fetchall():
                tabla.controls.append(
                    ft.Container(
                        bgcolor="#1e293b",
                        padding=10,
                        margin=5,
                        border_radius=10,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column([
                                    ft.Text(l[1], color="cyan"),
                                    ft.Text(l[2]),
                                    ft.Text(l[3]),
                                    ft.Text(f"Stock: {l[4]}")
                                ]),
                                ft.Row([
                                    ft.IconButton(ft.Icons.EDIT, on_click=lambda e, lib=l: editar(lib)),
                                    ft.IconButton(ft.Icons.DELETE, on_click=lambda e, id_lib=l[0]: borrar(id_lib))
                                ])
                            ]
                        )
                    )
                )
            page.update()

        def limpiar():
            t1.value = t2.value = t3.value = t4.value = ""
            libro_id["id"] = None

        def agregar():
            cursor.execute(
                "INSERT INTO libros (titulo, autor, categoria, stock) VALUES (%s,%s,%s,%s)",
                (t1.value, t2.value, t3.value, int(t4.value))
            )
            conexion.commit()

        def editar(lib):
            libro_id["id"] = lib[0]
            t1.value, t2.value, t3.value, t4.value = lib[1], lib[2], lib[3], str(lib[4])
            page.update()

        def borrar(id_lib):
            cursor.execute("DELETE FROM libros WHERE id=%s", (id_lib,))
            conexion.commit()
            cargar()

        def guardar(e):
            try:
                if libro_id["id"]:
                    cursor.execute(
                        "UPDATE libros SET titulo=%s, autor=%s, categoria=%s, stock=%s WHERE id=%s",
                        (t1.value, t2.value, t3.value, int(t4.value), libro_id["id"])
                    )
                else:
                    agregar()
                conexion.commit()
                limpiar()
                cargar()
            except Exception as error:
                print("Error al guardar libro:", error)

        cargar()

        page.add(
            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Icon(ft.Icons.BOOK, size=100, color="cyan"),
                    ft.Text(f"Bienvenido {usuario[1]}", color="white"),
                    t1, t2, t3, t4,
                    ft.ElevatedButton("Guardar", on_click=guardar),
                    tabla,
                    ft.ElevatedButton("Cerrar sesión", on_click=volver_login)
                ]
            )
        )

    volver_login()



ft.app(target=main)