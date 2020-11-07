import telebot
import config
from db_worker import get_current_state as get_state
from db_worker import set_state
from states import States as st
from Student import *
from keyboards import *
from utils import *
from match import match
import text

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ["start"])
def start(message):
	bot.send_message(message.chat.id, text.TEXT_START)
	bot.send_message(message.chat.id, "Enter your name to log in:", reply_markup=types.ReplyKeyboardRemove())
	print(f"[+] Login: {message.from_user.username}")
	set_state(message.chat.id, st.S_LOGIN_WAIT.value)

def print_info(message, student=None):
	if (not student):
		student = get_student_from_db(message.from_user.id)
	bot.send_message(message.chat.id, f"Your info:\n\n{student.to_string()}", reply_markup=types.ReplyKeyboardRemove())

	set_state(message.chat.id, st.S_TWO_BUTTONS.value)
	bot.send_message(message.chat.id, "You want to:", reply_markup=get_eval_keyboard())

@bot.message_handler(content_type = ["text"])
@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_LOGIN_WAIT.value)
def add_to_database(message):
	student = create_student_from_name(message.from_user.id, message.text, message.from_user.username)
	print(f"[+] Student {message.from_user.username} created!")
	add_student_to_db(student)
	print_info(message, student)

@bot.message_handler(content_type = ["text"])
@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_TWO_BUTTONS.value
											and message.text == "Evaluate")
def evaluate(message):
	print(f"[+] Evaluate {message.from_user.username}")

	set_state(message.chat.id, st.S_EVALUATE.value)
	current_student = get_student_from_db(message.from_user.id)
	current_student.set_eval(True)

	matched_student = match(current_student)
	if matched_student:
		bot.send_message(message.chat.id, f"Your peer:\n\n{matched_student.to_string()}", reply_markup=grade_keyboard())
		bot.send_message(message.chat.id, text.TEXT_FOR_EVALUATOR, reply_markup=grade_keyboard())
		bot.send_message(matched_student.get_user_id(), f"Your peer:\n\n{current_student.to_string()}", reply_markup=grade_keyboard())
		bot.send_message(matched_student.get_user_id(), text.TEXT_FOR_EVALUATED, reply_markup=grade_keyboard())
		set_state(message.chat.id, st.S_EVALUATE_PEERED.value)
		set_state(matched_student.get_user_id(), st.S_TO_BE_EVALUATE_PEERED.value)
	else:
		bot.send_message(message.chat.id, "Peer matching. Wait...")

@bot.message_handler(content_type = ["text"])
@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_TWO_BUTTONS.value
											and message.text == "Be evaluated")
def to_be_evaluate(message):
	print(f"[+] To be evaluated {message.from_user.username}")

	set_state(message.chat.id, st.S_TO_BE_EVALUATE.value)
	current_student = get_student_from_db(message.from_user.id)
	current_student.set_eval(False)

	matched_student = match(current_student)
	if matched_student:
		bot.send_message(message.chat.id, f"Your peer:\n\n{matched_student.to_string()}", reply_markup=grade_keyboard())
		bot.send_message(message.chat.id, text.TEXT_FOR_EVALUATED, reply_markup=grade_keyboard())
		bot.send_message(matched_student.get_user_id(), f"Your peer:\n\n{current_student.to_string()}", reply_markup=grade_keyboard())
		bot.send_message(matched_student.get_user_id(), text.TEXT_FOR_EVALUATOR, reply_markup=grade_keyboard())
		set_state(message.chat.id, st.S_TO_BE_EVALUATE_PEERED.value)
		set_state(matched_student.get_user_id(), st.S_EVALUATE_PEERED.value)
	else:
		bot.send_message(message.chat.id, "Peer matching. Wait...")



@bot.message_handler(content_type = ["text"])
@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_EVALUATE_PEERED.value
											and message.text == "Grade student")
def evaluate_grade_start(message):
	print(f"[+] evaluate_grade_start {message.from_user.username}")
	bot.send_message(message.chat.id, "Rate how the student did the task:", reply_markup=grade_task_keyboard())
	set_state(message.chat.id, st.S_EVALUATE_PEERED_GRADE_1.value)

@bot.message_handler(content_type = ["text"])
@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_EVALUATE_PEERED_GRADE_1.value
											and message.text in ["1", "2", "3", "4", "5"])
def evaluate_grade_1(message):
	print(f"[+] evaluate_grade_1 {message.from_user.username}")
	bot.send_message(message.chat.id, "Rate the student's mood (he or she will not see this grade):", reply_markup=grade_emoji_keyboard())
	set_state(message.chat.id, st.S_EVALUATE_PEERED_GRADE_2.value)

