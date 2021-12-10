import telebot
from telebot import types
from random import choice
import sqlite3

bot = telebot.TeleBot('1990831136:AAHQ0d0_SwGxngmgAhpU0PHr6-DknnRFeIs')
game_bool = False
change_name = False
username = ''

@bot.message_handler(content_types=['document', 'voice'])
def welcome(message):
  bot.send_message(message.chat.id, "Пиши текстом!")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Напишите /help для справки")


@bot.message_handler(commands=['help'])
def welcome(message):
  bot.send_message(message.chat.id, "/help - выводит справку \n /start - начало работы с ботом \n /leaders - выводит таблицу лидеров")



@bot.message_handler(commands=['leaders'])
def welcome(message):
    conn = sqlite3.connect("leaders.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM leaderboard ORDER BY score DESC LIMIT 5')
    rows = cursor.fetchall()
    conn.commit()
    text = ''
    for i in range(len(rows)):
        text += str(rows[i][0]) + ' ' + str(rows[i][1]) + '\n'
    bot.send_message(message.chat.id, text)











bot.polling(none_stop=True)

