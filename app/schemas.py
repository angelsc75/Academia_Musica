from pydantic import BaseModel

class Teacher(BaseModel):
	id: int
	first_name: str
	last_name: str
	phone: str
	mail: str
