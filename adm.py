from bot import bot

import db_worker
import config
import states
from telebot import types

attempt = 0

@bot.message_handler(commands = ["adm"])
# request admin password
def adm(message):
    bot.send_message(message.chat.id, "Input password (1234):")
    db_worker.set_state(message.chat.id, states.States.S_WRONG_ADM_PASS.value)

def set_keyboard():
    # display 'pull data' button for admin
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    button_1 = types.KeyboardButton ("Pull data")
    button_2 = types.KeyboardButton ("Quit")
    markup.add(button_1, button_2)

    return markup

@bot.message_handler(func = lambda message: db_worker.get_current_state(message.chat.id) == states.States.S_WRONG_ADM_PASS.value)
def check_pass(message):
    global attempt
    if message.text == "1234":
        attempt = 0
        bot.send_message(message.chat.id, "Hello, Admin!", reply_markup=set_keyboard())
        db_worker.set_state(message.chat.id, states.States.S_VALID_ADM_PASS.value)
    elif attempt < 2:
        attempt += 1
        bot.send_message(message.chat.id, "Wrong password!")
    else:
        attempt = 0
        bot.send_message(message.chat.id, "Cancel authorization", reply_markup = types.ReplyKeyboardRemove())
        db_worker.set_state(message.chat.id, states.States.S_START.value)

@bot.message_handler(func = lambda message: db_worker.get_current_state(message.chat.id) == states.States.S_VALID_ADM_PASS.value)
def pull_data(message):
    if message.text == "Pull data":
        bot.send_message(message.chat.id, "Pullling data... and logout", reply_markup = types.ReplyKeyboardRemove())
        db_worker.set_state(message.chat.id, states.States.S_START.value)
    elif message.text == "Quit":
        bot.send_message(message.chat.id, "Admin logout", reply_markup = types.ReplyKeyboardRemove())
        db_worker.set_state(message.chat.id, states.States.S_START.value)

if __name__ == "__main__":
    bot.infinity_polling()
