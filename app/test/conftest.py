import pytest
from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from models import Base
from db import get_db
from main import app


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
		"mail":"mica2.test@gmail.com"
	}

@pytest.fixture
def instrument():
	return {
		"name": "Piano",
		"price": 35
	}