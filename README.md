# Sistema de Biblioteca

## Descripción del Problema

Actualmente las bibliotecas manejan la información de libros, usuarios y préstamos de manera manual o poco organizada, lo que genera errores, pérdida de información y dificultad para consultar datos.

Por esta razón, se requiere el desarrollo de un sistema de base de datos que permita administrar de forma eficiente la información relacionada con libros, autores, usuarios y préstamos.

Las entidades principales del sistema son:

-  Autores  
-  Libros  
-  Usuarios  
-  Préstamos  

Estas entidades permiten organizar la información y establecer relaciones mediante claves primarias y foráneas.

---

# Integrantes del Equipo

## Datos Personales

### Luis Antonio Avila Robledo
- Edad: 17 años  
- Correo Electrónico: 23308060610140@cetis61.edu.mx  
- Especialidad: Programación  
- Institución: CETis 61  
- ##  Fotografía
<img width="236" height="248" alt="image" src="https://github.com/LorettoMolina/SISTEMADEBLIBLIOTECA/blob/master/WhatsApp%20Image%202026-05-14%20at%201.09.30%20PM.jpeg?raw=true" />

### Loretto Daniel Molina Moncada
- Edad: 17 años  
- Correo Electrónico: 23308060610601@cetis61.edu.mx  
- Especialidad: Programación  
- Institución: CETis 61 
- ##  Fotografía
<img width="236" height="248" alt="image" src="https://github.com/LorettoMolina/SISTEMADEBLIBLIOTECA/blob/master/WhatsApp%20Image%202026-05-14%20at%201.09.37%20PM.jpeg?raw=true" />

---

# Propósito del Proyecto

El propósito de este proyecto es desarrollar una base de datos relacional para un sistema de biblioteca que permita administrar de manera eficiente la información relacionada con libros, autores, usuarios, préstamos y devoluciones.

El sistema busca facilitar el control y organización de los registros, mejorar el flujo de información y garantizar la integridad de los datos mediante el uso de claves primarias y foráneas.

Además, el proyecto pretende aplicar los conocimientos adquiridos sobre modelado de bases de datos, normalización de tablas y creación de relaciones entre entidades utilizando MySQL Workbench.

---

# Alcance del Proyecto

El sistema de biblioteca permitirá:

- Registrar libros disponibles en la biblioteca.
- Registrar autores de los libros.
- Administrar usuarios registrados.
- Controlar préstamos y devoluciones de libros.
- Consultar información de libros y usuarios.
- Relacionar correctamente las tablas mediante llaves foráneas.
- Evitar redundancia de datos mediante normalización.

---

# El Proyecto Incluye

- Diseño del diagrama entidad-relación (ER).
- Creación de tablas normalizadas.
- Implementación de relaciones entre entidades.
- Desarrollo de la base de datos en MySQL Workbench.
- Generación y exportación del script SQL.

---

# Entidades que Intervienen en el Flujo de Información

## 1. Autores
Entidad encargada de almacenar la información de los autores de los libros.

### Atributos:
- id_autor
- nombre
- nacionalidad

---

## 2. Libros
Contiene la información de los libros disponibles en la biblioteca.

### Atributos:
- id_libro
- titulo
- editorial
- año_publicacion
- isbn
- id_autor

---

## 3. Usuarios
Almacena los datos de las personas registradas en el sistema.

### Atributos:
- id_usuario
- nombre
- apellido
- telefono
- correo

---

## 4. Prestamos
Registra los préstamos y devoluciones realizados por los usuarios.

### Atributos:
- id_prestamo
- id_usuario
- id_libro
- fecha_prestamo
- fecha_devolucion
- estado

---

# 🔗 Relaciones entre Entidades

- Un autor puede tener varios libros.
- Un libro pertenece a un autor.
- Un usuario puede realizar varios préstamos.
- Un préstamo pertenece a un usuario.
- Un libro puede aparecer en varios préstamos.

---

# Relaciones Principales

- `Libros.id_autor → Autores.id_autor`
- `Prestamos.id_usuario → Usuarios.id_usuario`
- `Prestamos.id_libro → Libros.id_libro`

---

# Normalización de Tablas

La base de datos se encuentra normalizada hasta la Tercera Forma Normal (3FN) para evitar redundancia de datos.

## Primera Forma Normal (1FN)
Los atributos contienen valores únicos y atómicos.

## Segunda Forma Normal (2FN)
Todos los atributos dependen completamente de la clave primaria.

## Tercera Forma Normal (3FN)
No existen dependencias transitivas.

Esto permite una mejor organización y mantenimiento de la información.

---

# Desarrollo de la Base de Datos en MySQL Workbench

Para el desarrollo de la base de datos se realizarán los siguientes pasos:

1. Crear la base de datos.
2. Crear las tablas:
   - Autores
   - Libros
   - Usuarios
   - Prestamos
3. Definir Primary Keys.
4. Configurar Foreign Keys.
5. Verificar las relaciones entre tablas.
6. Generar el diagrama ER automáticamente.
7. Validar el funcionamiento de las restricciones de integridad.

Las llaves foráneas permitirán mantener la integridad referencial entre las tablas relacionadas.

---

# SCRIPT SQL

```sql
CREATE DATABASE Biblioteca;
USE Biblioteca;

CREATE TABLE autores (
    id_autor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    nacionalidad VARCHAR(50)
);

CREATE TABLE libros (
    id_libro INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150),
    editorial VARCHAR(100),
    año_publicacion YEAR,
    isbn VARCHAR(20),
    id_autor INT,
    FOREIGN KEY (id_autor) REFERENCES autores(id_autor)
);

CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    telefono VARCHAR(15),
    correo VARCHAR(100)
);

CREATE TABLE prestamos (
    id_prestamo INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    id_libro INT,
    fecha_prestamo DATE,
    fecha_devolucion DATE,
    estado VARCHAR(20),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_libro) REFERENCES libros(id_libro)
);
