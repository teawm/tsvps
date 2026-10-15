import random
import time
INF = float('inf')

# ---------------- 4.3 Задача грабителя (неограниченный рюкзак) ----------------
def knapsack(m, c, M, trace=False, counter=None):
    """f(M) = max_{i: m_i <= M} ( f(M - m_i) + c_i );  T = M*k (m шагов по k товаров)."""
    k = len(m)
    f = [0] * (M + 1)
    choice = [-1] * (M + 1)                     # для восстановления ответа
    for cap in range(1, M + 1):
        best, bi, cands = 0, -1, []
        for i in range(k):
            if counter is not None: counter[0] += 1
            if m[i] <= cap:
                val = f[cap - m[i]] + c[i]
                cands.append(f"f({cap}-{m[i]})+{c[i]}={val}")
                if val > best:
                    best, bi = val, i
        f[cap] = best
        choice[cap] = bi
        if trace:
            print(f"  f({cap})={best:<3}" + (f" = max( {'; '.join(cands)} )" if cands
                                             else "  (ни один товар не помещается)"))
    items, cap = [], M
    while cap > 0 and choice[cap] >= 0:         # восстановление набора
        i = choice[cap]
        items.append(i + 1)
        cap -= m[i]
    return f[M], items, f

# ---------------- 4.4 Оптимальная расстановка скобок ----------------
def matrix_chain(r, trace=False, counter=None):
    """f(k,p) = min_{k<=j<p} ( f(k,j) + f(j+1,p) + r[k-1]*r[j]*r[p] );  T = C*n^3."""
    n = len(r) - 1                              # r_i - размерности: M_i имеет размер r[i-1] x r[i]
    f = [[0] * (n + 2) for _ in range(n + 2)]
    split = [[0] * (n + 2) for _ in range(n + 2)]
    for t in range(1, n):                       # t - длина блока: заполнение по диагоналям
        for k in range(1, n - t + 1):
            p = k + t
            best, bj, cands = INF, -1, []
            for j in range(k, p):
                if counter is not None: counter[0] += 1
                val = f[k][j] + f[j + 1][p] + r[k - 1] * r[j] * r[p]
                cands.append(f"j={j}: {val}")
                if val < best:
                    best, bj = val, j
            f[k][p], split[k][p] = best, bj
            if trace:
                print(f"  f({k},{p}) = {best:<6} min( {'; '.join(cands)} ) -> j={bj}")
    def build(k, p):                            # восстановление скобок
        if k == p:
            return f"M{k}"
        j = split[k][p]
        return f"({build(k, j)}*{build(j + 1, p)})"
    return f[1][n], build(1, n), f

# ---------------- прямой перебор для сверки ----------------
def brute_knapsack(m, c, M):
    best = 0
    def rec(i, mass, val):
        nonlocal best
        if val > best: best = val
        for j in range(i, len(m)):              # j от i: товар можно брать повторно
            if mass + m[j] <= M:
                rec(j, mass + m[j], val + c[j])
    rec(0, 0, 0)
    return best

def brute_chain(r, k, p):
    if k == p:
        return 0
    return min(brute_chain(r, k, j) + brute_chain(r, j + 1, p) + r[k - 1] * r[j] * r[p]
               for j in range(k, p))

# ---------------- демонстрация ----------------
if __name__ == "__main__":
    # рюкзак: пример методички
    m, c, M = [3, 5, 8], [8, 14, 23], 13
    print(f"Рюкзак (пример методички): m={m}, c={c}, M={M}")
    val, items, f = knapsack(m, c, M, trace=True)
    mass = sum(m[i - 1] for i in items)
    print(f"  ответ: стоимость {val}, набор {items}, масса {mass} <= {M}")
    print(f"  сверка с перебором: {val == brute_knapsack(m, c, M)}\n")
    
    # матрицы: пример методички
    r = [10, 20, 50, 1, 100]
    print("Матрицы (пример методички): " + ", ".join(f"M{i+1}[{r[i]}x{r[i+1]}]" for i in range(4)))
    cost, paren, F = matrix_chain(r, trace=True)
    print(f"  оптимальная расстановка: {paren}, трудоёмкость {cost}")
    print(f"  сверка с перебором: {cost == brute_chain(r, 1, 4)}\n")
    
    # трудоёмкость
    random.seed(2026)
    print("Трудоёмкость:")
    for Mb in (1000, 4000, 16000):
        mm = [random.randint(3, 20) for _ in range(5)]
        cc = [random.randint(5, 40) for _ in range(5)]
        cnt = [0]; t0 = time.perf_counter()
        knapsack(mm, cc, Mb, counter=cnt); t1 = time.perf_counter()
        print(f"  рюкзак:  M={Mb:>6}, k=5 -> операций {cnt[0]:>7} (=M*k), t={t1-t0:.3f}s")
    for n in (40, 80, 160):
        rr = [random.randint(1, 50) for _ in range(n + 1)]
        cnt = [0]; t0 = time.perf_counter()
        matrix_chain(rr, counter=cnt); t1 = time.perf_counter()
        print(f"  матрицы: n={n:>4}        -> операций {cnt[0]:>8} (~n^3/6), t={t1-t0:.3f}s")
    ok1 = brute_knapsack([4, 7, 9], [5, 11, 13], 60) == knapsack([4, 7, 9], [5, 11, 13], 60)[0]
    r7 = [random.randint(1, 30) for _ in range(8)]
    ok2 = matrix_chain(r7)[0] == brute_chain(r7, 1, 7)
    print(f"  сверка ДП с перебором на случайных: рюкзак {ok1}, матрицы(n=7) {ok2}")