def evaluation_is_over(message):
	bot.send_message(message.chat.id, "Evaluation is over!")
	bot.send_message(message.chat.id, text.TEXT_FINISH, reply_markup=continue_keyboard())
	set_state(message.chat.id, st.S_CONTINUE.value)


@bot.message_handler(content_type = ["text"])
@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_EVALUATE_PEERED_GRADE_2.value)
def evaluate_grade_2(message):
	print(f"[+] To_be_evaluate_grade_2 {message.from_user.username}")
	evaluation_is_over(message)



@bot.message_handler(content_type = ["text"])
@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_TO_BE_EVALUATE_PEERED.value
											and message.text == "Grade student")
def to_be_evaluated_grade_start(message):
	print(f"[+] To_be_evaluated_grade_start {message.from_user.username}")
	bot.send_message(message.chat.id, "Rate the student's mood (he or she will not see this grade):", reply_markup=grade_emoji_keyboard())
	set_state(message.chat.id, st.S_TO_BE_EVALUATE_PEERED_GRADE_1.value)

@bot.message_handler(content_type = ["text"])
@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_TO_BE_EVALUATE_PEERED_GRADE_1.value)
def to_be_evaluated_grade_grade_1(message):
	print(f"[+] to_be_evaluated_grade_grade_1 {message.from_user.username}")
	evaluation_is_over(message)

@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_CONTINUE.value)
def after_continue_button(message):
	print_info(message)



#### ADM BLOCK

attempt = 0

@bot.message_handler(commands = ["adm"])
def adm(message):
	bot.send_message(message.chat.id, "Input password (1234):", reply_markup=types.ReplyKeyboardRemove())
	set_state(message.chat.id, st.S_WRONG_ADM_PASS.value)

@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_WRONG_ADM_PASS.value)
def check_pass_adm(message):
	global attempt
	if message.text == "1234":
		attempt = 0
		bot.send_message(message.chat.id, "Hello, Admin!", reply_markup=adm_teacher_keyboard())
		set_state(message.chat.id, st.S_VALID_ADM_PASS.value)
	elif attempt < 2:
		attempt += 1
		bot.send_message(message.chat.id, "Wrong password!")
	else:
		attempt = 0
		bot.send_message(message.chat.id, "Cancel authorization", reply_markup = types.ReplyKeyboardRemove())
		print_info(message)

@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_VALID_ADM_PASS.value)
def pull_data_adm(message):
	if message.text == "Pull data":
		bot.send_message(message.chat.id, "Pullling 'mental health' data... and logout", reply_markup = types.ReplyKeyboardRemove())
	elif message.text == "Quit":
		bot.send_message(message.chat.id, "Admin logout", reply_markup = types.ReplyKeyboardRemove())
	print_info(message)

#### END ADM BLOCK

#### TEACHER BLOCK

@bot.message_handler(commands = ["teacher"])
# request teacher password
def teacher(message):
	bot.send_message(message.chat.id, "Input password (4321):", reply_markup=types.ReplyKeyboardRemove())
	set_state(message.chat.id, st.S_WRONG_TEACH_PASS.value)

@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_WRONG_TEACH_PASS.value)
def check_pass_teacher(message):
	global attempt
	if message.text == "4321":
		attempt = 0
		bot.send_message(message.chat.id, "Hello, Teacher!", reply_markup=adm_teacher_keyboard())
		set_state(message.chat.id, st.S_VALID_TEACH_PASS.value)
	elif attempt < 2:
		attempt += 1
		bot.send_message(message.chat.id, "Wrong password!")
	else:
		attempt = 0
		bot.send_message(message.chat.id, "Cancel authorization", reply_markup = types.ReplyKeyboardRemove())
		print_info(message)

@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_VALID_TEACH_PASS.value)
def pull_data_teacher(message):
	if message.text == "Pull data":
		bot.send_message(message.chat.id, "Pullling 'academic perfomance' data... and logout", reply_markup = types.ReplyKeyboardRemove())
	elif message.text == "Quit":
		bot.send_message(message.chat.id, "Teacher logout", reply_markup = types.ReplyKeyboardRemove())
	print_info(message)

#### END TEACHER BLOCK


#### ERROR BLOCK
@bot.message_handler(func = lambda message: True)
def repeat_all_messages(message):
	print(f"[-] Another message: {message.from_user.username}")
#### END ERROR BLOCK


if __name__ == "__main__":
	bot.infinity_polling()
