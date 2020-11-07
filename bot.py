import telebot
import config
from db_worker import get_current_state as get_state
from db_worker import set_state
from states import States as st

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ["start"])
def start(message):
	if (get_state(message.from_user.id) == st.S_START):
		set_state(st.S_NOT_IN_DATA)
	bot.send_message(message.chat.id, "Enter your name to log in:")
	print(f"[+] Login: {message.from_user.username}")

@bot.message_handler(lambda message: get_state(message.from_user.id) == st.S_NOT_IN_DATA)
def add_to_database(message):
	


####

@bot.message_handler(lambda message: True)
def repeat_all_messages(message):
	print(f"[-] Another message: {message.from_user.username}")

if __name__ == "__main__":
	bot.infinity_polling()

"""
{
	'content_type': 'text',
	'message_id': 18,
	'from_user': {
		'id': 312162559,
		'is_bot': False,
		'first_name': 'Даниил',
		'username': 'zkerriga',
		'last_name': None,
		'language_code': 'en',
		'can_join_groups': None,
		'can_read_all_group_messages': None,
		'supports_inline_queries': None
	},
	'date': 1604731942,
	'chat': {
		'id': 312162559,
		'type': 'private',
		'title': None,
		'username': 'zkerriga',
		'first_name': 'Даниил',
		'last_name': None
		'all_members_are_administrators': None
		'photo': None
		'description': None
		'invite_link': None
		'pinned_message': None
		'permissions': None
		'slow_mode_delay': None
		'sticker_set_name': None
		'can_set_sticker_set': None
	}
	'forward_from': None
	'forward_from_chat': None
	'forward_from_message_id': None
	'forward_signature': None
	'forward_date': None
	'reply_to_message': None
	'edit_date': None
	'media_group_id': None
	'author_signature': None
	'text': '/start'
	'entities': [<telebot.types.MessageEntity object at 0x102c73a60>]
	'caption_entities': None
	'audio': None
	'document': None
	'photo': None
	'sticker': None
	'video': None
	'video_note': None
	'voice': None
	'caption': None
	'contact': None
	'location': None
	'venue': None
	'animation': None
	'dice': None
	'new_chat_member': None
	'new_chat_members': None
	'left_chat_member': None
	'new_chat_title': None
	'new_chat_photo': None
	'delete_chat_photo': None
	'group_chat_created': None
	'supergroup_chat_created': None
	'channel_chat_created': None
	'migrate_to_chat_id': None
	'migrate_from_chat_id': None
	'pinned_message': None
	'invoice': None
	'successful_payment': None
	'connected_website': None
	'json': {
		'message_id': 18
		'from': {
			'id': 312162559
			'is_bot': False
			'first_name': 'Даниил'
			'username': 'zkerriga'
			'language_code': 'en'
		}
		'chat': {
			'id': 312162559
			'first_name': 'Даниил'
			'username': 'zkerriga'
			'type': 'private'
		}
		'date': 1604731942
		'text': '/start'
		'entities': [{
			'offset': 0
			'length': 6
			'type': 'bot_command'
		}]
	}
}
"""