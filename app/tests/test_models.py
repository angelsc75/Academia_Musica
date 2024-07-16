from models import Teacher, Student, Instrument, Level, Pack

'''Tests
client: fixture que permite hacer las peticiones http.
teacher: Datos de un profesor para hacer pruebas.

client y teacher se encuentran en el archivo contest.py
'''


''' Test for Teachers'''

def test_teacher_create_get(client, teacher):
	''' Test para verificar los endpoints de crear profesor
	y obtener profesor por id.
	'''
	# Creo un registro de profesor con los datos de teacher
	# client.post(ruta, datos_del_profesor)
	res = client.post("/teachers/", json=teacher)
	# Comprobar el código de respuesta
	assert res.status_code == 200, f"Error in post, expect: 200, not: {res.status_code}"
	# Obtener profesor creado, pasandole el id: 1
	res = client.get("/teachers/1")
	# Comprobar el código de respuesta 
	assert res.status_code == 200, f"Error in get, expect: 200, not: {res.status_code}"
	# Agregar "id": 1, al diccionario de teacher, ya que este no lo tiene
	teacher["id"] = 1
	# Recuperar la información del profesor obtenido del get
	data = res.json()
	# Validar la información del profesor.
	for t in teacher.items():
		assert t in data.items(), f"Error with data: {t}"

def test_teacher_duplicate_data_fail(client, teacher):
	''' Test para comprobar que no se permite crear datos
	duplicados '''
	# Creo un profeosor con los datos de teacher
	client.post("/teachers/", json=teacher)
	# Vuelvo a crear un profesor con los mismos datos para comprobar
	# la respuesta 404, guardo lo que devuelve la petición en res.
	res = client.post("/teachers/", json=teacher)
	# Compruebo el código de estado devuelto por la petición post.
	assert res.status_code == 400

def test_teacher_get_fail(client):
	''' Test para recuperar profesor no creado'''
	# Le paso el id de un profesor que no esta creado.
	res = client.get("/teachers/1")
	print(res.json())
	assert res.status_code == 404

def test_teacher_get_all(client, db_session):
	''' Test para endpoint de obtener todos los profesores.'''
	# Creo 3 objetos de Teacher con un bucle for
	# Y lo guardo en la bd
	for i in range(3):
		teacher = Teacher(
			first_name="teacher" + str(i), 
			last_name="test" + str(i),
			phone="555656789",
			mail=f"teacher{i}@gmail.com")
		db_session.add(teacher)
		db_session.commit()
	# Realizo la petición
	res = client.get("/teachers/")
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	# Verifico la cantidad de profesores.
	assert len(data) == 3, f"Error, expected quantity: 3, not: {len(data)}"

def test_teacher_update(client, teacher):
	''' Test para endpoint de update Teacher'''
	# Creo un profesor con la información de teacher.
	client.post("/teachers/", json=teacher)
	# Actualizo la información de phone.
	res = client.put("/teachers/1", json={'phone': '555555559'})
	# Verifico el codigo de respuesta
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	# Valido información.
	assert data["first_name"] == teacher["first_name"]
	assert data["phone"] == '555555559', "Error update data"

def test_teacher_delete(client, teacher):
	''' Test para endpoint delete Teacher'''
	# Creo un profesor con la información de teacher.
	client.post("/teachers/", json=teacher)
	# Elimino el profesor creado pasandole el id a la ruta.
	res = client.delete("/teachers/1")
	# Verifico el código de respuesta
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code} {res.content}"
	# Compruebo que se elimino
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
	for t in student.items():
		assert t in data.items(), f"Error with data: {t}"

def test_student_duplicate_data_fail(client, student):
	client.post("/students/", json=student)
	student_2 = {
		"first_name": "Mica2", 
		"last_name": "Test",
		"age": 30,
		"phone": "600090000", 
		"mail":"mica22.test@gmail.com",
		"family_id": False
	}
	res = client.post("/students/", json=student_2)
	assert res.status_code == 400

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
	new_student = {
		"first_name": "Mica2", 
		"last_name": "Test",
		"age": 30,
		"phone": "600090000", 
		"mail":"mica22.test@gmail.com",
		"family_id": False
	}
	res = client.put("/students/1", json=new_student)
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	print(data)
	assert data["first_name"] == student["first_name"]
	assert data["phone"] == '600090000', "Error update data"

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
	res = client.put("/instruments/1", json={'name': 'Piano2', 'price': 30})
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	assert data["name"] == 'Piano2', "Error update data"

