from database import Database
from Student import Student

def sort_for_adm(students):
	return sorted(students, key = lambda Student: Student.calc_average_mood(), reverse=True)

def sort_for_teacher(students):
	return sorted(students, key = lambda Student: Student.calc_average_grade(), reverse=True)
