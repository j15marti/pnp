"""TMR-5/090 native T5 ladder width firewall (stdlib, deterministic)."""
from itertools import product


def R(x, y):
    return (y - x) % 5 in (1, 3)


def edges(m):
    return ([(2*i, 2*i+1) for i in range(m)]
            + [(2*i, 2*i+2) for i in range(m-1)]
            + [(2*i+1, 2*i+3) for i in range(m-1)])


def transfer(m):
    states = [(a, b) for a in range(5) for b in range(5) if R(a, b)]
    dp = {s: 1 for s in states}
    for _ in range(m-1):
        dp = {t: sum(v for s, v in dp.items()
                     if R(s[0], t[0]) and R(s[1], t[1])) for t in states}
    return sum(dp.values())


def brute(m):
    es = edges(m)
    value = [0]*(2*m)
    count = 0
    def dfs(i):
        nonlocal count
        if i == 2*m:
            count += 1
            return
        for x in range(5):
            value[i] = x
            if all(R(value[u], value[v]) for u, v in es if max(u, v) == i):
                dfs(i+1)
    dfs(0)
    return count


def bit_minor(h):
    m = 3*h + 1
    es = edges(m)
    matrix = []
    for alpha in product((0, 1), repeat=h):
        line = []
        for beta in product((0, 1), repeat=h):
            top, bottom = [0]*m, [1]*m
            for k in range(h):
                top[3*k+1] = (1, 3)[alpha[k]]
                top[3*k+2] = 4
                bottom[3*k+1] = (2, 4)[beta[k]]
                bottom[3*k+2] = 0
            arr = [x for ab in zip(top, bottom) for x in ab]
            actual = int(all(R(arr[u], arr[v]) for u, v in es))
            predicted = int(all((a, b) != (1, 0) for a, b in zip(alpha, beta)))
            assert actual == predicted
            line.append(actual)
        matrix.append(line)
    return matrix


def rank(rows, p):
    a = [[v % p for v in row] for row in rows]
    n = len(a)
    r = 0
    for col in range(n):
        pivot = next((i for i in range(r, n) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][col], -1, p)
        a[r] = [x*inv % p for x in a[r]]
        for i in range(r+1, n):
            if a[i][col]:
                t = a[i][col]
                a[i] = [(x-t*y) % p for x, y in zip(a[i], a[r])]
        r += 1
        if r == n:
            break
    return r


if __name__ == '__main__':
    assert [[int(R(a, b)) for b in (2, 4)] for a in (1, 3)] == [[1, 1], [0, 1]]
    for m in range(2, 9):
        z = transfer(m)
        assert z == 10*3**(m-1)
        if m <= 7:
            assert z == brute(m)
        print('columns', m, 'count', z)
    for h in range(1, 9):
        mat = bit_minor(h)
        assert all(rank(mat, p) == 2**h for p in (2, 3, 5))
        print('h', h, 'minor_rank', 2**h, 'over GF(2),GF(3),GF(5)')
    print('ALL CHECKS PASS')
