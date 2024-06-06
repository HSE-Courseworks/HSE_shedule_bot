import telebot
import psycopg2
from TableScripts.download_google import download_sheet
from telebot import types
from TableScripts.db_in import DatabaseManager
from TableScripts.db_out import ScheduleManager

DB_CONNECTION_STRING = "dbname='botbase' user='annaerm' host='database' password='qwer1234'"


class MyTelegramBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.bot.message_handler(commands=['start'])(self.start)
        self.db_manager = DatabaseManager(dbname='botbase', user='annaerm', password='qwer1234', host='database')
        self.bot.message_handler(func=lambda message: True)(self.handle_group_name)
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("weekday_"))(self.handle_weekday)
        self.bot.callback_query_handler(func=lambda call: call.data == "retry")(self.handle_retry)
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("edit_note_"))(self.handle_edit_note)
        self.bot.callback_query_handler(func=lambda call: call.data.startswith("switch_actuality_"))(self.handle_switch_actuality)

        self.sh_manager = ScheduleManager(dbname='botbase', user='annaerm', password='qwer1234', host='database')
        self.user_group = {}
        self.user_selected_lesson = {}

    def start(self, message):
        self.bot.send_message(message.chat.id,
                              "Привет! Я бот для твоего расписания. Назови мне свою группу в формате 20ПИ2 (все буквы заглавные)")

    def handle_group_name(self, message):
        group_name = message.text.strip()
        if self.check_group_exists(group_name):
            self.user_group[message.chat.id] = group_name
            weekdays = self.sh_manager.get_weekdays_with_lessons(group_name)
            if weekdays:
                markup = types.InlineKeyboardMarkup()
                for day_id, day_name in weekdays:
                    markup.add(types.InlineKeyboardButton(text=day_name, callback_data=f"weekday_{day_id}"))
                self.bot.send_message(message.chat.id, "Выберите день недели:", reply_markup=markup)
            else:
                self.bot.send_message(message.chat.id, "Расписание для данной группы не найдено.")
        else:
            msg = self.bot.send_message(message.chat.id,
                                        "Твоей группы нет в базе данных :( Пожалуйста, отправь ссылку на Google таблицу")
            self.bot.register_next_step_handler(msg, self.request_schedule_link)

    def handle_weekday(self, call):
        weekday_id = int(call.data.split("_")[1])
        group_name = self.user_group.get(call.message.chat.id)
        if group_name:
            schedule = self.sh_manager.get_schedule_for_group(group_name)
            filtered_schedule = [
                item for item in schedule if item['weekday_id'] == weekday_id
            ]

            if filtered_schedule:
                weekday_name = filtered_schedule[0]['weekday_name']
                formatted_schedule = f"<b><code>Расписание на {weekday_name}:</code></b>\n\n"

                for item in filtered_schedule:
                    lesson_time = item['lesson_time']
                    subject_name = item['subject_name']
                    classroom_name = item['classroom_name']
                    address_name = item['address_name']
                    note = item['note']

                    lesson_info = f"<b>{lesson_time}</b> - {subject_name} в <b>{classroom_name}</b> {address_name} - {note}\n\n"
                    formatted_schedule += lesson_info

                markup = types.InlineKeyboardMarkup()
                for item in filtered_schedule:
                    markup.add(types.InlineKeyboardButton(
                        text=f"Изменить заметку для {item['lesson_time']}",
                        callback_data=f"edit_note_{item['lesson_id']}"
                    ))
                for item in filtered_schedule:
                    markup.add(types.InlineKeyboardButton(
                        text=f"Изменить актуальность для {item['lesson_time']}",
                        callback_data=f"switch_actuality_{item['lesson_id']}"
                    ))

                self.bot.send_message(call.message.chat.id, formatted_schedule, parse_mode='HTML', reply_markup=markup)
            else:
                self.bot.send_message(call.message.chat.id, "Похоже, расписание больше не актуально")

    def handle_edit_note(self, call):
        lesson_id = int(call.data.split("_")[2])
        self.user_selected_lesson[call.message.chat.id] = lesson_id
        self.bot.send_message(call.message.chat.id, "Введите новую заметку:")
        self.bot.register_next_step_handler(call.message, self.request_new_note)

    def request_new_note(self, message):
        lesson_id = self.user_selected_lesson.get(message.chat.id)
        if lesson_id:
            new_note = message.text.strip()
            success = self.sh_manager.update_note_for_lesson(lesson_id, new_note)
            if success:
                self.bot.send_message(message.chat.id, "Заметка успешно обновлена")

    def handle_switch_actuality(self, call):
        lesson_id = int(call.data.split("_")[2])
        success = self.sh_manager.switch_actuality_for_lesson(lesson_id)
        if success:
            self.bot.answer_callback_query(call.id, text="Актуальность успешно изменена")

    def request_schedule_link(self, message):
        sheet_link = message.text.strip()
        if 'docs.google.com/spreadsheets' in sheet_link:
            try:
                file_path = download_sheet(sheet_link)
                self.bot.reply_to(message, f"Расписание загружено. Введите группу еще раз")

                self.db_manager.process_schedule(file_path)

            except Exception as e:
                self.bot.reply_to(message, f"Произошла ошибка при попытке скачать расписание: {e}")
                self.send_retry_link_message(message)
        else:
            self.send_retry_link_message(message)

    def send_retry_link_message(self, message):
        markup = types.InlineKeyboardMarkup()
        retry_button = types.InlineKeyboardButton(text="Попробовать еще раз", callback_data="retry")
        markup.add(retry_button)
        self.bot.send_message(message.chat.id,
                              "Это не похоже на Google Таблицу. Пожалуйста, отправь корректную ссылку.",
                              reply_markup=markup)

    def handle_retry(self, call):
        self.bot.answer_callback_query(call.id, "Окей, давай попробуем еще раз")
        self.bot.send_message(call.message.chat.id,
                              "Пожалуйста, отправьте ссылку на Google таблицу еще раз")
        self.bot.register_next_step_handler(call.message, self.request_schedule_link)

    def check_group_exists(self, group_name):
        with psycopg2.connect(DB_CONNECTION_STRING) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1 FROM groups WHERE name = %s", (group_name,))
                return cursor.fetchone() is not None

    def run(self):
        self.bot.polling(none_stop=True)
