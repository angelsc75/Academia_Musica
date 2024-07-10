from sqlalchemy import ForeignKey, DECIMAL, Date, Boolean, String, Integer
from sqlalchemy.orm import relationship, declarative_base, Mapped, mapped_column

from typing import List
from datetime import date

Base = declarative_base()

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


class Teacher(Base):
    __tablename__ = 'teachers'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(50))
    mail: Mapped[str] = mapped_column(String(50))

    instruments: Mapped[List["Instrument"]] = relationship(secondary="teachers_instruments", back_populates="teachers")


class Instrument(Base):
    __tablename__ = 'instruments'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    price: Mapped[DECIMAL] = mapped_column(DECIMAL)

    levels: Mapped[List["Level"]] = relationship(back_populates="instrument")
    packs: Mapped[List["Pack"]] = relationship(secondary="packs_instruments", back_populates="instruments")
    teachers: Mapped[List["Teacher"]] = relationship(secondary="teachers_instruments", back_populates="instruments")


class Level(Base):
    __tablename__ = 'levels'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    instruments_id: Mapped[int] = mapped_column(ForeignKey('instruments.id'))
    level: Mapped[str] = mapped_column(String(50), nullable=False)

    instrument: Mapped["Instrument"] = relationship(back_populates="levels")
    inscriptions: Mapped[List["Inscription"]] = relationship(back_populates="level")


class Pack(Base):
    __tablename__ = 'packs'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    pack: Mapped[str] = mapped_column(String(50), nullable=False)
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

