# Бизнес-логика: вывод клиентов, меню, создание заказа через CLI.

from models import Order, OrderItemData


class CafeService:
    def __init__(self, db):
        self.db = db

    def show_random_customers(self, limit=20):
        rows = self.db.fetch_random(
            "customer", ["id", "full_name", "phone", "email"], limit
        )
        print("Случайные клиенты:")
        print("id	ФИО		Телефон		Email")
        for r in rows:
            print(f"{r[0]}	{r[1]}	{r[2]}	{r[3]}")

    def show_random_menu_items(self, limit=20):
        rows = self.db.fetch_random("menu_item", ["id", "name", "price"], limit)
        print("Случайные позиции меню:")
        print("id	Название	Цена")
        for r in rows:
            print(f"{r[0]}	{r[1]}	{r[2]:.2f} руб.")

    def create_order_cli(self, customer_id, table_id, items_map):
        waiter_id = self.db.get_random_id("waiter")
        items = []
        for menu_item_id, qty in items_map.items():
            items.append(OrderItemData(menu_item_id, qty, 0.0))

        order = Order(customer_id, table_id, waiter_id, items)
        order_id = self.db.create_order(order)
        header, order_items = self.db.get_order_info(order_id)

        print("\nЗаказ успешно создан!")
        print(f"Номер заказа: {header[0]}")
        print(f"Клиент: {header[1]}")
        print(f"Столик №: {header[2]}")
        print(f"Официант: {header[3]}")
        print(f"Дата/время: {header[4]}")
        print(f"Статус: {header[5]}")
        print("Позиции заказа:")
        for name, qty, price in order_items:
            print(f"- {name} x{qty} по {price:.2f} руб.")
        print(f"Итого: {header[6]:.2f} руб.\n")
