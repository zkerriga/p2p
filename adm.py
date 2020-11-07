from bot import bot

import db_worker
import config
import states
from telebot import types

@bot.message_handler(commands = ["adm"])
# request admin password
def adm(message):
    bot.send_message(message.chat.id, "Input password (1234):")
    db_worker.set_state(message.chat.id, states.States.S_WRONG_ADM_PASS.value)

def set_keyboard():
    # display 'pull data' button for admin
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    button_1 = types.KeyboardButton ("Pull data")
    markup.add(button_1)

    return markup

@bot.message_handler(func = lambda message: db_worker.get_current_state(message.chat.id) == states.States.S_WRONG_ADM_PASS.value)
def check_pass(message):
    if message.text == "1234":
        bot.send_message(message.chat.id, "Hello, Admin!", reply_markup=set_keyboard())
        db_worker.set_state(message.chat.id, states.States.S_VALID_ADM_PASS.value)
    else:
        bot.send_message(message.chat.id, "Wrong password!")


@bot.message_handler(func = lambda message: db_worker.get_current_state(message.chat.id) == states.States.S_VALID_ADM_PASS.value)
def pull_data(message):
    if message.text == "Pull data":
        bot.send_message(message.chat.id, "Pullling data...")
    else:
        bot.send_message(message.chat.id, "Pullling data...")




if __name__ == "__main__":
    bot.infinity_polling()
