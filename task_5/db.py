# Работа с базой данных MySQL: создание таблиц, заполнение, операции с заказами.
import mysql.connector

from config import DB_NAME, DB_CONFIG
from models import Order
from data_gen import (
    generate_customers,
    generate_waiters,
    generate_cafe_tables,
    generate_menu_items,
)


class Database:
    def __init__(self):
        self.cnx = None

    # ---------- подключение / создание базы ----------

    def create_database_if_not_exists(self):
        tmp_cnx = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )
        cursor = tmp_cnx.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME} "
            "DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        cursor.close()
        tmp_cnx.close()

    def connect(self):
        cfg = DB_CONFIG.copy()
        cfg["database"] = DB_NAME
        self.cnx = mysql.connector.connect(**cfg)
        self.cnx.autocommit = False

    def close(self):
        if self.cnx and self.cnx.is_connected():
            self.cnx.close()

    # ---------- служебные методы ----------

    def execute_ddl(self, ddl):
        cursor = self.cnx.cursor()
        cursor.execute(ddl)
        cursor.close()

    def create_tables(self):
        ddls = [
            # порядок важен из-за внешних ключей
            """            CREATE TABLE IF NOT EXISTS customer (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                registered_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB;
            """,
            """            CREATE TABLE IF NOT EXISTS cafe_table (
                id INT AUTO_INCREMENT PRIMARY KEY,
                table_number INT NOT NULL UNIQUE,
                seats INT NOT NULL,
                location ENUM('hall','bar','terrace') NOT NULL DEFAULT 'hall',
                is_active TINYINT(1) NOT NULL DEFAULT 1
            ) ENGINE=InnoDB;
            """,
            """            CREATE TABLE IF NOT EXISTS waiter (
                id INT AUTO_INCREMENT PRIMARY KEY,
                full_name VARCHAR(100) NOT NULL,
                phone VARCHAR(20),
                hire_date DATE NOT NULL,
                is_active TINYINT(1) NOT NULL DEFAULT 1
            ) ENGINE=InnoDB;
            """,
            """            CREATE TABLE IF NOT EXISTS menu_category (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL UNIQUE
            ) ENGINE=InnoDB;
            """,
            """            CREATE TABLE IF NOT EXISTS menu_item (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category_id INT NOT NULL,
                price DECIMAL(8,2) NOT NULL,
                is_active TINYINT(1) NOT NULL DEFAULT 1,
                CONSTRAINT fk_menu_item_category
                    FOREIGN KEY (category_id) REFERENCES menu_category(id)
            ) ENGINE=InnoDB;
            """,
            """            CREATE TABLE IF NOT EXISTS customer_order (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                customer_id INT NOT NULL,
                table_id INT NOT NULL,
                waiter_id INT NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                status ENUM('new','in_progress','served','paid','cancelled')
                    NOT NULL DEFAULT 'new',
                total_amount DECIMAL(10,2) NOT NULL DEFAULT 0,
                CONSTRAINT fk_order_customer
                    FOREIGN KEY (customer_id) REFERENCES customer(id),
                CONSTRAINT fk_order_table
                    FOREIGN KEY (table_id) REFERENCES cafe_table(id),
                CONSTRAINT fk_order_waiter
                    FOREIGN KEY (waiter_id) REFERENCES waiter(id),
                INDEX idx_orders_customer (customer_id),
                INDEX idx_orders_table (table_id),
                INDEX idx_orders_waiter (waiter_id)
            ) ENGINE=InnoDB;
            """,
            """            CREATE TABLE IF NOT EXISTS payment (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                order_id BIGINT NOT NULL UNIQUE,
                amount DECIMAL(10,2) NOT NULL,
                method ENUM('cash','card','online') NOT NULL,
                paid_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_payment_order
                    FOREIGN KEY (order_id) REFERENCES customer_order(id)
            ) ENGINE=InnoDB;
            """,
            """            CREATE TABLE IF NOT EXISTS order_item (
                id BIGINT AUTO_INCREMENT PRIMARY KEY,
                order_id BIGINT NOT NULL,
                menu_item_id INT NOT NULL,
                quantity INT NOT NULL,
                price DECIMAL(8,2) NOT NULL,
                CONSTRAINT fk_order_item_order
                    FOREIGN KEY (order_id) REFERENCES customer_order(id)
                    ON DELETE CASCADE,
                CONSTRAINT fk_order_item_menu
                    FOREIGN KEY (menu_item_id) REFERENCES menu_item(id),
                INDEX idx_order_item_order (order_id),
                INDEX idx_order_item_menu (menu_item_id)
            ) ENGINE=InnoDB;
            """,
        ]
        for ddl in ddls:
            self.execute_ddl(ddl)
        self.cnx.commit()

    def insert_many_one_query(self, table, columns, rows):
        if not rows:
            return
        placeholders_row = "(" + ", ".join(["%s"] * len(columns)) + ")"
        all_placeholders = ", ".join([placeholders_row] * len(rows))
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES {all_placeholders}"
        flat_params = []
        for row in rows:
            for value in row:
                flat_params.append(value)
        cursor = self.cnx.cursor()
        cursor.execute(sql, flat_params)
        self.cnx.commit()
        cursor.close()

    def count_rows(self, table):
        cursor = self.cnx.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        cursor.close()
        return count

    def fetch_random(self, table, columns, limit):
        sql = f"SELECT {', '.join(columns)} FROM {table} ORDER BY RAND() LIMIT %s"
        cursor = self.cnx.cursor()
        cursor.execute(sql, (limit,))
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def get_random_id(self, table):
        cursor = self.cnx.cursor()
        cursor.execute(f"SELECT id FROM {table} ORDER BY RAND() LIMIT 1")
        row = cursor.fetchone()
        cursor.close()
        if row is None:
            raise ValueError(f"В таблице {table} нет данных")
        return row[0]

    # ---------- заполнение начальными данными ----------

    def populate_initial_data(self, amount=1000):
        cursor = self.cnx.cursor()
        cursor.execute("SELECT COUNT(*) FROM menu_category")
        if cursor.fetchone()[0] == 0:
            categories = ["Кофе", "Чай", "Десерты", "Закуски", "Горячие блюда"]
            rows = [(name,) for name in categories]
            self.insert_many_one_query("menu_category", ["name"], rows)
        cursor.close()

        cursor = self.cnx.cursor()
        cursor.execute("SELECT id FROM menu_category")
        category_ids = [row[0] for row in cursor.fetchall()]
        cursor.close()

        if self.count_rows("customer") < amount:
            customers = generate_customers(amount)
            self.insert_many_one_query(
                "customer", ["full_name", "phone", "email"], customers
            )

        if self.count_rows("waiter") < amount:
            waiters = generate_waiters(amount)
            self.insert_many_one_query(
                "waiter", ["full_name", "phone", "hire_date"], waiters
            )

        if self.count_rows("cafe_table") < amount:
            tables = generate_cafe_tables(amount)
            self.insert_many_one_query(
                "cafe_table",
                ["table_number", "seats", "location", "is_active"],
                tables,
            )

        if self.count_rows("menu_item") < amount:
            menu_items = generate_menu_items(amount, category_ids)
            self.insert_many_one_query(
                "menu_item", ["name", "category_id", "price", "is_active"], menu_items
            )

    # ---------- операции с заказами ----------

    def create_order(self, order):
        cursor = self.cnx.cursor()

        cursor.execute("SELECT COUNT(*) FROM customer WHERE id = %s", (order.customer_id,))
        if cursor.fetchone()[0] == 0:
            cursor.close()
            raise ValueError(f"Клиент id={order.customer_id} не найден")

        cursor.execute("SELECT COUNT(*) FROM cafe_table WHERE id = %s", (order.table_id,))
        if cursor.fetchone()[0] == 0:
            cursor.close()
            raise ValueError(f"Столик id={order.table_id} не найден")

        cursor.execute("SELECT COUNT(*) FROM waiter WHERE id = %s", (order.waiter_id,))
        if cursor.fetchone()[0] == 0:
            cursor.close()
            raise ValueError(f"Официант id={order.waiter_id} не найден")

        menu_ids = [item.menu_item_id for item in order.items]
        format_strings = ", ".join(["%s"] * len(menu_ids))
        cursor.execute(
            f"SELECT id, price FROM menu_item WHERE id IN ({format_strings})",
            menu_ids,
        )
        price_map = {}
        for row in cursor.fetchall():
            price_map[row[0]] = float(row[1])

        missing = [mid for mid in menu_ids if mid not in price_map]
        if missing:
            cursor.close()
            raise ValueError(f"Позиции меню не найдены: {missing}")

        cursor.execute(
            """            INSERT INTO customer_order (customer_id, table_id, waiter_id, status, total_amount)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (order.customer_id, order.table_id, order.waiter_id, "new", 0.0),
        )
        order_id = cursor.lastrowid

        rows = []
        total = 0.0
        for item in order.items:
            price = price_map[item.menu_item_id]
            total += price * item.quantity
            rows.append((order_id, item.menu_item_id, item.quantity, price))

        if rows:
            placeholders = "(%s, %s, %s, %s)"
            all_placeholders = ", ".join([placeholders] * len(rows))
            sql = (
                "INSERT INTO order_item "
                "(order_id, menu_item_id, quantity, price) VALUES "
                + all_placeholders
            )
            flat = []
            for row in rows:
                for value in row:
                    flat.append(value)
            cursor.execute(sql, flat)

        cursor.execute(
            "UPDATE customer_order SET total_amount = %s WHERE id = %s",
            (total, order_id),
        )

        self.cnx.commit()
        cursor.close()
        return order_id

    def get_order_info(self, order_id):
        cursor = self.cnx.cursor()
        cursor.execute(
            """            SELECT o.id, c.full_name, ct.table_number, w.full_name, o.created_at,
                   o.status, o.total_amount
            FROM customer_order o
            JOIN customer c ON o.customer_id = c.id
            JOIN cafe_table ct ON o.table_id = ct.id
            JOIN waiter w ON o.waiter_id = w.id
            WHERE o.id = %s
            """,
            (order_id,),
        )
        header = cursor.fetchone()

        cursor.execute(
            """            SELECT m.name, oi.quantity, oi.price
            FROM order_item oi
            JOIN menu_item m ON oi.menu_item_id = m.id
            WHERE oi.order_id = %s
            """,
            (order_id,),
        )
        items = cursor.fetchall()
        cursor.close()
        return header, items
