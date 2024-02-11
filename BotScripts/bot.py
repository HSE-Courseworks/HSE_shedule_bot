import telebot


class MyTelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.bot.send_message(message.chat.id, "Привет! Я бот. Как я могу вам помочь?")

        @self.bot.message_handler(func=lambda message: True)
        def echo_all(message):
            self.bot.reply_to(message, message.text)

    def run(self):
        self.bot.polling(none_stop=True)
