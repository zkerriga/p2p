import sqlite3
import utils
import config
import random

class Database():
	"""
	Database for students
	"""
	table_student = "Student"
	table_level = "Level"
	table_project = "Project"
	table_mark = "Mark"

	def __init__(self, database):
		self.connection = sqlite3.connect(database)
		self.cursor = self.connection.cursor()

	def create_table_student(self):
		with self.connection:
			self.connection.execute(
				'''
				CREATE TABLE IF NOT EXISTS {0}
				([id] INTEGER PRIMARY KEY AUTOINCREMENT,
					[user_id] INTEGER UNIQUE,
					[name] TEXT,
					[level] INTEGER,
					[project] INTEGER,
					[mark] INTEGER,
					[mood] INTEGER,
					[link] TEXT,
					[username] TEXT)'''.format(self.table_student))

			self.connection.commit()

	def create_table_level(self):
		with self.connection:
			self.connection.execute('''
				CREATE TABLE IF NOT EXISTS {0}
	       	  	(
	       	  		[id] INTEGER PRIMARY KEY AUTOINCREMENT,
	       	   		[level] INTEGER UNIQUE
	       	   	)
	       	   	'''.format(self.table_level))
		
			self.connection.commit()

	def create_table_project(self):
		with self.connection:
			self.connection.execute('''CREATE TABLE IF NOT EXISTS {0}
			   	(
			    	[id] INTEGER PRIMARY KEY AUTOINCREMENT,
			    	[project] TEXT UNIQUE
			    )
			    '''.format(self.table_project))
			          
			self.connection.commit()

	def create_table_mark(self):
		with self.connection:
			self.connection.execute(
				'''
				CREATE TABLE IF NOT EXISTS {0}
				(
					[id] INTEGER PRIMARY KEY AUTOINCREMENT,
			    	[mark] TEXT UNIQUE
				)
				'''.format(self.table_mark))
	          
			self.connection.commit()

	def fill_table(self, table, name_col, value):
		
		with self.connection:
			self.cursor.execute("INSERT INTO {0} ({1}) VALUES(?)".format(table, name_col), (value, ))
			self.connection.commit()

	def add_student(self, user_id, name, link, username):
		"""
		Add a student with random parametrs: level, project, mark
		"""
		with self.connection:

			level = random.choice(self.cursor.execute("SELECT * FROM {0} ".format(self.table_level)).fetchall())
			project = random.choice(self.cursor.execute("SELECT * FROM {0} ".format(self.table_project)).fetchall())
			mark = self.cursor.execute("SELECT mark FROM {0} WHERE mark = ? ".format(self.table_mark), ('not_evaluated',)).fetchone()
			mood = 0
			print("Level list: {}".format(level))
			print("Mark list: {}".format(mark))
			print("Project list: {}".format(project))
			#try:
			self.cursor.execute("INSERT INTO {0} ({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}) VALUES(?, ?, ?, ?, ?, ?, ?, ?)".
				format(self.table_student, "user_id", "name", "level", "project", "mark", "mood", "link", "username"),
				(user_id, name, level[0], project[0], mark[0], mood, link, username))
			return 1
			#except:
			#	print("User already exist")
			#	return 0

	def get_info_student(self, user_id):
		"""
		get all info about student form Student table
		"""
		with self.connection:
			info_student = self.cursor.execute("SELECT * FROM {0} WHERE user_id = ?".format(self.table_student), (user_id, )).fetchall()

		return info_student[0]

	def get_info_for_adm(self):
		"""
		get some users with bad mood from 1 to -5 by decreasing
		return a list of everuthing except user_id
		"""
		with self.connection:
			info_students_adm = self.cursor.execute("SELECT name, level, project, mark, mood, link, username\
			  FROM {0}".format(self.table_student)).fetchall()
		
		return info_students_adm

	def get_info_for_teacher(self):
		"""
		get some users with bad mood from 1 to -5 by decreasing
		return a list with name, level, project, mark, link, username 
		"""
		with self.connection:
			info_students_teacher = self.cursor.execute("SELECT name, level, project, mark, link, username\
			  FROM {0}".format(self.table_student)).fetchall()
		
		return info_students_teacher

	def close(self):
		self.connection.close()


if __name__ == "__main__":
	a = Database(config.database) # Testing
	marks = ['A', 'B', 'D', 'C', 'not_evaluated']
	projects = ['double integral', 'differential equation', 'information security', 'electricity supply', 'limits']
	try:
		a.create_table_student()
		a.create_table_level()
		a.create_table_project()
		a.create_table_mark()
		
		for i in range(1,3):
			a.fill_table(a.table_level, "level", i)

		for mark in marks:
			a.fill_table(a.table_mark, "mark", mark) 
		for project in projects:
			a.fill_table(a.table_project, "project", project)
	except:
		print("tables already exist!")
	a.add_student(1, "Ken", "site", "username")
	a.add_student(2, "Ray", "site", "username")
	a.add_student(3, "Stephany", "site", "username")
	
	student_1 = a.get_info_student(1)
	student_2 = a.get_info_student(2)
	student_3 = a.get_info_student(3)
	
	print('------------------------')
	print("Students info for adm: {}".format(a.get_info_for_adm()))
	print()
	print("Students info for teacher: {}".format(a.get_info_for_teacher()))

	print()
	a.close()














