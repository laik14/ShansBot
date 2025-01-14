import sqlite3

# Подключение к базе данных (если базы данных нет, она будет создана)
conn = sqlite3.connect('services.db')
cursor = conn.cursor()

# Создание таблицы "services"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS services (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

# Создание таблицы "employees"
cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        chat_id INTEGER
    )
''')

# Сохранение изменений и закрытие соединения с базой данных
conn.commit()
conn.close()

print("Database and tables created successfully.")