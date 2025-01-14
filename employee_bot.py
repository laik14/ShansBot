import os
import sqlite3
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Загрузка переменных окружения из файла .env
load_dotenv()
TELEGRAM_API_TOKEN = os.getenv('EMPLOYEE_BOT_TOKEN')

# Подключение к базе данных
def get_db_connection():
    conn = sqlite3.connect('services.db')
    return conn

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Вы зарегистрировались как сотрудник. Используйте /available чтобы указать свою доступность.')

# Обработчик команды /available
async def available(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    employee_name = update.message.from_user.username
    chat_id = update.message.chat_id
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT OR REPLACE INTO employees (name, chat_id) VALUES (?, ?)', (employee_name, chat_id))
    conn.commit()
    conn.close()
    await update.message.reply_text('Вы указали свою доступность.')

def main() -> None:
    # Создаем экземпляр Application и передаем ему токен
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Регистрируем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("available", available))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()