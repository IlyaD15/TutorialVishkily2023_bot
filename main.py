import telebot
import requests as rq
url_kurs = 'https://www.cbr-xml-daily.ru/daily_json.js'
from time import time
from hide_token import token

bot = telebot.TeleBot(token)

kurs = dict()
ok_time_kurs = time()


def get_kurs(now_time):
    global ok_time_kurs, kurs

    if now_time < ok_time_kurs:
        return

    kurs = rq.get(url_kurs).json()
    ok_time_kurs += 60 * 60


get_kurs(ok_time_kurs)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Hi, {message.from_user.username}')


@bot.message_handler(commands=['kurs_all'])
def kurs_message(message):
    get_kurs(time())
    res = kurs
    ans = ''
    for key in res['Valute']:
        val = round(res['Valute'][key]['Value'] / res['Valute'][key]['Nominal'], 3)
        name = res['Valute'][key]['Name']
        ans += f'{name} ({key}): {val}\n'
    bot.send_message(message.chat.id, ans)


@bot.message_handler(commands=['kurs'])
def usd_kurs_message(message):
    try:
        get_kurs(time())
        res = kurs
        abb = message.text.split()[1].upper()
        val = round(res['Valute'][abb]['Value'] / res['Valute'][abb]['Nominal'], 3)
        name = res['Valute'][abb]['Name']
        bot.send_message(message.chat.id, f'{name} ({abb}): {val}')
    except:
        bot.send_message(message.chat.id, 'Неверная команда')


@bot.message_handler(content_types=['text'])
def exo(message):
    bot.send_message(message.chat.id, message.text)


bot.polling(none_stop=True, interval=0)
