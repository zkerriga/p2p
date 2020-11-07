import telebot
import config
from db_worker import get_current_state as get_state
from db_worker import set_state
from states import States as st
from Student import *
from keyboards import *
from database import Database
import utils


bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ["start"])
def start(message):
	bot.send_message(message.chat.id, "Enter your name to log in:")
	# ADD INFO MESSAGE
	print(f"[+] Login: {message.from_user.username}")
	set_state(message.chat.id, st.S_LOGIN_WAIT.value)

def print_info(message, student=None):
	if (not student):
		student = get_student_from_db(message.from_user.id)
	bot.send_message(message.chat.id, f"Your info:\n\n{student.to_string()}")

	set_state(message.chat.id, st.S_TWO_BUTTONS.value)
	bot.send_message(message.chat.id, "You want to:", reply_markup=get_eval_keyboard())

@bot.message_handler(content_type = ["text"])
@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_LOGIN_WAIT.value)
def add_to_database(message):
	student = create_student_from_name(message.from_user.id, message.text, message.from_user.username)
	print(f"[+] Student {message.from_user.username} created!")

	db = Database()
	db.add_student(student)
	db.close()

	print_info(message, student)

@bot.message_handler(content_type = ["text"])
@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_TWO_BUTTONS.value
											and message.text == "Evaluate")
def evaluate(message):
	print(f"[+] Evaluate {message.from_user.username}")

	set_state(message.chat.id, st.S_EVALUATE.value)
	current_student = get_student_from_db(message.from_user.id)
	current_student.set_eval(True)
	# update data for is_eval

	matched_student = match(current_student)
	if matched_student:
		bot.send_message(message.chat.id, f"Your peer:\n\n{matched_student.to_string()}")
	else:
		bot.send_message(message.chat.id, "Peer matching. Wait...")

@bot.message_handler(content_type = ["text"])
@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_TWO_BUTTONS.value
											and message.text == "To be evaluated")
def to_be_evaluate(message):
	print(f"[+] To be evaluated {message.from_user.username}")

	set_state(message.chat.id, st.S_TO_BE_EVALUATE.value)
	current_student = get_student_from_db(message.from_user.id)
	current_student.set_eval(False)
	# update data for is_eval

	matched_student = match(current_student)
	if matched_student:
		bot.send_message(message.chat.id, f"Your peer:\n\n{matched_student.to_string()}")
	else:
		bot.send_message(message.chat.id, "Peer matching. Wait...")

#### ADM BLOCK

attempt = 0

@bot.message_handler(commands = ["adm"])
# request admin password
def adm(message):
	bot.send_message(message.chat.id, "Input password (1234):", reply_markup=types.ReplyKeyboardRemove())
	set_state(message.chat.id, st.S_WRONG_ADM_PASS.value)

def set_keyboard():
	# display 'pull data' button for admin
	markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
	button_1 = types.KeyboardButton ("Pull data")
	button_2 = types.KeyboardButton ("Quit")
	markup.add(button_1, button_2)

	return markup

@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_WRONG_ADM_PASS.value)
def check_pass(message):
	global attempt
	if message.text == "1234":
		attempt = 0
		bot.send_message(message.chat.id, "Hello, Admin!", reply_markup=set_keyboard())
		set_state(message.chat.id, st.S_VALID_ADM_PASS.value)
	elif attempt < 2:
		attempt += 1
		bot.send_message(message.chat.id, "Wrong password!")
	else:
		attempt = 0
		bot.send_message(message.chat.id, "Cancel authorization", reply_markup = types.ReplyKeyboardRemove())
		print_info(message)

@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_VALID_ADM_PASS.value)
def pull_data(message):
	if message.text == "Pull data":
		bot.send_message(message.chat.id, "Pullling data... and logout", reply_markup = types.ReplyKeyboardRemove())
	elif message.text == "Quit":
		bot.send_message(message.chat.id, "Admin logout", reply_markup = types.ReplyKeyboardRemove())
	print_info(message)


#### END ADM BLOCK



#### ERROR BLOCK
@bot.message_handler(func = lambda message: True)
def repeat_all_messages(message):
	print(f"[-] Another message: {message.from_user.username}")
#### END ERROR BLOCK


if __name__ == "__main__":
	bot.infinity_polling()
