from sqlalchemy import create_engine, ForeignKey, DECIMAL, Date, Time, Enum, func, Boolean, select, Table, Column, Integer, String, Numeric, DateTime
from sqlalchemy import and_
from sqlalchemy.orm import relationship, sessionmaker, declarative_base, Mapped, mapped_column
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import date, time
from dotenv import load_dotenv
import pandas as pd
import os

from decimal import Decimal, InvalidOperation,  ROUND_HALF_UP



Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column()
    mail: Mapped[str] = mapped_column()
    family_id: Mapped[bool] = mapped_column(Boolean)

    inscriptions: Mapped[List["Inscription"]] = relationship(back_populates="student", cascade="all, delete-orphan")

class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    phone: Mapped[str] = mapped_column()
    mail: Mapped[str] = mapped_column()

    instruments: Mapped[List["Instrument"]] = relationship(secondary="teachers_instruments", back_populates="teachers")

class Instrument(Base):
    __tablename__ = 'instruments'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL)

    levels: Mapped[List["Level"]] = relationship(back_populates="instrument")
    packs: Mapped[List["Pack"]] = relationship(secondary="packs_instruments", back_populates="instruments")
    teachers: Mapped[List["Teacher"]] = relationship(secondary="teachers_instruments", back_populates="instruments")


class Level(Base):
    __tablename__ = 'levels'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    instruments_id: Mapped[int] = mapped_column(ForeignKey('instruments.id'))
    level: Mapped[str] = mapped_column(nullable=False)

    instrument: Mapped["Instrument"] = relationship(back_populates="levels")
    inscriptions: Mapped[List["Inscription"]] = relationship(back_populates="level")


class Pack(Base):
    __tablename__ = 'packs'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pack: Mapped[str] = mapped_column(nullable=False)
    discount_1: Mapped[DECIMAL] = mapped_column(DECIMAL)
    discount_2: Mapped[DECIMAL] = mapped_column(DECIMAL)

    instruments: Mapped[List["Instrument"]] = relationship(secondary="packs_instruments", back_populates="packs")


class PacksInstruments(Base):
    __tablename__ = 'packs_instruments'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    instrument_id: Mapped[int] = mapped_column(ForeignKey('instruments.id'))
    packs_id: Mapped[int] = mapped_column(ForeignKey('packs.id'))

class Inscription(Base):
    __tablename__ = 'inscriptions'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    level_id: Mapped[int] = mapped_column(ForeignKey('levels.id'))
    registration_date: Mapped[date] = mapped_column(Date)

    student: Mapped["Student"] = relationship(back_populates="inscriptions")
    level: Mapped["Level"] = relationship(back_populates="inscriptions")

class TeachersInstruments(Base):
    __tablename__ = 'teachers_instruments'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'))
    instrument_id: Mapped[int] = mapped_column(ForeignKey('instruments.id'))


#----------------------------------------------------------------------------------------------

def create_student(first_name, last_name, age, phone, mail, family_id):
    # Verificar si un alumno con el mismo nombre y edad ya existe
    existing_student = session.query(Student).filter(
        and_(
            Student.first_name == first_name,
            Student.last_name == last_name,
            Student.age == age
        )
    ).first()

    if existing_student:
        print(f"El alumno {first_name} {last_name}, edad {age}, ya existe con el ID {existing_student.id}")
        return existing_student

    # Si no existe un alumno con esos datos, crear uno nuevo
    new_student = Student(
        first_name=first_name,
        last_name=last_name,
        age=age,
        phone=phone,
        mail=mail,
        family_id=family_id
    )
    session.add(new_student)
    session.commit()
    print(f"Nuevo alumno creado: {new_student.first_name} {new_student.last_name} con ID {new_student.id}")
    return new_student


def update_student(student_id, **kwargs):
    student = session.get(Student, student_id)
    if student:
        for key, value in kwargs.items():
            setattr(student, key, value)
        session.commit()
        return student
    return None

def delete_student(student_id):
    student = session.get(Student, student_id)
    if student:
        try:
            session.delete(student)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error al eliminar al alumno: {str(e)}")
            return False
    else:
        return False

def make_inscription(student_id, level_id, registration_date):
    # Verificar si el alumno ya tiene esta inscripción
    existing_inscription = session.query(Inscription).filter(
        and_(
            Inscription.student_id == student_id,
            Inscription.level_id == level_id
        )
    ).first()

    if existing_inscription:
        return f"La inscripción ya existe para el alumno con ID {student_id} en el nivel ID {level_id}"

    # Si no existe inscripción, crear una nueva
    new_inscription = Inscription(student_id=student_id, level_id=level_id, registration_date=registration_date)
    session.add(new_inscription)
    session.commit()
    return f"Nueva inscripción creada para el alumno con ID {student_id} en el nivel ID {level_id}"

