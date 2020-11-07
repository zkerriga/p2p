from enum import Enum

class States(Enum):
    """
    All types of bot's Variebles
    """
    S_START = "0"
    S_NOT_IN_DATA = "1"
    S_WRONG_ADM_PASS = "ADWP"
    S_VALID_ADM_PASS = "ADVP"
