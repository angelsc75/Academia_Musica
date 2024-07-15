import streamlit as st
from sqlalchemy import create_engine, func, or_
from sqlalchemy.orm import sessionmaker
from datetime import date
from decimal import Decimal
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy.exc import TimeoutError
from sqlalchemy import text


# Import your models and schemas
from models import Base, Student, Teacher, Instrument, Level, Pack, Inscription, PacksInstruments, TeachersInstruments
from schemas import StudentCreate, InscriptionCreate

# Import CRUD functions

from crud.students_crud import (create_student, get_students, update_student, delete_student)

from crud.inscriptions_crud import (create_inscription, get_inscriptions, delete_inscription, get_inscriptions_by_student,
                                    calculate_student_fees, generate_fee_report)

# Load environment variables
load_dotenv()

# Database connection
DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a session for Streamlit to use
session = next(get_db())

# Function to handle database operations safely
def db_operation(operation):
    try:
        result = operation()
        session.commit()
        return result
    except Exception as e:
        session.rollback()
        st.error(f"An error occurred: {str(e)}")
        return None

# Function to query the database
def consultar_bbdd(*args, **kwargs):
    if 'student' in kwargs:
        student = kwargs['student'].strip()
        if student == "":
            # Return all students
            students = get_students(session)
        else:
            # Split the search input into parts
            parts = student.split()
            
            # Use get_students with a filter
            students = get_students(session)
            students = [s for s in students if any(part.lower() in s.first_name.lower() or part.lower() in s.last_name.lower() for part in parts)]
        
        if students:  # Only create DataFrame if students were found
            # Convert to DataFrame
            df = pd.DataFrame([{
                'id': s.id,
                'first_name': s.first_name,
                'last_name': s.last_name,
                'age': s.age,
                'phone': s.phone,
                'mail': s.mail,
                'family_id': s.family_id
            } for s in students])
            
            # Reorder columns
            column_order = ['id', 'first_name', 'last_name', 'age', 'phone', 'mail', 'family_id']
            df = df[column_order]
            
            return df
        else:
            return pd.DataFrame()  # Return an empty DataFrame if no students were found

    return pd.DataFrame()  # Return an empty DataFrame if no case is met


# Streamlit app
if 'selected_option' not in st.session_state:
    st.session_state.selected_option = "Consultar Alumnos"

# Use the remembered option or update it if changed
option = st.sidebar.selectbox(
    "Selecciona una opción",
    ["Consultar Alumnos", "Gestionar Alumnos", "Inscripciones", "Facturación", "Instrumentos"],
    index=["Consultar Alumnos", "Gestionar Alumnos", "Inscripciones", "Facturación", "Instrumentos"].index(st.session_state.selected_option)
)

# Update the remembered option
st.session_state.selected_option = option

if option == "Gestionar Alumnos":
    st.header("Gestión de Alumnos")

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

elif option == "Consultar Alumnos":
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


elif option == "Consultar Alumnos":
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
    
    elif inscription_action == "Crear":
        st.subheader("Crear Inscripción")
        with st.form("crear_inscripcion"):
            student_id = st.number_input("ID del Alumno", min_value=1, key="create_student_id")
            level_id = st.number_input("ID del Nivel", min_value=1, key="create_level_id")
            registration_date = st.date_input("Fecha de Registro")
            
            submit_create_inscription = st.form_submit_button("Crear Inscripción")
            if submit_create_inscription:
                inscription_data = InscriptionCreate(
                    student_id=student_id,
                    level_id=level_id,
                    registration_date=registration_date
                )
                new_inscription = db_operation(lambda: create_inscription(session, inscription_data))
                if new_inscription:
                    st.success(f"Inscripción creada para el alumno ID {new_inscription.student_id}")

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


elif option == "Facturación":
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
                    st.markdown(f"**Facturación Total de la Escuela: {total_sum:.2f}**")

                    st.write("Desglose de Facturación por Alumno:")
                    st.dataframe(df_fee_report, hide_index=True)

                    st.write("Estadísticas de Facturación:")
                    st.write(f"Número de alumnos facturados: {len(df_fee_report)}")
                    st.write(f"Facturación promedio por alumno: {df_fee_report['total_fee'].mean():.2f}")
                    st.write(f"Facturación máxima: {df_fee_report['total_fee'].max():.2f}")
                    st.write(f"Facturación mínima: {df_fee_report['total_fee'].min():.2f}")

elif option == "Instrumentos":
    st.header("Gestión de Instrumentos")
    
    instrument_action = st.radio("Selecciona una acción", ["Crear", "Actualizar Precio"])
    
    if instrument_action == "Crear":
        st.subheader("Crear Instrumento")
        with st.form("create_instrument"):
            name = st.text_input("Nombre del Instrumento")
            price = st.number_input("Precio", min_value=0.0, step=0.01)
            
            submitted = st.form_submit_button("Crear Instrumento")
            
            if submitted:
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





# Close the session at the end
session.close()
