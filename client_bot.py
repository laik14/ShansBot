import os
import sqlite3
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Загрузка переменных окружения из файла .env
load_dotenv()
TELEGRAM_API_TOKEN = os.getenv('CLIENT_BOT_TOKEN')

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('services.db')
    return conn

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM services')
    services = cursor.fetchall()
    conn.close()
    
    keyboard = [[InlineKeyboardButton(service[1], callback_data=f'service_{service[0]}')] for service in services]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Добро пожаловать! Выберите услугу:', reply_markup=reply_markup)

# Обработчик выбора услуги
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    service_id = query.data.split('_')[1]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM services WHERE id = ?', (service_id,))
    service = cursor.fetchone()[0]
    cursor.execute('SELECT id, name, chat_id FROM employees WHERE chat_id IS NOT NULL')
    employees = cursor.fetchall()
    conn.close()

    if not employees:
        await query.edit_message_text(text=f"Вы выбрали: {service}\nК сожалению, сейчас нет доступных сотрудников.")
        return

    employee = employees[0]  # Redirect to the first available employee
    await query.edit_message_text(text=f"Вы выбрали: {service}\nПеренаправляем к сотруднику: {employee[1]}")

    # Отправка сообщения сотруднику
    await context.bot.send_message(chat_id=employee[2], text=f"К вам перенаправлен клиент для услуги: {service}")
    
    # Отправка сообщения клиенту
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Пожалуйста, ожидайте ответа от {employee[1]}")

def main() -> None:
    # Создаем экземпляр Application и передаем ему токен
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button, pattern='^service_[0-9]+$'))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()