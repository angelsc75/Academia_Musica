import pytest
from fastapi.testclient import TestClient
from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from models import Base
from db import get_db
from main import app
from crud.instruments_crud import create_instrument
from crud.students_crud import create_student
from crud.levels_crud import create_level
from crud.packs_crud import create_pack

DATABASE_URL_TEST = "sqlite:///:memory"

engine = create_engine(DATABASE_URL_TEST, 
					   connect_args={"check_same_thread": False},
					   poolclass=StaticPool)

TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(bind=engine)

@pytest.fixture
def db_session():
	connection = engine.connect()
	transaction = connection.begin()
	session = TestingSessionLocal(bind=connection)
	yield session
	session.close()
	transaction.rollback()
	connection.close()

@pytest.fixture
def client(db_session):
	def override_get_db():
		yield db_session
	
	app.dependency_overrides[get_db] = override_get_db
	yield TestClient(app)
	del app.dependency_overrides[get_db]

@pytest.fixture
def teacher():
	return {
		"first_name": "Mica2", 
		"last_name": "Test", 
		"phone": "60009093", 
		"mail":"mica2.test@gmail.com"
		}

@pytest.fixture
def student():
	return {
		"first_name": "Mica2", 
		"last_name": "Test",
		"age": 30,
		"phone": "60009093", 
		"mail":"mica2.test@gmail.com",
		"family_id": True
	}

@pytest.fixture
def instrument():
	return {
		"name": "Piano",
		"price": 35
	}

@pytest.fixture
def level(db_session, instrument):
	instr = create_instrument(db_session, **instrument)
	return {
		"instruments_id": instr.id,
		"level": "Básico"
	}

@pytest.fixture
def pack():
	return {
		"pack": "Pack 1",
		"discount_1": 25,
		"discount_2": 35
	}

@pytest.fixture
def pack_instrument(db_session, pack, instrument):
	obj_pack = create_pack(db_session, **pack)
	obj_instr = create_instrument(db_session, **instrument)
	return {
		"instrument_id": obj_instr.id,
		"packs_id": obj_pack.id
	}

@pytest.fixture
def inscription(db_session, level, pack_instrument):
	obj_level = create_level(db_session, **level)
	return {
		"level_id": obj_level.id,
		"registration_date": "2024-03-12",
	}