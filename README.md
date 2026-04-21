<style>
  .readme {
  max-width: 900px;
  margin: 40px auto; /* mejor que 0 auto */
  padding: 20px;
}

  .center {
    text-align: center;
  }

  .badges {
    display: flex;
    justify-content: center;
    gap: 8px;
    flex-wrap: wrap;
  }
</style>

<section class="readme">

  <h1> Sistema de Gestión de Préstamos de Libros</h1>
  <p>
    API REST desarrollada con <strong>Django REST Framework</strong> para la gestión de libros y préstamos,
    permitiendo el control de disponibilidad, devoluciones parciales y completas, así como la extensión de préstamos.
    La solución implementa validaciones de negocio, control de acceso por roles y pruebas funcionales mediante Postman.
  </p>

  <hr>

  <h2> Tecnologías utilizadas</h2>

  <p style="text-align: center;">
    <img src="assets/banner.png" alt="Banner del sistema">
  </p>

  <p class="center">
  <img src="https://readme-typing-svg.herokuapp.com/?lines=Library+System+API;Django+REST+Backend;Docker+%2B+PostgreSQL&center=true&width=500&height=50">
</p>

<div class="badges">
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Django-REST-092E20?logo=django&logoColor=white">
  <img src="https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql&logoColor=white">
  <img src="https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white">
  <img src="https://img.shields.io/badge/Status-Completed-success">
</div>

  <hr>

  <h2> Funcionalidades principales</h2>

  <h3> Gestión de Libros</h3>
  <ul>
    <li>Crear, editar y eliminar libros (solo administradores)</li>
    <li>Listar libros disponibles (público)</li>
    <li>Filtros por:
      <ul>
        <li>Autor</li>
        <li>Año</li>
      </ul>
    </li>
    <li>Carga de imagen por libro (validación de tipo y tamaño)</li>
    <li>Control de inventario (copias totales y disponibles)</li>
  </ul>

  <hr>

  <h3> Gestión de Préstamos</h3>
  <ul>
    <li>Crear préstamo (usuario autenticado, soporta múltiples copias)</li>
    <li>Validación de disponibilidad (no permite préstamos sin stock)</li>
    <li>Devolución total de préstamo</li>
    <li>Devolución parcial con actualización dinámica del inventario</li>
    <li>Extensión de préstamos (+7 días)</li>
  </ul>

  <p><strong>Estados del préstamo:</strong></p>
  <ul>
    <li><code>active</code></li>
    <li><code>partial</code></li>
    <li><code>returned</code></li>
  </ul>

  <hr>

  <h3> Seguridad y control de acceso</h3>
  <ul>
    <li>Autenticación requerida para operaciones de préstamos</li>
  </ul>

  <p><strong>Roles:</strong></p>
  <ul>
    <li><strong>Admin/Staff:</strong> gestionan libros y consultan todos los préstamos</li>
    <li><strong>Usuario:</strong> solo puede consultar y operar sus propios préstamos</li>
  </ul>

  <p><strong>Reglas de seguridad:</strong></p>
  <ul>
    <li>Un usuario no puede acceder a préstamos de otros</li>
    <li>Si intenta hacerlo → <code>404 Not Found</code></li>
    <li>Solo administradores pueden gestionar libros → <code>403 Forbidden</code></li>
  </ul>

  <hr>

  <h2>🐳 Instalación con Docker</h2>

  <h3>1. Clonar repositorio</h3>
  <pre><code>git clone https://github.com/EliSalas1/library-system.git
