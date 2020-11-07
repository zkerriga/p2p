from Student import Student
import database
from Database import database

def match(current_student:Student):
	'''
	Return another student
	'''
	db.Database()
	db.set_eval_db(current_student)
	new_user = db.get_matched_user(current_student)
	db.close()
	if new_user:
		return new_user
	else:
		return None
	
	


	return Student(
		user_id = 312162559,
		university = "University of Oxford",
		name = "Daniil",
		link = "t.me/zkerriga",
		level = 1,
		project_name = "double integral",
		project_grades = [4, 4],
		mood_grades = [4, 5, 5]
	)