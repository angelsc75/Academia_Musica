from sqlalchemy.orm import Session
from sqlalchemy import and_, select, func
from models import Student, Inscription, Level, Instrument, Pack, PacksInstruments
from schemas import StudentCreate, InscriptionCreate
from typing import List, Dict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
import logging
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi import HTTPException
import logging

def create_inscription(db: Session, inscription: InscriptionCreate):
    # Check if the student exists
    student = db.query(Student).filter(Student.id == inscription.student_id).first()
    if not student:
        logging.warning(f"Estudiante con ID {inscription.student_id} no encontrado")
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Check if the instrument exists
    instrument = db.query(Instrument).filter(Instrument.id == inscription.instrument_id).first()
    if not instrument:
        logging.warning(f"Instrumento con ID {inscription.instrument_id} no encontrado")
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")

    # Check if the level exists
    level = db.query(Level).filter(Level.id == inscription.level_id).first()
    if not level:
        logging.warning(f"Nivel con ID {inscription.level_id} no encontrado")
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    # Check if the inscription already exists
    existing_inscription = db.query(Inscription).filter(
        Inscription.student_id == inscription.student_id,
        Inscription.level_id == inscription.level_id,
        Inscription.instrument_id == inscription.instrument_id
    ).first()
    
    if existing_inscription:
        logging.warning(f"Inscripción ya existe para estudiante ID {inscription.student_id}, nivel ID {inscription.level_id}, instrumento ID {inscription.instrument_id}")
        raise HTTPException(status_code=400, detail="Inscripción ya existe")

    # Create a new inscription
    db_inscription = Inscription(**inscription.model_dump())
    
    try:
        db.add(db_inscription)
        db.commit()
        db.refresh(db_inscription)
        logging.info(f"Inscripción creada con éxito: {db_inscription}")
        return db_inscription
    except IntegrityError:
        db.rollback()
        logging.error(f"Error de integridad al crear la inscripción: {inscription}")
        raise HTTPException(status_code=400, detail="Error de integridad al crear la inscripción")
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al crear la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al crear la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

