from telebot import types

def get_eval_keyboard():
	print("[+] keyboard")
	button_eval = types.KeyboardButton("Evaluate")
	button_be_eval = types.KeyboardButton("Be evaluated")
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

def grade_keyboard():
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	button_1 = types.KeyboardButton("Grade student")
	markup.add(button_1)
	return markup

def grade_task_keyboard():
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	button_1 = types.KeyboardButton("1")
	button_2 = types.KeyboardButton("2")
	button_3 = types.KeyboardButton("3")
	button_4 = types.KeyboardButton("4")
	button_5 = types.KeyboardButton("5")
	markup.add(button_1, button_2, button_3, button_4, button_5)
	return markup


def grade_emoji_keyboard():
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	button_1 = types.KeyboardButton("😁")
	button_2 = types.KeyboardButton("😐")
	button_3 = types.KeyboardButton("😞")
	markup.add(button_3, button_2, button_1)
	return markup