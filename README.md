
# ![OIG1 CY](https://github.com/user-attachments/assets/2da18247-5927-4b7c-aa6b-38d59cb6f178)         Proyecto: API Escuela de Música                                        

## Introducción 

Este proyecto es una API para la gestión de una escuela de música, diseñada para manejar estudiantes, profesores, instrumentos, niveles de aprendizaje y paquetes de instrumentos. La API está construida con FastAPI y SQLAlchemy, proporcionando endpoints para realizar operaciones CRUD (crear, leer, actualizar y eliminar) sobre los diferentes modelos de datos.

## Características principales

- Gestión de estudiantes, profesores e instrumentos.
- Gestión de niveles de aprendizaje y paquetes de instrumentos.
- Operaciones CRUD completas para cada entidad.
- Manejo de errores y logging detallado.
- Pruebas unitarias con fixtures para la base de datos.
- Interfaz gráfica para la gestión de datos utilizando Streamlit.
- Cálculo de tarifas de clases.
- Control de usuarios con roles y permisos (superadministrador, administrador y profesor).

## Instalación

Para instalar y ejecutar el proyecto localmente, sigue estos pasos:

1. Clona el repositorio:
2. Crea un entorno virtual y activa:
3. Instala las dependencias:
4. Configura la base de datos y ejecuta la aplicación:


## Estructura de la base de datos

![Diagrama](https://github.com/user-attachments/assets/0d34f9c6-c4e2-418d-a48d-d724948ac964)

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
- **Crear un profesor**
- **Obtener un profesor por ID**
- **Listar todos los profesores**

### Endpoints de Estudiantes
- **Crear un estudiante**
  **Obtener un estudiante por ID**
- **Listar todos los estudiantes**

### Endpoints de Instrumentos
- **Crear un instrumento**
- **Obtener un instrumento por ID**
- **Listar todos los instrumentos**
 
 ### Endpoints de Inscripciones
- **Crear una inscripción**
- **Obtener una inscripción por ID**

### Endpoints de Cálculo de Tarifas y Facturación
- **Calcular tarifa de clases para un estudiante**
- **Generar factura para un estudiante**

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
- Calcular tarifas de clases con los descuentos aplicables.
- Obtener facturación por alumno.
- Obtener facturación de la escuela.
  
## Pruebas

Las pruebas están diseñadas para garantizar que todos los endpoints y operaciones de la base de datos funcionen correctamente. Se utilizan fixtures para configurar el entorno de pruebas y los datos necesarios. Los tests están ubicados en el directorio `tests`.

Para ejecutar las pruebas, utiliza el siguiente comando: **pytest**

## Control de Usuarios y Roles

El sistema implementa un control de acceso basado en roles, con los siguientes roles y permisos:

- **Superadministrador:** Tiene acceso completo a todas las funcionalidades.
- **Administrador:** Puede gestionar estudiantes, profesores, instrumentos, y ver todas las inscripciones.
- **Profesor:** Puede ver sólo los estudiantes y las inscripciones de sus clases.
    
## Despliegue

Para desplegar la aplicación en un entorno de producción, se utiliza Uvicorn con un servidor ASGI: **uvicorn  main:app --reload**


## Tecnologías empleadas
![python](https://github.com/user-attachments/assets/87934ab9-f98b-49e6-b2d0-fcc97517f9da)
![fastapi](https://github.com/user-attachments/assets/1f0cefb5-72d5-4700-82ba-fb0c44e0b3a0)
![sqlAlchemy2](https://github.com/user-attachments/assets/8cfe2f0f-18fc-4f7f-92ca-278cd697fb07)
![sqlite2](https://github.com/user-attachments/assets/83e5c083-a03e-4dd2-a480-1d71feec68a0)
![mysql2](https://github.com/user-attachments/assets/0d3e55cd-d4d8-4dee-ad3e-883d24eb7220)
![uvicorn2](https://github.com/user-attachments/assets/06a3f0f0-5a3b-4864-b49d-b2cecde22f08)
![pytest2](https://github.com/user-attachments/assets/8b150301-d11d-4a20-a361-6b89c4a0dccf)
![docke](https://github.com/user-attachments/assets/64421d38-581b-4f8b-b607-91e72ab8b225)
![streamlit](https://github.com/user-attachments/assets/49fc5241-f912-4d0d-8f1a-ce932a9cee15)
![github2](https://github.com/user-attachments/assets/94c28d85-40bf-4c98-8bb4-7cc2e745fb56) 
![trello2](https://github.com/user-attachments/assets/c03484d1-b1a8-41f8-b845-df4f810421ec)


## Autores
- Angel Sanz Crespo
- Emma Montalbán Alvaro
- Jose Antonio Rodriguez
- Luis Paez Bravo
- Xiomara Torres
