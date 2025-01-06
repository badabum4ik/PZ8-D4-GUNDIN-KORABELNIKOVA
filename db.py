import sqlite3
from datetime import datetime

# Создание базы данных и подключение
conn = sqlite3.connect('new_database.db')
cursor = conn.cursor()

# Создание таблицы с указанными столбцами
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL,
    messages TEXT NOT NULL,
    date TEXT NOT NULL,
    command TEXT NOT NULL
)
''')

# Заполнение базы данных демонстрационными данными
data = [
    (123456789, "Привет, как дела?", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "/start"),
    (987654321, "Помоги мне с задачей", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "/start_timer"),
    (123123123, "Что нового?", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "/stop_timer"),
    (456456456, "Какая погода?", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "/start_game"),
    (789789789, "До свидания!", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "/stop_game")
]

cursor.executemany('''
INSERT INTO user_data (telegram_id, messages, date, command) 
VALUES (?, ?, ?, ?)
''', data)

# Сохранение изменений и закрытие соединения
conn.commit()
conn.close()

print("База данных создана и заполнена данными.")
