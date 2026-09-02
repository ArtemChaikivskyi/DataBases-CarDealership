# DataBases CarDealership 🚗

Настільний додаток для управління базою даних автосалону, розроблений на Python з використанням PyQt (Qt Designer) та SQLite.

## Опис

Проєкт реалізує систему обліку автомобілів автосалону з графічним інтерфейсом користувача: авторизація, перегляд, додавання та редагування записів про автомобілі.

## Функціонал

- 🔐 Авторизація користувача (вікно логіну)
- 📋 Перегляд списку автомобілів у базі даних
- ➕ Додавання нового запису про автомобіль
- ✏️ Редагування існуючого запису
- 🗄️ Зберігання даних у локальній базі даних SQLite

## Технології

- **Python 3**
- **PyQt** — графічний інтерфейс (файли `.ui`, згенеровані у Qt Designer)
- **SQLite** — зберігання даних (`databases.db`)

## Структура проєкту

```
├── Elite_Motors.py          # Головний модуль додатку
├── Login.py                 # Логіка вікна авторизації
├── Login_base.py            # Базовий клас логіну
├── DataBases_Car.py         # Робота з базою даних
├── Frame1-Elite_Motors.ui   # UI головного вікна
├── Frame2-AddEntry.ui       # UI вікна додавання запису
├── Frame3-EditEntry.ui      # UI вікна редагування запису
├── Login.ui                 # UI вікна авторизації
├── Form_Login.qrc           # Файл ресурсів Qt
├── databases.db             # Файл бази даних SQLite
└── README.md
```

## Встановлення та запуск

1. Клонуйте репозиторій:
```bash
git clone https://github.com/ArtemChaikivskyi/DataBases-CarDealership.git
cd DataBases-CarDealership
```

2. Запустіть додаток через [uv](https://docs.astral.sh/uv/) (сам створить `.venv`,
   візьме Python 3.12 і встановить залежності з `pyproject.toml` / `uv.lock`):
```bash
uv run python Login.py
```

Головне вікно без авторизації:
```bash
uv run python Elite_Motors.py
```

### Без uv
```bash
pip install "PyQt5>=5.15"
python Login.py
```

## Автор

**Artem Chaikivskyi**
GitHub: [@ArtemChaikivskyi](https://github.com/ArtemChaikivskyi)

## Ліцензія

Цей проєкт створено в навчальних цілях.
