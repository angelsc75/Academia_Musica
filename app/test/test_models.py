from models import Teacher, Student, Instrument

''' Test for Teachers'''

def test_teacher_create_get(client, teacher):
	res = client.post("/teachers/", json=teacher)
	assert res.status_code == 200, f"Error in post, expect: 200, not: {res.status_code}"
	res = client.get("/teachers/1")
	assert res.status_code == 200, f"Error in get, expect: 200, not: {res.status_code}"
	teacher["id"] = 1
	data = res.json()
	assert teacher == data, f"Error, data exp: {teacher}, not: {data}"

def test_teacher_duplicate_data_fail(client, teacher):
	client.post("/teachers/", json=teacher)
	res = client.post("/teachers/", json=teacher)
	assert res.status_code == 404

def test_teacher_get_fail(client):
	res = client.get("/teachers/1")
	assert res.status_code == 404

def test_teacher_get_all(client, db_session):
	for i in range(3):
		teacher = Teacher(
			first_name="teacher" + str(i), 
			last_name="test" + str(i),
			phone="555656789",
			mail=f"teacher{i}@gmail.com")
		db_session.add(teacher)
		db_session.commit()
	res = client.get("/teachers/")
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	assert len(data) == 3, f"Error, expected quantity: 3, not: {len(data)}"

def test_teacher_update(client, teacher):
	client.post("/teachers/", json=teacher)
	res = client.put("/teachers/1", json={'phone': '555555559'})
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	assert data["first_name"] == teacher["first_name"]
	assert data["phone"] == '555555559', "Error update data"

def test_teacher_delete(client, teacher):
	client.post("/teachers/", json=teacher)
	res = client.delete("/teachers/1")
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code} {res.content}"
	res = client.get("/teachers/1")
	assert res.status_code == 404, "Error delete data"


'''Tests for Students'''
def test_student_create_get(client, student):
	res = client.post("/students/", json=student)
	assert res.status_code == 200, f"Error in post, expect: 200, not: {res.status_code}"
	res = client.get("/students/1")
	assert res.status_code == 200, f"Error in get, expect: 200, not: {res.status_code}"
	student["id"] = 1
	data = res.json()
	assert student == data, f"Error, data exp: {student}, not: {data}"

def test_student_duplicate_data_fail(client, student):
	client.post("/students/", json=student)
	res = client.post("/students/", json=student)
	assert res.status_code == 404

def test_student_get_fail(client):
	res = client.get("/students/1")
	assert res.status_code == 404

def test_student_get_all(client, db_session):
	for i in range(3):
		student = Student(
			first_name="teacher" + str(i), 
			last_name="test" + str(i),
			age=30,
			phone="555656789",
			mail=f"teacher{i}@gmail.com")
		db_session.add(student)
		db_session.commit()
	res = client.get("/students/")
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	assert len(data) == 3, f"Error, expected quantity: 3, not: {len(data)}"

def test_student_update(client, student):
	client.post("/students/", json=student)
	res = client.put("/students/1", json={'phone': '555555559'})
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	print(data)
	assert data["first_name"] == student["first_name"]
	assert data["phone"] == '555555559', "Error update data"

def test_student_delete(client, student):
	client.post("/students/", json=student)
	res = client.delete("/students/1")
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code} {res.content}"
	res = client.get("/students/1")
	assert res.status_code == 404, "Error delete data"


'''Tests for Instruments'''

def test_instrument_create_get(client, instrument):
	res = client.post("/instruments/", json=instrument)
	assert res.status_code == 200, f"Error in post, expect: 200, not: {res.status_code}"
	res = client.get("/instruments/1")
	assert res.status_code == 200, f"Error in get, expect: 200, not: {res.status_code}"
	instrument["id"] = 1
	data = res.json()
	assert instrument == data, f"Error, data exp: {instrument}, not: {data}"

def test_instrument_duplicate_data_fail(client, instrument):
	client.post("/instruments/", json=instrument)
	res = client.post("/instruments/", json=instrument)
	assert res.status_code == 404

def test_instrument_get_fail(client):
	res = client.get("/instruments/1")
	assert res.status_code == 404

def test_instrument_get_all(client, db_session):
	for i in range(3):
		instrument = Instrument(name="instrument" + str(i), price=40)
		db_session.add(instrument)
		db_session.commit()
	res = client.get("/instruments/")
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	assert len(data) == 3, f"Error, expected quantity: 3, not: {len(data)}"

def test_instrument_update(client, instrument):
	client.post("/instruments/", json=instrument)
	res = client.put("/instruments/1", json={'price': 30})
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	assert data["price"] == 30, "Error update data"

def test_instrument_delete(client, instrument):
	client.post("/instruments/", json=instrument)
	res = client.delete("/instruments/1")
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code} {res.content}"
	res = client.get("/instruments/1")
	assert res.status_code == 404, "Error delete data"


'''Tests for Levels'''

def test_level_create_get(client, instrument):
	client.post("/instruments/", json=instrument)
	instr = client.get("/instruments/1").json()
	res = client.post("/levels/", json={"instruments_id": instr["id"], "level": "Básico"})
	print(res.json())
	assert res.status_code == 200, f"Error in post, expect: 200, not: {res.status_code}"
	res = client.get("/levels/1")
	assert res.status_code == 200, f"Error in get, expect: 200, not: {res.status_code}"
	data = res.json()
	print("data: \n", data)
	assert data["instruments_id"] == instr["id"]
	assert data["level"] != "Básico"

def test_level_duplicate_data_fail(client, instrument):
	client.post("/instruments/", json=instrument)
	instr = client.get("/instruments/1").json()
	client.post("/levels/", json={"instruments_id": instr["id"], "level": "Básico"})
	res = client.post("/levels/", json={"instruments_id": instr["id"], "level": "Básico"})
	assert res.status_code == 400

# def test_level_get_fail(client):
# 	res = client.get("/instruments/1")
# 	assert res.status_code == 404

# def test_level_get_all(client, db_session):
# 	for i in range(3):
# 		instrument = Instrument(name="instrument" + str(i), price=40)
# 		db_session.add(instrument)
# 		db_session.commit()
# 	res = client.get("/instruments/")
# 	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
# 	data = res.json()
# 	assert len(data) == 3, f"Error, expected quantity: 3, not: {len(data)}"

# def test_level_update(client, instrument):
# 	client.post("/instruments/", json=instrument)
# 	res = client.put("/instruments/1", json={'price': 30})
# 	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
# 	data = res.json()
# 	assert data["price"] == 30, "Error update data"

# def test_level_delete(client, instrument):
# 	client.post("/instruments/", json=instrument)
# 	res = client.delete("/instruments/1")
# 	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code} {res.content}"
# 	res = client.get("/instruments/1")
# 	assert res.status_code == 404, "Error delete data"