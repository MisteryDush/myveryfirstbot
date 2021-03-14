from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from cfg import LANG


def generate_lang_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(text='Меню')
    for language in LANG.keys():
        btn = KeyboardButton(text=language)
        keyboard.add(btn)
    keyboard.add(btn1)
    return keyboard
