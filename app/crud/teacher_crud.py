from sqlalchemy import select
from sqlalchemy.orm import Session

from models import Teacher


def get_teacher(db: Session, teacher_id: int):
	stmt = select(Teacher).where(Teacher.id == teacher_id)
	result = db.scalars(stmt).first()
	return result

def get_teachers(db: Session):
	stmt = select(Teacher)
	return db.scalars(stmt).all()

def create_teacher(db: Session, teacher: Teacher):
	stmt = select(Teacher).where(
		Teacher.first_name == teacher.first_name and
		Teacher.last_name == teacher.last_name
		)
	result = db.execute(stmt).scalars().first()
	if result is not None:
		return None
	new_teacher = Teacher(
		first_name = teacher.first_name,
		last_name = teacher.last_name,
		phone = teacher.phone,
		mail = teacher.mail
		)
	db.add(new_teacher)
	db.commit()
	return new_teacher

def update_teacher(db: Session, teacher_id: int, new_teacher: dict):
	teacher = get_teacher(db, teacher_id)
	if teacher:
		for key, value in new_teacher.items():
			setattr(teacher, key, value)
		db.commit()
		db.refresh(teacher)
		return teacher
	return None

