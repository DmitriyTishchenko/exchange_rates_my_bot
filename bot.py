import telebot
import config
import random
from telebot import types
import urllib.request
import json
from datetime import datetime
import locale

bot = telebot.TeleBot(config.TOKEN)

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')


@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/trade.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Курс валют")
    item2 = types.KeyboardButton("🎲 Рандомное число")
    item3 = types.KeyboardButton("😊 Как дела?")
    markup.row(item1)
    markup.row(item2, item3)

    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ Бот - <b>{1.first_name}</b>, созданный чтобы предоставлять "
                     "информацию по курсам валют.".format(
                         message.from_user, bot.get_me()),
                     parse_mode='HTML', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == 'Курс валют':
            # получение курса валют
            try:
                html = urllib.request.urlopen('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5')
                data = html.read()
                JSON_object = json.loads(data)
                name_usd = JSON_object[0]['ccy']
                buy_usd = JSON_object[0]['buy']
                sale_usd = JSON_object[0]['sale']
                name_eur = JSON_object[1]['ccy']
                buy_eur = JSON_object[1]['buy']
                sale_eur = JSON_object[1]['sale']
                name_rur = JSON_object[2]['ccy']
                buy_rur = JSON_object[2]['buy']
                sale_rur = JSON_object[2]['sale']
                now = datetime.now()
                format_date = now.strftime("%d-%m-%Y")
                exchange_rates = "Сегодня: {9}\n"\
                                 "<b>Наличный курс ПриватБанка</b> (в отделениях):\n" \
                                 "\n" \
                                 "<b>Валюта</b>       <b>Покупка</b>        <b>Продажа</b>\n" \
                                 "<b>{0}</b>                {1}         {2}\n" \
                                 "<b>{3}</b>                {4}         {5}\n" \
                                 "<b>{6}</b>                {7}           {8}\n" \
                                 "\n" \
                                 "----------------------------------------------- ".format(name_usd, buy_usd, sale_usd, name_eur, buy_eur, sale_eur, name_rur, buy_rur, sale_rur, format_date)

                bot.send_message(message.chat.id,  exchange_rates, parse_mode='html')
            except:
                bot.send_message(message.chat.id, 'При получении курса валют возникла ошибка')

        elif message.text == '🎲 Рандомное число':
            bot.send_message(message.chat.id, str(random.randint(0, 100)))
        elif message.text == '😊 Как дела?':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Хорошо', callback_data='good')
            item2 = types.InlineKeyboardButton('Не очень', callback_data='bad')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Отлично, сам как?', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')

                # remove inline buttons
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text="😊 Как дела?",
                                      reply_markup=None)

                # show alert
                # bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                #                           text="ВСЕ БУДЕТ ХОРОШО!")
    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
