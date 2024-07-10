from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Student, Inscription, Level, Instrument, Pack, PacksInstruments
from schemas import StudentCreate, InscriptionCreate
from typing import List, Dict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
import logging

def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

def get_students(db: Session, skip: int = 0, limit: int = 200):
    try:
        students = db.query(Student).offset(skip).limit(limit).all()
        logging.info(f"Retrieved {len(students)} students")
        return students
    except Exception as e:
        logging.error(f"Error in get_students: {str(e)}")
        raise

    
def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()

def update_student(db: Session, student_id: int, student_data: dict):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        for key, value in student_data.items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
    return db_student

def delete_student(db: Session, student_id: int):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False

def create_inscription(db: Session, inscription: InscriptionCreate):
    db_inscription = Inscription(**inscription.dict())
    db.add(db_inscription)
    db.commit()
    db.refresh(db_inscription)
    return db_inscription

def get_inscriptions(db: Session):
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

    return inscriptions

def calculate_student_fees(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return None

    inscriptions = db.query(Inscription).filter(Inscription.student_id == student_id).all()
    if not inscriptions:
        return Decimal('0.00')

    total_fee = Decimal('0.00')
    pack_inscriptions = {}

    for inscription in inscriptions:
        instrument = inscription.level.instrument
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

    if student.family_id:
        total_fee *= Decimal('0.90')  

    final_fee = total_fee.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return final_fee

def generate_fee_report(db: Session):
    student_query = (
        db.query(
            Student,
            db.func.count(Inscription.id).label('inscription_count')
        )
        .outerjoin(Inscription)
        .group_by(Student.id)
    )

    report = []
    for student, inscription_count in student_query:
        fee_value = calculate_student_fees(db, student.id)
        
        if fee_value is not None:
            report.append({
                'student_id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'total_fee': float(fee_value),
                'inscription_count': inscription_count,
                'family_discount': 'Sí' if student.family_id else 'No'
            })

    return report
