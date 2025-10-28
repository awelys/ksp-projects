import argparse
from abc import ABC, abstractmethod

class Order:
    def __init__(self, number):
        self.number = number

class User(ABC):
    def __init__(self, lastname, firstname, telephone, address):
        self.lastname = lastname
        self.firstname = firstname
        self.telephone = telephone
        self.address = address

    @abstractmethod
    def create(self):
        pass


class Employee(User):
    def __init__(self, lastname, firstname, telephone, address, position, salary):
        super().__init__(lastname, firstname, telephone, address)
        self.position = position
        self.salary = salary

    def create(self):
        with open('users.txt', 'a', encoding='utf-8') as file:
            file.write(str({
                'lastname': self.lastname,
                'firstname': self.firstname,
                'telephone': self.telephone,
                'address': self.address,
                'position': self.position,
                'salary': self.salary
            }) + '\n')

class Client(User):
    def __init__(self, lastname, firstname, telephone, address, order):
        super().__init__(lastname, firstname, telephone, address)
        self.order = order

    def create(self):
        with open('users.txt', 'a', encoding='utf-8') as file:
            file.write(str({
                'lastname': self.lastname,
                'firstname': self.firstname,
                'telephone': self.telephone,
                'address': self.address,
                'order': self.order.number
            }) + '\n')

# Основной класс сценариев
class CScenario:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Модуль создания пользователей")
        self.parser.add_argument('-mode', choices=['auto', 'handle'], required=True, help='Режим работы')
        self.parser.add_argument('-type', choices=['employee', 'client'], required=True, help='Тип пользователя')
        self.parser.add_argument('-lastname', help='Фамилия')
        self.parser.add_argument('-firstname', help='Имя')
        self.parser.add_argument('-telephone', help='Телефон')
        self.parser.add_argument('-address', help='Адрес')
        self.parser.add_argument('-position', help='Должность')
        self.parser.add_argument('-salary', help='Зарплата')
        self.parser.add_argument('-order', help='Номер заказа')

    def run(self):
        args = self.parser.parse_args()

        if args.mode == 'auto':
            print("Автоматический сценарий создания пользователя")
            order = Order("auto-order-001")
            emp = Employee("Иванов", "Иван", "+79991234567", "Москва", "инженер", "50000")
            emp.create()
            client = Client("Петров", "Петр", "+79997654321", "Казань", order)
            client.create()
            print("Созданы тестовые Employee и Client (auto)")

        elif args.mode == 'handle':
            # Проверка на обязательные аргументы
            required_fields = ['lastname', 'firstname', 'telephone', 'address']
            for field in required_fields:
                if getattr(args, field) is None:
                    print(f"Ошибка: параметр -{field} обязателен для режима handle")
                    return

            if args.type == 'employee':
                if not args.position or not args.salary:
                    print("Ошибка: для employee нужны -position и -salary")
                    return
                emp = Employee(args.lastname, args.firstname, args.telephone,
                               args.address, args.position, args.salary)
                emp.create()
                print("Создан Employee:", args.firstname, args.lastname)

            elif args.type == 'client':
                if not args.order:
                    print("Ошибка: для client нужен -order")
                    return
                order = Order(args.order)
                client = Client(args.lastname, args.firstname, args.telephone,
                                args.address, order)
                client.create()
                print("Создан Client:", args.firstname, args.lastname)

# Точка входа
if __name__ == '__main__':
    scenario = CScenario()
    scenario.run()
