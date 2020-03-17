import telebot
import time
from torrentHelper import *

bot_token= '701428206:AAHrylLjv7s59PAJf6tliGGdxcEy1Wle3cg'

allowed_users= [
     570877444,
     391658447
    ]


bot= telebot.TeleBot(token=bot_token)

def isAllowedUser(message):
    return message.from_user.id in allowed_users

@bot.message_handler(commands=['start'])
def send_hello(message):

    handleToken()
    bot.send_message(message.chat.id, "Bot initialized.")
    # markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    # btn1 = telebot.types.KeyboardButton('1')
    # btn2 = telebot.types.KeyboardButton('2')
    # btn3 = telebot.types.KeyboardButton('3')
    # markup.add(btn1, btn2, btn3)

    # bot.send_message(message.chat.id,"Hello, user. What do you want to do?",reply_markup=markup)

# @bot.message_handler(func= lambda message: message.file_path[-8:] == '.torrent')
# def receiveTorrentFile(message):
#     bot.send_message(message.chat.id, "This is a torrent file!")


# @bot.message_handler(commands=['exit'])
# def exit(message):
#     markup=telebot.types.ReplyKeyboardRemove(selective=False)
#     bot.send_message(message.chat.id, "bye")
def formatList(data):
    txt = ""
    for e in data['arguments']['torrents']:
        txt += '__'+str(e['id'])+')__ ['+str(e['status'])+'] '+ e['name'][:30] + ' __'+ str(e['percentDone']*100) +'__ '
    return txt


@bot.message_handler(commands=['list'])
def listTorrents(message):
    res = getTorrent()
    msg = formatList(json.loads(res.text))
    print(msg)
    bot.send_message(message.chat.id, msg, parse_mode='Markdown')

@bot.message_handler(commands=['add'])
def add(message):
    msg = bot.send_message(message.chat.id, "Ok, send the magnet link")
    bot.register_next_step_handler(msg,receiveTorrent)

def receiveTorrent(message):
    try:
        if (isTorrentMagnet):
            link = message.text
            res = addTorrent(filename=link)
            if (res.status_code != 200):
                bot.reply_to(message, 'Error ocurred when trying to add torrent'+res.text)
                raise Exception('Exception caught when adding a torrent: '+ '[' + res.status_code + ']' + res.text)
            bot.reply_to(message, 'Ok, downloading the torrent '+res.text['name'])
        else:
            if (isTorrentFile):
                print(message)
    except Exception as e:
        bot.reply_to(message, 'Oooops, the error was '+e)



def isTorrentFile(message):
    return message.content_type == 'document' and message.document.mime_type == 'application/x-bittorrent'

@bot.message_handler(func=lambda message: isTorrentFile(message) and isAllowedUser(message))
def file(message):
    print(message)
    
    msg = bot.send_message(message.chat.id, "I have received the torrent file, if you want to rename it, answer with its name, if not just send ok")
    bot.register_next_step_handler(msg,request_torrent_name_step)

def request_torrent_name_step(message):
    try:
        name = message.text
        if name == 'ok':
            bot.reply_to(message, 'Ok, downloading torrent with default name')
        else:
            bot.reply_to(message, 'Ok, downloading torrent with name '+name)
            
    except Exception as e:
        bot.reply_to(message, 'oooops, the error was '+e)

def isTorrentMagnet(message):
    return message.content_type == 'text' and 'magnet:?' in message.text

@bot.message_handler(func=lambda message: isTorrentMagnet(message) and isAllowedUser(message))
def magnet(message):
    bot.send_message(message.chat.id, "Its a magnet link")

@bot.message_handler(func=lambda message: not isAllowedUser(message))
def reject(message):
    bot.send_message(message.chat.id, "Nigga, who the fuck are you? I dont talk to nigga ass motherfuckers...")


bot.polling(interval=10)
