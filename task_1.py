import random

random_number = random.randint(1, 20)
entered_number = 0
attempts = 0
while random_number != entered_number:
    print('Введите число от 1 до 20')
    attempts += 1
    try:
        entered_number = int(input())
    except:
        attempts -= 1
        entered_number = 0
        print("Введите правильно число")
print(f'Ура! Вы отгадали число за {attempts} попыток!')