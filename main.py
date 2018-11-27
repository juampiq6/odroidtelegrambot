import telebot
import time

bot_token= '701428206:AAHrylLjv7s59PAJf6tliGGdxcEy1Wle3cg'

bot= telebot.TeleBot(token=bot_token)

@bot.message_handler(commands=['start'])
def send_hello(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    btn1 = telebot.types.KeyboardButton('1')
    btn2 = telebot.types.KeyboardButton('2')
    btn3 = telebot.types.KeyboardButton('3')
    markup.add(btn1, btn2, btn3)

    bot.send_message(message.chat.id,"Hello, user. What do you want to do?",reply_markup=markup)

@bot.message_handler(commands=['exit'])
def exit(message):
    markup=telebot.types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "bye", reply_markup=markup)


bot.polling(interval=10)
