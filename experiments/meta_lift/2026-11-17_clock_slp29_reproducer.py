#!/usr/bin/env python3
"""CLOCKSLP29 compact independent reproducer, deterministic finite tests."""
import json, random
RNG = random.Random(202611172231)
checks = models = endpoints = 0

def test(ok, msg):
    global checks
    checks += 1
    if not ok:
        raise AssertionError(msg)

def fib(n):
    rules = [('z', 0), ('z', 1), ('c', 0, 1)]
    lens = [1, 1, 2]
    fibs = [0, 2]
    while lens[fibs[-1]] < (1 << n):
        a, b = fibs[-1], fibs[-2]
        fibs.append(len(rules))
        rules.append(('c', a, b))
        lens.append(lens[a] + lens[b])
    def prefix(x, length):
        if length == lens[x]:
            return x
        _, a, b = rules[x]
        if length <= lens[a]:
            return prefix(a, length)
        y = prefix(b, length - lens[a])
        new = len(rules)
        rules.append(('c', a, y))
        lens.append(lens[a] + lens[y])
        return new
    return rules, lens, prefix(fibs[-1], 1 << n)

def run(rules, root, F, bits, start=0):
    def symbol(x, i):
        while rules[x][0] == 'c':
            _, a, b = rules[x]
            if i < length[a]:
                x = a
            else:
                i -= length[a]
                x = b
        return rules[x][1]
    state = start
    for i, bit in enumerate(bits):
        state = F[symbol(root, i)][state][bit]
    return state

for n in range(1, 9):
    for K in (2, 3):
        rules, length, root = fib(n)
        for trial in range(32):
            F = [[[RNG.randrange(K) for b in range(2)] for q in range(K)] for z in range(2)]
            rel, mid = {}, {}
            for x, r in enumerate(rules):
                rel[x] = set()
                if r[0] == 'z':
                    for p in range(K):
                        for bit in (0, 1):
                            q = F[r[1]][p][bit]
                            rel[x].add((p, q))
                            mid.setdefault((x, p, q), bit)
                else:
                    _, a, b = r
                    for p in range(K):
                        for q in range(K):
                            z = next((z for z in range(K) if (p, z) in rel[a] and (z, q) in rel[b]), None)
                            if z is not None:
                                rel[x].add((p, q))
                                mid[x, p, q] = z
            def bit_at(i, p, q):
                x = root
                while rules[x][0] == 'c':
                    _, a, b = rules[x]
                    z = mid[x, p, q]
                    if i < length[a]:
                        x, q = a, z
                    else:
                        i, x, p = i - length[a], b, z
                return mid[x, p, q]
            for p, q in rel[root]:
                bits = [bit_at(i, p, q) for i in range(1 << n)]
                test(run(rules, root, F, bits, p) == q, 'reconstructed endpoint')
                endpoints += 1
            if n <= 3:
                for p in range(K):
                    exhaustive = {run(rules, root, F, ((v >> i) & 1 for i in range(1 << n)), p) for v in range(1 << (1 << n))}
                    test(exhaustive == {q for x, q in rel[root] if x == p}, 'independent brute relation')
            models += 1
print(json.dumps({'reproducer':'CLOCKSLP29','models':models,'endpoint_checks':endpoints,'assertions':checks,'failures':0,'seed':202611172231},sort_keys=True))
