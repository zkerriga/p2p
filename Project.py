
class Project(object):
	"""
	This class contains information about a specific active project.
	How many checks are left, what were the ratings?
	"""
	def __init__(self, project_name:str, grades:list):
		super(Project, self).__init__()
		
		self._project_name:str = project_name
		self._grades:list = grades

	def get_name(self):
		return self._project_name

	def get_grades(self):
		return self._grades
