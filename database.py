import sqlite3
import utils
import config
import random
from Student import Student

class Database():
	"""
	Database for students
	"""
	table_student = "Students"

	def __init__(self):
		self.connection = sqlite3.connect(config.database)
		self.cursor = self.connection.cursor()
		self.create_table_student()

	def create_table_student(self):
		with self.connection:
			self.connection.execute(
				'''
				CREATE TABLE IF NOT EXISTS {0}
				([id] INTEGER PRIMARY KEY AUTOINCREMENT,
					[user_id] INTEGER UNIQUE,
					[university] TEXT,
					[name] TEXT,
					[link] TEXT,
					[level] INTEGER,
					[mood_grades] TEXT,
					[project_name] TEXT,
					[project_grades] TEXT,
					[match_state] INTEGER
					)'''.format(self.table_student))

			self.connection.commit()

	def add_student(self, student:Student):

		"""
		Add a new student to db with data in dict 
		"""
		with self.connection:
			d = student.to_dictionary()
			try:
				self.cursor.execute("INSERT INTO {0} ({1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)".
				format(self.table_student, "user_id", "university", "name", "link", "level", "mood_grades", "project_name", "project_grades", "match_state"),
				(
					d.get("user_id", ""),
					d.get("university", ""),
					d.get("name", ""), 
					d.get("link", ""),
					d.get("level", ""),
					d.get("mood_grades", ""),
					d.get("project_name", ""),
					d.get("project_grades", ""),
					d.get("match_state", ""),
				))
			
			except:
				print("[-] User already exist")
				return 0

	def get_student(self, user_id):
		"""
		get all info about student form Student table
		"""
		with self.connection:
			info_student = self.cursor.execute("SELECT * FROM {0} WHERE user_id = ?".format(self.table_student), (user_id, )).fetchall()
			print("Student: {}".format(info_student))
		if info_student[0] != []:
			info = info_student[0]
			student = Student(user_id = info[1],
						university = info[2],
						name = info[3],
						link = info[4],
						level = info[5],
						mood_grades = info[6],
						project_name = info[7],
						project_grades = info[8],
						match_state = info[9])

			return student
		return None

	def set_eval_db(self, current_student:Student):
		"""
		set eval to db 
		"""
		user_id = current_student.get_user_id()
		 
		match_state = current_student.get_match_state()
		if match_state == 1:
			searching_match = 2
		else:
			searching_match = 1 
		with self.connection:
			self.cursor.execute("UPDATE {0} SET match_state = ? WHERE user_id = ?".format(self.table_student), (match_state, user_id))
			self.commit()
			find_matched_id = self.cursor.execute("SELECT user_id FROM {0} WHERE match_state = ? ".format(self.table_student), (searching_match)).fetchone()[0]
			print("find_match: {0}".format(find_matched_id))
			if find_matched_id:
				not_matching = 0
				self.cursor.execute("UPDATE {0} SET match_state = ? WHERE user_id = ?".format(self.table_student), (not_matching, user_id))
				self.cursor.execute("UPDATE {0} SET match_state = ? WHERE user_id = ?".format(self.table_student), (not_matching, find_matched_id))
				self.commit()
				matched_student = self.get_student(find_matched_id)
				current_student.set_not_match()
				matched_student.set_not_match()
				return matched_student
			else:
				None
		return None		




	def close(self):
		self.connection.close()
	

if __name__ == "__main__":
	a.create_table_student()

