import telebot
from bot import MyTelegramBot

if __name__ == "__main__":
    bot = MyTelegramBot('TOKEN')
    bot.run()