cd library-system</code></pre>

  <h3>2. Construir y levantar contenedores</h3>
  <pre><code>docker-compose up --build</code></pre>

  <h3>3. Ejecutar migraciones</h3>
  <pre><code>docker-compose exec web python manage.py migrate</code></pre>

  <h3>4. Crear superusuario</h3>
  <pre><code>docker-compose exec web python manage.py createsuperuser</code></pre>

  <hr>

  <h2>🌐 Acceso al sistema</h2>
  <ul>
    <li>API: <a href="http://localhost:8000/api/" target="_blank">http://localhost:8000/api/</a></li>
    <li>Admin Django: <a href="http://localhost:8000/admin/" target="_blank">http://localhost:8000/admin/</a></li>
  </ul>

  <hr>

  <h2>🔑 Autenticación</h2>
  <p>La API utiliza:</p>
  <ul>
    <li>Session Authentication</li>
    <li>Basic Authentication</li>
  </ul>

  <p><strong>Para pruebas:</strong></p>
  <ul>
    <li>Navegador → iniciar sesión en <code>/api/</code> o <code>/admin/</code></li>
    <li>Postman → usar <strong>Basic Auth</strong></li>
  </ul>

  <hr>

  <h2>📡 Endpoints principales</h2>

  <h3> Libros</h3>
  <pre><code>GET     /api/books/
POST    /api/books/        (soporta imagen - multipart/form-data)
GET     /api/books/{id}/
PATCH   /api/books/{id}/
DELETE  /api/books/{id}/</code></pre>

  <hr>

  <h3> Préstamos</h3>
  <pre><code>GET     /api/loans/
POST    /api/loans/
GET     /api/loans/{id}/</code></pre>

  <hr>

  <h3> Acciones personalizadas</h3>
  <pre><code>POST /api/loans/{id}/partial_return/
POST /api/loans/{id}/return_book/
POST /api/loans/{id}/extend/</code></pre>

  <hr>

  <h2>🔍 Filtros disponibles</h2>
  <pre><code>GET /api/books/?author=Gabriel
GET /api/books/?year=2020</code></pre>

  <hr>

  <h2>🧪 Pruebas</h2>
  <p>Se incluye colección de Postman con:</p>
  <ul>
    <li>Flujo completo de préstamos</li>
    <li>Pruebas de devolución parcial y total</li>
    <li>Pruebas de extensión de préstamos</li>
    <li>Validación de carga de imágenes</li>
    <li>Validación de stock (sin disponibilidad)</li>
    <li>Casos de error (datos inválidos, cantidades incorrectas)</li>
    <li>Pruebas de seguridad (acceso restringido por usuario)</li>
    <li>Uso de variables de entorno y scripts de validación</li>
  </ul>

  <hr>

  <h2>📁 Estructura del proyecto</h2>
  <pre><code>library-system/
│
├── config/                 # Configuración principal Django
├── library/                # App principal (models, views, serializers)
│
├── docs/                   # Documentación técnica
│   └── Documentacion_Tecnica.pdf
│
├── postman/                # Pruebas de API
│   ├── Library_System.postman_collection.json
│   └── Library_System.postman_environment.json
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md</code></pre>

  <hr>

  <h2> Archivos incluidos</h2>
<ul>
  <li>Documentación técnica (PDF) en carpeta <code>/docs</code></li>
  <li>Colección Postman en carpeta <code>/postman</code></li>
  <li>Archivo de entorno de ejemplo (<code>.env.example</code>)</li>
</ul>

  <h2>📌 Notas importantes</h2>
  <ul>
    <li>Control automático de disponibilidad de libros</li>
    <li>No se permiten préstamos sin stock</li>
    <li>Soporte para múltiples copias por préstamo</li>
    <li>Devoluciones parciales con actualización de inventario</li>
    <li>Validación de imágenes (tipo y tamaño máximo)</li>
    <li>Seguridad basada en roles y filtrado por queryset</li>
  </ul>

  <hr>

  <h2>📄 Documentación adicional</h2>
  <p>Se incluye documentación técnica en formato PDF con:</p>
  <ul>
    <li>Arquitectura del sistema</li>
    <li>Diagramas (ER, clases y flujo)</li>
    <li>Requerimientos funcionales y no funcionales</li>
    <li>Criterios de aceptación</li>
    <li>Matriz de pruebas</li>
    <li>Casos de uso y actores del sistema</li>
  </ul>

  <hr>

  <h2> Autor: Salas Chacón Esther Elizabeth</h2>
  <p>Proyecto desarrollado como prueba técnica backend.</p>

</section>