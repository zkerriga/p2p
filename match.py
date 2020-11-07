from Student import Student
import database

def match(current_student:Student):
	'''
	Return another student
	'''
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