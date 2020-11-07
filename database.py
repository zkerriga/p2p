import sqlite3
import config
import random
from Student import Student

class Database():
	"""
	Database for students
	"""
	table_student = "Students"
	student_1 = Student(user_id = 51325135,
						university = "California Institute of Technology",
						name = "Nick",
						link = "t.me/zkerriga",
						level = 1,
						mood_grades = [1, 2, 3],
						project_name = 'Differential equation',
						project_grades = [1, 3, 4, 2, 2],
						match_state = 0)
	student_2 = Student(user_id = 531253125,
						university = "Yale University",
						name = "Kelly",
						link = "t.me/Sasha_mar9",
						level = 2,
						mood_grades = [1, 1, 1],
						project_name = 'Double integral',
						project_grades = [5, 3, 4, 4, 5],
						match_state = 0)
	student_3 = Student(user_id = 521351,
						university = "University of Cambridge",
						name = "Ray",
						link = "t.me/awerebea",
						level = 1,
						mood_grades = [3, 2, 3],
						project_name = 'Double integral',
						project_grades = [3, 3, 5, 5, 2],
						match_state = 0)

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
			info_student = self.cursor.execute("SELECT * FROM {0} WHERE user_id = ?".
				format(self.table_student), (user_id, )).fetchall()
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

	def get_matched_user(self, current_student:Student):
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
			self.cursor.execute("UPDATE {0} SET match_state = ? WHERE user_id = ?"
				.format(self.table_student), (match_state, user_id))
			self.connection.commit()
			find_matched_id = self.cursor.execute("SELECT user_id FROM {0} WHERE match_state = ? "
				.format(self.table_student),(searching_match,)).fetchone()
			if (not find_matched_id):
				return None
			find_matched_id = find_matched_id[0]
			print("find_match: {0}".format(find_matched_id))
			if find_matched_id:
				not_matching = 0
				self.cursor.execute("UPDATE {0} SET match_state = ? WHERE user_id = ?"
					.format(self.table_student), (not_matching, user_id))
				self.cursor.execute("UPDATE {0} SET match_state = ? WHERE user_id = ?"
					.format(self.table_student), (not_matching, find_matched_id))
				self.connection.commit()
				matched_student = self.get_student(find_matched_id)
				current_student.set_not_match()
				matched_student.set_not_match()
				return matched_student
			else:
				None
		return None	

	def get_list_students(self):
		"""
		Get whole list of studends
		"""
		with self.connection:
			studends = self.cursor.execute("SELECT * FROM {}". format(self.table_student)).fetchall()
		studends_list = []
		if (not studends):
			
			for student in studends:

				temp_student = Student(user_id = student[1],
						university = student[2],
						name = student[3],
						link = student[4],
						level = student[5],
						mood_grades = student[6],
						project_name = student[7],
						project_grades = student[8],
						match_state = student[9])
				studends_list.append(temp_student)
		studends_list.append(self.student_1)
		studends_list.append(self.student_2)
		studends_list.append(self.student_3)
		return studends_list
		

	def close(self):
		self.connection.close()

	
	

if __name__ == "__main__":
	"""
	a = Database()
	l = a.get_list_students()
	for i in l:
		print()
		print("The student: {}", i)
		print()
	"""
