├── cafe_app.py        # Главная точка входа (CLI)
├── config.py          # Конфигурация подключения к MySQL
├── db.py              # Работа с базой данных
├── services.py        # Логика интерфейса: вывод меню, клиентов, создание заказов
├── utils.py           # Парсер аргумента --items
├── models.py          # Классы Order и OrderItemData (без dataclass)
├── data_gen.py        # Генерация случайных данных
└── schema.sql         # SQL-схема БД (ручной вариант)



Основные связи:
* customer → customer_order (1:M)
* waiter → customer_order (1:M)
* cafe_table → customer_order (1:M)
* menu_category → menu_item (1:M)
* customer_order → order_item (1:M)
* menu_item → order_item (1:M)
* customer_order ↔ menu_item (M:N через order_item)
* customer_order ↔ payment (1:1 по UNIQUE order_id)

**Создание БД**
python cafe_app.py init-db

**Показать случайных клиентов**
python cafe_app.py list-customers --limit 10

**Показать случайные позиции меню**
python cafe_app.py list-menu --limit 10

**Создать заказ клиента**
python cafe_app.py create-order --customer-id 5 --table-id 3 --items "10:2,15:1"