def delete_inscription(inscription_id):
    inscription = session.get(Inscription, inscription_id)
    if inscription:
        session.delete(inscription)
        session.commit()
        return True
    return False

def create_instrument(name, price):
    new_instrument = Instrument(name=name, price=price)
    session.add(new_instrument)
    session.commit()
    return new_instrument

def update_instrument_price(instrument_id, new_price):
    instrument = session.get(Instrument, instrument_id)
    if instrument:
        instrument.price = new_price
        session.commit()
        return instrument
    return None

def view_student_details(student_id):
    student = session.get(Student, student_id)
    if not student:
        return "Alumno no encontrado."

    # Consulta para obtener las inscripciones del alumno con el instrumento y nivel relacionados
    stmt = (
        select(Inscription, Level, Instrument)
        .join(Student)
        .join(Level)
        .join(Instrument, Level.instruments_id == Instrument.id)
        .where(Student.id == student_id)
    )
    results = session.execute(stmt).all()

    # Preparar detalles del alumno
    details = {
        "id": student.id,
        "name": f"{student.first_name} {student.last_name}",
        "age": student.age,
        "phone": student.phone,
        "mail": student.mail,
        "family_member": "Sí" if student.family_id else "No",
        "inscriptions": []
    }

    # Añadir detalles de inscripciones
    for inscription, level, instrument in results:
        details["inscriptions"].append({
            "instrument": instrument.name,
            "level": level.level,
            "registration_date": inscription.registration_date
        })

    # Formatear la salida
    output = f"Detalles del Alumno para el ID {details['id']}:\n"
    output += f"Nombre: {details['name']}\n"
    output += f"Edad: {details['age']}\n"
    output += f"Teléfono: {details['phone']}\n"
    output += f"Correo: {details['mail']}\n"
    output += f"Familiar en la Escuela: {details['family_member']}\n"
    output += "Inscripciones:\n"
    
    if details['inscriptions']:
        for idx, insc in enumerate(details['inscriptions'], 1):
            output += f"  {idx}. Instrumento: {insc['instrument']}, "
            output += f"Nivel: {insc['level']}, "
            output += f"Registrado el: {insc['registration_date']}\n"
    else:
        output += "  No se encontraron inscripciones.\n"

    return output



def calculate_student_fees(student_id):
    student = session.get(Student, student_id)
    if not student:
        return "Alumno no encontrado."

    inscriptions = session.query(Inscription).filter(Inscription.student_id == student_id).all()
    if not inscriptions:
        return "No se encontraron inscripciones para este alumno."

    total_fee = Decimal('0.00')
    pack_inscriptions = {}

    # Agrupar inscripciones por pack
    for inscription in inscriptions:
        instrument = inscription.level.instrument
        pack = session.query(Pack).join(PacksInstruments).filter(PacksInstruments.instrument_id == instrument.id).first()
        
        pack_id = pack.id if pack else None  # Instrumentos sin pack

        if pack_id not in pack_inscriptions:
            pack_inscriptions[pack_id] = []
        pack_inscriptions[pack_id].append((instrument, pack))

    # Debugging, imprimimos las inscripciones por pack
    """
    print("\n Inscripciones agrupadas por Pack:")
    for pack_id, insc_list in pack_inscriptions.items():
        print(f"Pack ID: {pack_id}")
        for instrument, pack in insc_list:
            print(f"  Instrument: {instrument.name}, Price: {instrument.price}")
    """
    # Calcula precio para cada pack
    for pack_id, insc_list in pack_inscriptions.items():
        insc_list.sort(key=lambda x: x[0].price, reverse=True)  # por precio descendente

        for i, (instrument, pack) in enumerate(insc_list):
            price = Decimal(instrument.price)

            if pack:
                if i == 1:  # Segunda inscripción del pack
                    discount = Decimal(pack.discount_1)
                    price -= price * discount / 100
                elif i > 1:  # Tercera inscripción en adelante
                    discount = Decimal(pack.discount_2)
                    price -= price * discount / 100

            total_fee += price

    # Aplicar descuento familiar si procede
    if student.family_id:
        total_fee *= Decimal('0.90')  

    final_fee = total_fee.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return final_fee

