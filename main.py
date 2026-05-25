def abrir_sistema(usuario):

    page.clean()

    # =========================================
    # CAMPOS LIBROS
    # =========================================

    txt_titulo = ft.TextField(label="Título", width=250)
    txt_autor = ft.TextField(label="Autor", width=250)
    txt_categoria = ft.TextField(label="Categoría", width=250)
    txt_stock = ft.TextField(label="Stock", width=250)

    tabla = ft.Column()

    libro_id = {"id": None}

    

    def cargar_libros():

        tabla.controls.clear()

        cursor.execute("SELECT * FROM libros")
        libros = cursor.fetchall()

        for libro in libros:

            fila = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[

                    ft.Text(
                        f"{libro[1]} | {libro[2]} | {libro[3]} | Stock: {libro[4]}",
                        color="white",
                        width=300
                    ),

                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color="yellow",
                            on_click=lambda e, l=libro: editar_libro(l)
                        ),

                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color="red",
                            on_click=lambda e, id=libro[0]: eliminar_libro(id)
                        )
                    ])
                ]
            )

            tabla.controls.append(fila)

        page.update()

    

    def limpiar():

        txt_titulo.value = ""
        txt_autor.value = ""
        txt_categoria.value = ""
        txt_stock.value = ""

        libro_id["id"] = None

        btn_guardar.text = "Agregar Libro"

        page.update()

    

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

    

    def editar_libro(libro):

        libro_id["id"] = libro[0]

        txt_titulo.value = libro[1]
        txt_autor.value = libro[2]
        txt_categoria.value = libro[3]
        txt_stock.value = str(libro[4])

        btn_guardar.text = "Actualizar Libro"

        page.update()

    
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

    
    def eliminar_libro(id):

        cursor.execute(
            "DELETE FROM libros WHERE id=%s",
            (id,)
        )

        conexion.commit()

        cargar_libros()

    

    def guardar(e):

        if libro_id["id"] is None:
            agregar_libro(e)
        else:
            actualizar_libro(e)

    btn_guardar = ft.ElevatedButton(
        "Agregar Libro",
        bgcolor="cyan",
        color="black",
        width=250,
        on_click=guardar
    )

    
    cargar_libros()

    page.add(
        ft.Container(
            expand=True,
            padding=20,
            bgcolor="#0f172a",

            content=ft.Column(
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,

                controls=[

                    ft.Icon(
                        ft.Icons.LIBRARY_BOOKS,
                        size=100,
                        color="cyan"
                    ),

                    ft.Text(
                        "SISTEMA BIBLIOTECA",
                        size=32,
                        weight=ft.FontWeight.BOLD,
                        color="cyan"
                    ),

                    ft.Text(
                        f"Bienvenido: {usuario[1]} {usuario[2]}",
                        size=18,
                        color="white"
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
                        width=200,
                        bgcolor="red",
                        color="white",
                        on_click=volver_login
                    )
                ]
            )
        )
    )

    page.update()