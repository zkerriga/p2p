from enum import Enum

class States(Enum):
	"""
	All types of bot's Variebles
	"""
	S_START = "0"
	S_CHANGE_PHONE = "1"
	S_ENTER_PHONE = "2"
	S_SHOW_KEYBOARD = "3"
	S_OWNER_MODE = "4"