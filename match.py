from Student import Student
from database import Database

def match(current_student:Student):
	'''
	Return another student
	'''
	db = Database()
	# db.set_eval_db(current_student)
	new_user = db.get_matched_user(current_student)
	db.close()
	if new_user:
		return new_user
	else:
		return None
