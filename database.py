import sqlite3
import utils
import config

class Database():
	"""

	"""
	def __init__(self, database):
		self.connection = sqlite3.connect(database)
		self.cursor = self.connection.cursor()

	def create_table(self):

		self.connection.execute('''CREATE TABLE IF NOT EXISTS Student
       	  ([id] INTEGER PRIMARY KEY AUTOINCREMENT, [user_id] INTEGER, [name] TEXT,
       	   [course] TEXT, [project] TEXT,
       	    [mark] integer, [left_verify] integer)''')
          
		self.connection.commit()

	def add_student(self, user_id, name, course, project, mark, left_verify):
		with self.connection:
			self.cursor.execute("INSERT INTO Student VALUES(?, ?, ?, ?, ?, ?)", (user_id, name, course, project, mark, left_verify))



	def close(self):
		self.connection.close()


#TEST!!!!!!!!!!!!!!!!!
a = Database(config.database)
	
a.create_table()
a.add_student(12, "Vitalya", "1", "Mathematics", 0, 3)
a.add_student(13, "Danya", "1", "Phisic", 0, 3)
a.add_student(14,"Andrew", "1", "Eng", 0, 3)
a.add_student(15,"Amir", "1", "History", 0, 3)
a.add_student(16,"Alex", "1", "Philisophy", 0, 3)
a.close()