def create_instrument(db: Session, name: str, price: Decimal) -> Instrument:
    """
    Crea un nuevo instrumento en la base de datos.
    
    :param db: Sesión de base de datos SQLAlchemy
    :param name: Nombre del instrumento
    :param price: Precio del instrumento
    :return: Objeto Instrument creado
    """
    # Crear una nueva instancia de Instrument
    new_instrument = Instrument(name=name, price=price)
    
    # Añadir el nuevo instrumento a la sesión
    db.add(new_instrument)
    
    try:
        # Intentar confirmar los cambios en la base de datos
        db.commit()
        # Refrescar el objeto para obtener cualquier valor generado por la base de datos
        db.refresh(new_instrument)
    except IntegrityError:
        # Si hay un error de integridad (por ejemplo, nombre duplicado), revertir los cambios
        db.rollback()
        raise ValueError(f"Ya existe un instrumento con el nombre '{name}'")
    
    return new_instrument

def get_instrument(db: Session, instrument_id: int) -> Optional[Instrument]:
    """
    Recupera un instrumento por su ID.
    
    :param db: Sesión de base de datos SQLAlchemy
    :param instrument_id: ID del instrumento a recuperar
    :return: Objeto Instrument si se encuentra, None en caso contrario
    """
    # Consultar la base de datos para encontrar el instrumento por su ID
    return db.query(Instrument).filter(Instrument.id == instrument_id).first()

def get_all_instruments(db: Session) -> List[Instrument]:
    """
    Recupera todos los instrumentos de la base de datos.
    
    :param db: Sesión de base de datos SQLAlchemy
    :return: Lista de todos los objetos Instrument
    """
    # Consultar todos los instrumentos en la base de datos
    return db.query(Instrument).all()

def update_instrument(db: Session, instrument_id: int, name: Optional[str] = None, price: Optional[Decimal] = None) -> Optional[Instrument]:
    """
    Actualiza un instrumento existente en la base de datos.
    
    :param db: Sesión de base de datos SQLAlchemy
    :param instrument_id: ID del instrumento a actualizar
    :param name: Nuevo nombre para el instrumento (opcional)
    :param price: Nuevo precio para el instrumento (opcional)
    :return: Objeto Instrument actualizado si se encuentra, None en caso contrario
    """
    # Obtener el instrumento de la base de datos
    instrument = get_instrument(db, instrument_id)
    if instrument:
        # Actualizar los campos si se proporcionan nuevos valores
        if name:
            instrument.name = name
        if price is not None:
            instrument.price = price
        
        try:
            # Intentar confirmar los cambios en la base de datos
            db.commit()
            # Refrescar el objeto para obtener cualquier valor actualizado
            db.refresh(instrument)
        except IntegrityError:
            # Si hay un error de integridad (por ejemplo, nombre duplicado), revertir los cambios
            db.rollback()
            raise ValueError(f"Ya existe un instrumento con el nombre '{name}'")
        
        return instrument
    return None

def delete_instrument(db: Session, instrument_id: int) -> bool:
    """
    Elimina un instrumento de la base de datos.
    
    :param db: Sesión de base de datos SQLAlchemy
    :param instrument_id: ID del instrumento a eliminar
    :return: True si el instrumento fue eliminado, False si no se encontró
    """
    # Obtener el instrumento de la base de datos
    instrument = get_instrument(db, instrument_id)
    if instrument:
        # Si se encuentra el instrumento, eliminarlo y confirmar los cambios
        db.delete(instrument)
        db.commit()
        return True
    return False

def get_instruments_by_price_range(db: Session, min_price: Decimal, max_price: Decimal) -> List[Instrument]:
    """
    Recupera instrumentos dentro de un rango de precios específico.
    
    :param db: Sesión de base de datos SQLAlchemy
    :param min_price: Precio mínimo
    :param max_price: Precio máximo
    :return: Lista de objetos Instrument dentro del rango de precios
    """
    # Consultar instrumentos dentro del rango de precios especificado
    return db.query(Instrument).filter(Instrument.price >= min_price, Instrument.price <= max_price).all()

def get_instruments_by_teacher(db: Session, teacher_id: int) -> List[Instrument]:
    """
    Recupera todos los instrumentos enseñados por un profesor específico.
    
    :param db: Sesión de base de datos SQLAlchemy
    :param teacher_id: ID del profesor
    :return: Lista de objetos Instrument enseñados por el profesor
    """
    # Consultar instrumentos asociados con el profesor especificado
    return db.query(Instrument).join(Instrument.teachers).filter(Teacher.id == teacher_id).all()

