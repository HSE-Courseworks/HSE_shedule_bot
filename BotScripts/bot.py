import telebot
from TableScripts.download_google import download_sheet



class MyTelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)

        @self.bot.message_handler(commands=['get_sheet'])
        def handle_get_sheet(message):
            self.bot.send_message(message.chat.id, "Привет! Я бот. Отправь мне ссылку на таблицу")

        @self.bot.message_handler(func=lambda message: True)
        def handle_get_sheet(message):
            if 'docs.google.com/spreadsheets' in message.text:
                sheet_link = message.text
                sheet_content = download_sheet(sheet_link)
                with open(sheet_content, 'rb') as document:
                    self.bot.send_document(message.chat.id, document)
            else:
                # Отправляем сообщение пользователю о том, что ссылка не распознана
                self.bot.send_message(message.chat.id, "Пожалуйста, отправьте действительную ссылку на Google таблицу.")

    def run(self):
        self.bot.polling(none_stop=True)

