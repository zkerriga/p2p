from Project import Project

class Student(object):
	"""
	The student object contains all the information about it.
	"""
	def __init__(self, name, university, ):
		super(Student, self).__init__()
		
		self.user_id:int
		self.university:str
		self.name:str
		self.link:str
		self.level:str
		self.project:Project
		self.mood_grades:list

	def to_dictionary():
		return {"user_id": self.name}

if (__name__ == "__main__"):
	dictionary = {}

	dictionary["user_id"] = 1
	dictionary["university"] = "KFU"
	dictionary["name"] = "Max"
	dictionary["link"] = "t.me/zkerriga"
	dictionary["level"] = 1
	dictionary["mood_grades"] = "1,2,3,4,5"
	dictionary["project_name"] = "MatLab"
	dictionary["project_grades"] = "double integral"

def get_random_student():
	projects = ['double integral', 'differential equation', 'information security', 'electricity supply', 'limits']
	universitys = []