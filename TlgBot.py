from datetime import datetime
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton


class TlgBot:
    time_slots = []

    def __init__(self, token, app):
        for i in range(24):
            self.time_slots.append("{}:00".format(i))
        self.app = app
        self.token = token

        self.bot = telebot.TeleBot(token)
        self.bot.register_message_handler(self.handle_start, commands=['start', 'help'])
        self.bot.register_message_handler(self.subscribing, commands=['subscribe'])
        self.bot.register_message_handler(self.unsubscribing, commands=['unsubscribe'])
        self.bot.register_message_handler(self.send_by_request, commands=['send_today'])
        self.bot.register_message_handler(self.try_set_time)

    def send_today(self, chat_id, picture):
        self.bot.send_photo(chat_id, picture)

    def handle_start(self, message):
        self.bot.send_message(message.chat.id,
                              "Hi, I'm sending pages from stoic book every day. Do you want to /subscribe for everyday updates or just /send_today?",
                              reply_markup=self.get_subscribed_markup())

    def get_time_selection_markup_markup(self):
        markup = ReplyKeyboardMarkup(row_width=6,one_time_keyboard=True)
        for i in range(4):
            row = [KeyboardButton(time) for time in self.time_slots[i * 6:(i + 1) * 6]]
            markup.add(*row)
        return markup

    def try_set_time(self, message):
        try:
            datetime.strptime(message.text, '%H:%M')
            self.app.subscribe(message.chat.id, message.text)
        except ValueError:
            self.bot.reply_to(message, "Not a valid time slot", reply_markup=self.get_time_selection_markup_markup())

    def subscribed(self, chat_id, time, success):
        if success:
            self.bot.send_message(chat_id, "Updates will be sent at {} every day".format(time),
                                  reply_markup=self.get_subscribed_markup())
        else:
            self.bot.send_message(chat_id, "Updates will be sent at {} every day".format(time),
                                  reply_markup=self.get_subscribed_markup())

    def subscribing(self, message):
        self.bot.reply_to(message, "What time should it be?", reply_markup=self.get_time_selection_markup_markup())

    def get_subscribed_markup(self):
        markup = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        row = [KeyboardButton("/send_today"), KeyboardButton("/unsubscribe")]
        markup.add(*row)
        return markup

    def get_unsubscribed_markup(self):
        markup = ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        row = [KeyboardButton("/send_today"), KeyboardButton("/subscribe")]
        markup.add(*row)
        return markup

    def unsubscribing(self, message):
        self.app.unsubscribe(message.chat.id)

    def unsubscribed(self, id, success):
        if success:
            self.bot.send_message(id, "Unsubscribed", reply_markup=self.get_unsubscribed_markup())
            print(id, " unsubscribed")
        else:
            self.bot.send_message(id, "You're not subscribed", reply_markup=self.get_unsubscribed_markup())
            print(id, " wasn't subscribed")

    def send_by_request(self, message):
        self.app.send_today(message.chat.id)

    def run_bot(self):
        self.bot.infinity_polling()
