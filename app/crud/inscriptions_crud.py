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

'''
Cada función en este código está diseñada para interactuar con la base de datos a través de SQLAlchemy y manejar las operaciones 
CRUD (crear, leer, actualizar y eliminar) para las inscripciones (Inscription). Además, se incluyen manejos de errores detallados y 
logging para registrar las operaciones y posibles fallos.
Se calcula tarifas por alumno y por inscripción y se genera un informe de facturación
'''
# Obtener el logger configurado
logger = logging.getLogger("music_app")

# Crear una nueva inscripción
def create_inscription(db: Session, inscription: InscriptionCreate):
    # Comprobar si exite el estudiante
    student = db.query(Student).filter(Student.id == inscription.student_id).first()
    if not student:
        logger.warning("Estudiante no encontrado")
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    # Comprobar si exite el instrumento
    instrument = db.query(Instrument).filter(Instrument.id == inscription.instrument_id).first()
    if not instrument:
        logger.warning("Instrumento no encontrado")
        raise HTTPException(status_code=404, detail="Instrumento no encontrado")

    # Comprobar si exite el nivel
    level = db.query(Level).filter(Level.id == inscription.level_id).first()
    if not level:
        logger.warning("Nivel no encontrado")
        raise HTTPException(status_code=404, detail="Nivel no encontrado")

    # Comprueba si la inscripción ya existe.
    existing_inscription = db.query(Inscription).filter(
        Inscription.student_id == inscription.student_id,
        Inscription.level_id == inscription.level_id,
        Inscription.instrument_id == inscription.instrument_id
    ).first()
    
    if existing_inscription:
        logger.warning("Inscripción ya existe")
        raise HTTPException(status_code=400, detail="Inscripción ya existe")

    # Crear una nueva inscripción
    db_inscription = Inscription(**inscription.model_dump())
    
    try:
        db.add(db_inscription)
        db.commit()
        db.refresh(db_inscription)
        logger.info("Inscripción creada con éxito")
        return db_inscription
    except IntegrityError:
        db.rollback()
        logger.error("Error de integridad al crear la inscripción")
        raise HTTPException(status_code=400, detail="Error de integridad al crear la inscripción")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al crear la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al crear la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

# Consultar Inscripción por ID
def get_inscription(db: Session, inscription_id: int):
    try:
        stmt = select(Inscription).where(Inscription.id == inscription_id)
        result = db.scalars(stmt).first()
        
        if result is None:
            logger.warning("Inscripción no encontrada")
            raise HTTPException(status_code=404, detail="Inscripción no encontrada")
        
        return result

    except SQLAlchemyError as e:
        logger.error(f"Error al obtener la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

# Consultar todas las inscripciones
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
        logger.info(f"Recuperadas con éxito {len(inscriptions)} inscripciones")
        return inscriptions

    except SQLAlchemyError as e:
        logger.error(f"Error al obtener inscripciones: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    except Exception as e:
        logger.error(f"Error inesperado al obtener inscripciones: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

# Consultar inscripciones por id de estudiante
def get_inscriptions_by_student(db: Session, student_id: int):
    try:
        # Comprobar si el estudiante existe
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            logger.warning("Estudiante no encontrado")
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        # Consulta de inscripciones para el estudiane
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
        logger.info("Inscripciones para el estudiante obtenidas con éxito")
        return inscriptions

    except SQLAlchemyError as e:
        logger.error(f"Error al obtener inscripciones para el estudiante: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    except HTTPException:
        raise  # Re-raise HTTPException to maintain status code and detail
    except Exception as e:
        logger.error(f"Error inesperado al obtener inscripciones: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

# Actualizar una inscripción
def update_inscription(db: Session, inscription_id: int, inscription_data: dict):
    try:
        # Comprueba si la inscripción existe.
        db_inscription = db.query(Inscription).filter(Inscription.id == inscription_id).first()
        if not db_inscription:
            logger.warning("Inscripción no encontrada")
            raise HTTPException(status_code=404, detail="Inscripción no encontrada")

        # Comprueba si el estudiante existe.
        if 'student_id' in inscription_data:
            student = db.query(Student).filter(Student.id == inscription_data['student_id']).first()
            if not student:
                logger.warning("Estudiante no encontrado")
                raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        # Comprueba si el instrumento existe.
        if 'instrument_id' in inscription_data:
            instrument = db.query(Instrument).filter(Instrument.id == inscription_data['instrument_id']).first()
            if not instrument:
                logger.warning("Instrumento no encontrado")
                raise HTTPException(status_code=404, detail="Instrumento no encontrado")

        # Comprueba si el nivel existe.
        if 'level_id' in inscription_data:
            level = db.query(Level).filter(Level.id == inscription_data['level_id']).first()
            if not level:
                logger.warning("Nivel no encontrado")
                raise HTTPException(status_code=404, detail="Nivel no encontrado")

        # Actualiza la inscripción
        for key, value in inscription_data.items():
            setattr(db_inscription, key, value)

        db.commit()
        db.refresh(db_inscription)
        logger.info("Inscripción actualizada con éxito")
        return db_inscription

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al actualizar la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al actualizar la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

# Eliminar una inscripción
def delete_inscription(db: Session, inscription_id: int) -> bool:
    try:
        db_inscription = db.query(Inscription).filter(Inscription.id == inscription_id).first()
        
        if not db_inscription:
            logger.warning("Inscripción no encontrada")
            raise HTTPException(status_code=404, detail="Inscripción no encontrada")

        db.delete(db_inscription)
        db.commit()
        logger.info("Inscripción eliminada con éxito")
        return True
    
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Error de base de datos al eliminar la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")
    
    except Exception as e:
        db.rollback()
        logger.error(f"Error inesperado al eliminar la inscripción: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

# Calcular tarifas de estudiantes
def calculate_student_fees(db: Session, student_id: int) -> Decimal:
    try:
        # Comprueba si el estudante existe
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            logger.warning("Estudiante no encontrado")
            raise HTTPException(status_code=404, detail="Estudiante no encontrado")

        # Retrieve inscriptions for the student
        inscriptions = db.query(Inscription).filter(Inscription.student_id == student_id).all()
        if not inscriptions:
            logger.info("No se encontraron inscripciones para el estudiante")
            return Decimal('0.00')

        total_fee = Decimal('0.00')
        pack_inscriptions = {}

        # Calcular tarifa por cada inscripción
        for inscription in inscriptions:
            instrument = inscription.level.instrument
            if not instrument:
                logger.warning("Instrumento no encontrado para la inscripción")
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

        # Aplicar descuento familiar
        if student.family_id:
            total_fee *= Decimal('0.90')

        final_fee = total_fee.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        logger.info("Tarifas calculadas con éxito")        
        return final_fee

    except SQLAlchemyError as e:
        logger.error(f"Error de base de datos al calcular las tarifas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")

    except Exception as e:
        logger.error(f"Error inesperado al calcular las tarifas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")

# Generar informe de tarifas
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
                logger.warning("Omitiendo estudiante debido a error: {e.detail}")
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
        logger.error(f"Error de base de datos al generar el informe de tarifas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error en la base de datos")

    except Exception as e:
        logger.error(f"Error inesperado al generar el informe de tarifas: {str(e)}")
        raise HTTPException(status_code=500, detail="Error inesperado")