import telebot
import config
from db_worker import get_current_state as get_state
from db_worker import set_state
from states import States as st
from Student import *
from keyboards import *
from database import Database

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ["start"])
def start(message):
	bot.send_message(message.chat.id, "Enter your name to log in:")
	# ADD INFO MESSAGE
	print(f"[+] Login: {message.from_user.username}")
	set_state(message.chat.id, st.S_LOGIN_WAIT.value)

def print_info(message, student=None):
	if (not student):
		db = Database()
		student = db.get_student(message.from_user.id)
		db.close()
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
	# set_state(message.chat.id, st.S_TWO_BUTTONS.value)
	# bot.send_message(message.chat.id, "You want to:", reply_markup=get_eval_keyboard())

@bot.message_handler(content_type = ["text"])
@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_TWO_BUTTONS.value
											and message.text == "Evaluate")
def evaluate(message):
	set_state(message.chat.id, st.S_EVALUATE.value)
	db = Database()
	current_student = db.get_student(message.from_user.id)
	db.close()
	matched_student = match(current_student)
	if matched_student:
		bot.send_message(message.chat.id, f"Your peer:\n\n{matched_student.to_string()}")
	else:
		bot.send_message(message.chat.id, "Peer matching...")

@bot.message_handler(content_type = ["text"])
@bot.message_handler(func = lambda message: get_state(message.chat.id) == st.S_TWO_BUTTONS.value
											and message.text == "To be evaluated")
def evaluate(message):
	set_state(message.chat.id, st.S_TO_BE_EVALUATE.value)
	db = Database()
	current_student = db.get_student(message.from_user.id)
	db.close()
	matched_student = match(current_student)
	if matched_student:
		bot.send_message(message.chat.id, f"Your peer:\n\n{matched_student.to_string()}")
	else:
		bot.send_message(message.chat.id, "Peer matching...")

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

@bot.message_handler(func = lambda message: True)
def repeat_all_messages(message):
	print(f"[-] Another message: {message.from_user.username}")

if __name__ == "__main__":
	bot.infinity_polling()

# """
# {
# 	'content_type': 'text',
# 	'message_id': 18,
# 	'from_user': {
# 		'id': 312162559,
# 		'is_bot': False,
# 		'first_name': 'Даниил',
# 		'username': 'zkerriga',
# 		'last_name': None,
# 		'language_code': 'en',
# 		'can_join_groups': None,
# 		'can_read_all_group_messages': None,
# 		'supports_inline_queries': None
# 	},
# 	'date': 1604731942,
# 	'chat': {
# 		'id': 312162559,
# 		'type': 'private',
# 		'title': None,
# 		'username': 'zkerriga',
# 		'first_name': 'Даниил',
# 		'last_name': None
# 		'all_members_are_administrators': None
# 		'photo': None
# 		'description': None
# 		'invite_link': None
# 		'pinned_message': None
# 		'permissions': None
# 		'slow_mode_delay': None
# 		'sticker_set_name': None
# 		'can_set_sticker_set': None
# 	}
# 	'forward_from': None
# 	'forward_from_chat': None
# 	'forward_from_message_id': None
# 	'forward_signature': None
# 	'forward_date': None
# 	'reply_to_message': None
# 	'edit_date': None
# 	'media_group_id': None
# 	'author_signature': None
# 	'text': '/start'
# 	'entities': [<telebot.types.MessageEntity object at 0x102c73a60>]
# 	'caption_entities': None
# 	'audio': None
# 	'document': None
# 	'photo': None
# 	'sticker': None
# 	'video': None
# 	'video_note': None
# 	'voice': None
# 	'caption': None
# 	'contact': None
# 	'location': None
# 	'venue': None
# 	'animation': None
# 	'dice': None
# 	'new_chat_member': None
# 	'new_chat_members': None
# 	'left_chat_member': None
# 	'new_chat_title': None
# 	'new_chat_photo': None
# 	'delete_chat_photo': None
# 	'group_chat_created': None
# 	'supergroup_chat_created': None
# 	'channel_chat_created': None
# 	'migrate_to_chat_id': None
# 	'migrate_from_chat_id': None
# 	'pinned_message': None
# 	'invoice': None
# 	'successful_payment': None
# 	'connected_website': None
# 	'json': {
# 		'message_id': 18
# 		'from': {
# 			'id': 312162559
# 			'is_bot': False
# 			'first_name': 'Даниил'
# 			'username': 'zkerriga'
# 			'language_code': 'en'
# 		}
# 		'chat': {
# 			'id': 312162559
# 			'first_name': 'Даниил'
# 			'username': 'zkerriga'
# 			'type': 'private'
# 		}
# 		'date': 1604731942
# 		'text': '/start'
# 		'entities': [{
# 			'offset': 0
# 			'length': 6
# 			'type': 'bot_command'
# 		}]
# 	}
# }
# """