def get_instruments_by_pack(db: Session, pack_id: int) -> List[Instrument]:
    """
    Recupera todos los instrumentos incluidos en un pack específico.
    
    :param db: Sesión de base de datos SQLAlchemy
    :param pack_id: ID del pack
    :return: Lista de objetos Instrument incluidos en el pack
    """
    # Consultar instrumentos asociados con el pack especificado
    return db.query(Instrument).join(Instrument.packs).filter(Pack.id == pack_id).all()

 

#---------------------------------------


load_dotenv()

# Create the database and tables
engine = create_engine(os.environ['DATABASE_URL'], echo=False)
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()


def print_menu():
    print("\nSistema de Gestión de Escuela de Música")
    print("1. Crear Alumno")
    print("2. Actualizar Alumno")
    print("3. Eliminar Alumno")
    print("4. Hacer Inscripción")
    print("5. Eliminar Inscripción")
    print("6. Crear Instrumento")
    print("7. Actualizar Precio del Instrumento")
    print("8. Ver Detalles del Alumno")
    print("9. Calcular Factura del Alumno")
    print("x. Salir")

if __name__ == "__main__":

    while True:
        print_menu()
        choice = input("Introduzca su elección: ").lower()

        if choice == 'x':
            print("Saliendo del programa...")
            break

        elif choice == '1':
            first_name = input("Introduzca el nombre: ")
            last_name = input("Introduzca el apellido: ")
            age = int(input("Introduzca la edad: "))
            phone = input("Introduzca el número de teléfono: ")
            mail = input("Introduzca el correo electrónico: ")
            familiar = str(input("¿Familiar en la Escuela? (Si/No): ").lower())
            if familiar == "si":
                family_id = True
            else:
                family_id = False
                
            new_student = create_student(first_name, last_name, age, phone, mail, family_id)
            print(f"Detalles del alumno: {new_student.first_name} {new_student.last_name}, ID: {new_student.id}")

        elif choice == '2':
            student_id = int(input("Introduzca el ID del alumno a actualizar: "))
            field = input("Introduzca el campo a actualizar  (first_name, last_name, age, phone, mail, family_id): ")
            value = input("Introduzca el nuevo valor: ")
            if field == 'age':
                value = int(value)
            elif field == 'family_id':
                value = value.lower() == 'true'
            updated_student = update_student(student_id, **{field: value})
            if updated_student:
                print(f"Alumno actualizado: {updated_student.first_name} {updated_student.last_name}")
            else:
                print("Alumno no encontrado")

        elif choice == '3':
            student_id = int(input("Introduzca el ID del alumno a eliminar: "))
            if delete_student(student_id):
                print("Alumno eliminado con éxito")
            else:
                print("Alumno no encontrado")

        elif choice == '4':
            student_id = int(input("Introduzca el ID del alumno: "))
            level_id = int(input("Introduzca el ID del nivel: "))
            registration_date = date.today()
            new_inscription = make_inscription(student_id, level_id, registration_date)
            print(f"Nueva inscripción creada para el alumno ID {student_id} en el nivel ID {level_id}")

        elif choice == '5':
            inscription_id = int(input("Introduzca el ID de la inscripción a eliminar: "))
            if delete_inscription(inscription_id):
                print("Inscripción eliminada con éxito")
            else:
                print("Inscripción no encontrada")
                
        elif choice == '6':
            name = input("Introduzca el nombre del instrumento: ")
            price = float(input("Introduzca el precio del instrumento: "))
            new_instrument = create_instrument(name, price)
            print(f"Nuevo instrumento creado: {new_instrument.name}, Precio: {new_instrument.price}")

        elif choice == '7':
            instrument_id = int(input("Introduzca el ID del instrumento: "))
            new_price = float(input("Introduzca el nuevo precio: "))
            updated_instrument = update_instrument_price(instrument_id, new_price)
            if updated_instrument:
                print(f"Instrumento actualizado: {updated_instrument.name}, Nuevo Precio: {updated_instrument.price}")
            else:
                print("Instrumento no encontrado")

        elif choice == '8':
            student_id = int(input("Introduzca el ID del alumno para ver los detalles: "))
            details = view_student_details(student_id)
            print("")
            print(details)

        elif choice == '9':
            student_id = int(input("Introduzca el ID del alumno para ver facturación: "))
            fees = calculate_student_fees(student_id)
            
            student = session.get(Student, student_id)
            print("")
            print(f"Facturación del Alumno {student.first_name} {student.last_name} con ID {student_id}: {fees}€")

      
            
        else:
            print("Elección inválida. Por favor, inténtelo de nuevo.")


    # Close the session
    session.close()


