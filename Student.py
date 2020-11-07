from Project import Project
import random

class Student(object):
	"""
	The student object contains all the information about it.
	"""
	def __init__(self, user_id:int, university:str, name:str, link:str, level:int, project_name:str, project_grades:list, mood_grades:list):
		super(Student, self).__init__()
		
		self._user_id:int = user_id
		self._university:str = university
		self._name:str = name
		self._link:str = link
		self._level:int = level
		self._project:Project = Project(project_name, project_grades)
		self._mood_grades:list = mood_grades
		self._match_state:int = 0

	def set_not_match(self):
		self._match_state = 0

	def set_eval(self, is_eval):
		if is_eval:
			self._match_state = 1
		else:
			self._match_state = 2
	
	def get_match_state(self):
		return self._match_state

	def to_string(self):
		return '''\
Student: {0}
University: {1}
Level: {2}
Project: {3}
Link: {4}'''.format(
			self._name,
			self._university,
			self._level,
			self._project.get_name(),
			self._link
			)

	def __str__(self):
		return self.to_string()

	def to_dictionary(self):
		mood_grades = [str(integer) for integer in self._mood_grades]
		project_grades = [str(integer) for integer in self._project.get_grades()]
		return {
			"user_id": self._user_id,
			"university": self._university,
			"name": self._name,
			"link": self._link,
			"level": self._level,
			"mood_grades": ",".join(mood_grades),
			"project_name": self._project.get_name(),
			"project_grades": ",".join(project_grades)
		}

if (__name__ == "__main__"):
	stud = Student(
		user_id = 312162559,
		university = "University of Oxford",
		name = "Daniil",
		link = "t.me/zkerriga",
		level = 1,
		project_name = "double integral",
		project_grades = [4, 4],
		mood_grades = [4, 5, 5]
	)
	print(stud)

def create_student_from_name(user_id:int, input_name:str, username):
	projects = ['Double integral', 'Differential equation']
	universitys = ["University of Oxford", "California Institute of Technology", "University of Cambridge", "Yale University", "The University of Chicago"]
	levels = [1, 2]
	grades = [1, 2, 3, 4, 5]

	if (username):
		link = "t.me/" + username
	else:
		link = "t.me/" + "error_link"
	return Student(
		user_id,
		random.choice(universitys),
		input_name,
		link,
		random.choice(levels),
		random.choice(projects),
		[random.choice(grades), random.choice(grades), random.choice(grades)],
		[random.choice(grades), random.choice(grades), random.choice(grades)]
	)