def test_instrument_delete(client, instrument):
	client.post("/instruments/", json=instrument)
	res = client.delete("/instruments/1")
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code} {res.content}"
	res = client.get("/instruments/1")
	assert res.status_code == 404, "Error delete data"


'''Tests for Levels'''

def test_level_create_get(client, level):
	res = client.post("/levels/", json=level)
	assert res.status_code == 200, f"Error in post, expect: 200, not: {res.status_code}"
	res = client.get("/levels/1")
	assert res.status_code == 200, f"Error in get, expect: 200, not: {res.status_code}"
	data = res.json()
	assert data["instruments_id"] == 1
	assert data["level"] == level["level"]

def test_level_duplicate_data_fail(client, level):
	client.post("/levels/", json=level)
	res = client.post("/levels/", json=level)
	assert res.status_code == 400

def test_level_get_fail(client):
	res = client.get("/levels/1")
	assert res.status_code == 404

def test_level_get_all(client, instrument, db_session):
	instr = client.post("/instruments/", json=instrument).json()
	for i in range(3):
		level = Level(instruments_id=instr["id"], level="Test" + str(i))
		db_session.add(level)
		db_session.commit()
	res = client.get("/levels/")
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	assert len(data) == 3, f"Error, expected quantity: 3, not: {len(data)}"

def test_level_update(client, level):
	client.post("/levels/", json=level)
	res = client.put("/levels/1", json={'level': "Intermedio", 'instruments_id': 1})
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	assert data["level"] == "Intermedio", "Error update data"

def test_level_delete(client, level):
	client.post("/levels/", json=level)
	res = client.delete("/levels/1")
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code} {res.content}"
	res = client.get("/levels/1")
	assert res.status_code == 404, "Error delete data"

'''Tests for packs'''
def test_pack_create_get(client, pack):
	res = client.post("/packs/", json=pack)
	assert res.status_code == 200, f"Error in post, expect: 200, not: {res.status_code}"
	res = client.get("/packs/1")
	assert res.status_code == 200, f"Error in get, expect: 200, not: {res.status_code}"
	data = res.json()
	for t in pack.items():
		assert t in data.items(), f"Error with data: {t}"

def test_pack_duplicate_data_fail(client, pack):
	client.post("/packs/", json=pack)
	res = client.post("/packs/", json=pack)
	assert res.status_code == 400

def test_pack_get_fail(client):
	res = client.get("/packs/1")
	assert res.status_code == 404

def test_pack_get_all(client, pack, db_session):
	for i in range(3):
		pack = Pack(pack="Test"+str(i), discount_1= 20, discount_2=25)
		db_session.add(pack)
		db_session.commit()
	res = client.get("/packs/")
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	assert len(data) == 3, f"Error, expected quantity: 3, not: {len(data)}"

def test_pack_update(client, pack):
	client.post("/packs/", json=pack)
	res = client.put("/packs/1", json={'pack': "Pack 2", 'discount_1': 25, 'discount_2': 40})
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code}"
	data = res.json()
	assert data["pack"] == "Pack 2", "Error update data"

def test_pack_delete(client, pack):
	client.post("/packs/", json=pack)
	res = client.delete("/packs/1")
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code} {res.content}"
	res = client.get("/packs/1")
	assert res.status_code == 404, "Error delete data"

'''Tests for inscriptions'''
def test_inscriptions_create_get(client, inscription, student):
	new_student = client.post("/students/", json=student).json()
	inscription["student_id"] = new_student["id"]
	res = client.post("/inscriptions/", json=inscription)
	assert res.status_code == 200, f"Error in post, expect: 200, not: {res.status_code}"
	res = client.get("/inscriptions/1")
	assert res.status_code == 200, f"Error in get, expect: 200, not: {res.status_code}"
	data = res.json()
	for t in inscription.items():
		assert t in data.items(), f"Error with data: {t}"

def test_inscriptions_get_fail(client):
	res = client.get("/inscriptions/1")
	assert res.status_code == 404

def test_inscriptions_delete(client, inscription, student):
	new_student = client.post("/students/", json=student).json()
	inscription["student_id"] = new_student["id"]
	res = client.post("/inscriptions/", json=inscription)
	client.delete("/inscriptions/1")
	assert res.status_code == 200, f"Error, expected:200, not:{res.status_code} {res.content}"
	res = client.get("/inscriptions/1")
	assert res.status_code == 404, "Error delete data"