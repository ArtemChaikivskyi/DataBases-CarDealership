import sqlite3

# Створюємо або відкриваємо файл бази даних
avtosalon= sqlite3.connect('databases.db')
claws = avtosalon.cursor()
print("Готово! Файл databases.db відкрито (або створено).")

claws.execute("""
CREATE TABLE IF NOT EXISTS Clients (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  telephone TEXT NOT NULL,
  email TEXT
)
""")

claws.execute("""
CREATE TABLE IF NOT EXISTS Cars (
  id INTEGER PRIMARY KEY,
  brand TEXT NOT NULL,
  model TEXT NOT NULL,
  prise INTEGER NOT NULL
)
""")

claws.execute("""
CREATE TABLE IF NOT EXISTS Employees (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  telephone TEXT NOT NULL
)
""")

claws.execute("""
CREATE TABLE IF NOT EXISTS Sales (
  client_id INTEGER,
  car_id INTEGER,
  employee_id INTEGER,
  date TEXT
)
""")

avtosalon.commit()
print("Таблиці створено!")

# Клієнти
claws.execute("INSERT INTO Clients (name, telephone, email) VALUES (?, ?, ?)", ("Бондар Віталій Олегович", "+380672345111", "bondar.vitalii@gmail.com"))
claws.execute("INSERT INTO Clients (name, telephone, email) VALUES (?, ?, ?)", ("Савчук Христина Ігорівна", "+380503337722", None ))
claws.execute("INSERT INTO Clients (name, telephone, email) VALUES (?, ?, ?)", ("Ткаченко Роман Володимирович", "+380931117744", "tkachenko.roman@gmail.com"))
claws.execute("INSERT INTO Clients (name, telephone, email) VALUES (?, ?, ?)", ("Литвин Наталія Олександрівна", "+380661559933", "lytvyn.nataliia@gmail.com"))

# Автомобілі
claws.execute("INSERT INTO Cars (brand, model, prise) VALUES (?, ?, ?)", ("Toyota", "Corolla", 720000))
claws.execute("INSERT INTO Cars (brand, model, prise) VALUES (?, ?, ?)", ("BMW", "X5", 2080000))
claws.execute("INSERT INTO Cars (brand, model, prise) VALUES (?, ?, ?)", ("Audi", "A6", 1880000))
claws.execute("INSERT INTO Cars (brand, model, prise) VALUES (?, ?, ?)", ("Volkswagen", "Passat", 920000))
claws.execute("INSERT INTO Cars (brand, model, prise) VALUES (?, ?, ?)", ("Skoda", "Octavia", 840000))
claws.execute("INSERT INTO Cars (brand, model, prise) VALUES (?, ?, ?)", ("Ford", "Focus", 780000))
claws.execute("INSERT INTO Cars (brand, model, prise) VALUES (?, ?, ?)", ("Hyundai", "Tucson", 1040000))
claws.execute("INSERT INTO Cars (brand, model, prise) VALUES (?, ?, ?)", ("Mercedes", "C-Class", 1920000))

# Працівники
claws.execute("INSERT INTO Employees (name, telephone) VALUES (?, ?)", ("Кравець Олег Миколайович", "+380671112233"))
claws.execute("INSERT INTO Employees (name, telephone) VALUES (?, ?)", ("Гнатюк Ірина Василівна", "+380501234567"))
claws.execute("INSERT INTO Employees (name, telephone) VALUES (?, ?)", ("Шевчук Андрій Петрович", "+380931445566"))

# Продажі
claws.execute("INSERT INTO Sales VALUES (?, ?, ?, ?)", (1, 2, 1, "2026.01.06"))
claws.execute("INSERT INTO Sales VALUES (?, ?, ?, ?)", (2, 6, 2, "2026.01.15"))
claws.execute("INSERT INTO Sales VALUES (?, ?, ?, ?)", (3, 8, 3, "2026.02.11"))
claws.execute("INSERT INTO Sales VALUES (?, ?, ?, ?)", (4, 1, 1, "2026.02.14"))

# avtosalon.commit()
# print("Дані додано!")
#
# query = '''
# SELECT Clients.name, Cars.brand, Cars.model, Cars.prise, Employees.name, Sales.date
# FROM Sales
# JOIN Clients ON Clients.id = Sales.client_id
# JOIN Cars ON Cars.id = Sales.car_id
# JOIN Employees ON Employees.id = Sales.employee_id
# ORDER BY Clients.name;
# '''

# claws.execute(query)
for row in claws.fetchall():
    print(row)

avtosalon.close()
print("З'єднання закрито!")