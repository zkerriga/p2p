from telebot import types

def get_eval_keyboard():
	print("[+] keyboard")
	button_eval = types.KeyboardButton("Evaluate")
	button_be_eval = types.KeyboardButton("To be evaluated")
	start_two_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True)
	start_two_buttons.add(button_eval)
	start_two_buttons.add(button_be_eval)
	return start_two_buttons

def adm_teacher_keyboard():
	# display 'pull data' button for admin
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	button_1 = types.KeyboardButton ("Pull data")
	button_2 = types.KeyboardButton ("Quit")
	markup.add(button_1, button_2)
	return markup
