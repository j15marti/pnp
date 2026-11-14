"""Independent check: build actual Tseitin DIMACS text for explicit 3-regular graphs
(K4 and the 3-prism, odd charge) and compare with the closed-form byte count;
also confirm UNSAT by brute force (<= 9 variables)."""
import itertools, sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from tseitin_length import dimacs_bytes
def tseitin(n, edges):
    inc = {v: [i + 1 for i, e in enumerate(edges) if v in e] for v in range(n)}
    clauses = []
    for v in range(n):
        charge = 1 if v == 0 else 0
        for signs in itertools.product((0, 1), repeat=len(inc[v])):
            if sum(signs) % 2 != charge:           # forbid assignments with wrong parity
                clauses.append([x if s == 0 else -x for x, s in zip(inc[v], signs)])
    return clauses
def text(V, cl): return f"p cnf {V} {len(cl)}\n" + "".join(" ".join(map(str, c)) + " 0\n" for c in cl)
def sat(V, cl): return any(all(any((a[abs(l)-1] == 1) == (l > 0) for l in c) for c in cl) for a in itertools.product((0,1), repeat=V))
K4 = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
PR = [(0,1),(1,2),(2,0),(3,4),(4,5),(5,3),(0,3),(1,4),(2,5)]
ok = True
for name, n, E in (("K4", 4, K4), ("prism", 6, PR)):
    cl = tseitin(n, E); t = text(len(E), cl)
    r = (len(t) == dimacs_bytes(n, 3), sat(len(E), cl))
    print(name, len(t), dimacs_bytes(n, 3), "SAT" if r[1] else "UNSAT"); ok &= r[0] and not r[1]
print("PASS" if ok else "FAIL")
