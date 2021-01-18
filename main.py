import config
import telebot
from telebot import types
import sqlite3
import random
bot = telebot.TeleBot(config.token)
conn = sqlite3.connect('data_main.db', check_same_thread=False)
c = conn.cursor()
    

@bot.message_handler(commands=["study"])
def study(message):
    try:
        id = message.chat.id
        c.execute("SELECT admin FROM user WHERE admin='%d'"%(id))
        conn.commit()
        row = c.fetchone()
        if row==None:
            bot.send_message(message.chat.id, "Sorry! For this operation you must be as admin")
            return 0
        if row[0]==id:
            msg = bot.send_message(message.chat.id, "ASK")
            bot.register_next_step_handler(msg, study_one)
    except:
        bot.send_message(message.chat.id, "Прости.. У меня меленькие проблемки")
def study_one(message):
    try:
        text = message.text
        text = text.lower()
        c.execute("INSERT INTO user(ask, text, admin) VALUES('%s','None','None')"%(text))
        conn.commit()
        msg = bot.send_message(message.chat.id, "TEXT")
        bot.register_next_step_handler(msg, study_two)
    except:
        bot.send_message(message.chat.id, "Прости.. У меня меленькие проблемки")
def study_two(message):
    try:
        text = message.text
        c.execute("UPDATE user SET text='%s' WHERE text='None'"%(text))
        conn.commit()
        bot.send_message(message.chat.id, "Спасибо за обучение!")
    except:
        bot.send_message(message.chat.id, "Прости.. У меня меленькие проблемки")
@bot.message_handler(content_types=["text"])
def ask(message):
    try:
        text = message.text
        text = text.lower()
        c.execute("SELECT ask FROM user WHERE ask='%s'"%(text))
        conn.commit()
        row = c.fetchone()
        if row == None:
            a = ['Что что?','Что прости?','Я тебя не понимаю =(','Повтори-ка =)']
            b = random.choice(a)
            bot.send_message(message.chat.id, b)
        else:
            c.execute("SELECT text FROM user WHERE ask='%s'"%(text))
            conn.commit()
            row = c.fetchone()
            bot.send_message(message.chat.id, row[0])
    except:
        bot.send_message(message.chat.id, "Бу бу бу! Притормози!")
bot.polling(none_stop = True)
