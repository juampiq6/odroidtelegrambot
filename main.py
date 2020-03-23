import telebot
import time
from torrentHelper import *

bot_token= '701428206:AAHrylLjv7s59PAJf6tliGGdxcEy1Wle3cg'

allowed_users= [
     570877444,
     391658447
    ]

temporalId = {}

bot= telebot.TeleBot(token=bot_token)

def isAllowedUser(message):
    return message.from_user.id in allowed_users

@bot.message_handler(func=lambda message: not isAllowedUser(message))
def reject(message):
    bot.send_message(message.chat.id, "Nigga, who the fuck are you? I dont talk to nigga ass motherfuckers...")

def isCommand(message, com=None):
    if ('entities' not in message.json):
        return False
    else:
        return message.json['entities'][0]['type'] == 'bot_command' and message.text.split()[0][1:] == com

def hasArgument(message,t: type=None):
    try:
        b = message.text.split()[1]
        if (t != None):
            return type(t(b)) is t
    except IndexError:
        print("index error in argument")
        return False

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

## LIST TORRENTS

def formatList(data):
    def getStatusCharacter(s):
        switcher={
            0:"ST",
            6:"CP",
            4:"DL"
            }
        return switcher.get(s, str(s))
    def getDoneNumbers(l,t):
        tmb = t//(1024*1024)
        dmb = (t - l)//(1024*1024)
        return str(dmb)+" of "+str(tmb)+" MB"
    txt = ""
    if (data['arguments']['torrents'] == []):
        txt = "No torrents"
    else:
        for e in data['arguments']['torrents']:
            txt += '*'+str(e['id'])+')* ('+ getStatusCharacter(e['status']) +') '\
            +e['name'] + '\n*--'+ str(e['percentDone']*100)[0:4] +'%--* '\
            + getDoneNumbers(e['leftUntilDone'], e['totalSize'])+' - '\
            +str((e['rateDownload'])//1024)+' KB/s\n\n'
    return txt

@bot.message_handler(commands=['list'])
def listTorrents(message):
    res = getTorrent()
    msg = formatList(json.loads(res.text))
    print(msg)
    bot.send_message(message.chat.id, msg, parse_mode='markdown',disable_web_page_preview=True)

## ADD TORRENT

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
        bot.reply_to(message, 'Oooops, the error was '+str(e))

def isTorrentFile(message):
    return message.content_type == 'document' and message.document.mime_type == 'application/x-bittorrent'

def isTorrentMagnet(message):
    return message.content_type == 'text' and 'magnet:?' in message.text

# @bot.message_handler(func=lambda message: isTorrentFile(message) and isAllowedUser(message))
# def file(message):
#     print(message)
    
#     msg = bot.send_message(message.chat.id, "I have received the torrent file, if you want to rename it, answer with its name, if not just send ok")
#     bot.register_next_step_handler(msg,request_torrent_name_step)

# def request_torrent_name_step(message):
#     try:
#         name = message.text
#         if name == 'ok':
#             bot.reply_to(message, 'Ok, downloading torrent with default name')
#         else:
#             bot.reply_to(message, 'Ok, downloading torrent with name '+name)
            
#     except Exception as e:
#         bot.reply_to(message, 'oooops, the error was '+e)

@bot.message_handler(func=lambda message: isTorrentMagnet(message) and isAllowedUser(message))
def magnet(message):
    bot.send_message(message.chat.id, "Its a magnet link")

## DELETE TORRENT

def deleteFile(message):
    try:
        res = deleteTorrent(True if message.text == "YES" else False, temporalId['delete'])
                
        if (res.status_code != 200):
            bot.reply_to(message, 'Error ocurred when trying to delete torrent'+res.text)
            raise Exception('Exception caught when deleting a torrent: '+ '[' + res.status_code + ']' + res.text)
        else:
            bot.reply_to(message, 'Torrent n° '+ str(temporalId['delete']) + ' deleted ')
    except Exception as e:
        bot.reply_to(message, 'Oooops, the error was '+e)

@bot.message_handler(func=lambda message: isCommand(message,com="delete") and hasArgument(message,t=int))
def delete(message):
    arg = int(message.text.split()[1])
    temporalId['delete'] = arg
    t = json.loads(getTorrent(int(arg)).text)

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    btn1 = telebot.types.KeyboardButton('YES')
    btn2 = telebot.types.KeyboardButton('NO')
    # btn3 = telebot.types.KeyboardButton('3')
    markup.add(btn1, btn2)
    msg = bot.send_message(message.chat.id, "Do you want to delete the file of torrent:\n"+ t['arguments']['torrents'][0]['name'] +' ?', reply_markup=markup)
    bot.register_next_step_handler(msg,deleteFile)

## PAUSE AND RESUME

@bot.message_handler(func=lambda message: isCommand(message,com="pause") and hasArgument(message,t=int))
def pause(message):
    arg = message.text.split()[1]
    pauseTorrent(int(arg))
    bot.send_message(message.chat.id, "Paused torrent n° "+arg)

@bot.message_handler(func=lambda message: isCommand(message,com="resume") and hasArgument(message,t=int))
def resume(message):
    arg = message.text.split()[1]
    resumeTorrent(int(arg))
    bot.send_message(message.chat.id, "Resumed torrent n° "+arg)

## DEFAULT COMMAND HANDLER

@bot.message_handler(func=lambda message: isCommand(message) and not hasArgument(message))
def commandDefault(message):
    bot.send_message(message.chat.id, "Unknown command, or missing or bad parameter.")

@bot.message_handler(func=lambda message: not isCommand(message))
def notcommandDefault(message):
    bot.send_message(message.chat.id, "I don't understand. I'm a bot, use commands")

bot.polling(interval=1)
