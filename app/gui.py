# Importar streamlit y otras bibliotecas necesarias
import streamlit as st
from sqlalchemy import create_engine, func, or_, text, select
from sqlalchemy.orm import sessionmaker, Session
from datetime import date
from decimal import Decimal
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy.exc import TimeoutError
from simple_response import *
from PIL import Image
import base64
from typing import List, Tuple
import hashlib
import logging


# Importar  modelos y schemas
from models import Base, Student, Teacher, Instrument, Level, Pack, Inscription, PacksInstruments, TeachersInstruments
from schemas import StudentCreate, InscriptionCreate

# Importar funciones CRUD
from crud.students_crud import (create_student, get_students, update_student, delete_student)
from crud.inscriptions_crud import (create_inscription, get_inscriptions, delete_inscription, get_inscriptions_by_student,
                                    calculate_student_fees, generate_fee_report)

# Cargar variables de entorno
load_dotenv()

# Obtener el logger configurado
logger = logging.getLogger("music_app")

# Conexión a la base de datos
DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crear una sesión 
session = next(get_db())

# Función para manejar operaciones de base de datos de forma segura
def db_operation(operation):
    try:
        result = operation()
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        st.error(f"Ha ocurrido un error: {str(e)}")
        logger.warning("Se ha producido un error")
        return None

# Función para consultar la base de datos
def consultar_bbdd(*args, **kwargs):
    if 'student' in kwargs:
        student = kwargs['student'].strip()
        if student == "":
            students = get_students(session)
        else:
            parts = student.split()
            students = get_students(session)
            students = [s for s in students if any(part.lower() in s.first_name.lower() or part.lower() in s.last_name.lower() for part in parts)]
        
        if students:
            df = pd.DataFrame([{
                'id': s.id,
                'first_name': s.first_name,
                'last_name': s.last_name,
                'age': s.age,
                'phone': s.phone,
                'mail': s.mail,
                'family_id': s.family_id
            } for s in students])
            
            column_order = ['id', 'first_name', 'last_name', 'age', 'phone', 'mail', 'family_id']
            df = df[column_order]
            
            return df
        else:
            return pd.DataFrame()

    return pd.DataFrame()

# Función para cargar y codificar la imagen
def get_image_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    return encoded_string

def hash_string(input_string):
    # Función que devuelve el hash de una cadena de texto.
    return hashlib.md5(input_string.encode()).hexdigest()



def get_levels_with_instruments(db: Session) -> pd.DataFrame:
    """
    Recupera los niveles con los nombres de sus instrumentos asociados, ordenados por ID de nivel.
    
    """
    # Construir la consulta
    query = (
        select(Level.id, Instrument.name, Level.level)
        .join(Instrument, Level.instruments_id == Instrument.id)
        .order_by(Level.id)
    )
    
    try:
        result = db.execute(query).fetchall()
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        return pd.DataFrame()  # Devolver un DataFrame vacío en caso de error

    # Convertir el resultado a un DataFrame
    df = pd.DataFrame(result, columns=["level_id", "instrument_name", "level"])
    return df


users = {
    "admin": os.getenv("ADMIN_PASSWORD"),
    "super": os.getenv("SUPER_PASSWORD"),
    "profesor1": os.getenv("PROF1_PASSWORD"),
    "profesor2": os.getenv("PROF2_PASSWORD"),
}


#----------------------- STREAMLIT--------------------------

# Inicializar session_state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None

# Formulario de inicio de sesión
if not st.session_state.logged_in:
    # Crea dos columnas
    col1, col2 = st.columns([3, 1])

    # Muestra el logo en la segunda columna
    with col2:
        try:
            #logo_path = "logo.gif"
            logo_path = "unicorn.jpg"
            st.image(logo_path, width=300)
        except Exception as e:
            st.error(f"Error al cargar el logo: {e}")


    # Muestra el formulario de inicio de sesión en la primera columna
    with col1:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        
        st.title("Escuela de Música")
        with st.form("login_form"):
            username = st.text_input("Usuario")
            password = st.text_input("Contraseña", type="password")
            submitted = st.form_submit_button("Iniciar sesión")
            
            if submitted:
                
                if username in users  and users["admin"] == hash_string(password):
                    st.session_state.logged_in = True
                    st.session_state.user_type = "administrator"
                    st.success("Sesión iniciada como administrador")
                elif username in users  and users["profesor1"] == hash_string(password):
                    st.session_state.logged_in = True
                    st.session_state.user_type = "profesor"
                    st.success(f"Sesión iniciada como {username}")
                elif username in users  and users["profesor2"] == hash_string(password):
                    st.session_state.logged_in = True
                    st.session_state.user_type = "profesor"
                    st.success(f"Sesión iniciada como {username}")
                else:
                    st.error("Usuario o contraseña inválidos")

