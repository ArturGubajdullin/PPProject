# Импорт библиотеки
import sqlite3

# Подключение к БД
con = sqlite3.connect("Games.db")

# Создание курсора
cur = con.cursor()

# Выполнение запроса и получение всех результатов
result = cur.execute("""SELECT * FROM Games""").fetchall()

# Вывод результатов на экран
for elem in result:
    print(elem)


con.close()
