import telebot
import config
# from telebot import types
from database import Database


bot = telebot.TeleBot(config.TOKEN)
db = Database('database.db')
# айди психолога 1057999762
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id != 1057999762:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = telebot.types.KeyboardButton('Обратиться к психологу 🌻')
        markup.add(item1)
        bot.send_message(message.chat.id, 'Привет 👋\n Скоро мы вас свяжем с психологом) ', reply_markup = markup)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
        item1 = telebot.types.KeyboardButton('Следующая консультация')
        markup.add(item1)
        bot.send_message(message.chat.id, 'Здравствуйте! 👋\n Скоро мы вас свяжем с учеником)', reply_markup=markup)


@bot.message_handler(commands=['stop'])
def stop(message):
    chat_info = db.get_active_chat(message.chat.id)
    if chat_info != False:
        if message.chat.id != 1057999762:
            db.delete_chat(chat_info[0])
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = telebot.types.KeyboardButton('Обратиться к психологу 🌻')
            markup.add(item1)
            markup2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
            item2 = telebot.types.KeyboardButton('Следующая консультация')
            markup2.add(item2)
            bot.send_message(message.chat.id, "Вы вышли из чата 😔", reply_markup = markup)
            bot.send_message(1057999762, "Ученик вышел из чата", reply_markup = markup2)
        else:
            db.delete_chat(chat_info[0])
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
            item1 = telebot.types.KeyboardButton('Следующая консультация')
            markup.add(item1)
            markup2 = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
            item2 = telebot.types.KeyboardButton('Обратиться к психологу 🌻')
            markup2.add(item2)
            bot.send_message(message.chat.id, "Вы закончили беседу", reply_markup = markup)
            bot.send_message(chat_info[1], "Беседа закрыта", reply_markup = markup2)




@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'Следующая консультация':

            chat_two = db.get_chat()

            if db.create_chat(message.chat.id, chat_two) == False:
                bot.send_message(1057999762, "Обращений нет")
            else:
                markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
                item1 = telebot.types.KeyboardButton('/stop')
                markup.add(item1)

                bot.send_message(message.chat.id, "Чат начат", reply_markup = markup)
                bot.send_message(chat_two, "Психолог на связи :)", reply_markup = markup)



        elif message.text == 'Обратиться к психологу 🌻':
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = telebot.types.KeyboardButton('Убрать меня из очереди 😔')
            markup.add(item1)

            db.add_queue(message.chat.id)
            bot.send_message(message.chat.id, "Мы добавили вас в очередь, пожалуйста, подождите ☺", reply_markup = markup)
            bot.send_message(1057999762, "К вам обратился еще один ученик")

        elif message.text == 'Убрать меня из очереди 😔':
            markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = telebot.types.KeyboardButton('Обратиться к психологу 🌻')
            markup.add(item1)

            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, "По вашей просьбе мы удалили вас из очереди 🌞", reply_markup = markup)

        else:
            try:
                chat_info = db.get_active_chat(message.chat.id)
                bot.send_message(chat_info[1], message.text)
            except:
                pass


try:
    bot.polling(none_stop=True)
except:
    pass

