from pydantic import BaseModel

class CreateTeacher(BaseModel):
	first_name: str
	last_name: str
	phone: str
	mail: str

class Teacher(CreateTeacher):
	id: int
