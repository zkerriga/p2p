import telebot
import config

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands = ["start"])
def start(message):
	"""
	show to user his info which maded up
	"""
	bot.send_message(message.chat.id, "Hello world")


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)

if __name__ == "__main__":
	bot.infinity_polling()
