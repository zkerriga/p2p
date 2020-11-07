from enum import Enum

class States(Enum):
	"""
	All types of bot's Variebles
	"""
	S_START = '0'
	S_LOGIN_WAIT = '1'
	S_TWO_BUTTONS = '2'
	S_EVALUATE = '3'
	S_TO_BE_EVALUATE = '3'
	S_WRONG_ADM_PASS = "ADWP"
	S_VALID_ADM_PASS = "ADVP"
	S_WRONG_TEACH_PASS = "TEACHWP"
	S_VALID_TEACH_PASS = "TEACHVP"
