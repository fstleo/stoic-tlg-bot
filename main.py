import datetime
import os
import threading
import time
import requests
import json
import telebot
from dotenv import load_dotenv
import schedule
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()
users_file_name = "users"
picture_name_template = "days/stoicism_{}_{}.png"
token = os.environ["TLG_BOT_TOKEN"]
bot = telebot.TeleBot(token)


def send_today(chat_id):
    current_day = datetime.datetime.now()
    print("send day ", current_day, " to ", chat_id)
    run_dir = os.path.dirname(__file__)
    requests.post("https://api.telegram.org/bot%s/sendPhoto?chat_id=%s" % (token, chat_id),
                  files={'photo': open(os.path.join(run_dir, picture_name_template.format(current_day.month, current_day.day)), 'rb')})


def save_users_list():
    with open(users_file_name, "w") as fp:
        json.dump(users_list, fp)


def load_users_list():
    with open(users_file_name, "rb") as fp:
        users = json.load(fp)
        return users


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.reply_to(message, "Hi, I'm sending pages from stoic book every day. Do you want to /subscribe or just /send_today?")
    set_unsubscribed_commands_for_user(message.chat.id)


@bot.message_handler(commands=['subscribe'])
def subscribing(message):
    if message.chat.id not in users_list:
        users_list.append(message.chat.id)
        save_users_list()
        bot.reply_to(message, "Subscribed, do you want me to /send_today ?")
        print(message.chat.id, " subscribed")
        set_subscribed_commands_for_user(message.chat.id)
    else:
        bot.reply_to(message, "Already subscribed, do you want me to /send_today ?")
        print(message.chat.id, " already subscribed")


def set_subscribed_commands_for_user(chat_id):
    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("/send_today", "Send today's picture"),
            telebot.types.BotCommand("/unsubscribe", "Unsubscribe every day update")
        ],
        scope=telebot.types.BotCommandScopeChat(chat_id)
    )


def set_unsubscribed_commands_for_user(chat_id):
    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("/send_today", "Send today's picture"),
            telebot.types.BotCommand("/subscribe", "Subscribe for every day update")
        ],
        scope=telebot.types.BotCommandScopeChat(chat_id)
    )


@bot.message_handler(commands=['unsubscribe'])
def unsubscribing(message):
    if message.chat.id in users_list:
        users_list.remove(message.chat.id)
        save_users_list()
        set_unsubscribed_commands_for_user(message.chat.id)
        bot.reply_to(message, "Unsubscribed")
        print(message.chat.id, " unsubscribed")


@bot.message_handler(commands=['send_today'])
def send_by_request(message):
    send_today(message.chat.id)


def send_to_all():
    print("Send to all")
    for user in users_list:
        send_today(user)


def setup_timer():
    schedule.every().day.at("07:00").do(send_to_all)
    while True:
        schedule.run_pending()
        time.sleep(60)


def run_bot():
    bot.set_my_commands(
        commands=[
            telebot.types.BotCommand("/start", "Start")
        ]
    )
    for user in users_list:
        set_subscribed_commands_for_user(user)
    bot.infinity_polling()


if __name__ == '__main__':
    users_list = load_users_list()
    threading.Thread(target=run_bot).start()
    threading.Thread(target=setup_timer()).start()
