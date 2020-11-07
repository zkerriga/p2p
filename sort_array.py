from database import Database
from Student import Student

def sort_for_adm(students):
	return sorted(students, key = lambda Student: Student.calc_average_mood(), reverse=True)

def sort_for_teacher(students):
	return sorted(students, key = lambda Student: Student.calc_average_grade(), reverse=True)

db = Database()

students = db.get_list_students()

db.close()
for i in sort_for_adm(students):
	print (i.calc_average_mood())
	print (i._name)

print()

for i in sort_for_teacher(students):
	print (i.calc_average_grade())
	print (i._name)

