import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base

load_dotenv()

# Create the database and tables
engine = create_engine(os.environ['DATABASE_URL'], echo=False)
Base.metadata.create_all(engine)

# Create a session
SessionLocal = sessionmaker(bind=engine)
# session = Session()
