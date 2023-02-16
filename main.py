import datetime
import os
import threading
import time
import requests
import json
import telebot
from dotenv import load_dotenv

load_dotenv()
users_file_name = "users.txt"
token = os.environ["TLG_BOT_TOKEN"]
bot = telebot.TeleBot(token)


def send_today(chat_id):
    current_day = datetime.datetime.now()
    print("send day ", current_day, " to ", chat_id)
    run_dir = os.path.dirname(__file__)
    requests.post("https://api.telegram.org/bot%s/sendPhoto?chat_id=%s" % (token, chat_id),
                  files={'photo': open(os.path.join(run_dir, "days/stoicism_{}_{}.png".format(current_day.month, current_day.day)), 'rb')})


def save_users_list():
    with open(users_file_name, "w") as fp:
        json.dump(users_list, fp)


def load_users_list():
    with open(users_file_name, "rb") as fp:
        users = json.load(fp)
        return users


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    bot.reply_to(message, "Hi, I'm sending stoic pages every day. You can /subscribe or /unsubscribe")


@bot.message_handler(commands=['subscribe'])
def subscribing(message):
    bot.reply_to(message, "Subscribed, do you want me to /send_today ?")
    users_list.append(message.chat.id)
    save_users_list()
    print(message.chat.id, " subscribed")


@bot.message_handler(commands=['unsubscribe'])
def unsubscribing(message):
    bot.reply_to(message, "Unsubscribed")
    print(message.chat.id, " unsubscribed")
    if message.chat.id in users_list:
        users_list.remove(message.chat.id)
        save_users_list()


@bot.message_handler(commands=['send_today'])
def send_by_request(message):
    send_today(message.chat.id)


def send_to_all():
    print("Send to all")
    for user in users_list:
        send_today(user)


def save_last_day(last_day):
    with open("last_day.txt", "w") as fp:
        json.dump(last_day, fp)


def load_last_day():
    with open("last_day.txt", "rb") as fp:
        last_day = datetime.datetime.fromtimestamp(json.load(fp))
        return last_day


def check_if_need_to_send():
    last_day_sent = load_last_day()
    print("last time checked %s" % last_day_sent)
    while True:
        time.sleep(60)
        print("Check if today is the day at {}".format(datetime.datetime.utcnow()))

        if ((datetime.datetime.utcnow() - last_day_sent).days >= 1) and (datetime.datetime.utcnow().hour > 7):
            send_to_all()
            last_day_sent = datetime.datetime.utcnow()
            save_last_day(last_day_sent.timestamp())


def run_bot():
    bot.infinity_polling()


if __name__ == '__main__':
    users_list = load_users_list()
    threading.Thread(target=run_bot).start()
    threading.Thread(target=check_if_need_to_send()).start()
