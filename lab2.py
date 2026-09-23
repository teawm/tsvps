import random

# ==========================================================
# Задача 1: Лестница
# ==========================================================

def generate_stairs(n=25, min_value=-100, max_value=50):
    return [random.randint(min_value, max_value) for _ in range(n)]


def solve_stairs(values, must_start_first=False):
    n = len(values)

    if n == 0:
        return 0, []

    dp = [0] * (n + 1)

    parent = [0] * (n + 1)

    if must_start_first:
        dp[1] = values[0]
        parent[1] = 0

        if n >= 2:
            dp[2] = dp[1] + values[1]
            parent[2] = 1

        start = 3
    else:
        start = 1

    for i in range(start, n + 1):
        best_prev_sum = dp[i - 1]
        best_prev_step = i - 1

        if i >= 2 and dp[i - 2] > best_prev_sum:
            best_prev_sum = dp[i - 2]
            best_prev_step = i - 2

        dp[i] = best_prev_sum + values[i - 1]
        parent[i] = best_prev_step

    path = []
    current = n

    while current > 0:
        path.append(current)
        current = parent[current]

    path.reverse()

    return dp[n], path


# ==========================================================
# Задача 2: Рюкзак
# ==========================================================

def generate_knapsack_instance(
    capacity_min=25,
    capacity_max=50,
    items_min=5,
    items_max=25,
    weight_max=50,
    value_max=100
):
    capacity = random.randint(capacity_min, capacity_max)
    items_count = random.randint(items_min, items_max)

    items = []
    for _ in range(items_count):
        weight = random.randint(1, weight_max)
        value = random.randint(1, value_max)
        items.append((weight, value))

    return capacity, items


def solve_knapsack_01(capacity, items):
    n = len(items)

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        weight, value = items[i - 1]

        for c in range(capacity + 1):
            dp[i][c] = dp[i - 1][c]

            if weight <= c:
                candidate = dp[i - 1][c - weight] + value

                if candidate > dp[i][c]:
                    dp[i][c] = candidate

    chosen_items = []
    c = capacity

    for i in range(n, 0, -1):
        if dp[i][c] != dp[i - 1][c]:
            chosen_items.append(i)
            c -= items[i - 1][0]

    chosen_items.reverse()

    total_weight = sum(items[idx - 1][0] for idx in chosen_items)
    best_value = dp[n][capacity]

    return best_value, total_weight, chosen_items


# ==========================================================
# Запуск и вывод результатов
# ==========================================================

if __name__ == "__main__":

    # ---------------- Лестница ----------------
    print("=== Задача 1: Лестница ===")

    stairs_values = generate_stairs(n=25, min_value=-100, max_value=50)

    best_sum, path = solve_stairs(stairs_values, must_start_first=False)

    print("Числа на ступеньках:")
    print(stairs_values)

    print("Максимальная сумма:", best_sum)
    print("Номера ступеней пути:", path)
    print("Собранные значения:", [stairs_values[i - 1] for i in path])
    print("Сумма по пути:", sum(stairs_values[i - 1] for i in path))

    print()

    # ---------------- Рюкзак ----------------
    print("=== Задача 2: Рюкзак")

    capacity, items = generate_knapsack_instance()

    best_value, total_weight, chosen_items = solve_knapsack_01(capacity, items)

    print("Вместимость рюкзака:", capacity)
    print("Список товаров: (вес, стоимость)")

    for i, item in enumerate(items, start=1):
        weight, value = item
        print(f"Товар {i:2d}: вес = {weight:2d}, стоимость = {value:3d}")

    print()
    print("Максимальная стоимость:", best_value)
    print("Суммарный вес выбранных товаров:", total_weight)
    print("Номера выбранных товаров:", chosen_items)

    print("Выбранные товары:")
    for idx in chosen_items:
        weight, value = items[idx - 1]
        print(f"Товар {idx}: вес = {weight}, стоимость = {value}")