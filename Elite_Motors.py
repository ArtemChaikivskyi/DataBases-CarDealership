import sys          # Модуль для роботи з системними аргументами та завершення програми
import sqlite3      # Модуль для роботи з базою даних SQLite

# Імпортуємо потрібні віджети PyQt5
from PyQt5.QtWidgets import (
    QApplication,   # Головний клас застосунку PyQt
    QWidget,        # Базовий клас для головного вікна
    QLabel,         # Віджет для текстових написів
    QLineEdit,      # Поле для введення тексту
    QPushButton,    # Кнопка
    QVBoxLayout,    # Вертикальне розміщення елементів
    QHBoxLayout,    # Горизонтальне розміщення елементів
    QGridLayout,    # Табличне розміщення елементів
    QMessageBox,    # Діалогові вікна повідомлень
    QDialog,        # Базовий клас для діалогових вікон
)
from PyQt5.QtGui import QIntValidator, QPixmap, QPainter   # Валідатор, картинка, малювання
from PyQt5.QtCore import Qt                                # Константи Qt


DB_NAME = "databases.db"   # Назва файлу бази даних SQLite

# _________________________ Розміри вікон ________________________________
WINDOW_MAIN_W,  WINDOW_MAIN_H  = 651, 341   # Головне вікно  — Elite.Motors
WINDOW_ADD_W,   WINDOW_ADD_H   = 600, 450   # Вікно додавання клієнта
WINDOW_EDIT_W,  WINDOW_EDIT_H  = 600, 450   # Вікно редагування клієнта

# _________________________ Стилі ________________________________________

# Стиль для підписів полів (Name, Email, Telephone, Id_Client)
STYLE_LABEL = """
    color: white;
    font-size: 14px;
    font-weight: bold;
    background-color: #1a1a4e;
    border: 2px solid black;
    padding: 5px;
"""

# Стиль для полів введення тексту
STYLE_INPUT = """
    background-color: white;
    color: black;
    font-size: 14px;
    border: 2px solid black;
    padding: 3px;
"""

# Стиль для полів тільки для читання (головне вікно)
STYLE_INPUT_READONLY = """
    background-color: lightgray;
    color: black;
    font-size: 14px;
    border: 2px solid black;
    padding: 3px;
"""

# Стиль для фіолетових кнопок
STYLE_BTN_PURPLE = """
    QPushButton {
        background-color: purple;
        color: white;
        font-size: 14px;
        font-weight: bold;
        border: 2px solid black;
        padding: 8px 20px;
    }
    QPushButton:hover {
        background-color: #7b00b5;
    }
"""


