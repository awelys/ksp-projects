# Простые классы для описания заказа и строки заказа (без dataclass).
class OrderItemData:
    def __init__(self, menu_item_id, quantity, price):
        self.menu_item_id = menu_item_id
        self.quantity = quantity
        self.price = price


class Order:
    def __init__(self, customer_id, table_id, waiter_id, items):
        # items — список объектов OrderItemData
        self.customer_id = customer_id
        self.table_id = table_id
        self.waiter_id = waiter_id
        self.items = items

    @property
    def total_amount(self):
        total = 0.0
        for item in self.items:
            total += item.price * item.quantity
        return total
