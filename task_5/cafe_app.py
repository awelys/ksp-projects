# Точка входа: CLI-интерфейс для работы с системой кафе
import argparse
from db import Database
from services import CafeService
from utils import parse_items_arg


def main():
    parser = argparse.ArgumentParser(
        description="Система обслуживания клиентов в кафе (Python + MySQL)"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init-db
    subparsers.add_parser(
        "init-db",
        help="Создать БД, таблицы и заполнить основными таблицами по 1000 записей",
    )

    # list-customers
    p_lc = subparsers.add_parser(
        "list-customers", help="Вывести случайных клиентов"
    )
    p_lc.add_argument("--limit", type=int, default=20, help="Сколько клиентов вывести")

    # list-menu
    p_lm = subparsers.add_parser(
        "list-menu", help="Вывести случайные позиции меню"
    )
    p_lm.add_argument("--limit", type=int, default=20, help="Сколько позиций вывести")

    # create-order
    p_co = subparsers.add_parser(
        "create-order",
        help=(
            "Создать заказ: требуется id клиента, id столика "
            "и список блюд формата 'menu_id:qty,menu_id:qty'"
        ),
    )
    p_co.add_argument("--customer-id", type=int, required=True, help="ID клиента")
    p_co.add_argument("--table-id", type=int, required=True, help="ID столика")
    p_co.add_argument("--items", type=str, required=True, help="Например: --items '10:2,15:1'",
    )

    args = parser.parse_args()

    if args.command == "init-db":
        db = Database()
        db.create_database_if_not_exists()
        db.connect()
        db.create_tables()
        db.populate_initial_data(amount=1000)
        db.close()
        print("База данных создана и заполнена начальными данными.")
        return

    db = Database()
    db.connect()
    service = CafeService(db)

    try:
        if args.command == "list-customers":
            service.show_random_customers(limit=args.limit)
        elif args.command == "list-menu":
            service.show_random_menu_items(limit=args.limit)
        elif args.command == "create-order":
            items_map = parse_items_arg(args.items)
            service.create_order_cli(
                customer_id=args.customer_id,
                table_id=args.table_id,
                items_map=items_map,
            )
    except Exception as exc:
        print("Ошибка:", exc)
    finally:
        db.close()


if __name__ == "__main__":
    main()
