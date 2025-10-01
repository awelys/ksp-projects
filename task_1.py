import random

random_number = random.randint(1, 20)
entered_number = 0
attempts = 0
while random_number != entered_number:
    print('Введите число от 1 до 20')
    entered_number = int(input())
    attempts += 1
print(f'Ура! Вы отгадали число за {attempts} попыток!')