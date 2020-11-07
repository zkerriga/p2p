import sqlite3
import utils
import config

class Database():
	"""
	Database for students
	"""
	database_name = "Student"

	def __init__(self, database):
		self.connection = sqlite3.connect(database)
		self.cursor = self.connection.cursor()

	def create_table(self):

		self.connection.execute(
			'''
			CREATE TABLE IF NOT EXISTS {0}
			(
				[id] INTEGER PRIMARY KEY AUTOINCREMENT,
				[user_id] INTEGER,
				[name] TEXT,
				[course] TEXT,
				[project] TEXT,
				[mark] integer,
				[left_verify] integer
			)
			'''.format(database_name)
		)
		self.connection.commit()

	def add_student(self, user_id, name, course, project, mark, left_verify):
		with self.connection:
			self.cursor.execute(
				"INSERT INTO {0} VALUES(?, ?, ?, ?, ?, ?)".format(database_name),
				(user_id, name, course, project, mark, left_verify)
			)

	def close(self):
		self.connection.close()


if __name__ == "__main__":
	a = Database(config.database) # Testing

	a.create_table()
	a.add_student(12, "Vitalya", "1", "Mathematics", 0, 3)
	a.add_student(13, "Danya", "1", "Phisic", 0, 3)
	a.add_student(14,"Andrew", "1", "Eng", 0, 3)
	a.add_student(15,"Amir", "1", "History", 0, 3)
	a.add_student(16,"Alex", "1", "Philisophy", 0, 3)
	a.close()