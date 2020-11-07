import sqlite3
import utils
import config
import random

class Database():
	"""
	Database for students
	"""
	table_student = "Student"

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
					[project] TEXT,
					[grade_project] TEXT,
					[grade_mood] TEXT,
					[link] TEXT,
					[university] TEXT)'''.format(self.table_student))

			self.connection.commit()

	def add_student(self, dict):
		"""
		Add a new student to db with data in dict 
		"""
		with self.connection:

			dict = 
			#try:
			self.cursor.execute("INSERT INTO {0} ({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}) VALUES(?, ?, ?, ?, ?, ?, ?, ?)".
				format(self.table_student, "user_id", "name", "level", "project", "grade_project", "grade_mood", "link", "university"),
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

		if info_student[0] != []:
			dict_info = to_dict(info_student[0])
		return dict_info
"""
	def get_info_for_adm(self):
		
		#get some users with bad mood from 1 to -5 by decreasing
		#return a list of everuthing except user_id
		
		with self.connection:
			info_students_adm = self.cursor.execute("SELECT name, level, project, mark, mood, link, username\
			  FROM {0}".format(self.table_student)).fetchall()
		
		return info_students_adm

	def get_info_for_teacher(self):
		
		#get some users with bad mood from 1 to -5 by decreasing
		#return a list with name, level, project, mark, link, username 
		
		with self.connection:
			info_students_teacher = self.cursor.execute("SELECT name, level, project, mark, link, username\
			  FROM {0}".format(self.table_student)).fetchall()
		
		return info_students_teacher
"""
	def close(self):
		self.connection.close()


if __name__ == "__main__":
	a = Database(config.database) # Testing
	














