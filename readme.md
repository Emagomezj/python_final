# Proyecto Final: Gestión de Blogs

## Descripción

Este proyecto es una aplicación web para gestionar blogs, implementada usando Django. Permite a los usuarios crear, leer, actualizar y eliminar blogs y posts. Además, proporciona funciones de autenticación para que los usuarios puedan gestionar sus propios blogs y posts. También incluye una interfaz administrativa para que los administradores puedan gestionar todos los blogs y posts desde el panel de administración de Django.

## Principales Características

- **Gestión de Blogs**: Los usuarios pueden crear, editar y eliminar blogs.
- **Gestión de Posts**: Los usuarios pueden añadir, editar y eliminar posts dentro de los blogs.
- **Autenticación de Usuarios**: Los usuarios deben iniciar sesión para gestionar blogs y posts. Los administradores tienen permisos adicionales para gestionar todos los blogs y posts.
- **Paginación**: Los blogs y posts están paginados para una mejor visualización.
- **Búsqueda**: Los usuarios pueden buscar blogs por título, keywords y descripción, y posts por contenido.
- **Interfaz Administrativa**: Los administradores pueden gestionar blogs, imágenes de blogs y posts desde el panel de administración de Django.

## Guía de Instalación

1. **Clonar el Repositorio**

   ```bash
   git clone https://github.com/Emagomezj/python_final

2. **Instalar Dependencias**

   Asegúrate de tener un entorno virtual activado y luego instala las dependencias necesarias:
   
   ```bash
   pip install -r requirements.txt


3. **Configurar la Base de Datos**

   Ejecuta las migraciones para configurar la base de datos:
   
   ```bash
   python manage.py migrate


4. **Crear un Superusuario**

   Para acceder al panel de administración, puedes utilizar el usuario admin creado:
   
   - **Usuario**: admin
   - **Contraseña**: A.b.c.d.1234

5. **Iniciar el Servidor**

   Ejecuta el servidor de desarrollo de Django:
   
   ```bash
   python manage.py runserver


## Uso

- **Visitar el Sitio**: Abre un navegador y ve a `http://127.0.0.1:8000/` para ver la aplicación en acción.
- **Acceso al Panel de Administración**: Ve a `http://127.0.0.1:8000/admin/` e inicia sesión con las credenciales pertinentes.

## Pruebas

1. **Verificación de Funcionalidades**:
   - Asegúrate de que puedes crear, editar y eliminar blogs y posts.
   - Verifica la funcionalidad de búsqueda en el sitio.
   - Comprueba la paginación en las listas de blogs y posts.

2. **Interfaz Administrativa**:
   - Accede al panel de administración y verifica que los blogs, imágenes de blogs y posts se muestran y pueden ser gestionados correctamente.

## Datos de Prueba

A continuación se incluyen algunos usuarios y contraseñas de prueba que puedes usar para verificar la funcionalidad del sitio:

- **Usuarios**:
    - **AlonsoJerez**
    - **CarlosLopez**
    - **JohnDoe**
    - **JuanDoe**
    - **Pedro**
    - **aB**
    - **alguienAlguno**
    - **janeDoe**
    - **joaquinGonzalez**
    - **pepeGomez**
    - **pepePerez**
    - **pepitoPerez**
- **Password**: A.b.c.d.1234