def get_inscription(db: Session, inscription_id: int):
    try:
        stmt = select(Inscription).where(Inscription.id == inscription_id)
        result = db.scalars(stmt).first()
        
        if result is None:
            logging.warning(f"Inscripción con ID {inscription_id} no encontrada")
            raise HTTPException(status_code=404, detail="Inscripción no encontrada")
        
        return result

    except SQLAlchemyError as e:
        logging.error(f"Error al obtener la inscripción con ID {inscription_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    except Exception as e:
        logging.error(f"Error inesperado al obtener la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

def get_inscriptions(db: Session):
    try:
        inscription_query = (
            db.query(
                Inscription,
                Student,
                Level,
                Instrument
            )
            .join(Student, Inscription.student_id == Student.id)
            .join(Level, Inscription.level_id == Level.id)
            .join(Instrument, Level.instruments_id == Instrument.id)
            .order_by(Inscription.registration_date.desc())
        )

        inscriptions = []
        for inscription, student, level, instrument in inscription_query:
            inscriptions.append({
                'inscription_id': inscription.id,
                'student_id': student.id,
                'student_name': f"{student.first_name} {student.last_name}",
                'instrument_name': instrument.name,
                'level': level.level,
                'registration_date': inscription.registration_date.strftime('%Y-%m-%d'),
                'instrument_price': float(instrument.price)
            })
        logging.info(f"Inscripciones obtenidas con éxito: {len(inscriptions)} inscripciones")
        return inscriptions

    except SQLAlchemyError as e:
        logging.error(f"Error al obtener inscripciones: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    except Exception as e:
        logging.error(f"Error inesperado al obtener inscripciones: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

def get_inscriptions_by_student(db: Session, student_id: int):
    try:
        # Check if the student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            logging.warning(f"Estudiante con ID {student_id} no encontrado")
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        # Query inscriptions for the student
        inscription_query = (
            db.query(
                Inscription,
                Student,
                Level,
                Instrument
            )
            .join(Student, Inscription.student_id == Student.id)
            .join(Level, Inscription.level_id == Level.id)
            .join(Instrument, Level.instruments_id == Instrument.id)
            .filter(Student.id == student_id)
            .order_by(Inscription.registration_date.desc())
        )

        inscriptions = []
        for inscription, student, level, instrument in inscription_query:
            inscriptions.append({
                'inscription_id': inscription.id,
                'student_id': student.id,
                'student_name': f"{student.first_name} {student.last_name}",
                'instrument_name': instrument.name,
                'level': level.level,
                'registration_date': inscription.registration_date.strftime('%Y-%m-%d'),
                'instrument_price': float(instrument.price)  
            })
        logging.info(f"Inscripciones para el estudiante ID {student_id} obtenidas con éxito")
        return inscriptions

    except SQLAlchemyError as e:
        logging.error(f"Error al obtener inscripciones para el estudiante con ID {student_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    except HTTPException:
        raise  # Re-raise HTTPException to maintain status code and detail
    except Exception as e:
        logging.error(f"Error inesperado al obtener inscripciones: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")


def update_inscription(db: Session, inscription_id: int, inscription_data: dict):
    try:
        # Check if the inscription exists
        db_inscription = db.query(Inscription).filter(Inscription.id == inscription_id).first()
        if not db_inscription:
            logging.warning(f"Inscripción con ID {inscription_id} no encontrada")
            raise HTTPException(status_code=404, detail="Inscripción no encontrada")

        # Check if the student exists
        if 'student_id' in inscription_data:
            student = db.query(Student).filter(Student.id == inscription_data['student_id']).first()
            if not student:
                logging.warning(f"Estudiante con ID {inscription_data['student_id']} no encontrado")
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        # Check if the instrument exists
        if 'instrument_id' in inscription_data:
            instrument = db.query(Instrument).filter(Instrument.id == inscription_data['instrument_id']).first()
            if not instrument:
                logging.warning(f"Instrumento con ID {inscription_data['instrument_id']} no encontrado")
                raise HTTPException(status_code=404, detail="Instrumento no encontrado")

        # Check if the level exists
        if 'level_id' in inscription_data:
            level = db.query(Level).filter(Level.id == inscription_data['level_id']).first()
            if not level:
                logging.warning(f"Nivel con ID {inscription_data['level_id']} no encontrado")
                raise HTTPException(status_code=404, detail="Nivel no encontrado")

        # Update the inscription
        for key, value in inscription_data.items():
            setattr(db_inscription, key, value)

        db.commit()
        db.refresh(db_inscription)
        logging.info(f"Inscripción con ID {inscription_id} actualizada con éxito")
        return db_inscription

    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al actualizar la inscripción {inscription_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al actualizar la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

def delete_inscription(db: Session, inscription_id: int) -> bool:
    try:
        db_inscription = db.query(Inscription).filter(Inscription.id == inscription_id).first()
        
        if not db_inscription:
            logging.warning(f"Inscripción con ID {inscription_id} no encontrada")
            raise HTTPException(status_code=404, detail="Inscripción no encontrada")

        db.delete(db_inscription)
        db.commit()
        logging.info(f"Inscripción con ID {inscription_id} eliminada con éxito")
        return True
    
    except SQLAlchemyError as e:
        db.rollback()
        logging.error(f"Error de base de datos al eliminar la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    
    except Exception as e:
        db.rollback()
        logging.error(f"Error inesperado al eliminar la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

def calculate_student_fees(db: Session, student_id: int) -> Decimal:
    try:
        # Check if the student exists
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            logging.warning(f"Estudiante con ID {student_id} no encontrado")
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        # Retrieve inscriptions for the student
        inscriptions = db.query(Inscription).filter(Inscription.student_id == student_id).all()
        if not inscriptions:
            logging.info(f"No se encontraron inscripciones para el estudiante con ID {student_id}")
            return Decimal('0.00')

        total_fee = Decimal('0.00')
        pack_inscriptions = {}

        # Calculate fees for each inscription
        for inscription in inscriptions:
            instrument = inscription.level.instrument
            if not instrument:
                logging.warning(f"Instrumento no encontrado para la inscripción ID {inscription.id}")
                raise HTTPException(status_code=404, detail="Instrumento no encontrado")
                
            pack = db.query(Pack).join(PacksInstruments).filter(PacksInstruments.instrument_id == instrument.id).first()
            pack_id = pack.id if pack else None

            if pack_id not in pack_inscriptions:
                pack_inscriptions[pack_id] = []
            pack_inscriptions[pack_id].append((instrument, pack))

        for pack_id, insc_list in pack_inscriptions.items():
            insc_list.sort(key=lambda x: x[0].price, reverse=True)

            for i, (instrument, pack) in enumerate(insc_list):
                price = Decimal(instrument.price)

                if pack:
                    if i == 1:
                        discount = Decimal(pack.discount_1)
                        price -= price * discount / 100
                    elif i > 1:
                        discount = Decimal(pack.discount_2)
                        price -= price * discount / 100

                total_fee += price

        # Apply family discount if applicable
        if student.family_id:
            total_fee *= Decimal('0.90')

        final_fee = total_fee.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        logging.info(f"Tarifas calculadas con éxito para el estudiante con ID {student_id}: {final_fee}")        
        return final_fee

    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al calcular las tarifas con ID {student_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")

    except Exception as e:
        logging.error(f"Error inesperado al calcular las tarifas con ID {student_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

def generate_fee_report(db: Session):
    try:
        student_query = (
            db.query(
                Student,
                func.count(Inscription.id).label('inscription_count')
            )
            .outerjoin(Inscription)
            .group_by(Student.id)
        )

        report = []
        for student, inscription_count in student_query:
            try:
                fee_value = calculate_student_fees(db, student.id)
            except HTTPException as e:
                logging.warning(f"Omitiendo estudiante con ID {student.id} debido a error: {e.detail}")
                continue  # Skip this student if there's an issue calculating fees
            
            report.append({
                'student_id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'total_fee': float(fee_value),
                'inscription_count': inscription_count,
                'family_discount': 'Sí' if student.family_id else 'No'
            })

        return report

    except SQLAlchemyError as e:
        logging.error(f"Error de base de datos al generar el informe de tarifas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")

    except Exception as e:
        logging.error(f"Error inesperado al generar el informe de tarifas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")