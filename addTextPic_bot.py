# -*- coding: utf-8 -*-
"""
telegram bot for register_next_step handler.
"""

import telebot #pip install pyTelegramBotAPI
from pathlib import Path
import datetime
import logging
import multipleLines
import imageMerger
import os
logging.basicConfig(filename='addTextPic_bot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

API_TOKEN = os.environ.get('MERGEIMAGES')

bot = telebot.TeleBot(API_TOKEN)

user_dict = {}

class User: #get user data
    def __init__(self, name):
        self.name = name #string for the header
        self.name2 = None #string for the main text


print("Listening...")
logging.debug("Listening...")
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.reply_to(message, """\
Привіт! Я бот для кліпання шаблонів для інсти.
                                 \n Напиши пліз заголовок для поста """)

    bot.register_next_step_handler(msg, process_name_step)

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name)
        user_dict[chat_id] = user
        print(f'Working with with user {chat_id}, who typed header... {user_dict[chat_id].name}')
        logging.debug(f'Working with with user {chat_id}, who typed header... {user_dict[chat_id].name}')
        msg = bot.reply_to(message, 'Введіть будь ласка текст, що буде під фото')  # bot replying for a certain message
        bot.register_next_step_handler(msg, process_name2_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_name2_step(message):
    try:
        chat_id = message.chat.id
        name2 = message.text
        user = user_dict[chat_id]
        user.name2 = name2
        print(f'Working with with user {chat_id}, who typed main text... {user_dict[chat_id].name2}')
        logging.debug(f'Working with with user {chat_id}, who typed main text... {user_dict[chat_id].name2}')
        # msg = bot.reply_to(message, 'Дякую') #bot replying for a certain message
        bot.send_message(chat_id, 'Загрузить, будь-ласка, фотку') #bot replying for a certain message
    except Exception as e:
        bot.reply_to(message, 'oooops')

@bot.message_handler(content_types=['photo'])
def photo(message):
    """Preapiring folder"""
    chat_id = message.chat.id
    user = user_dict[chat_id]
    """Prepairing directory with chat_id and output file with timestamp"""
    TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    directory = f'dir_{chat_id}_{TIMESTAMP}'
    print(f'Directory: {directory}')
    logging.debug(f'Directory: {directory}')
    Path(directory).mkdir(exist_ok=True)  # creating a new directory if not exist
    print(f'Directory is made... {directory}')
    logging.debug(f'Directory is made... {directory}')
    """Downloading photo"""
    print('message.photo =', message.photo)
    fileID = message.photo[-1].file_id
    print('fileID =', fileID)
    file_info = bot.get_file(fileID)
    print('file.file_path =', file_info.file_path)
    downloaded_file = bot.download_file(file_info.file_path)
    filename = f"{directory}/image_{TIMESTAMP}.jpg"
    with open(filename, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.send_message(chat_id,
                     text='Готую файл до відправки. Почекайте...')  # bot send message not depending on previous messages

    imageMerger.main(filename, directory)
    multipleLines.main(user_dict[chat_id].name, user_dict[chat_id].name2, directory)
    file = open(f'./{directory}/pic_text.png', 'rb')
    bot.send_document(chat_id, file)  # sending file to user
    """End of program"""


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will happen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

bot.infinity_polling()