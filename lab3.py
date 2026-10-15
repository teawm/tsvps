import random
import time

BASE = 10
CUTOFF = 64          

def trim(x):
    while len(x) > 1 and x[-1] == 0:
        x.pop()
    return x

def to_digits(v):
    d = []
    while v:
        d.append(v % BASE)
        v //= BASE
    return d or [0]

def from_digits(d):
    v = 0
    for x in reversed(d):
        v = v * BASE + x
    return v

def add(u, v, cnt):
    if len(u) < len(v):
        u, v = v, u
    n, m = len(u), len(v)
    res = [0] * (n + 1)
    carry = 0
    for i in range(m):
        s = u[i] + v[i] + carry
        cnt[0] += 1
        if s >= BASE:
            res[i] = s - BASE
            carry = 1
        else:
            res[i] = s
            carry = 0
    i = m
    while carry and i < n:                
        s = u[i] + 1
        cnt[0] += 1
        if s >= BASE:
            res[i] = 0
        else:
            res[i] = s
            carry = 0
        i += 1
    while i < n:
        res[i] = u[i]
        i += 1
    res[n] = carry                        
    return trim(res)

def sub(u, v, cnt):                       
    n, m = len(u), len(v)
    res = [0] * n
    borrow = 0
    for i in range(m):
        d = u[i] - v[i] - borrow
        cnt[0] += 1
        if d < 0:
            res[i] = d + BASE
            borrow = 1
        else:
            res[i] = d
            borrow = 0
    i = m
    while borrow and i < n:               
        d = u[i] - 1
        cnt[0] += 1
        if d < 0:
            res[i] = BASE - 1
        else:
            res[i] = d
            borrow = 0
        i += 1
    while i < n:
        res[i] = u[i]
        i += 1
    return trim(res)

def shift(u, k):
    return [0] * k + u

def mul_column(u, v, cnt):
    n, m = len(u), len(v)
    acc = [0] * (n + m)
    for i in range(n):
        ui, carry = u[i], 0
        for j in range(m):
            carry, acc[i + j] = divmod(acc[i + j] + ui * v[j] + carry, BASE)
            cnt[0] += 1
        k = i + m
        while carry:
            carry, acc[k] = divmod(acc[k] + carry, BASE)
            cnt[0] += 1
            k += 1
    return trim(acc)

def mul_fast(u, v, cnt):
    u, v = trim(list(u)), trim(list(v))
    n = max(len(u), len(v))
    if n <= CUTOFF:
        return mul_column(u, v, cnt)

    u += [0] * (n - len(u))
    v += [0] * (n - len(v))
    k = n // 2
    a, b = u[k:], u[:k]                   
    c, d = v[k:], v[:k]                   

    s1 = add(a, b, cnt)                   
    s2 = add(c, d, cnt)                   
    uu = mul_fast(s1, s2, cnt)            
    vv = mul_fast(a, c, cnt)              
    ww = mul_fast(b, d, cnt)              
    mid = sub(sub(uu, vv, cnt), ww, cnt)  
    return add(add(shift(vv, 2 * k), shift(mid, k), cnt), ww, cnt)

if __name__ == "__main__":
    x, y = 1234567, 7654321
    c = [0]; r1 = from_digits(mul_column(to_digits(x), to_digits(y), c))
    c = [0]; r2 = from_digits(mul_fast(to_digits(x), to_digits(y), c))
    print(f"{x} * {y}: столбиком = {r1}, быстрым = {r2}, эталон = {x * y}\n")

    random.seed(2026)
    print(f"{'n':>5} | {'опер. столбик':>13} | {'опер. быстрое':>13} | {'t столбик':>9} | {'t быстрое':>9} | совп.")
    for n in (64, 256, 1024, 4096, 8192):
        x = random.randrange(10 ** (n - 1), 10 ** n)
        y = random.randrange(10 ** (n - 1), 10 ** n)
        ux, uy = to_digits(x), to_digits(y)

        c1 = [0]; t0 = time.perf_counter()
        r1 = from_digits(mul_column(ux, uy, c1)); t1 = time.perf_counter()
        c2 = [0]
        r2 = from_digits(mul_fast(ux, uy, c2));   t2 = time.perf_counter()

        print(f"{n:>5} | {c1[0]:>13} | {c2[0]:>13} | {t1-t0:>8.3f}s | {t2-t1:>8.3f}s | {r1 == r2 == x * y}")