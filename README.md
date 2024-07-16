# Proyecto: API Escuela de Música

## Introducción

Este proyecto es una API para la gestión de una escuela de música, diseñada para manejar estudiantes, profesores, instrumentos, niveles de aprendizaje y paquetes de instrumentos. La API está construida con FastAPI y SQLAlchemy, proporcionando endpoints para realizar operaciones CRUD (crear, leer, actualizar y eliminar) sobre los diferentes modelos de datos.

## Características principales

- Gestión de estudiantes, profesores e instrumentos.
- Gestión de niveles de aprendizaje y paquetes de instrumentos.
- Operaciones CRUD completas para cada entidad.
- Manejo de errores y logging detallado.
- Pruebas unitarias con fixtures para la base de datos.
- Interfaz gráfica para la gestión de datos utilizando Streamlit.

## Instalación

Para instalar y ejecutar el proyecto localmente, sigue estos pasos:

1. Clona el repositorio:
2. Crea un entorno virtual y activa:
3. Instala las dependencias:
4. Configura la base de datos y ejecuta la aplicación:


## Estructura de la base de datos

La base de datos está estructurada en los siguientes modelos:

- **Student**: Representa a los estudiantes, incluyendo atributos como nombre, apellido, edad, teléfono y correo electrónico.
- **Teacher**: Representa a los profesores, incluyendo atributos como nombre, apellido, teléfono y correo electrónico.
- **Instrument**: Representa a los instrumentos, incluyendo atributos como nombre y precio.
- **Level**: Representa los niveles de aprendizaje de un instrumento.
- **Pack**: Representa los paquetes de instrumentos.
- **Inscription**: Representa las inscripciones de los estudiantes en los niveles de aprendizaje de un instrumento.

## Modelos de datos

Los modelos de datos están definidos en el archivo `models.py` utilizando SQLAlchemy. Cada modelo incluye relaciones y atributos específicos, como se detalla a continuación:


## API REST

La API REST ofrece varios endpoints para interactuar con los diferentes modelos de datos. Aquí se describen algunos de los principales endpoints:

### Endpoints de Profesores

- **Crear un profesor:**
- **Obtener un profesor por ID:**
- **Listar todos los profesores:**

### Endpoints de Estudiantes
- **Crear un estudiante:**
  **Obtener un estudiante por ID:**
- **Listar todos los estudiantes:**

### Endpoints de Instrumentos
- **Crear un instrumento:**
- **Obtener un instrumento por ID:**
- **Listar todos los instrumentos:**
 
 ### Endpoints de Inscripciones
- **Crear una inscripción:**
- **Obtener una inscripción por ID:**

## Interfaz Gráfica

Se ha desarrollado una interfaz gráfica utilizando Streamlit para facilitar la gestión de los datos de la escuela de música. Esta interfaz permite realizar operaciones CRUD de manera interactiva y amigable.
Ejecución de la Interfaz Gráfica

Para ejecutar la interfaz gráfica, utiliza el siguiente comando: **streamlit run gui_test.py**

## Funcionalidades de la Interfaz Gráfica

La interfaz gráfica permite:

- Crear, leer, actualizar y eliminar estudiantes.
- Crear, leer, actualizar y eliminar profesores.
- Crear, leer, actualizar y eliminar instrumentos.
- Visualizar las inscripciones y gestionar los niveles de aprendizaje.

## Pruebas

Las pruebas están diseñadas para garantizar que todos los endpoints y operaciones de la base de datos funcionen correctamente. Se utilizan fixtures para configurar el entorno de pruebas y los datos necesarios. Los tests están ubicados en el directorio `tests`.

Para ejecutar las pruebas, utiliza el siguiente comando: **pytest**


## Despliegue

Para desplegar la aplicación en un entorno de producción, se utiliza Uvicorn con un servidor ASGI: **uvicorn  main:app --reload**


## Tecnologías empleadas

- **Lenguaje:** Python
- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Base de datos:** SQLite (para pruebas locales)
- **Servidor ASGI:** Uvicorn
- **Testing:** Pytest

## Autores
Angel Sanz Crespo
Emma Montalbán Alvaro
Jose Antonio Rodriguez
Luis Paez Bravo
Xiomara Torres