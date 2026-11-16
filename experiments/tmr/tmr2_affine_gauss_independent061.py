# TMR-2/061 independent CPython binary affine-character checker; run python experiments/tmr/tmr2_affine_gauss_independent061.py
import json

def solve(rows, width, rhs):
    a = [int(v) | (((rhs >> i) & 1) << width) for i, v in enumerate(rows)]
    r, piv = 0, []
    for j in range(width):
        p = next((t for t in range(r, len(a)) if (a[t] >> j) & 1), None)
        if p is None: continue
        a[r], a[p] = a[p], a[r]
        for t in range(len(a)):
            if t != r and (a[t] >> j) & 1: a[t] ^= a[r]
        piv.append(j)
        r += 1
        if r == len(a): break
    if any((v & ((1 << width) - 1)) == 0 and ((v >> width) & 1) for v in a[r:]): return None
    return sum(((a[i] >> width) & 1) << p for i, p in enumerate(piv)), r

def analytic(a, b, M, lin):
    rows = [(M >> (i * b)) & ((1 << b) - 1) for i in range(a)]
    trans = [sum(((rows[i] >> j) & 1) << i for i in range(a)) for j in range(b)]
    u = lin & ((1 << a) - 1)
    v = lin >> a
    sy, sx = solve(rows, b, u), solve(trans, a, v)
    if sy is None or sx is None: return 0
    assert sy[1] == sx[1]
    return (-1 if (sx[0] & u).bit_count() % 2 else 1) * (1 << (a + b - sy[1]))

def brute(a, b, M, lin):
    total = 0
    for x in range(1 << a):
        for y in range(1 << b):
            xy = sum(((x >> i) & 1) * ((y >> j) & 1) * ((M >> (i * b + j)) & 1) for i in range(a) for j in range(b)) % 2
            aff = ((lin & ((1 << a) - 1) & x).bit_count() + ((lin >> a) & y).bit_count()) % 2
            total += (-1) ** (xy ^ aff)
    return total

def main():
    checks = 0
    for a, b in [(1,1), (2,2), (2,3), (3,2)]:
        for M in range(1 << (a*b)):
            for lin in range(1 << (a+b)):
                assert analytic(a,b,M,lin) == brute(a,b,M,lin), (a,b,M,lin)
                checks += 1
    return {"revision": "TMR2_AFFINE_GAUSS_INDEPENDENT061_v1", "python_character_checks": checks,
            "families": [[1,1], [2,2], [2,3], [3,2]], "failures": 0,
            "status": "COMPUTATIONAL, independent pure-Python rank solve vs exhaustive signed-sum"}

if __name__ == "__main__": print(json.dumps(main(), indent=2))
