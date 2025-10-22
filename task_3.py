import random
import time

# --- Функции для генерации лабиринта ---

def create_initial_grid(width, height):
    grid = [[empty_char for _ in range(width)] for _ in range(height)]

    for y in range(height):
        for x in range(width):
            if y == 0 or y == height - 1 or x == 0 or x == width - 1:
                grid[y][x] = wall_char
    return grid


def display_maze(grid, step_count, wall_info=""):
    if wall_info:
        print(f"Шаг: {step_count} - {wall_info}")
    else:
        print(f"Шаг: {step_count}")

    for row in grid:
        print(" ".join(row))
    print("\n")
    time.sleep(delay)


def recursive_division(grid, x, y, width, height, step_counter):
    # условие остановки рекурсии
    if width < 3 or height < 3:
        return

    is_horizontal = width < height
    if width == height:
        is_horizontal = random.choice([True, False])

    if not is_horizontal:
        # вертикальное деление
        possible_wall_xs = range(x + 1, x + width - 1, 2)
        if not possible_wall_xs: return
        wall_x = random.choice(possible_wall_xs)

        # случайный проход с нечетной у координатой
        possible_passage_ys = range(y, y + height, 2)
        if not possible_passage_ys: return
        passage_y = random.choice(possible_passage_ys)

        # построение стены
        for i in range(y, y + height):
            if i != passage_y:
                grid[i][wall_x] = wall_char

        step_counter[0] += 1
        wall_info = f"Вертикальная стена: x={wall_x}, проход: y={passage_y}"
        display_maze(grid, step_counter[0], wall_info)

        # Левая под-область
        recursive_division(grid, x, y, wall_x - x, height, step_counter)
        # Правая под-область
        recursive_division(grid, wall_x + 1, y, width - (wall_x - x) - 1, height, step_counter)

    else:
        # горизонтальное деление

        possible_wall_ys = range(y + 1, y + height - 1, 2)
        if not possible_wall_ys: return
        wall_y = random.choice(possible_wall_ys)

        # проход с нечетной х координатой
        possible_passage_xs = range(x, x + width, 2)
        if not possible_passage_xs: return
        passage_x = random.choice(possible_passage_xs)

        # построение стены
        for i in range(x, x + width):
            if i != passage_x:
                grid[wall_y][i] = wall_char

        step_counter[0] += 1
        display_maze(grid, step_counter[0])

        # верхняя под-область
        recursive_division(grid, x, y, width, wall_y - y, step_counter)
        # нижняя под-область
        recursive_division(grid, x, wall_y + 1, width, height - (wall_y - y) - 1, step_counter)


if __name__ == "__main__":
    maze_width = 27
    maze_height = 15

    wall_char = '█'
    empty_char = ' '
    delay = 0.1

    maze = create_initial_grid(maze_width, maze_height)

    step_count = [0]
    display_maze(maze, step_count[0])
    recursive_division(maze, 1, 1, maze_width - 2, maze_height - 2, step_count)
