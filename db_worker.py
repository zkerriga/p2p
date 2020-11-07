from vedis import Vedis 
import config
from states import States

def get_current_state(user_id):
	"""
	get current condition of the bot
	"""
	with Vedis(config.db_file) as db:
		try:
			return db[user_id].decode()
		except KeyError:
			print("{-}")
			return States.S_START.value

def set_state(user_id, value):
	"""
	Save the current condition
	"""
	with Vedis(config.db_file) as db:
		try:
			db[user_id] = value
			return True
		except:
			print("{-} set")
			return False