import telebot
from config import *
from extensions import Convertor
from extensions import BotError
from telebot import types

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    user_name = message.from_user.first_name
    text = f"<b>{user_name}</b>, бот приветствует вас!\n" \
           f"\nБот осуществляет перевод валют по текущему курсу.\n" \
           f"\nЧтобы начать конвертацию, выберите команду /convert \n" \
           f"\nДоступные валюты можно узнать по команде /cur"
    bot.send_message(message.chat.id, text, parse_mode='html')


@bot.message_handler(commands=['cur'])
def values(message: telebot.types.Message):
    text = '<b><u>Доступные валюты:</u></b>'
    for i in currencies.keys():
        text = '\n\n✅ '.join((text, i))
    bot.reply_to(message, text, parse_mode='html')


@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберите валюту - из который будем конвертировать'
    bot.send_message(message.chat.id, text, reply_markup=creat_markup())
    bot.register_next_step_handler(message, cur_from_handler)


def cur_from_handler(message: telebot.types.Message):
    cur_from = message.text.strip()
    text = 'Выберите валюту - в которую будем конвертировать'
    bot.send_message(message.chat.id, text, reply_markup=creat_markup(cur_from))
    bot.register_next_step_handler(message, cur_to_handler, cur_from)


def cur_to_handler(message: telebot.types.Message, cur_from):
    cur_to = message.text.strip()
    text = f'Укажите сумму конвертации из {cur_from} в {cur_to}'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, cur_from, cur_to)


def amount_handler(message: telebot.types.Message, cur_from, cur_to):
    amount = message.text.strip()
    text = f'<b><u>Результат конвертации</u></b>:\n\n'
    try:
        answer = Convertor.convert_currency(cur_from, cur_to, amount)
    except BotError as e:
        bot.reply_to(message, f'Ошибочка вышла: {e}')
        text = f'Укажите сумму конвертации из {cur_from} в {cur_to}'
        bot.send_message(message.chat.id, text)
        bot.register_next_step_handler(message, amount_handler, cur_from, cur_to)
    else:
        bot.send_message(message.chat.id, text + answer, parse_mode='html')


# BUTTONS
def creat_markup(cur_from=None):
    buttons = []
    for cur in currencies:
        if cur != cur_from:
            buttons.append(telebot.types.KeyboardButton(cur))
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    markup.add(*buttons)
    return markup

# MENU
bot_commands = [telebot.types.BotCommand("/help", "Описание работы"),
                telebot.types.BotCommand("/cur", "Доступные валюты"),
                telebot.types.BotCommand("/convert", "Провести конвертацию")]
bot.set_my_commands(bot_commands)
# bot.delete_my_commands()

bot.polling()






