import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import pytz

# Загрузка переменных окружения из файла .env
load_dotenv()
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Список услуг и сотрудников
services = {
    "service1": "Услуга 1",
    "service2": "Услуга 2",
    "service3": "Услуга 3"
}

employees = {
    "employee1": "Сотрудник 1",
    "employee2": "Сотрудник 2",
    "employee3": "Сотрудник 3"
}

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [[InlineKeyboardButton(services[service], callback_data=service)] for service in services]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите услугу:', reply_markup=reply_markup)

# Обработчик выбора услуги
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    service = services[query.data]

    keyboard = [[InlineKeyboardButton(employees[employee], callback_data=f"{query.data}_{employee}")] for employee in employees]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=f"Вы выбрали: {service}\nТеперь выберите сотрудника:", reply_markup=reply_markup)

# Обработчик выбора сотрудника
async def notify_employee(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    service_key, employee_key = query.data.split('_')
    service = services[service_key]
    employee = employees[employee_key]

    await query.edit_message_text(text=f"Вы выбрали: {service}\nСотрудник: {employee}\nУведомление отправлено.")

    # Отправка уведомления сотруднику
    # Здесь вы можете добавить логику для отправки уведомления сотруднику
    # Например, через email или другой Telegram-бот

def main() -> None:
    # Создаем экземпляр Application и передаем ему токен
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button, pattern='^service[0-9]+$'))
    application.add_handler(CallbackQueryHandler(notify_employee, pattern='^service[0-9]+_employee[0-9]+$'))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()