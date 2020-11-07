from database import Database

def get_student_from_db(user_id:int):
	db = Database()
	student = db.get_student(user_id)
	db.close()
	return student

def add_student_to_db(student):
	db = Database()
	db.add_student(student)
	db.close()