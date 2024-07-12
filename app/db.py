import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

load_dotenv()

# Create the database and tables
engine = create_engine(os.environ['DATABASE_URL'], echo=False)
Base.metadata.create_all(engine)

# Create a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)
# session = Session()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()