# Aplicación principal
if st.session_state.logged_in:
    st.title("Gestor de la Escuela de Música")
    st.write(f"Nivel de Acceso: {st.session_state.user_type}")
    #logo_path = "logo.gif"
    #st.image(logo_path, width=100)

    # Opciones de la barra lateral
    option = st.sidebar.selectbox(
        "Selecciona una opción",
        ["Consultar Alumnos", "Gestionar Alumnos", "Inscripciones",  "Instrumentos", "Profesores", "Facturación", "SQL - IA"]
    )

    if option == "Consultar Alumnos":
        st.header("Consultas")
        
        query_type = st.radio("Selecciona el tipo de consulta", ["Todos los alumnos", "Alumno por ID", "Alumno por nombre"])

        if query_type == "Todos los alumnos":
            with st.form("mostrar_todos_los_alumnos"):
                submit_all_students = st.form_submit_button("Mostrar todos los alumnos")
                if submit_all_students:
                    df_students = consultar_bbdd(student="")
                    if not df_students.empty:
                        st.write("Resultados de la consulta:")
                        st.dataframe(df_students, hide_index=True)
                    else:
                        st.info("No se encontraron alumnos.")

        elif query_type == "Alumno por ID":
            with st.form("mostrar_alumno_por_id"):
                student_id = st.number_input("ID del Alumno", min_value=1, key="view_student_id1")
                submit_student_by_id = st.form_submit_button("Mostrar alumno")
                if submit_student_by_id:
                    student = session.get(Student, student_id)
                    if student:
                        student_data = {
                            'id': student.id,
                            'first_name': student.first_name,
                            'last_name': student.last_name,
                            'age': student.age,
                            'phone': student.phone,
                            'mail': student.mail,
                            'family_id': student.family_id
                        }
                        df_student_query = pd.DataFrame([student_data])
                        st.dataframe(df_student_query, hide_index=True)
                    else:
                        st.info(f"No se ha encontrado el alumno con ID {student_id}.")
                    
        elif query_type == "Alumno por nombre":
            with st.form("search_student"):
                search_name = st.text_input("Nombre del Alumno")
                submitted = st.form_submit_button("Buscar")
                
                if submitted:
                    if search_name:
                        df_students = consultar_bbdd(student=search_name)
                        if not df_students.empty:
                            st.write("Resultados de la búsqueda:")
                            st.dataframe(df_students, hide_index=True)
                        else:
                            st.info("No se encontraron alumnos con ese nombre.")
                    else:
                        st.warning("Por favor, introduzca un nombre para buscar.")

    elif option == "Gestionar Alumnos":
        st.header("Gestión de Alumnos")

        if st.session_state.user_type == "administrator":
            student_action = st.radio("Selecciona una acción", ["Crear", "Actualizar", "Eliminar"])

            if student_action == "Crear":
                st.subheader("Crear Nuevo Alumno")
                with st.form("create_student"):
                    first_name = st.text_input("Nombre")
                    last_name = st.text_input("Apellido")
                    age = st.number_input("Edad", min_value=0, max_value=120)
                    phone = st.text_input("Teléfono")
                    mail = st.text_input("Correo Electrónico")
                    family_id = st.checkbox("Miembro de la Familia")

                    submitted = st.form_submit_button("Crear Alumno")
                    
                    if submitted:


                        # Comprobamos si existe un alumno con el mismo nombre y edad
                        existing_student = db_operation(lambda: session.query(Student).filter(
                            Student.first_name == first_name,
                            Student.last_name == last_name,
                            Student.age == age
                        ).first())

                        
                        if existing_student:
                            st.error(f"Ya existe un alumno con el nombre {first_name} {last_name} y edad {age}.")
                        else:
                            student_data = StudentCreate(
                                first_name=first_name,
                                last_name=last_name,
                                age=age,
                                phone=phone,
                                mail=mail,
                                family_id=family_id
                            )
                            new_student = db_operation(lambda: create_student(session, student_data))
                            if new_student:
                                st.success(f"Alumno creado: {new_student.first_name} {new_student.last_name}")

            elif student_action == "Actualizar":

                st.subheader("Actualizar Alumno")
                
                if 'update_student' not in st.session_state:
                    st.session_state.update_student = None

                with st.form("buscar_alumno"):
                    student_id = st.number_input("ID del Alumno a Actualizar", min_value=1)
                    buscar_submitted = st.form_submit_button("Buscar Alumno")
                    if buscar_submitted:
                        student = db_operation(lambda: session.query(Student).filter(Student.id == student_id).first())
                        if student:
                            st.session_state.update_student = student
                            student_data = {
                                'id': student.id,
                                'first_name': student.first_name,
                                'last_name': student.last_name,
                                'age': student.age,
                                'phone': student.phone,
                                'mail': student.mail,
                                'family_id': student.family_id
                            }
                            df_student_query = pd.DataFrame([student_data])
                            st.dataframe(df_student_query, hide_index=True)
                        else:
                            st.session_state.update_student = None
                            st.error("No se encontró un alumno con el ID proporcionado.")

                if st.session_state.update_student:
                    with st.form("update_student_form"):
                        first_name = st.text_input("Nuevo Nombre", value=st.session_state.update_student.first_name)
                        last_name = st.text_input("Nuevo Apellido", value=st.session_state.update_student.last_name)
                        age = st.number_input("Nueva Edad", min_value=0, max_value=120, value=st.session_state.update_student.age)
                        phone = st.text_input("Nuevo Teléfono", value=st.session_state.update_student.phone)
                        mail = st.text_input("Nuevo Correo Electrónico", value=st.session_state.update_student.mail)
                        family_id = st.checkbox("Miembro de la Familia", value=st.session_state.update_student.family_id)
                        
                        submitted = st.form_submit_button("Actualizar Alumno")
                        
                        if submitted:
                            student_data = {
                                "first_name": first_name,
                                "last_name": last_name,
                                "age": age,
                                "phone": phone,
                                "mail": mail,
                                "family_id": family_id
                            }
                            updated_student = db_operation(lambda: update_student(session, st.session_state.update_student.id, student_data))
                            if updated_student:
                                st.success(f"Alumno actualizado: {updated_student.first_name} {updated_student.last_name}")
                                st.session_state.update_student = updated_student
                            else:
                                st.error("No se pudo actualizar el alumno. Por favor, inténtelo de nuevo.")
                elif st.session_state.update_student is None:
                    st.info("Por favor, busque un alumno antes de intentar actualizarlo.")
                            

            elif student_action == "Eliminar":
                st.subheader("Eliminar Alumno")
                with st.form("eliminar_alumno"):
                    student_id = st.number_input("ID del Alumno a Eliminar", min_value=0)
                    eliminar_submitted = st.form_submit_button("Eliminar Alumno")
                    if eliminar_submitted:
                        result = db_operation(lambda: delete_student(session, student_id))
                        if result:
                            st.success(f"Alumno con ID {student_id} borrado con éxito")
                        else:
                            st.error("No se encontró un alumno con el ID proporcionado.")
        else:
            st.warning("Solo el Administrador puede gestionar alumnos.")

    elif option == "Inscripciones":
        st.header("Gestión de Inscripciones")
        
        inscription_action = st.radio("Selecciona una acción", ["Ver", "Crear", "Eliminar"])
        
        if inscription_action == "Ver":
            view_option = st.radio("Selecciona una opción de visualización", ["Todas las inscripciones", "Por ID de alumno concreto"])
            
            if view_option == "Todas las inscripciones":
                with st.form("mostrar_todas_las_inscripciones"):
                    submit_all_inscriptions = st.form_submit_button("Mostrar todas las inscripciones")
                    if submit_all_inscriptions:
                        inscriptions = db_operation(lambda: get_inscriptions(session))
                        if inscriptions:
                            df_inscriptions = pd.DataFrame(inscriptions)
                            df_inscriptions = df_inscriptions.sort_values('student_id')
                            st.dataframe(df_inscriptions, hide_index=True)
                        else:
                            st.info("No se encontraron inscripciones.")
            
            elif view_option == "Por ID de alumno concreto":
                with st.form("mostrar_inscripciones_por_id"):
                    student_id = st.number_input("ID del Alumno", min_value=1, key="view_student_id")
                    submit_student_inscriptions = st.form_submit_button("Mostrar inscripciones del alumno")
                    if submit_student_inscriptions:
                        student_inscriptions = db_operation(lambda: get_inscriptions_by_student(session, student_id))
                        if student_inscriptions:
                            df_student_inscriptions = pd.DataFrame(student_inscriptions)
                            st.dataframe(df_student_inscriptions, hide_index=True)
                        else:
                            st.info(f"No se encontraron inscripciones para el alumno con ID {student_id}.")
        
        elif inscription_action in ["Crear", "Eliminar"]:
            if st.session_state.user_type == "administrator":
                if inscription_action == "Crear":
                    st.subheader("Crear Inscripción")
                    with st.form("crear_inscripcion"):
                        student_id = st.number_input("ID del Alumno", min_value=1, key="create_student_id")
                        level_id = st.number_input("ID del Nivel", min_value=1, key="create_level_id")
                        registration_date = st.date_input("Fecha de Registro")
                        
                        submit_create_inscription = st.form_submit_button("Crear Inscripción")
                        if submit_create_inscription:
                            # Vemos si existe el alumno
                            student = db_operation(lambda: session.query(Student).get(student_id))
                            if not student:
                                st.error(f"No se encontró un alumno con el ID {student_id}.")
                            else:
                                # Comprobamos si ya existe la inscripción para el mismo alumno
                                existing_inscription = db_operation(lambda: session.query(Inscription).filter(
                                    Inscription.student_id == student_id,
                                    Inscription.level_id == level_id
                                ).first())

                                if existing_inscription:
                                    st.error(f"Ya existe una inscripción para el alumno {student.first_name} {student.last_name} en este nivel.")
                                else:
                                    inscription_data = InscriptionCreate(
                                        student_id=student_id,
                                        level_id=level_id,
                                        registration_date=registration_date
                                    )
                                    new_inscription = db_operation(lambda: create_inscription(session, inscription_data))
                                    if new_inscription:
                                        st.success(f"Inscripción creada para el alumno ID {new_inscription.student_id}")
                        
                    if st.button("Ayuda Niveles"):
                        levels_df = db_operation(lambda: get_levels_with_instruments(session))
                        if not levels_df.empty:
                            st.subheader("Niveles e Instrumentos Disponibles")
                            st.dataframe(levels_df, hide_index=True)
                        else:
                            st.info("No se encontraron niveles o instrumentos.")
               
                elif inscription_action == "Eliminar":
                    st.subheader("Eliminar Inscripción")
                    with st.form("eliminar_inscripcion"):
                        inscription_id = st.number_input("ID de la Inscripción a Eliminar", min_value=1)
                        submit_delete_inscription = st.form_submit_button("Eliminar Inscripción")
                        if submit_delete_inscription:
                            result = db_operation(lambda: delete_inscription(session, inscription_id))
                            if result:
                                st.success(f"Inscripción con ID {inscription_id} eliminada con éxito")
                            else:
                                st.error("No se encontró una inscripción con el ID proporcionado.")
            else:
                st.warning("Solo el Administrador puede crear o eliminar inscripciones.")

    elif option == "Facturación":
        if st.session_state.user_type == "administrator":
            st.header("Facturación")

            facturacion_option = st.radio("Selecciona una opción", ["Facturación Alumno Individual", "Facturación de la Escuela"])

            if facturacion_option == "Facturación Alumno Individual":
                with st.form("calcular_facturacion_alumno"):
                    student_id = st.number_input("ID del Alumno", min_value=1, key="invoice_student_id")
                    submit_calculate_invoice = st.form_submit_button("Calcular Facturación")
                    
                    if submit_calculate_invoice:
                        student = session.get(Student, student_id)
                        if student:
                            fee = db_operation(lambda: calculate_student_fees(session, student_id))
                            if fee is not None:
                                subscription_count = session.query(Inscription).filter_by(student_id=student_id).count()
                                df_fee = pd.DataFrame([{
                                    'student_id': student_id,
                                    'first_name': student.first_name,
                                    'last_name': student.last_name,
                                    'subscriptions': subscription_count,
                                    'family_id': 'Sí' if student.family_id else 'No',
                                    'total_fee': float(fee)
                                }])
                                st.write(f"Facturación para {student.first_name} {student.last_name}:")
                                st.dataframe(df_fee, hide_index=True)
                        else:
                            st.error("No se encontró un alumno con el ID proporcionado.")

            elif facturacion_option == "Facturación de la Escuela":
                with st.form("generar_facturacion_escuela"):
                    submit_generate_school_invoice = st.form_submit_button("Generar Facturación de la Escuela")
                    
                    if submit_generate_school_invoice:
                        fee_report = db_operation(lambda: generate_fee_report(session))
                        if fee_report:
                            df_fee_report = pd.DataFrame(fee_report)
                            
                            total_sum = df_fee_report['total_fee'].sum()
                            st.markdown(f"**Facturación Total de la Escuela: {total_sum:.2f} €/Mes**")

                            st.write("Desglose de Facturación por Alumno:")
                            st.dataframe(df_fee_report, hide_index=True)

                            st.write("Estadísticas de Facturación:")
                            st.write(f"Número de alumnos facturados: {len(df_fee_report)}")
                            st.write(f"Facturación promedio por alumno: {df_fee_report['total_fee'].mean():.2f}")
                            st.write(f"Facturación máxima: {df_fee_report['total_fee'].max():.2f}")
                            st.write(f"Facturación mínima: {df_fee_report['total_fee'].min():.2f}")
        else:
            st.warning("Solo el Administrador puede acceder a Facturación.")


    elif option == "Instrumentos":
        st.header("Gestión de Instrumentos")
        
        instrument_action = st.radio("Selecciona una acción", ["Ver", "Crear", "Actualizar Precio",  "Eliminar"])
        
        if instrument_action == "Ver":
            
            st.subheader("Ver Instrumentos")
            
            # Añadir un formulario con un botón para activar la visualización de instrumentos
            with st.form("ver_instrumentos"):
                submitted = st.form_submit_button("Mostrar Instrumentos")
                
                if submitted:
                    instruments = db_operation(lambda: session.query(Instrument).all())
                    if instruments:
                        df_instruments = pd.DataFrame([{
                            'id': i.id,
                            'name': i.name,
                            'price': float(i.price)
                        } for i in instruments])
                        st.dataframe(df_instruments, hide_index=True)
                    else:
                        st.info("No se encontraron instrumentos.")
        
        elif instrument_action in ["Crear", "Actualizar Precio",  "Eliminar"]:
            if st.session_state.user_type == "administrator":
                if instrument_action == "Crear":
                    st.subheader("Crear Instrumento")
                    with st.form("create_instrument"):
                        name = st.text_input("Nombre del Instrumento")
                        price = st.number_input("Precio", min_value=0.0, step=0.01)
                        
                        submitted = st.form_submit_button("Crear Instrumento")
                        
                        if submitted:
                            # Comprobar si ya existe un instrumento con el mismo nombre
                            def check_existing_instrument():
                                existing_instrument = session.query(Instrument).filter(Instrument.name == name).first()
                                return existing_instrument

                            existing_instrument = db_operation(check_existing_instrument)

                            if existing_instrument:
                                st.error(f"Ya existe un instrumento con el nombre '{name}'.")
                            else:
                                def create_instrument_op():
                                    new_instrument = Instrument(name=name, price=Decimal(str(price)))
                                    session.add(new_instrument)
                                    session.flush()
                                    return new_instrument

                                new_instrument = db_operation(create_instrument_op)
                                if new_instrument:
                                    st.success(f"Instrumento creado: {new_instrument.name} - Precio: {new_instrument.price}")


                elif instrument_action == "Actualizar Precio":
                    st.subheader("Actualizar Precio del Instrumento")
                    with st.form("update_instrument_price"):
                        instrument_id = st.number_input("ID del Instrumento", min_value=1)
                        new_price = st.number_input("Nuevo Precio", min_value=0.0, step=0.01)
                        
                        submitted = st.form_submit_button("Actualizar Precio")
                        
                        if submitted:
                            def update_instrument_price_op():
                                instrument = session.get(Instrument, instrument_id)
                                if instrument:
                                    instrument.price = Decimal(str(new_price))
                                    session.flush()
                                return instrument

                            updated_instrument = db_operation(update_instrument_price_op)
                            if updated_instrument:
                                st.success(f"Precio actualizado para el instrumento {updated_instrument.name}: {updated_instrument.price}")
                            else:
                                st.error("Instrumento no encontrado")
                #
                elif instrument_action == "Eliminar":
                    st.subheader("Eliminar Instrumento")
                    with st.form("eliminar_instrumento"):
                        instrument_id = st.number_input("ID del Instrumento a Eliminar", min_value=1)
                        submitted = st.form_submit_button("Eliminar Instrumento")
                        
                        if submitted:
                            def delete_instrument_op():
                                instrument = session.get(Instrument, instrument_id)
                                if instrument:
                                    # Comprobar si el instrumento está asociado a algún nivel
                                    associated_levels = session.query(Level).filter(Level.instruments_id == instrument_id).first()
                                    if associated_levels:
                                        return "associated"
                                    session.delete(instrument)
                                    session.flush()
                                    return True
                                return False

                            result = db_operation(delete_instrument_op)
                            if result == True:
                                st.success(f"Instrumento con ID {instrument_id} eliminado con éxito")
                            elif result == "associated":
                                st.error(f"No se puede eliminar el instrumento con ID {instrument_id} porque está asociado a uno o más niveles.")
                            else:
                                st.error("Instrumento no encontrado")
            else:
                st.warning("Solo el Administrador puede crear o actualizar instrumentos.")
                

    elif option == "Profesores":
        st.header("Gestión de Profesores")

        teacher_action = st.radio("Selecciona una acción", ["Consultar", "Crear", "Actualizar", "Eliminar"])

        if teacher_action == "Consultar":
            st.subheader("Consultar Profesores")
            with st.form("consultar_profesores"):
                submitted = st.form_submit_button("Mostrar todos los profesores")
                if submitted:
                    teachers = db_operation(lambda: session.query(Teacher).all())
                    if teachers:
                        df_teachers = pd.DataFrame([{
                            'id': t.id,
                            'first_name': t.first_name,
                            'last_name': t.last_name,
                            'phone': t.phone,
                            'mail': t.mail
                        } for t in teachers])
                        st.dataframe(df_teachers, hide_index=True)
                    else:
                        st.info("No se encontraron profesores.")

        elif teacher_action in ["Crear", "Actualizar", "Eliminar"]:
            if st.session_state.user_type == "administrator":
                if teacher_action == "Crear":
                    st.subheader("Crear Nuevo Profesor")
                    with st.form("crear_profesor"):
                        first_name = st.text_input("Nombre")
                        last_name = st.text_input("Apellido")
                        phone = st.text_input("Teléfono")
                        mail = st.text_input("Correo Electrónico")
                        submitted = st.form_submit_button("Crear Profesor")
                        
                        if submitted:
                            def create_teacher_op():
                                new_teacher = Teacher(first_name=first_name, last_name=last_name, phone=phone, mail=mail)
                                session.add(new_teacher)
                                session.flush()
                                return new_teacher

                            new_teacher = db_operation(create_teacher_op)
                            if new_teacher:
                                st.success(f"Profesor creado: {new_teacher.first_name} {new_teacher.last_name}")

                elif teacher_action == "Actualizar":
                    st.subheader("Actualizar Profesor")
                    with st.form("actualizar_profesor"):
                        teacher_id = st.number_input("ID del Profesor", min_value=1)
                        first_name = st.text_input("Nuevo Nombre")
                        last_name = st.text_input("Nuevo Apellido")
                        phone = st.text_input("Nuevo Teléfono")
                        mail = st.text_input("Nuevo Correo Electrónico")
                        submitted = st.form_submit_button("Actualizar Profesor")
                        
                        if submitted:
                            def update_teacher_op():
                                teacher = session.get(Teacher, teacher_id)
                                if teacher:
                                    teacher.first_name = first_name or teacher.first_name
                                    teacher.last_name = last_name or teacher.last_name
                                    teacher.phone = phone or teacher.phone
                                    teacher.mail = mail or teacher.mail
                                    session.flush()
                                return teacher

                            updated_teacher = db_operation(update_teacher_op)
                            if updated_teacher:
                                st.success(f"Profesor actualizado: {updated_teacher.first_name} {updated_teacher.last_name}")
                            else:
                                st.error("Profesor no encontrado")

                elif teacher_action == "Eliminar":
                    st.subheader("Eliminar Profesor")
                    with st.form("eliminar_profesor"):
                        teacher_id = st.number_input("ID del Profesor a Eliminar", min_value=1)
                        submitted = st.form_submit_button("Eliminar Profesor")
                        
                        if submitted:
                            def delete_teacher_op():
                                teacher = session.get(Teacher, teacher_id)
                                if teacher:
                                    session.delete(teacher)
                                    session.flush()
                                    return True
                                return False

                            result = db_operation(delete_teacher_op)
                            if result:
                                st.success(f"Profesor con ID {teacher_id} eliminado con éxito")
                            else:
                                st.error("Profesor no encontrado")
            else:
                st.warning("Solo el Administrador puede crear, actualizar o eliminar profesores.")

    elif option == "SQL - IA":
        if st.session_state.user_type == "administrator":
            st.header("Ejecutar Instrucciones SQL")

            # Initialize session state for authentication if not exists
            if 'super_user_authenticated' not in st.session_state:
                st.session_state.super_user_authenticated = False

            # Access level selection
            access_level = st.radio("Nivel de Acceso", ["Admin", "Super-user"])

            # Password input for Super-user
            if access_level == "Super-user" and not st.session_state.super_user_authenticated:
                with st.expander("Autenticación de Super-user", expanded=True):
                    with st.form("autenticar_super_user"):
                        super_user_password = st.text_input("Ingrese la contraseña de Super-user:", type="password")
                        submit_authenticate = st.form_submit_button("Autenticar")
                        
                        if submit_authenticate:
                            if users["super"] == hash_string(super_user_password):
                                st.session_state.super_user_authenticated = True
                                st.success("Autenticación realizada con éxito.")
                            else:
                                st.error("Contraseña incorrecta.")
            
            # Display current authentication status
            if access_level == "Super-user":
                if st.session_state.super_user_authenticated:
                    st.info("Estado: Autenticado como Super-user")
                else:
                    st.info("Estado: No autenticado como Super-user")

            # New text area for user input (always visible)
            user_input = st.text_area("**Introduzca su consulta en Lenguaje Natural:**", height=100)

            # Button to generate SQL (always visible)
            if st.button("Generar SQL"):
                if access_level == "Super-user" and st.session_state.super_user_authenticated:
                    if user_input:
                        # Call the dame_sql function
                        generated_sql = dame_sql(user_input)
                        # Store the generated SQL in session state
                        st.session_state.generated_sql = generated_sql
                        st.success("SQL generado con éxito.")
                    else:
                        st.warning("Por favor, introduzca una consulta en lenguaje natural.")
                else:
                    st.error("Solo los Super-users autenticados pueden generar SQL.")

            # Text area for SQL query input
            with st.form("ejecutar_consulta_sql"):
                query = st.text_area("Introduzca su consulta SQL aquí:", 
                                     value=st.session_state.get('generated_sql', ''),
                                     height=150)
                submit_execute_query = st.form_submit_button("Ejecutar Código")

                if submit_execute_query:
                    if query:
                        # Check access level, authentication, and query type
                        if access_level == "Admin" and not query.strip().upper().startswith("SELECT"):
                            st.error("Como Admin, solo se permiten consultas SELECT.")
                        elif access_level == "Super-user" and not st.session_state.super_user_authenticated:
                            st.error("Por favor, autentíquese como Super-user antes de ejecutar la consulta.")
                        else:
                            try:
                                # Execute the query using SQLAlchemy with a timeout
                                from sqlalchemy.exc import TimeoutError
                                
                                # Start a transaction
                                with session.begin():
                                    result = session.execute(text(query.strip()), execution_options={"timeout": 10})
                                    
                                    # Check if the query returns rows
                                    if result.returns_rows:
                                        # Fetch results (limit to 1000 rows for safety)
                                        data = result.fetchmany(1000)
                                        
                                        if data:
                                            # Get column names
                                            columns = result.keys()
                                            
                                            # Create a DataFrame
                                            df = pd.DataFrame(data, columns=columns)
                                            
                                            # Display the results
                                            st.subheader("Resultado de la Instrucción:")
                                            st.dataframe(df, hide_index=True)
                                            
                                            # Display the number of rows returned
                                            st.info(f"El código devolvió {len(df)} filas")
                                        else:
                                            st.info("La consulta no devolvió resultados.")
                                    
                                    else:
                                        # For non-SELECT queries, show the number of affected rows
                                        st.success(f"Consulta ejecutada con éxito. Filas afectadas: {result.rowcount}")
                            
                            except TimeoutError:
                                st.error("La consulta excedió el tiempo límite de ejecución.")
                            except Exception as e:
                                st.error(f"Error al ejecutar la consulta: {str(e)}")
                    else:
                        st.warning("Por favor, ingrese código SQL.")
        else:
            st.error("Solo el Administrador puede acceder a esta sección.")

# Logout button
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.super_user_authenticated = False
    st.rerun()

# Close the session at the end
session.close()
