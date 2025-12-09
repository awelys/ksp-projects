# Генерация случайных данных для заполнения таблиц.

import random
from datetime import date, timedelta

FIRST_NAMES = [
    "Иван", "Петр", "Сергей", "Анна", "Мария",
    "Ольга", "Дмитрий", "Наталья", "Елена", "Алексей",
]

LAST_NAMES = [
    "Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов",
    "Попов", "Васильев", "Соколов", "Михайлов", "Новиков",
]

BASE_DISHES = [
    "Американо", "Капучино", "Эспрессо", "Латте", "Раф",
    "Чай черный", "Чай зеленый", "Чизкейк", "Круассан",
    "Шоколадный торт", "Сэндвич с ветчиной", "Салат Цезарь",
]


def random_full_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def random_phone():
    return "+7" + "".join(random.choice("0123456789") for _ in range(10))


def random_date(start_year=2019, end_year=2024):
    start = date(start_year, 1, 1)
    end = date(end_year, 12, 31)
    delta_days = (end - start).days
    return start + timedelta(days=random.randint(0, delta_days))


def generate_customers(n=1000):
    rows = []
    for i in range(n):
        full_name = random_full_name()
        phone = random_phone()
        email = f"user{i}@example.com"
        rows.append((full_name, phone, email))
    return rows


def generate_waiters(n=1000):
    rows = []
    for _ in range(n):
        full_name = random_full_name()
        phone = random_phone()
        hire = random_date()
        rows.append((full_name, phone, hire))
    return rows


def generate_cafe_tables(n=1000):
    locations = ["hall", "bar", "terrace"]
    rows = []
    for table_number in range(1, n + 1):
        seats = random.randint(2, 6)
        location = random.choice(locations)
        is_active = 1
        rows.append((table_number, seats, location, is_active))
    return rows


def generate_menu_items(n, category_ids):
    rows = []
    for i in range(n):
        base = random.choice(BASE_DISHES)
        name = f"{base} #{i + 1}"
        category_id = random.choice(category_ids)
        price = round(random.uniform(100, 600), 2)
        is_active = 1
        rows.append((name, category_id, price, is_active))
    return rows
