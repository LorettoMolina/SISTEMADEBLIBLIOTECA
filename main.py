import flet as ft
import mysql.connector
import random
import smtplib

from email.mime.text import MIMEText

# ======================================================
# CONEXIÓN MYSQL
# ======================================================

conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="biblioteca"
)

cursor = conexion.cursor()

# ======================================================
# CORREO
# ======================================================

CORREO_SISTEMA = "23308060610601@cetis61.edu.mx"
PASSWORD_CORREO = "fpot ykuc ebut gsuk"

codigo_recuperacion = ""

# ======================================================
# MAIN
# ======================================================

def main(page: ft.Page):

    global codigo_recuperacion

    # ==================================================
    # CONFIGURACIÓN
    # ==================================================

    page.title = "Sistema Biblioteca"

    page.window_width = 450
    page.window_height = 750

    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0f172a"

    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # ==================================================
    # LOGIN
    # ==================================================

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

    # ==================================================
    # DASHBOARD + CRUD
    # ==================================================

    def abrir_sistema(usuario):

        page.clean()

        # ==============================================
        # CAMPOS
        # ==============================================

        txt_titulo = ft.TextField(label="Título", width=300)
        txt_autor = ft.TextField(label="Autor", width=300)
        txt_categoria = ft.TextField(label="Categoría", width=300)
        txt_stock = ft.TextField(label="Stock", width=300)

        tabla = ft.Column()

        libro_id = {"id": None}

        # ==============================================
        # MOSTRAR LIBROS
        # ==============================================

        def cargar_libros():

            tabla.controls.clear()

            cursor.execute("SELECT * FROM libros")
            libros = cursor.fetchall()

            for libro in libros:

                fila = ft.Container(
                    bgcolor="#1e293b",
                    border_radius=10,
                    padding=10,
                    margin=5,

                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,

                        controls=[

                            ft.Column(
                                spacing=2,
                                controls=[

                                    ft.Text(
                                        libro[1],
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color="cyan"
                                    ),

                                    ft.Text(
                                        f"Autor: {libro[2]}",
                                        color="white"
                                    ),

                                    ft.Text(
                                        f"Categoría: {libro[3]}",
                                        color="white"
                                    ),

                                    ft.Text(
                                        f"Stock: {libro[4]}",
                                        color="white"
                                    ),
                                ]
                            ),

                            ft.Row(
                                controls=[

                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        icon_color="yellow",
                                        on_click=lambda e, l=libro: editar_libro(l)
                                    ),

                                    ft.IconButton(
                                        icon=ft.icons.DELETE,
                                        icon_color="red",
                                        on_click=lambda e, id=libro[0]: eliminar_libro(id)
                                    )
                                ]
                            )
                        ]
                    )
                )

                tabla.controls.append(fila)

            page.update()

        # ==============================================
        # LIMPIAR
        # ==============================================

        def limpiar():

            txt_titulo.value = ""
            txt_autor.value = ""
            txt_categoria.value = ""
            txt_stock.value = ""

            libro_id["id"] = None

            btn_guardar.text = "Agregar Libro"

            page.update()

        # ==============================================
        # AGREGAR
        # ==============================================

        def agregar_libro(e):

            sql = """
            INSERT INTO libros
            (titulo, autor, categoria, stock)
            VALUES (%s,%s,%s,%s)
            """

            valores = (
                txt_titulo.value,
                txt_autor.value,
                txt_categoria.value,
                txt_stock.value
            )

            cursor.execute(sql, valores)
            conexion.commit()

            limpiar()
            cargar_libros()

        # ==============================================
        # EDITAR
        # ==============================================

        def editar_libro(libro):

            libro_id["id"] = libro[0]

            txt_titulo.value = libro[1]
            txt_autor.value = libro[2]
            txt_categoria.value = libro[3]
            txt_stock.value = str(libro[4])

            btn_guardar.text = "Actualizar Libro"

            page.update()

        # ==============================================
        # ACTUALIZAR
        # ==============================================

        def actualizar_libro(e):

            sql = """
            UPDATE libros
            SET titulo=%s,
                autor=%s,
                categoria=%s,
                stock=%s
            WHERE id=%s
            """

            valores = (
                txt_titulo.value,
                txt_autor.value,
                txt_categoria.value,
                txt_stock.value,
                libro_id["id"]
            )

            cursor.execute(sql, valores)
            conexion.commit()

            limpiar()
            cargar_libros()

        # ==============================================
        # ELIMINAR
        # ==============================================

        def eliminar_libro(id):

            cursor.execute(
                "DELETE FROM libros WHERE id=%s",
                (id,)
            )

            conexion.commit()

            cargar_libros()

        # ==============================================
        # GUARDAR
        # ==============================================

        def guardar(e):

            if libro_id["id"] is None:
                agregar_libro(e)
            else:
                actualizar_libro(e)

        btn_guardar = ft.ElevatedButton(
            "Agregar Libro",
            width=300,
            bgcolor="cyan",
            color="black",
            on_click=guardar
        )

        # ==============================================
        # CARGAR LIBROS
        # ==============================================

        cargar_libros()

        # ==============================================
        # UI
        # ==============================================

        page.add(

            ft.Column(
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    ft.Icon(
                        ft.icons.LIBRARY_BOOKS,
                        size=100,
                        color="cyan"
                    ),

                    ft.Text(
                        "SISTEMA BIBLIOTECA",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color="cyan"
                    ),

                    ft.Text(
                        f"Bienvenido {usuario[1]} {usuario[2]}",
                        color="white",
                        size=18
                    ),

                    ft.Divider(),

                    ft.Text(
                        "CRUD LIBROS",
                        size=25,
                        color="cyan"
                    ),

                    txt_titulo,
                    txt_autor,
                    txt_categoria,
                    txt_stock,

                    btn_guardar,

                    ft.Divider(),

                    tabla,

                    ft.ElevatedButton(
                        "Cerrar sesión",
                        width=250,
                        bgcolor="red",
                        color="white",
                        on_click=volver_login
                    )
                ]
            )
        )

        page.update()

    # ==================================================
    # LOGIN
    # ==================================================

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
            abrir_sistema(usuario)

        else:
            mensaje.value = "Correo o contraseña incorrectos"
            mensaje.color = "red"

        page.update()

    # ==================================================
    # REGISTRO
    # ==================================================

    def abrir_registro(e):

        page.clean()

        nombre = ft.TextField(label="Nombre", width=320)
        apellido = ft.TextField(label="Apellido", width=320)
        telefono = ft.TextField(label="Teléfono", width=320)
        correo = ft.TextField(label="Correo", width=320)

        password = ft.TextField(
            label="Contraseña",
            password=True,
            can_reveal_password=True,
            width=320
        )

        mensaje_registro = ft.Text()

        def registrar(e):

            sql = """
            INSERT INTO usuarios
            (nombre, apellido, telefono, correo, contrasena)
            VALUES (%s,%s,%s,%s,%s)
            """

            try:

                cursor.execute(sql, (
                    nombre.value,
                    apellido.value,
                    telefono.value,
                    correo.value,
                    password.value
                ))

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

                    ft.Text(
                        "REGISTRO",
                        size=30,
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

    # ==================================================
    # RECUPERAR PASSWORD
    # ==================================================

    def recuperar_password(e):

        page.clean()

        correo = ft.TextField(label="Correo", width=320)
        codigo = ft.TextField(label="Código", width=320)

        nueva_password = ft.TextField(
            label="Nueva contraseña",
            password=True,
            can_reveal_password=True,
            width=320
        )

        mensaje_rec = ft.Text()

        # ==============================================
        # ENVIAR CÓDIGO
        # ==============================================

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

                    mensaje_rec.value = "Código enviado"
                    mensaje_rec.color = "green"

                except Exception as error:

                    mensaje_rec.value = str(error)
                    mensaje_rec.color = "red"

            else:

                mensaje_rec.value = "Correo no encontrado"
                mensaje_rec.color = "red"

            page.update()

        # ==============================================
        # CAMBIAR PASSWORD
        # ==============================================

        def cambiar_password(e):

            global codigo_recuperacion

            if codigo.value == codigo_recuperacion:

                cursor.execute("""

                    UPDATE usuarios
                    SET contrasena=%s
                    WHERE correo=%s

                """, (
                    nueva_password.value,
                    correo.value
                ))

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

                    ft.Text(
                        "RECUPERAR CONTRASEÑA",
                        size=30,
                        color="cyan"
                    ),

                    correo,

                    ft.ElevatedButton(
                        "Enviar código",
                        on_click=enviar_codigo
                    ),

                    codigo,
                    nueva_password,

                    ft.ElevatedButton(
                        "Cambiar contraseña",
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

    # ==================================================
    # LOGIN UI
    # ==================================================

    def volver_login(e=None):

        page.clean()

        page.add(

            ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    ft.Icon(
                        ft.icons.LIBRARY_BOOKS,
                        size=100,
                        color="cyan"
                    ),

                    ft.Text(
                        "SISTEMA BIBLIOTECA",
                        size=30,
                        color="cyan",
                        weight=ft.FontWeight.BOLD
                    ),

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

                    ft.TextButton(
                        "Registrarse",
                        on_click=abrir_registro
                    ),

                    ft.TextButton(
                        "Recuperar contraseña",
                        on_click=recuperar_password
                    )
                ]
            )
        )

        page.update()

    # ==================================================
    # INICIO
    # ==================================================

    volver_login()

# ======================================================
# EJECUTAR
# ======================================================

ft.app(target=main)