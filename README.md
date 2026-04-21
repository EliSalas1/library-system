# 📚 Sistema de Gestión de Préstamos de Libros

API REST desarrollada con Django REST Framework para la gestión de libros y préstamos, permitiendo el control de disponibilidad, devoluciones y extensiones de préstamos.

---

## 🚀 Tecnologías utilizadas 
<p align="center">
  <img src="https://raw.githubusercontent.com/tu-usuario/library-system/main/assets/banner.png"/>
</p>
<p align="center"> <img src="https://readme-typing-svg.herokuapp.com/?lines=Library+System+API;Django+REST+Backend;Docker+%2B+PostgreSQL&center=true&width=500&height=50"> </p> <p align="center"> <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/Django-REST-092E20?logo=django&logoColor=white"/> <img src="https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql&logoColor=white"/> <img src="https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white"/> <img src="https://img.shields.io/badge/Status-Completed-success"/> </p>

---

## 📦 Funcionalidades principales

### 📚 Gestión de Libros

* Crear, editar, eliminar libros (solo administradores)
* Listar libros disponibles (público)
* Filtros por:

  * Autor
  * Año
* Carga de imagen por libro
* Control de inventario (copias totales y disponibles)

---

### 📦 Gestión de Préstamos

* Crear préstamo (usuario autenticado, soporta múltiples copias)
* Devolver libro (total)
* Devolución parcial de préstamo
* Extender préstamo (+7 días)

**Estados:**

* `active`
* `partial`
* `returned`
---

### 🔐 Seguridad y control de acceso

* Autenticación requerida para préstamos

**Roles:**

* **Admin/Staff:** gestionan libros y ven todos los préstamos
* **Usuario:** solo puede ver y operar sobre sus propios préstamos

**Regla de seguridad:**

* Un usuario no puede acceder a préstamos de otros
* Si intenta hacerlo → `404 Not Found`

---

## 🐳 Instalación con Docker

### 1. Clonar repositorio

```bash
git clone https://github.com/EliSalas1/library-system.git
cd library-system
```

### 2. Construir y levantar contenedores

```bash
docker-compose up --build
```

### 3. Ejecutar migraciones

```bash
docker-compose exec web python manage.py migrate
```

### 4. Crear superusuario

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## 🌐 Acceso al sistema

* API: http://localhost:8000/api/
* Admin Django: http://localhost:8000/admin/

---

## 🔑 Autenticación

La API utiliza:

* Session Authentication
* Basic Authentication

**Para pruebas:**

* Navegador → iniciar sesión en `/api/` o `/admin/`
* Postman → usar **Basic Auth**

---

## 📡 Endpoints principales

### 📚 Libros

```bash
GET     /api/books/
POST    /api/books/
GET     /api/books/{id}/
PUT     /api/books/{id}/
DELETE  /api/books/{id}/
```

---

### 📦 Préstamos

```bash
GET     /api/loans/
POST    /api/loans/
GET     /api/loans/{id}/
```

---

### 🔹 Acciones personalizadas

```bash
POST /api/loans/{id}/return_book/
POST /api/loans/{id}/extend/
POST /api/loans/{id}/partial_return/
```

---

## 🔍 Filtros disponibles

```bash
GET /api/books/?author=Gabriel
GET /api/books/?year=2020
```

---

## 🧪 Pruebas

Se incluye colección de Postman con:

* Creación de libros
* Creación de préstamos
* Devolución
* Extensión
* Casos de error
* Validaciones

---

## 📁 Estructura del proyecto

```bash
library-system/
│
├── config/           # Configuración principal Django
├── library/          # App principal
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 📌 Notas importantes

* Control automático de disponibilidad de libros
* No se permiten préstamos sin stock
* Usuarios solo pueden operar sus propios préstamos
* Validación de imágenes (tipo y tamaño)

---

## 📄 Documentación adicional

Se incluye documentación técnica en PDF con:

* Diagramas
* Requerimientos funcionales
* Matriz de pruebas
* Casos de uso

---

## 👩‍💻 Autor

Proyecto desarrollado como prueba técnica backend.
