from sqlalchemy.orm import Session
from sqlalchemy import and_
from models import Student, Inscription, Level, Instrument, Pack, PacksInstruments
from schemas import StudentCreate, InscriptionCreate
from typing import List, Dict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
import logging
from sqlalchemy import func

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

def get_inscriptions_by_student(db: Session, student_id: int):
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

    return inscriptions

def delete_inscription(db: Session, inscription_id: int):
    db_inscription = db.query(Inscription).filter(Inscription.id == inscription_id).first()
    if db_inscription:
        db.delete(db_inscription)
        db.commit()
        return True
    return False

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
            func.count(Inscription.id).label('inscription_count')
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