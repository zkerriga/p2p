import database

def get_student_from_db(user_id:int):
	db = Database()
	student = db.get_student(user_id)
	db.close()
	return student
