# Backend del Sistema de Gestión de Museo (ABM Museo)

Este proyecto es el backend desarrollado en Django y Django REST framework para el sistema de gestión de un museo. Proporciona una API RESTful para administrar visitantes, registros de asistencia y usuarios del sistema.

## Prerrequisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

* Python (versión 3.8 o superior recomendada)
* pip (manejador de paquetes de Python)
* Git (para clonar el repositorio)
* Un gestor de base de datos compatible con Django (ej. PostgreSQL, MySQL, SQLite). Este proyecto está configurado para conectarse a una base de datos existente.
* (Opcional pero recomendado) `virtualenv` o `venv` para crear entornos virtuales.

## Configuración del Proyecto

Sigue estos pasos para configurar el entorno de desarrollo local:

1.  **Clonar el Repositorio:**
    ```bash
    git clone <URL_DE_TU_REPOSITORIO_GIT>
    cd ABM_MUSEO_BACKEND_DJANGO 
    ```
    *(Reemplaza `<URL_DE_TU_REPOSITORIO_GIT>` con la URL real de tu repositorio en GitHub)*

2.  **Crear y Activar un Entorno Virtual:**
    Es altamente recomendado usar un entorno virtual para aislar las dependencias del proyecto.
    ```bash
    # Crear el entorno virtual (puedes nombrarlo 'venv' o como prefieras)
    python -m venv venv

    # Activar el entorno virtual
    # En Windows (Git Bash o PowerShell):
    source venv/Scripts/activate
    # En macOS y Linux:
    source venv/bin/activate
    ```

3.  **Instalar Dependencias:**
    Asegúrate de tener un archivo `requirements.txt` con todas las dependencias. Si no lo tienes, puedes generarlo con `pip freeze > requirements.txt` una vez tengas todo instalado en tu entorno virtual.
    ```bash
    pip install -r requirements.txt
    ```
    Las dependencias clave probablemente incluyan:
    * `django`
    * `djangorestframework`
    * `django-cors-headers`
    * `django-filter`
    * El conector de base de datos específico (ej. `psycopg2-binary` para PostgreSQL).

4.  **Configurar Variables de Entorno y Base de Datos:**
    Este proyecto se conecta a una base de datos existente. Deberás configurar los detalles de la conexión en `backend_museo_crud/settings.py`.
    Es una buena práctica usar variables de entorno para información sensible. Considera crear un archivo `.env` y usar una librería como `python-dotenv` para cargarlas.

    Un ejemplo de archivo `.env.example` podría ser:
    ```env
    SECRET_KEY='tu_super_secreto_django_secret_key'
    DEBUG=True

    DB_ENGINE='django.db.backends.postgresql' # o mysql, sqlite3
    DB_NAME='nombre_tu_bd'
    DB_USER='usuario_bd'
    DB_PASSWORD='password_bd'
    DB_HOST='localhost' # o la IP/hostname de tu servidor de BD
    DB_PORT='5432' # o el puerto de tu BD
    ```
    En `settings.py`, podrías cargar estas variables:
    ```python
    # backend_museo_crud/settings.py
    import os
    from dotenv import load_dotenv
    load_dotenv() # Carga variables del archivo .env

    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = os.getenv('DEBUG', 'False') == 'True' # Default a False si no está

    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE'),
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': os.getenv('DB_PORT'),
        }
    }
    ```
    *No olvides añadir `.env` a tu archivo `.gitignore` para no subir tus credenciales al repositorio.*

5.  **Aplicar Migraciones (Opcional para Modelos Existentes):**
    Dado que los modelos principales de la app `api` están configurados con `managed = False`, Django no intentará crear o modificar esas tablas. Sin embargo, Django tiene sus propias tablas internas (para autenticación, sesiones, etc.) que sí necesitan migraciones.
    ```bash
    python manage.py migrate
    ```

## Ejecutar el Servidor de Desarrollo

Una vez configurado el proyecto y activado el entorno virtual:

```bash
python manage.py runserver
