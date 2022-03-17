from telebot import TeleBot
from translate import Translator
from keyboards import generate_lang_menu
from cfg import LANG
from py_currency_converter import convert  # pip install py-currency-converter
from menukeyboard import generate_main_menu, generate_bnw_blur
import urllib.request
from time import sleep, strftime, localtime

time = lambda x: strftime("%H:%M:%S %d.%m.%Y", localtime(x))

TOKEN = ''  # <<<<<<<-----------Your telegram bot token here
bot = TeleBot(TOKEN)
CURRENCIES = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD',
              'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD',
              'CDF', 'CHF', 'CLP', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP',
              'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'FOK', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD',
              'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY',
              'KES', 'KGS', 'KHR', 'KID', 'KMF', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD',
              'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD',
              'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON',
              'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP',
              'SLL', 'SOS', 'SRD', 'SSP', 'STN', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TVD',
              'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XDR', 'XOF',
              'XPF', 'YER', 'ZAR', 'ZMW']


@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    first_name = message.chat.first_name
    bot.send_message(chat_id, f'Привет {first_name}!')
    msg = bot.send_message(chat_id, '''Выбери услугу:
P.S. Что бы посмотреть все доступные валюты напишите /currencies''', reply_markup=generate_main_menu())
    bot.register_next_step_handler(msg, choice)


# ПЛАНЫ НА БУДУЩЕЕ: ДОБАВИТЬ ВОЗВРАТ НА ГЛАВНОЕ МЕНЮ В ЛЮБОЕ ВРЕМЯ
def choice(message):
    print(message.text)
    chat_id = message.chat.id
    if message.text == 'Переводчик':
        msg = bot.send_message(chat_id, 'Выберите язык на который хотите перевести:', reply_markup=generate_lang_menu())
        bot.register_next_step_handler(msg, get_fromlanguage)
    elif message.text == 'Конвертер валюты':
        msg = bot.send_message(chat_id, 'Напишите валюту с которой будете ковертировать:')
        bot.register_next_step_handler(msg, to_currency)
    elif message.text == 'Рандомная картинка':
        width = bot.send_message(chat_id, 'Введите ширину: ')
        bot.register_next_step_handler(width, get_length)
    elif message.text == 'Таймер/напоминалка':
        date = message.date
        print(time(date))
    elif message.text == 'Секретная кнопка ;)':
        bot.send_message(chat_id, 'Камила не грусти)')
        bot.send_sticker(chat_id, 'CAACAgIAAxkBAAL4WGBNzrTjVDZuo6tNQjjXEMqssQiKAAIRAAPEh5Iv7MRrGIsAARl2HgQ')
        sleep(5)
        send_welcome(message)
    elif message.text == '/currencies':
        currencies(message)


def to_currency(message):
    from_currency = message.text
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'На какую валюту хотите перевести:')
    bot.register_next_step_handler(msg, converter, from_currency=from_currency)


@bot.message_handler(commands=['currencies'])
def currencies(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f'Вот все доступные валюты: {CURRENCIES}')


@bot.message_handler(commands=['123'])
def reply(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 123)


@bot.message_handler(commands=['about'])
def about(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, f'''Это тестовый бот!''')


def get_tolanguage(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Выберите язык на который хотите перевести: ', reply_markup=generate_lang_menu())
    bot.register_next_step_handler(msg, get_fromlanguage)


def get_fromlanguage(message):
    chat_id = message.chat.id
    if message.text == 'Меню':
        send_welcome(message)
    else:
        try:
            text = message.text
            to_lang = LANG[text]
            msg = bot.send_message(chat_id, 'Выберите язык с которого хотите перевести: ',
                                   reply_markup=generate_lang_menu())
            bot.register_next_step_handler(msg, get_text, to_lang)
        except KeyError:
            bot.reply_to(message, 'Упс такой язык не поддерживается.')


def get_text(message, to_lang):
    chat_id = message.chat.id
    try:
        text = message.text
        from_lang = LANG[text]
        msg = bot.send_message(chat_id, 'Введите слово или предложение:')
        bot.register_next_step_handler(msg, translate, to_lang, from_lang)

    except KeyError:
        bot.reply_to(message, 'Упс такой язык не поддерживается.')


def translate(message, to_lang, from_lang):
    chat_id = message.chat.id
    text = message.text
    translator = Translator(to_lang=to_lang, from_lang=from_lang)
    text_trans = translator.translate(text)
    bot.send_message(chat_id, text_trans)
    get_tolanguage(message)


def converter(message, from_currency):
    to_currency = message.text
    chat_id = message.chat.id
    conv = convert(base=from_currency, amount=1, to=[to_currency])
    if type(conv) == dict:
        bot.send_message(chat_id, f'{to_currency} : {conv.get(to_currency)}')
    else:
        bot.send_message(chat_id, conv)
    print(conv)
    send_welcome(message)


def get_length(message):
    chat_id = message.chat.id
    width = message
    lenght = bot.send_message(chat_id, 'Введите высоту: ')
    bot.register_next_step_handler(lenght, bnw, width)


def bnw(message, width):
    chat_id = message.chat.id
    length = message.text
    width = width.text
    choice = bot.send_message(chat_id, 'Хотите что бы фотография была черно-белая или размытая?',
                              reply_markup=generate_bnw_blur())
    bot.register_next_step_handler(choice, blur, width, length)


def blur(message, width, length):
    chat_id = message.chat.id
    if message.text == 'Черно-белая':
        URL = 'https://picsum.photos/' + width + '/' + length + '?grayscale'
        img = urllib.request.urlopen(URL).read()
        bot.send_photo(chat_id, img)
        sleep(3)
        send_welcome(message)
    elif message.text == 'Обычная':
        URL = 'https://picsum.photos/' + width + '/' + length
        img = urllib.request.urlopen(URL).read()
        bot.send_photo(chat_id, img)
        sleep(3)
        send_welcome(message)
    elif message.text == 'Размытая':
        msg = bot.send_message(chat_id, 'Насколько размытую фотографию вы хотите? 1-10')
        bot.register_next_step_handler(msg, blur_amount, width, length)


def blur_amount(message, width, length):
    chat_id = message.chat.id
    if int(message.text) > 0 and int(message.text) < 11:
        URL = 'https://picsum.photos/' + width + '/' + length + '/?blur=' + str(message.text)
        img = urllib.request.urlopen(URL).read()
        bot.send_photo(chat_id, img)
        sleep(3)
        send_welcome(message)
    else:
        bot.send_message(chat_id, 'Вы ввели неверное число! :( ')
        send_welcome(message)


bot.polling(none_stop=True)

# Here are some changes for my bot!
