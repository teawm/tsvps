import math
import random
import time
INF = float('inf')

# ---------------- 3.2 Алгоритм Краскалла (минимальный остов) ----------------
def kruskal(n, edges, counter=None, trace=False):
    comp = list(range(n))                       # компоненты связности
    mst = []
    k = len(edges)
    if counter is not None and k > 1:
        counter[0] += int(k * math.log2(k))     # этап сортировки рёбер: k*log k
    for u, v, w in sorted(edges, key=lambda e: e[2]):       # шаг 1: рёбра по возрастанию веса
        if comp[u] == comp[v]:                  # концы в одной компоненте -> цикл
            if counter is not None: counter[0] += 1         # нерезультативный шаг: 1 сравнение
            if trace: print(f"  -({u+1},{v+1}) w={w:<2} цикл")
            continue
        old, new = comp[u], comp[v]
        for i in range(n):                      # результативный шаг: слияние компонент, n операций
            if comp[i] == old: comp[i] = new
            if counter is not None: counter[0] += 1
        mst.append((u, v, w))
        if trace:
            d = {}
            for i, c in enumerate(comp): d.setdefault(c, []).append(i + 1)
            print(f"  +({u+1},{v+1}) w={w:<2} связи: {' | '.join(','.join(map(str, g)) for g in d.values())}")
        if len(mst) == n - 1: break             # остов построен (n-1 ребро)
    return mst

# ---------------- 3.3.1 Алгоритм Форда-Беллмана, формула (3.1) ----------------
def ford_bellman(C, s=0, counter=None, trace=False):
    n = len(C)
    D = [0 if i == s else INF for i in range(n)]            # D[0] = (0, inf, ..., inf)
    if trace: print("  D[0] =", " ".join('inf' if x == INF else str(x) for x in D))
    it = 0
    while True:
        newD = D[:]
        for i in range(n):                                  # D[k+1](i) = min_j (D[k](j) + C(j,i))
            best = D[i]
            for j in range(n):
                cand = D[j] + C[j][i]
                if counter is not None: counter[0] += 1     # n^2 операций за итерацию
                if cand < best: best = cand
            newD[i] = best
        it += 1
        if trace:
            print("  D[{}] = {}".format(it, " ".join('inf' if x == INF else str(x) for x in newD))
                  + ("  -- стабилизация" if newD == D else ""))
        if newD == D or it > n: break                       # транзитивное замыкание
        D = newD
    return D, it

# ---------------- 3.3.2 Алгоритм Дейкстры, формула (3.2) ----------------
def dijkstra(C, s=0, counter=None, trace=False):
    n = len(C)
    D = list(C[s])                              # D[i] = C(0,i)
    S = [False] * n                             # S = {0}
    S[s] = True
    ns = 1
    while ns < n:                               # While S != V
        w, bw = -1, INF
        for i in range(n):                      # 1) вершина w из V\S с минимальной D[w]
            if not S[i]:
                if counter is not None: counter[0] += 1
                if D[i] < bw: bw, w = D[i], i
        if w == -1 or bw == INF: break
        S[w] = True                             # 2) S := S + w
        ns += 1
        for v in range(n):                      # 3) релаксация D[v] = min(D[v], D[w]+C(w,v))
            if not S[v]:
                if counter is not None: counter[0] += 1
                cand = D[w] + C[w][v]
                if cand < D[v]: D[v] = cand
        if trace:
            print("  S={%s} w=%d  D: %s" % (
                ",".join(str(i) for i in range(n) if S[i]), w,
                " ".join('—' if S[i] else ('inf' if D[i] == INF else str(D[i])) for i in range(n))))
    return D

# ---------------- эталон для проверки и генератор графов ----------------
def prim(n, C):                                 # простой остовный алгоритм для сверки Краскалла
    inT = [False] * n; inT[0] = True
    best = list(C[0]); total = 0
    for _ in range(n - 1):
        w, bw = -1, INF
        for i in range(n):
            if not inT[i] and best[i] < bw: bw, w = best[i], i
        if w == -1: break
        total += bw; inT[w] = True
        for v in range(n):
            if not inT[v] and C[w][v] < best[v]: best[v] = C[w][v]
    return total

def rand_graph(n, k, seed):                     # связный неориент. взвешенный граф, k рёбер
    rnd = random.Random(seed)
    edges = {}
    order = list(range(n)); rnd.shuffle(order)
    for i in range(1, n):                       # сначала случайное остовное дерево (связность)
        u, v = order[i], order[rnd.randrange(i)]
        edges[(min(u, v), max(u, v))] = rnd.randint(1, 100)
    while len(edges) < k:
        u, v = rnd.randrange(n), rnd.randrange(n)
        if u != v: edges.setdefault((min(u, v), max(u, v)), rnd.randint(1, 100))
    elist = [(u, v, w) for (u, v), w in edges.items()]
    C = [[INF] * n for _ in range(n)]
    for i in range(n): C[i][i] = 0
    for u, v, w in elist: C[u][v] = C[v][u] = w
    return elist, C

# ---------------- демонстрация ----------------
if __name__ == "__main__":
    # Краскалл на графе рис. 3.1 методички
    edges31 = [(0,1,20),(0,5,23),(0,6,1),(1,6,4),(1,2,5),(5,6,36),
               (2,6,8),(4,5,28),(4,6,25),(3,6,16),(2,3,3),(3,4,17)]
    print("Краскалл, граф рис. 3.1:")
    mst = kruskal(7, edges31, trace=True)
    print("  остов:", ", ".join(f"({u+1},{v+1})" for u, v, w in mst),
          "| вес =", sum(w for _, _, w in mst), "\n")
    # Форд-Беллман и Дейкстра на графе рис. 3.5/3.7
    C5 = [[INF] * 5 for _ in range(5)]
    for i in range(5): C5[i][i] = 0
    for u, v, w in [(0,1,25),(0,2,15),(0,3,7),(0,4,2),(1,2,6),(2,3,4),(3,4,3)]:
        C5[u][v] = C5[v][u] = w
    print("Форд-Беллман, граф рис. 3.5 (расстояния от вершины 0):")
    D_fb, it = ford_bellman(C5, trace=True)
    print("\nДейкстра, он же:")
    D_dj = dijkstra(C5, trace=True)
    print("  ответы совпадают:", D_fb == D_dj, D_fb, "\n")
    # сравнение трудоёмкости на случайных графах
    random.seed(2026)
    print(f"{'n':>4} | {'k':>5} | {'Краскалл опер.(t)':>18} | {'Ф-Б опер.(t), итер.':>20} | "
          f"{'Дейкстра опер.(t)':>18} | К=Prim | ФБ=Д")
    for n in (100, 200, 400, 800):
        elist, C = rand_graph(n, 5 * n, seed=1000 + n)
        c1 = [0]; t0 = time.perf_counter(); mst = kruskal(n, elist, c1);            t1 = time.perf_counter()
        c2 = [0]; Df, l = ford_bellman(C, counter=c2);                              t2 = time.perf_counter()
        c3 = [0]; Dd = dijkstra(C, counter=c3);                                     t3 = time.perf_counter()
        print(f"{n:>4} | {len(elist):>5} | {c1[0]:>9} ({t1-t0:5.3f}s) | {c2[0]:>9} ({t2-t1:5.3f}s), {l:>2} | "
              f"{c3[0]:>9} ({t3-t2:5.3f}s) | {sum(w for _,_,w in mst) == prim(n, C)!s:>6} | {Df == Dd!s:>5}")