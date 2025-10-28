import string

def caesar_cipher(text, shift):
    result = []
    for ch in text:
        if ch.isalpha():
            if ch.islower():
                alphabet = string.ascii_lowercase
            else:
                alphabet = string.ascii_uppercase
            new_index = (alphabet.index(ch) + shift) % 26
            result.append(alphabet[new_index])
        else:
            result.append(ch)
    return "".join(result)


def encrypt(text, k, m):
    print("Исходная строка:", text)

    # 1. Разбиваем строку на слова
    words = text.split()
    print("Список слов:", words)

    # 2. Переворачиваем список слов
    words.reverse()
    print("После реверса слов:", words)

    # 3. Циклический сдвиг вправо на k
    k = k % len(words)
    words = words[-k:] + words[:-k]
    print(f"После циклического сдвига на {k}:", words)

    # 4. Меняем первую и последнюю букву
    swapped_words = []
    for w in words:
        if len(w) > 1:
            w = w[-1] + w[1:-1] + w[0]
        swapped_words.append(w)
    print("После обмена первой и последней буквы:", swapped_words)

    # 5. Шифр Цезаря
    caesar_words = [caesar_cipher(w, m) for w in swapped_words]
    print(f"После шифра Цезаря (m={m}):", caesar_words)

    # 6. Собираем обратно в строку
    encrypted_text = " ".join(caesar_words)
    print("Зашифрованная строка:", encrypted_text)

    # 7. Сначала берем уникальные символы и потом преобразовываем в словарь
    unique_chars = list(dict.fromkeys(encrypted_text))
    char_to_num = {ch: str(100 + i) for i, ch in enumerate(unique_chars)}
    print("Словарь символов:", char_to_num)

    # 8. Преобразовываем строку в числа
    number_text = "".join(char_to_num[ch] for ch in encrypted_text)
    print("Строка в виде чисел:", number_text)

    return encrypted_text, number_text, char_to_num


def decrypt(number_text, char_to_num, k, m):
    print("\n=== ДЕШИФРОВКА ===")

    # 1. Обратный словарь: число в символ
    num_to_char = {v: k for k, v in char_to_num.items()}

    # Разбиваем числовую строку по 3 цифры
    chars = [num_to_char[number_text[i:i+3]] for i in range(0, len(number_text), 3)]
    decoded_text = "".join(chars)
    print("Из чисел обратно в символы:", decoded_text)

    # 2. Разбить строку на слова
    words = decoded_text.split()
    print("Список слов:", words)

    # 3. Обратный шифр Цезаря (сдвиг -m)
    caesar_words = [caesar_cipher(w, -m) for w in words]
    print(f"После обратного шифра Цезаря (m={m}):", caesar_words)

    # 4. Меняем первую и последнюю букву обратно
    swapped_back = []
    for w in caesar_words:
        if len(w) > 1:
            w = w[-1] + w[1:-1] + w[0]
        swapped_back.append(w)
    print("После обратного обмена букв:", swapped_back)

    # 5. Обратный циклический сдвиг (влево на k)
    k = k % len(swapped_back)
    words_shifted = swapped_back[k:] + swapped_back[:k]
    print(f"После обратного сдвига на {k}:", words_shifted)

    # 6. Перевернуть список обратно
    words_shifted.reverse()
    print("После обратного реверса:", words_shifted)

    # 7. Собираем строку
    original_text = " ".join(words_shifted)
    print("Расшифрованная строка:", original_text)
    return original_text

# Запуск программы
text = "I need Help!"
k = 1
m = 2
encrypted_text, number_text, dictionary = encrypt(text, k, m)
decrypted_text = decrypt(number_text, dictionary, k, m)
