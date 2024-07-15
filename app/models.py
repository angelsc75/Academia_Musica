from sqlalchemy import ForeignKey, DECIMAL, Date, Boolean, String, Integer
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column

from typing import List
from datetime import date

Base = declarative_base()

"""
Modelo de estudiante que representa a los estudiantes en la base de datos.

Atributos:
    id (int): Identificador único del estudiante.
    first_name (str): Nombre del estudiante.
    last_name (str): Apellido del estudiante.
    age (int): Edad del estudiante.
    phone (str): Número de teléfono del estudiante.
    mail (str): Correo electrónico del estudiante.
    family_id (bool | None): Indicador si el estudiante tiene un ID de familia.
    inscriptions (List[Inscription]): Lista de inscripciones del estudiante.
"""
class Student(Base):
    __tablename__ = 'students'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    phone: Mapped[str] = mapped_column(String(50))
    mail: Mapped[str] = mapped_column(String(50))
    family_id: Mapped[bool | None] = mapped_column(Boolean, nullable=True)

    inscriptions: Mapped[List["Inscription"]] = relationship(back_populates="student", cascade="all, delete-orphan")

'''
    Modelo de profesor que representa a los profesores en la base de datos.

    Atributos:
        id (int): Identificador único del profesor.
        first_name (str): Nombre del profesor.
        last_name (str): Apellido del profesor.
        phone (str): Número de teléfono del profesor.
        mail (str): Correo electrónico del profesor.
        instruments (List[Instrument]): Lista de instrumentos que el profesor puede enseñar.

'''
class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(50))
    mail: Mapped[str] = mapped_column(String(50))

    instruments: Mapped[List["Instrument"]] = relationship(secondary="teachers_instruments", back_populates="teachers")

"""
Modelo de instrumento que representa a los instrumentos en la base de datos.

Atributos:
    id (int): Identificador único del instrumento.
    name (str): Nombre del instrumento.
    price (DECIMAL): Precio del instrumento.
    levels (List[Level]): Lista de niveles del instrumento.
    packs (List[Pack]): Lista de paquetes que incluyen el instrumento.
    teachers (List[Teacher]): Lista de profesores que pueden enseñar el instrumento.
"""
class Instrument(Base):
    __tablename__ = 'instruments'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL)

    levels: Mapped[List["Level"]] = relationship(back_populates="instrument")
    packs: Mapped[List["Pack"]] = relationship(secondary="packs_instruments", back_populates="instruments")
    teachers: Mapped[List["Teacher"]] = relationship(secondary="teachers_instruments", back_populates="instruments")

"""
Modelo de nivel que representa a los niveles de aprendizaje de un instrumento en la base de datos.

Atributos:
    id (int): Identificador único del nivel.
    instruments_id (int): Identificador del instrumento relacionado.
    level (str): Nombre del nivel.
    instrument (Instrument): Relación al instrumento.
    inscriptions (List[Inscription]): Lista de inscripciones en este nivel.
"""
class Level(Base):
    __tablename__ = 'levels'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    instruments_id: Mapped[int] = mapped_column(ForeignKey('instruments.id'))
    level: Mapped[str] = mapped_column(String(50), nullable=False)

    instrument: Mapped["Instrument"] = relationship(back_populates="levels")
    inscriptions: Mapped[List["Inscription"]] = relationship(back_populates="level")

"""
Modelo de paquete que representa a los paquetes de instrumentos en la base de datos.

Atributos:
    id (int): Identificador único del paquete.
    pack (str): Nombre del paquete.
    discount_1 (DECIMAL): Primer descuento del paquete.
    discount_2 (DECIMAL): Segundo descuento del paquete.
    instruments (List[Instrument]): Lista de instrumentos incluidos en el paquete.
"""
class Pack(Base):
    __tablename__ = 'packs'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pack: Mapped[str] = mapped_column(String(50), nullable=False)
    discount_1: Mapped[DECIMAL] = mapped_column(DECIMAL)
    discount_2: Mapped[DECIMAL] = mapped_column(DECIMAL)

    instruments: Mapped[List["Instrument"]] = relationship(secondary="packs_instruments", back_populates="packs")

"""
Modelo de relación muchos a muchos entre paquetes e instrumentos.

Atributos:
    id (int): Identificador único de la relación.
    instrument_id (int): Identificador del instrumento.
    packs_id (int): Identificador del paquete.
"""
class PacksInstruments(Base):
    __tablename__ = 'packs_instruments'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    instrument_id: Mapped[int] = mapped_column(ForeignKey('instruments.id'))
    packs_id: Mapped[int] = mapped_column(ForeignKey('packs.id'))

"""
Modelo de inscripción que representa a las inscripciones de los estudiantes en los niveles de instrumentos.

Atributos:
    id (int): Identificador único de la inscripción.
    student_id (int): Identificador del estudiante.
    level_id (int): Identificador del nivel.
    registration_date (date): Fecha de inscripción.
    student (Student): Relación al estudiante.
    level (Level): Relación al nivel.
"""
class Inscription(Base):
    __tablename__ = 'inscriptions'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'))
    level_id: Mapped[int] = mapped_column(ForeignKey('levels.id'))
    registration_date: Mapped[date] = mapped_column(Date)

    student: Mapped["Student"] = relationship(back_populates="inscriptions")
    level: Mapped["Level"] = relationship(back_populates="inscriptions")

"""
Modelo de relación muchos a muchos entre profesores e instrumentos.

Atributos:
    id (int): Identificador único de la relación.
    teacher_id (int): Identificador del profesor.
    instrument_id (int): Identificador del instrumento.
"""
class TeachersInstruments(Base):
    __tablename__ = 'teachers_instruments'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id'))
    instrument_id: Mapped[int] = mapped_column(ForeignKey('instruments.id'))

