import cmath
import math
import time
import random


def factor_pair(N):
    """Пара множителей p1*p2 = N, ближайшая к sqrt(N) -> минимум N*(p1+p2)."""
    p1 = math.isqrt(N)
    while N % p1:
        p1 -= 1
    return p1, N // p1


# ------------------------------------------------------------------
# 1) Прямое ДПФ "в лоб" по формуле (2.1): трудоёмкость C*N^2
#    A_k = (1/N) * sum_{j=0}^{N-1} exp(-2*pi*i*k*j/N) * f_j
# ------------------------------------------------------------------
def dft_naive(f, counter=None):
    N = len(f)
    A = [0j] * N
    for k in range(N):
        s = 0j
        for j in range(N):
            s += f[j] * cmath.exp(-2j * math.pi * k * j / N)
            if counter is not None:
                counter[0] += 1
        A[k] = s / N
    return A


# ------------------------------------------------------------------
# 2) Полубыстрое преобразование Фурье (ППФ), формулы (2.3а) и (2.3б):
#    N = p1*p2,  k = k1 + p1*k2,  j = j2 + p2*j1,
#    трудоёмкость N*(p1+p2) ~ 2*N^(3/2) при p1 = p2 = sqrt(N)
# ------------------------------------------------------------------
def dft_half_fast(f, p1=None, p2=None, counter=None):
    N = len(f)
    if p1 is None:
        p1, p2 = factor_pair(N)
    assert p1 * p2 == N

    # --- этап 1, формула (2.3а) ------------------------------------
    # A1[k1][j2] = (1/p1) * sum_{j1=0}^{p1-1} f[j2 + p2*j1] * exp(-2*pi*i*j1*k1/p1)
    A1 = [[0j] * p2 for _ in range(p1)]
    for k1 in range(p1):
        for j2 in range(p2):
            s = 0j
            for j1 in range(p1):
                s += f[j2 + p2 * j1] * cmath.exp(-2j * math.pi * j1 * k1 / p1)
                if counter is not None:
                    counter[0] += 1
            A1[k1][j2] = s / p1

    # --- этап 2, формула (2.3б) ------------------------------------
    # A2(k1,k2) = (1/p2) * sum_{j2=0}^{p2-1} A1[k1][j2] * exp(-2*pi*i*j2*(k1+p1*k2)/N)
    A = [0j] * N
    for k1 in range(p1):
        for k2 in range(p2):
            s = 0j
            for j2 in range(p2):
                s += A1[k1][j2] * cmath.exp(-2j * math.pi * j2 * (k1 + p1 * k2) / N)
                if counter is not None:
                    counter[0] += 1
            A[k1 + p1 * k2] = s / p2
    return A


# ------------------------------------------------------------------
# Обратное преобразование по формуле (2.2) -- для контроля:
# тот же код, но exp(+...) и без множителя 1/N (как сказано в лекции)
# ------------------------------------------------------------------
def idft_naive(A):
    N = len(A)
    f = [0j] * N
    for k in range(N):
        s = 0j
        for j in range(N):
            s += A[j] * cmath.exp(+2j * math.pi * k * j / N)
        f[k] = s
    return f


if __name__ == "__main__":
    random.seed(2026)
    print(f"{'N':>6} | {'p1 x p2':>8} | {'опер. N^2':>10} | {'опер. ППФ':>10} | "
          f"{'t наивное':>9} | {'t ППФ':>8} | {'max|разниц|':>11}")
    for N in (64, 256, 1024):
        f = [random.random() for _ in range(N)]
        p1, p2 = factor_pair(N)

        c1 = [0]; t0 = time.perf_counter()
        A_naive = dft_naive(f, c1)
        t1 = time.perf_counter()

        c2 = [0]
        A_fast = dft_half_fast(f, p1, p2, c2)
        t2 = time.perf_counter()

        err = max(abs(a - b) for a, b in zip(A_naive, A_fast))
        f_back = idft_naive(A_fast)
        assert max(abs(x - y) for x, y in zip(f, f_back)) < 1e-9

        print(f"{N:>6} | {p1:>3} x {p2:<3} | {c1[0]:>10} | {c2[0]:>10} | "
              f"{t1-t0:>8.4f}s | {t2-t1:>7.4f}s | {err:>11.2e}")