
# ![OIG1 CY](https://github.com/user-attachments/assets/2da18247-5927-4b7c-aa6b-38d59cb6f178)         Proyecto: API Escuela de Música                                        

## Introducción 

Este proyecto es una API para la gestión de una escuela de música, diseñada para manejar estudiantes, profesores, instrumentos, niveles de aprendizaje y paquetes de instrumentos. 
La API está construida con FastAPI y SQLAlchemy, proporcionando endpoints para realizar operaciones CRUD (crear, leer, actualizar y eliminar) sobre los diferentes modelos de datos. 

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

1. Clona el repositorio
2. Crea un entorno virtual y activa
3. Instala las dependencias
4. Configura la base de datos MySQL y ejecuta la aplicación

## Configuración de la base de datos MySQL

Asegúrate de tener MySQL instalado y en funcionamiento. Luego, sigue estos pasos para configurar la base de datos:

1. Inicia sesión en MySQL
2. Crea una nueva base de datos
3. Actualiza el archivo db.py con las credenciales de tu base de datos

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

Los modelos de datos están definidos en el archivo `models.py` utilizando SQLAlchemy. 


## API REST

La API REST ofrece varios endpoints para interactuar con los diferentes modelos de datos. Se describen algunos de los principales endpoints:

### Endpoints de Profesores
- Crear un profesor
- Obtener un profesor por ID
- Listar todos los profesores

### Endpoints de Estudiantes
- Crear un estudiante
- Obtener un estudiante por ID
- Listar todos los estudiantes

### Endpoints de Instrumentos
- Crear un instrumento
- Obtener un instrumento por ID
- Listar todos los instrumentos
 
 ### Endpoints de Inscripciones
- Crear una inscripción
- Obtener una inscripción por ID

### Endpoints de Cálculo de Tarifas y Facturación
- Calcular tarifa de clases para un estudiante
- Generar factura para un estudiante


## Cálculo de Tarifas

La API permite calcular las tarifas de las clases para un estudiante en función de sus inscripciones a diferentes niveles de instrumentos. 
Se tienen en cuenta posibles descuentos según el nivel y el instrumento. 
 
## Interfaz Gráfica

Se ha desarrollado una interfaz gráfica utilizando Streamlit para facilitar la gestión de los datos de la escuela de música. 
Esta interfaz permite realizar operaciones CRUD de manera interactiva y amigable.

**Ejecución de la Interfaz Gráfica**

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

Las pruebas están diseñadas para garantizar que todos los endpoints y operaciones de la base de datos funcionen correctamente. 
Se utilizan fixtures para configurar el entorno de pruebas y los datos necesarios. Los tests están ubicados en el directorio `tests`.

Para ejecutar las pruebas, utiliza el siguiente comando: **pytest**

## Control de Usuarios y Roles

El sistema implementa un control de acceso basado en roles, con los siguientes roles y permisos:

- **Superadministrador:** Tiene acceso completo a todas las funcionalidades.
- **Administrador:** Puede gestionar estudiantes, profesores, instrumentos, y ver todas las inscripciones.
- **Profesor:** Puede ver sólo los estudiantes y las inscripciones de sus clases.
    
## Despliegue

Para desplegar la aplicación en un entorno de producción, se utiliza Uvicorn con un servidor ASGI: **uvicorn  main:app --reload**

## Dockerización de la Aplicación

Para facilitar el despliegue y la ejecución de la aplicación, se ha dockerizado utilizando Docker.

## Tecnologías empleadas
![python](https://github.com/user-attachments/assets/268d8461-5957-42e8-a051-0526b44a6dbe)
![mysql2](https://github.com/user-attachments/assets/abbbb085-e538-4d15-90b0-a98609e9d42c)

![fastapi](https://github.com/user-attachments/assets/459f92f9-7758-4011-a5a6-08df65c8b685)
![sqlAlchemy2](https://github.com/user-attachments/assets/2a412693-98a9-4e0c-a785-4368e5181b80)
![uvicorn2](https://github.com/user-attachments/assets/380288af-dab7-4364-99e2-6abde4c1e7e3)

![streamlit](https://github.com/user-attachments/assets/890b99fa-009a-4cb3-bfa1-ef681ee214c6)

![pytest2](https://github.com/user-attachments/assets/1cd59921-14ce-4230-b22d-99f6865081dc)
![sqlite2](https://github.com/user-attachments/assets/acc5ba5f-a357-4677-a4da-e3eb32f4d10c)

![docke](https://github.com/user-attachments/assets/fb06b980-57d9-4d09-84dc-db23270aad3e)

![github2](https://github.com/user-attachments/assets/9811b1fb-9817-4b1d-994f-5afc6cdde005)
![trello2](https://github.com/user-attachments/assets/fbbcd782-0999-4d3c-84df-5657d44f7e57)


## Autores
- Angel Sanz Crespo
- Emma Montalbán Alvaro
- Jose Antonio Rodriguez
- Luis Paez Bravo
- Xiomara Torres
