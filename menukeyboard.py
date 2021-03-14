from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def generate_main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton(text='Переводчик')
    btn2 = KeyboardButton(text='Конвертер валюты')
    btn3 = KeyboardButton(text='Рандомная картинка')
    btn4 = KeyboardButton(text='Таймер/напоминалка')
    btn5 = KeyboardButton(text='Секретная кнопка ;)')
    keyboard.row(btn1)
    keyboard.row(btn2)
    keyboard.row(btn3)
    keyboard.row(btn4)
    keyboard.row(btn5)
    return keyboard

def generate_bnw_blur():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    bnw = KeyboardButton(text='Черно-белая')
    blur = KeyboardButton(text='Размытая')
    usual = KeyboardButton(text='Обычная')
    keyboard.add(bnw, blur, usual)
    return keyboard

def generate_yes_no():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    yes = KeyboardButton(text='Да')
    no = KeyboardButton(text='Нет')
    keyboard.add(yes, no)
    return keyboard
