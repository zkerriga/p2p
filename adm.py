from bot import bot

import config
from telebot.types import ReplyKeyboardMarkup

@bot.message_handler(commands = ["adm"])
# request admin password
def adm(message):
    bot.send_message(message.chat.id, "Input password (1234):")

def set_keyboard():
    # display 'pull data' button for admin
    markup = ReplyKeyboardMarkup(resize_keyboard = True)
    pull_data = "Pull data⚙️"
    markup.add(pull_data)

    return markup

@bot.message_handler(content_types=["text"])
def check_pass(message):
    if message.text == "1234":
        bot.send_message(message.chat.id, "Hello, Admin!", reply_markup=set_keyboard())
    else:
        bot.send_message(message.chat.id, "Wrong password!")
if __name__ == "__main__":
    bot.infinity_polling()
