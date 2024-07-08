from fastapi import FastAPI

from app.db import Session

app = FastAPI()

# Dependency
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()