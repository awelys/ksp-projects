import random


def create_labyrinth(width, height):
    # Создаем поле, заполненное пробелами
    maze = [[" " for _ in range(width)] for _ in range(height)]

    # Рисуем рамку
    for x in range(width):
        maze[0][x] = "#"
        maze[height - 1][x] = "#"
    for y in range(height):
        maze[y][0] = "#"
        maze[y][width - 1] = "#"

    # Запускаем рекурсивное деление
    divide(maze, 1, 1, width - 2, height - 2)

    # Печатаем лабиринт
    for row in maze:
        print("".join(row))


def divide(maze, x, y, width, height):
    # Минимальный размер области
    if width < 3 or height < 3:
        return

    # Выбираем направление: True = горизонтально, False = вертикально
    horizontal = random.choice([True, False])

    if horizontal:
        # --- Горизонтальная стена ---
        # Координата стены (чётная)
        wall_y = y + random.randrange(0, height // 2) * 2
        if wall_y >= y + height - 1:
            return
        # Проход (нечётная координата)
        passage_x = x + random.randrange(0, width // 2) * 2 + 1

        for i in range(x, x + width):
            if i == passage_x:
                continue
            maze[wall_y][i] = "#"

        # Рекурсивно делим две части
        divide(maze, x, y, width, wall_y - y)
        divide(maze, x, wall_y + 1, width, y + height - wall_y - 1)

    else:
        # --- Вертикальная стена ---
        wall_x = x + random.randrange(0, width // 2) * 2
        if wall_x >= x + width - 1:
            return
        passage_y = y + random.randrange(0, height // 2) * 2 + 1

        for i in range(y, y + height):
            if i == passage_y:
                continue
            maze[i][wall_x] = "#"

        # Рекурсивно делим две части
        divide(maze, x, y, wall_x - x, height)
        divide(maze, wall_x + 1, y, x + width - wall_x - 1, height)


# Пример запуска
create_labyrinth(21, 15)