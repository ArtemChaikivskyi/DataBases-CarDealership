# DataBases CarDealership 🚗

Настільний застосунок автосалону «Elite Motors»: вікно авторизації та графічний
інтерфейс для роботи з базою даних клієнтів. Написаний на **Python + PyQt5**,
дані зберігаються у **SQLite**.

> Навчальний проєкт. Інтерфейс зібраний вручну у коді; `.ui`-файли — це вихідні
> макети з Qt Designer і під час запуску не використовуються.

## Можливості

- 🔐 Вхід за логіном і паролем (`admin` / `1234`)
- 🔎 Пошук клієнта за `id`
- ➕ Додавання клієнта (`id`, ім'я, телефон, email)
- ✏️ Редагування даних клієнта
- 🗑️ Видалення клієнта
- 🗄️ Зберігання у локальному файлі `databases.db`

База також містить наповнені таблиці `Cars`, `Employees`, `Sales` — їх створює й
заповнює скрипт `DataBases_Car.py` (CRUD в інтерфейсі працює з таблицею `Clients`).

## Стек

| Компонент | Призначення |
|---|---|
| Python 3.12 | мова, фіксується через `.python-version` |
| PyQt5 | графічний інтерфейс |
| SQLite (`sqlite3`) | вбудована БД, файл `databases.db` |
| uv | керування залежностями та середовищем |

## Запуск

Потрібен [uv](https://docs.astral.sh/uv/). Він сам створить `.venv`, візьме
Python 3.12 і встановить залежності з `pyproject.toml` / `uv.lock`.

```bash
uv run python Login_base.py
```

Відкриється вікно входу → після `admin` / `1234` з'явиться головне вікно.

Головне вікно напряму, без авторизації:

```bash
uv run python Elite_Motors.py
```

### Створити базу даних

Створює таблиці у `databases.db`, якщо їх немає, і додає тестові записи:

```bash
uv run python DataBases_Car.py
```

### Без uv

```bash
pip install "PyQt5>=5.15"
python Login_base.py
```

## Структура

```
Login_base.py            # Точка входу: логіка авторизації
Login.py                 # Згенерований клас вікна входу (Ui_Form)
Elite_Motors.py          # Головне вікно + шар роботи з БД (AutosalonDatabase)
DataBases_Car.py         # Створення та наповнення databases.db
databases.db             # Файл бази даних SQLite
*.ui                     # Вихідні макети Qt Designer (довідково)
Form_Login.qrc           # Файл ресурсів Qt
Car1.jpeg, car2.png      # Фонові зображення інтерфейсу
```

### Таблиці

| Таблиця | Поля |
|---|---|
| `Clients` | `id`, `name`, `telephone`, `email` |
| `Cars` | `id`, `brand`, `model`, `prise` |
| `Employees` | `id`, `name`, `telephone` |
| `Sales` | `client_id`, `car_id`, `employee_id`, `date` |

## Автор

**Artem Chaikivskyi** — [@ArtemChaikivskyi](https://github.com/ArtemChaikivskyi)

Створено в навчальних цілях.