# _________________________ Робота з базою даних _________________________
class AutosalonDatabase:
    # Конструктор класу бази даних
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name      # Зберігаємо назву бази даних у властивість об'єкта
        self.create_table()         # Одразу створюємо таблицю якщо вона ще не існує

    # Метод підключення до бази даних
    def connect(self):
        return sqlite3.connect(self.db_name)   # Повертаємо об'єкт підключення до SQLite

    # Метод створення таблиці Clients якщо вона ще не існує
    def create_table(self):
        conn = self.connect()       # Відкриваємо з'єднання з базою даних
        cursor = conn.cursor()      # Створюємо курсор для виконання SQL-запитів
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Clients (
                id        INTEGER PRIMARY KEY,
                name      TEXT NOT NULL,
                telephone TEXT NOT NULL,
                email     TEXT
            )
        """)                        # SQL-запит: створити таблицю якщо не існує
        conn.commit()               # Підтверджуємо зміни
        conn.close()                # Закриваємо з'єднання

    # Метод пошуку клієнта за ID
    def find_client(self, client_id):
        conn = self.connect()       # Відкриваємо з'єднання
        cursor = conn.cursor()      # Створюємо курсор
        cursor.execute(
            "SELECT id, name, telephone, email FROM Clients WHERE id = ?",
            (client_id,)
        )                           # Шукаємо клієнта за ID
        client = cursor.fetchone()  # Отримуємо один запис або None якщо не знайдено
        conn.close()                # Закриваємо з'єднання
        return client               # Повертаємо знайдений запис

    # Метод додавання нового клієнта
    def add_client(self, client_id, name, telephone, email):
        conn = self.connect()       # Відкриваємо з'єднання
        cursor = conn.cursor()      # Створюємо курсор
        cursor.execute("""
            INSERT INTO Clients (id, name, telephone, email)
            VALUES (?, ?, ?, ?)
        """, (client_id, name, telephone, email))   # Додаємо новий запис у таблицю
        conn.commit()               # Зберігаємо зміни
        conn.close()                # Закриваємо з'єднання

    # Метод оновлення даних існуючого клієнта
    def update_client(self, client_id, name, telephone, email):
        conn = self.connect()       # Відкриваємо з'єднання
        cursor = conn.cursor()      # Створюємо курсор
        cursor.execute("""
            UPDATE Clients
            SET name = ?, telephone = ?, email = ?
            WHERE id = ?
        """, (name, telephone, email, client_id))   # Оновлюємо дані клієнта за ID
        conn.commit()               # Підтверджуємо зміни
        conn.close()                # Закриваємо з'єднання

    # Метод видалення клієнта за ID
    def delete_client(self, client_id):
        conn = self.connect()       # Відкриваємо з'єднання
        cursor = conn.cursor()      # Створюємо курсор
        cursor.execute(
            "DELETE FROM Clients WHERE id = ?", (client_id,)
        )                           # Видаляємо запис клієнта
        conn.commit()               # Підтверджуємо зміни
        conn.close()                # Закриваємо з'єднання


# _________________________ Вікно додавання нового клієнта _______________
class AddClientDialog(QDialog):
    # Конструктор діалогового вікна додавання
    def __init__(self, db, parent=None):
        super().__init__(parent)                            # Викликаємо конструктор QDialog
        self.db = db                                        # Зберігаємо об'єкт бази даних
        self.setWindowTitle("Elite.Motors — New Client") # Встановлюємо заголовок вікна
        self.setFixedSize(WINDOW_ADD_W, WINDOW_ADD_H)      # Встановлюємо фіксований розмір
        self._bg = QPixmap("Car1.jpeg")                     # Завантажуємо фонову картинку
        self.init_ui()                                     # Будуємо інтерфейс

    # Метод малювання фону — картинка тільки на вікні, не на віджетах
    def paintEvent(self, event):
        painter = QPainter(self)                           # Створюємо об'єкт малювання
        painter.drawPixmap(self.rect(), self._bg)          # Малюємо картинку на весь розмір вікна

    # Метод побудови інтерфейсу вікна додавання
    def init_ui(self):
        main_layout = QVBoxLayout()   # Головний вертикальний макет

        # ---- ТАБЛИЦЯ ПОЛІВ: Id_Client / Name / Email / Telephone ----
        table_layout = QGridLayout()  # Табличний макет — ліворуч підписи, праворуч поля

        self.id_input        = QLineEdit()   # Поле введення ID клієнта
        self.pib_input       = QLineEdit()   # Поле введення імені клієнта
        self.email_input     = QLineEdit()   # Поле введення email
        self.telephone_input = QLineEdit()   # Поле введення телефону

        self.id_input.setValidator(QIntValidator())   # ID приймає тільки цілі числа

        # Додаємо всі поля в таблицю через цикл
        for i, (field, widget) in enumerate([
            ("Id_Client", self.id_input),
            ("Name",      self.pib_input),
            ("Email",     self.email_input),
            ("Telephone", self.telephone_input),
        ]):
            label = QLabel(field)                  # Створюємо підпис для поля
            label.setAlignment(Qt.AlignCenter)     # Вирівнюємо текст по центру
            label.setStyleSheet(STYLE_LABEL)       # Застосовуємо стиль підпису
            widget.setStyleSheet(STYLE_INPUT)      # Застосовуємо стиль поля

            table_layout.addWidget(label,  i, 0)  # Підпис у лівий стовпець
            table_layout.addWidget(widget, i, 1)  # Поле у правий стовпець

        main_layout.addLayout(table_layout)   # Додаємо таблицю в головний макет
        main_layout.addStretch()              # Відступ між таблицею і кнопками

        # ---- КНОПКИ: Add / Cansel ----
        button_layout = QHBoxLayout()   # Горизонтальний макет для кнопок

        add_button    = QPushButton("Add")     # Кнопка додавання клієнта
        cancel_button = QPushButton("Cansel")  # Кнопка скасування

        add_button.setStyleSheet(STYLE_BTN_PURPLE)    # Фіолетовий стиль
        cancel_button.setStyleSheet(STYLE_BTN_PURPLE) # Фіолетовий стиль

        add_button.clicked.connect(self.add_client)   # При натисканні Add — додаємо клієнта
        cancel_button.clicked.connect(self.reject)    # При натисканні Cansel — закриваємо

        button_layout.addStretch()                 # Відступ зліва
        button_layout.addWidget(add_button)        # Кнопка Add
        button_layout.addWidget(cancel_button)     # Кнопка Cansel

        main_layout.addLayout(button_layout)   # Додаємо кнопки в головний макет
        main_layout.addStretch()               # Відступ знизу
        self.setLayout(main_layout)            # Встановлюємо макет для вікна

    # Метод збереження нового клієнта в базу даних
    def add_client(self):
        client_id = self.id_input.text().strip()          # Зчитуємо ID і прибираємо пробіли
        name      = self.pib_input.text().strip()         # Зчитуємо ім'я
        email     = self.email_input.text().strip()       # Зчитуємо email
        telephone = self.telephone_input.text().strip()   # Зчитуємо телефон

        if not client_id or not name or not telephone:    # Перевіряємо обов'язкові поля
            QMessageBox.warning(self, "Error", "ID, Name and Telephone are required!")
            return   # Зупиняємо метод якщо поля порожні

        if self.db.find_client(int(client_id)):           # Перевіряємо чи ID вже є в базі
            QMessageBox.warning(self, "Error", f"Client with ID {client_id} already exists!")
            return   # Зупиняємо метод якщо такий ID вже є

        try:   # Спробуємо додати клієнта в базу
            self.db.add_client(int(client_id), name, telephone, email)
            QMessageBox.information(self, "Success", "Client added successfully!")
            self.accept()   # Закриваємо діалог як успішно виконаний
        except Exception as e:   # Якщо виникла будь-яка помилка
            QMessageBox.critical(self, "Error", f"Failed to add client:\n{e}")


# _________________________ Вікно редагування клієнта ____________________
class EditClientDialog(QDialog):
    # Конструктор діалогового вікна редагування
    def __init__(self, db, client_data, parent=None):
        super().__init__(parent)                           # Викликаємо конструктор QDialog
        self.db          = db                              # Зберігаємо об'єкт бази даних
        self.client_data = client_data                     # Зберігаємо дані клієнта (id, name, telephone, email)
        self.setWindowTitle("Elite.Motors — Edit Client") # Заголовок вікна
        self.setFixedSize(WINDOW_EDIT_W, WINDOW_EDIT_H)   # Фіксований розмір вікна
        self._bg = QPixmap("Car1.jpeg")                    # Завантажуємо фонову картинку
        self.init_ui()                                    # Будуємо інтерфейс

    # Метод малювання фону — картинка тільки на вікні, не на віджетах
    def paintEvent(self, event):
        painter = QPainter(self)                          # Створюємо об'єкт малювання
        painter.drawPixmap(self.rect(), self._bg)         # Малюємо картинку на весь розмір вікна

    # Метод побудови інтерфейсу вікна редагування
    def init_ui(self):
        main_layout = QVBoxLayout()   # Головний вертикальний макет

        # ---- ТАБЛИЦЯ ПОЛІВ: Id_Client / Name / Email / Telephone ----
        table_layout = QGridLayout()  # Табличний макет

        # Заповнюємо поля поточними даними клієнта
        self.id_input        = QLineEdit(str(self.client_data[0]))     # ID клієнта
        self.pib_input       = QLineEdit(self.client_data[1] or "")    # Ім'я клієнта
        self.email_input     = QLineEdit(self.client_data[3] or "")    # Email клієнта
        self.telephone_input = QLineEdit(self.client_data[2] or "")    # Телефон клієнта

        self.id_input.setReadOnly(True)   # ID не можна змінювати — тільки для перегляду

        # Додаємо всі поля в таблицю через цикл
        for i, (field, widget) in enumerate([
            ("Id_Client", self.id_input),
            ("Name",      self.pib_input),
            ("Email",     self.email_input),
            ("Telephone", self.telephone_input),
        ]):
            label = QLabel(field)                  # Створюємо підпис
            label.setAlignment(Qt.AlignCenter)     # Вирівнюємо по центру
            label.setStyleSheet(STYLE_LABEL)       # Застосовуємо стиль підпису
            widget.setStyleSheet(STYLE_INPUT)      # Застосовуємо стиль поля

            table_layout.addWidget(label,  i, 0)  # Підпис у лівий стовпець
            table_layout.addWidget(widget, i, 1)  # Поле у правий стовпець

        main_layout.addLayout(table_layout)   # Додаємо таблицю в головний макет
        main_layout.addStretch()              # Відступ між таблицею і кнопками

        # ---- КНОПКИ: Save / Cansel ----
        button_layout = QHBoxLayout()   # Горизонтальний макет для кнопок

        save_button   = QPushButton("Save")    # Кнопка збереження змін
        cancel_button = QPushButton("Cansel")  # Кнопка скасування

        save_button.setStyleSheet(STYLE_BTN_PURPLE)    # Фіолетовий стиль
        cancel_button.setStyleSheet(STYLE_BTN_PURPLE)  # Фіолетовий стиль

        save_button.clicked.connect(self.save_client)  # При натисканні Save — зберігаємо
        cancel_button.clicked.connect(self.reject)     # При натисканні Cansel — закриваємо

        button_layout.addStretch()                 # Відступ зліва
        button_layout.addWidget(save_button)       # Кнопка Save
        button_layout.addWidget(cancel_button)     # Кнопка Cansel

        main_layout.addLayout(button_layout)   # Додаємо кнопки в макет
        main_layout.addStretch()               # Відступ знизу
        self.setLayout(main_layout)            # Встановлюємо макет

    # Метод збереження оновлених даних клієнта
    def save_client(self):
        name      = self.pib_input.text().strip()         # Зчитуємо ім'я
        email     = self.email_input.text().strip()       # Зчитуємо email
        telephone = self.telephone_input.text().strip()   # Зчитуємо телефон

        if not name or not telephone:   # Перевіряємо обов'язкові поля
            QMessageBox.warning(self, "Error", "Name and Telephone are required!")
            return   # Зупиняємо метод якщо поля порожні

        try:   # Спробуємо оновити дані клієнта
            self.db.update_client(self.client_data[0], name, telephone, email)
            QMessageBox.information(self, "Success", "Client data updated!")
            self.accept()   # Закриваємо діалог як успішно виконаний
        except Exception as e:   # Якщо виникла будь-яка помилка
            QMessageBox.critical(self, "Error", f"Failed to update data:\n{e}")


# _________________________ Головне вікно ________________________________
class Autosalon_UI(QWidget):
    # Конструктор головного вікна
    def __init__(self):
        super().__init__()                               # Викликаємо конструктор QWidget
        self.db = AutosalonDatabase()                    # Створюємо об'єкт для роботи з базою даних
        self.setWindowTitle("Elite.Motors")              # Назва головного вікна
        self.setFixedSize(WINDOW_MAIN_W, WINDOW_MAIN_H) # Фіксований розмір вікна
        self._bg = QPixmap("Car1.jpeg")                  # Завантажуємо фонову картинку
        self.init_ui()                                  # Будуємо інтерфейс

    # Метод малювання фону — картинка тільки на вікні, не на віджетах
    def paintEvent(self, event):
        painter = QPainter(self)                        # Створюємо об'єкт малювання
        painter.drawPixmap(self.rect(), self._bg)       # Малюємо картинку на весь розмір вікна

    # Метод побудови інтерфейсу головного вікна
    def init_ui(self):
        main_layout = QVBoxLayout()   # Головний вертикальний макет

        # ---- ВЕРХНІЙ РЯДОК: Elite.Motors + кнопка Add new entry ----
        top_layout = QHBoxLayout()   # Горизонтальний макет для верхнього рядка

        self.label_title = QLabel("Elite.Motors")   # Назва автосалону зліва
        self.label_title.setStyleSheet("""
            color: purple;
            font-size: 22px;
            font-weight: bold;
            border: 2px solid black;
            padding: 5px;
        """)

        new_button = QPushButton("+ Add new entry")  # Кнопка додавання нового клієнта
        new_button.setStyleSheet(STYLE_BTN_PURPLE)   # Фіолетовий стиль

        top_layout.addWidget(self.label_title)   # Назва зліва
        top_layout.addStretch()                  # Відступ між назвою і кнопкою
        top_layout.addWidget(new_button)         # Кнопка справа
        main_layout.addLayout(top_layout)        # Додаємо верхній рядок у головний макет

        # ---- ЛЕЙБЛ: Client ----
        client_label = QLabel("Client")                  # Підзаголовок секції клієнта
        client_label.setAlignment(Qt.AlignCenter)        # По центру
        client_label.setStyleSheet("color: white; font-size: 18px;")
        main_layout.addWidget(client_label)              # Додаємо в макет

        # ---- РЯДОК: Id_Client + поле введення + кнопка Find ----
        id_layout = QHBoxLayout()   # Горизонтальний макет для пошуку

        id_label = QLabel("Id_Client")       # Підпис поля ID
        id_label.setStyleSheet(STYLE_LABEL)  # Застосовуємо стиль підпису

        self.id_input = QLineEdit()                   # Поле введення ID для пошуку
        self.id_input.setValidator(QIntValidator())   # Дозволяємо вводити тільки числа
        self.id_input.setStyleSheet(STYLE_INPUT)      # Застосовуємо стиль поля

        find_button = QPushButton("Find")             # Кнопка пошуку клієнта
        find_button.setStyleSheet(STYLE_BTN_PURPLE)   # Фіолетовий стиль

        id_layout.addWidget(id_label)       # Підпис зліва
        id_layout.addWidget(self.id_input)  # Поле по центру
        id_layout.addWidget(find_button)    # Кнопка справа
        main_layout.addLayout(id_layout)    # Додаємо рядок у головний макет

        # ---- ТАБЛИЦЯ: Name / Email / Telephone (тільки для перегляду) ----
        table_layout = QGridLayout()   # Табличний макет

        self.pib_input       = QLineEdit()   # Поле відображення імені
        self.email_input     = QLineEdit()   # Поле відображення email
        self.telephone_input = QLineEdit()   # Поле відображення телефону

        # У головному вікні поля тільки для перегляду — не можна редагувати
        self.pib_input.setReadOnly(True)
        self.email_input.setReadOnly(True)
        self.telephone_input.setReadOnly(True)

        # Додаємо підписи і поля в таблицю через цикл
        for i, (field, widget) in enumerate([
            ("Name",      self.pib_input),
            ("Email",     self.email_input),
            ("Telephone", self.telephone_input),
        ]):
            label = QLabel(field)                       # Створюємо підпис
            label.setAlignment(Qt.AlignCenter)          # По центру
            label.setStyleSheet(STYLE_LABEL)            # Стиль підпису
            widget.setStyleSheet(STYLE_INPUT_READONLY)  # Стиль поля readonly

            table_layout.addWidget(label,  i, 0)   # Підпис у лівий стовпець
            table_layout.addWidget(widget, i, 1)   # Поле у правий стовпець

        main_layout.addLayout(table_layout)   # Додаємо таблицю в головний макет
        main_layout.addStretch()              # Відступ між таблицею і кнопками

        # ---- КНОПКИ: Edit / Remove ----
        button_layout = QHBoxLayout()   # Горизонтальний макет для кнопок

        edit_button   = QPushButton("Edit")    # Кнопка відкриття вікна редагування
        delete_button = QPushButton("Remove")  # Кнопка видалення клієнта

        edit_button.setStyleSheet(STYLE_BTN_PURPLE)    # Фіолетовий стиль
        delete_button.setStyleSheet(STYLE_BTN_PURPLE)  # Фіолетовий стиль

        button_layout.addStretch()              # Відступ зліва
        button_layout.addWidget(edit_button)    # Кнопка Edit
        button_layout.addWidget(delete_button)  # Кнопка Remove
        button_layout.addStretch()              # Відступ справа

        main_layout.addLayout(button_layout)   # Додаємо кнопки в головний макет
        self.setLayout(main_layout)            # Встановлюємо головний макет для вікна

        # ---- ПРИВ'ЯЗКА КНОПОК ДО МЕТОДІВ ----
        new_button.clicked.connect(self.open_add_dialog)    # NEW відкриває вікно додавання
        find_button.clicked.connect(self.find_client)       # Find шукає клієнта
        edit_button.clicked.connect(self.open_edit_dialog)  # Edit відкриває вікно редагування
        delete_button.clicked.connect(self.remove_client)   # Remove видаляє клієнта

    # Метод очищення всіх інформаційних полів
    def clear_fields(self):
        self.pib_input.clear()        # Очищаємо поле імені
        self.email_input.clear()      # Очищаємо поле email
        self.telephone_input.clear()  # Очищаємо поле телефону

    # Метод заповнення полів даними знайденого клієнта
    def fill_fields(self, client):
        # client = (id, name, telephone, email)
        self.pib_input.setText(client[1] or "")        # Записуємо ім'я у поле
        self.telephone_input.setText(client[2] or "")  # Записуємо телефон у поле
        self.email_input.setText(client[3] or "")      # Записуємо email у поле

    # Метод пошуку клієнта за введеним ID
    def find_client(self):
        client_id = self.id_input.text().strip()   # Зчитуємо текст з поля ID

        if not client_id:          # Якщо поле порожнє — очищаємо і виходимо
            self.clear_fields()
            return

        client = self.db.find_client(int(client_id))   # Шукаємо клієнта в базі
        if client:                                     # Якщо клієнта знайдено
            self.fill_fields(client)                   # Заповнюємо поля його даними
        else:                                          # Якщо не знайдено
            self.clear_fields()
            QMessageBox.information(self, "Not Found", f"Client with ID {client_id} does not exist.")

    # Метод відкриття діалогу додавання нового клієнта
    def open_add_dialog(self):
        dialog = AddClientDialog(self.db, self)   # Створюємо вікно додавання
        if dialog.exec_():                        # Якщо діалог завершився успішно
            self.id_input.clear()                 # Очищаємо поле ID
            self.clear_fields()                   # Очищаємо інформаційні поля

    # Метод видалення клієнта
    def remove_client(self):
        client_id = self.id_input.text().strip()   # Зчитуємо ID з поля

        if not client_id:   # Якщо ID не введено
            QMessageBox.warning(self, "Error", "Enter the client ID to delete.")
            return

        client = self.db.find_client(int(client_id))   # Шукаємо клієнта в базі
        if not client:                                  # Якщо не знайдено
            QMessageBox.warning(self, "Error", "No client found with this ID.")
            return

        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Are you sure you want to delete the client:\n{client[1]}?",  # Показуємо ім'я клієнта
            QMessageBox.Yes | QMessageBox.No,   # Кнопки Так / Ні
            QMessageBox.No                      # За замовчуванням — Ні
        )

        if reply == QMessageBox.Yes:                    # Якщо користувач підтвердив
            self.db.delete_client(int(client_id))       # Видаляємо клієнта з бази
            QMessageBox.information(self, "Success", "Client deleted.")
            self.id_input.clear()                       # Очищаємо поле ID
            self.clear_fields()                         # Очищаємо інформаційні поля

    # Метод відкриття діалогу редагування клієнта
    def open_edit_dialog(self):
        client_id = self.id_input.text().strip()   # Зчитуємо ID з поля

        if not client_id:   # Якщо ID не введено
            QMessageBox.warning(self, "Error", "Enter the client ID to edit.")
            return

        client = self.db.find_client(int(client_id))   # Шукаємо клієнта в базі
        if not client:                                  # Якщо не знайдено
            QMessageBox.warning(self, "Error", "No client found with this ID.")
            return

        dialog = EditClientDialog(self.db, client, self)   # Створюємо вікно редагування
        if dialog.exec_():                                  # Якщо редагування успішне
            updated = self.db.find_client(int(client_id))  # Знову зчитуємо оновлені дані
            if updated:
                self.fill_fields(updated)                   # Показуємо оновлені дані у формі


# _________________________ Запуск _______________________________________
if __name__ == "__main__":
    app = QApplication(sys.argv)   # Створюємо об'єкт застосунку PyQt
    window = Autosalon_UI()        # Створюємо головне вікно програми
    window.show()                  # Показуємо головне вікно
    sys.exit(app.exec_())          # Запускаємо головний цикл і коректно завершуємо