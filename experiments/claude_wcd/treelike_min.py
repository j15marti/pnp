"""Exact minimum tree-like Resolution refutation size (free choice of every branching
variable, i.e. optimal reduction sequence granted for free) for small UNSAT CNFs.
Uses the KNOWN equivalence: min tree-like Resolution size (nodes) = min size of a
decision tree for the falsified-clause search problem (Lovasz-Naor-Newman-Wigderson).
Each instance runs well under 30 s; instances are separate stages (argv selects one)."""
import itertools, json, sys, time, random
from functools import lru_cache

def php(m):  # m+1 pigeons, m holes; var (i,j) -> i*m+j+1
    v = lambda i, j: i*m+j+1
    C = [tuple(v(i, j) for j in range(m)) for i in range(m+1)]
    for j in range(m):
        for a, b in itertools.combinations(range(m+1), 2):
            C.append((-v(a, j), -v(b, j)))
    return C

def tseitin(edges, odd_vertex=0):
    idx = {e: k+1 for k, e in enumerate(edges)}
    verts = sorted({u for e in edges for u in e})
    C = []
    for x in verts:
        inc = [idx[e] for e in edges if x in e]
        charge = 1 if x == odd_vertex else 0
        for signs in itertools.product([0, 1], repeat=len(inc)):
            if sum(signs) % 2 != charge:  # forbid assignments with wrong parity
                C.append(tuple(-l if s else l for l, s in zip(inc, signs)))
    return C

def rand3(n, m, seed):
    r = random.Random(seed)
    return [tuple(x if r.random() < .5 else -x for x in r.sample(range(1, n+1), 3)) for _ in range(m)]

def brute_unsat(C):
    n = max(abs(l) for c in C for l in c)
    for a in itertools.product([False, True], repeat=n):
        if all(any((l > 0) == a[abs(l)-1] for l in c) for c in C):
            return False
    return True

def min_tree(C):
    @lru_cache(maxsize=None)
    def S(F):
        if () in F: return 1
        vs = {abs(l) for c in F for l in c}
        best = None
        for x in vs:
            tot = 1
            for val in (x, -x):  # literal set true
                G = frozenset(tuple(l for l in c if l != -val) for c in F if val not in c)
                tot += S(G)
                if best is not None and tot >= best: break
            if best is None or tot < best: best = tot
        return best
    r = S(frozenset(tuple(sorted(c)) for c in C))
    return r, S.cache_info().currsize

K4 = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
K33 = [(a, b) for a in range(3) for b in range(3, 6)]
PRISM = [(0,1),(1,2),(0,2),(3,4),(4,5),(3,5),(0,3),(1,4),(2,5)]
CUBE = [(a, b) for a in range(8) for b in range(a+1, 8) if bin(a ^ b).count('1') == 1]
INST = {'PHP2_1': lambda: php(1), 'PHP3_2': lambda: php(2), 'PHP4_3': lambda: php(3),
        'TS_K4': lambda: tseitin(K4), 'TS_K33': lambda: tseitin(K33),
        'TS_PRISM': lambda: tseitin(PRISM), 'TS_CUBE': lambda: tseitin(CUBE)}
for n in (6, 8, 10, 12):
    for s in range(3):
        INST[f'R3_n{n}_s{s}'] = (lambda n=n, s=s: rand3(n, int(6*n), 1000*n+s))

if __name__ == '__main__':
    out = {}
    for name in sys.argv[1:]:
        C = INST[name](); t = time.time()
        uns = brute_unsat(C)
        if not uns: out[name] = {'unsat': False}; continue
        size, states = min_tree(C)
        n = max(abs(l) for c in C for l in c)
        bits = sum(len(c) for c in C) * max(1, n.bit_length()+1)
        out[name] = {'unsat': True, 'vars': n, 'clauses': len(C), 'enc_bits': bits,
                     'min_treelike_size': size, 'memo_states': states, 'sec': round(time.time()-t, 2)}
        print(name, out[name], flush=True)
    json.dump(out, sys.stdout if False else open(f'/dev/null', 'w'))
    print('JSON', json.dumps(out))
