#!/usr/bin/env python3
"""TMR-5/038 independent audit of TMR-1/041 (separator lattice, NAE_n pair,
C-SEP all-step tariff).  Pure standard library; independent of the TMR-1 JS.
Runs in a few seconds.  Output: JSON on stdout."""
import itertools, json, sys
from collections import deque

checks = 0; failures = []
def ok(cond, msg):
    global checks
    checks += 1
    if not cond: failures.append(msg)

def assignments(n): return list(itertools.product((0,1), repeat=n))

def cnf_sat(cnf, a):  # literals +i / -i, 1-indexed
    return all(any((a[abs(l)-1]==1) == (l>0) for l in c) for c in cnf)

# ---- 1. Separator lattice, exhaustive n=1,2,3 ------------------------------
lattice = {}
for n in (1,2,3):
    pts = assignments(n); N = len(pts)
    pairs = 0; unique = 0; total_tables = 0
    for lab in itertools.product((0,1,2), repeat=N):   # 0:U 1:V 2:neither
        pairs += 1
        U = {i for i in range(N) if lab[i]==0}; V = {i for i in range(N) if lab[i]==1}
        cnt = 0
        for t in range(1<<N):
            I = [(t>>i)&1 for i in range(N)]
            if all(I[i]==1 for i in U) and all(I[i]==0 for i in V): cnt += 1
        free = N-len(U)-len(V)
        ok(cnt == 2**free, f"lattice count n={n} lab={lab}")
        ok((cnt==1) == (free==0), f"uniqueness iff cover n={n} lab={lab}")
        unique += (cnt==1); total_tables += cnt
    lattice[n] = dict(pairs=pairs, unique=unique, tables=total_tables)
    ok(pairs==3**(2**n) and unique==2**(2**n) and total_tables==4**(2**n), f"totals n={n}")

# ---- 2. 64-separator hostile control: U={000}, V={001} -------------------
def exact_point_cnf(p):  # proper 3-CNF on 3 vars forbidding every assignment except p
    cnf = []
    for q in assignments(3):
        if q != p:
            cnf.append([ (i+1) if q[i]==0 else -(i+1) for i in range(3)])
    return cnf
A = exact_point_cnf((0,0,0)); B = exact_point_cnf((0,0,1))
ok(len(A)==7 and len(B)==7, "seven clauses each")
projA = [a for a in assignments(3) if cnf_sat(A,a)]; projB = [a for a in assignments(3) if cnf_sat(B,a)]
ok(projA==[(0,0,0)] and projB==[(0,0,1)], "exact projections")
seps = 0
pts = assignments(3)
for t in range(256):
    I = {pts[i]:(t>>i)&1 for i in range(8)}
    if I[(0,0,0)]==1 and I[(0,0,1)]==0: seps += 1
ok(seps==64, "64 separators")

# ---- 3. NAE_n complementary pair (wide and Tseitin width<=3) ---------------
nae = {}
for n in range(3,8):
    pts = assignments(n)
    def A_wide(x): return any(x) and not all(x)
    def B_proj(x): return any(all(xi==s for xi in x) for s in (0,1))
    part = all(A_wide(x) != B_proj(x) for x in pts)
    ok(part, f"NAE_{n} wide pair complementary")
    # Tseitin: chain OR wires o_k = o_{k-1} or x_k, and AND wires a_k = a_{k-1} and x_k
    # A' = Tseitin(or-chain) & Tseitin(and-chain) & (o_n) & (not a_n); width<=3.
    m = n  # variables x1..xn, o2..on, a2..an
    idx = {('x',i):i+1 for i in range(n)}
    nxt = n+1
    for k in range(1,n): idx[('o',k)] = nxt; nxt+=1
    for k in range(1,n): idx[('a',k)] = nxt; nxt+=1
    def prev(kind,k): return idx[('x',0)] if k==1 else idx[(kind,k-1)]
    cnf = []
    for k in range(1,n):
        o, p, x = idx[('o',k)], prev('o',k), idx[('x',k)]
        cnf += [[-p,o],[-x,o],[-o,p,x]]
        a, q = idx[('a',k)], prev('a',k)
        cnf += [[-a,q],[-a,x],[a,-q,-x]]
    cnf += [[idx[('o',n-1)]], [-idx[('a',n-1)]]]
    ok(max(len(c) for c in cnf) <= 3, f"width<=3 n={n}")
    nv = nxt-1
    good = True
    for x in pts:
        ex = False
        # wires are functionally determined: evaluate directly then check CNF
        a = [0]*nv
        for i in range(n): a[i]=x[i]
        o=x[0]; an=x[0]
        for k in range(1,n):
            o = o|x[k]; an = an&x[k]
            a[idx[('o',k)]-1]=o; a[idx[('a',k)]-1]=an
        ex = cnf_sat(cnf, a)
        if ex != A_wide(x): good=False
    ok(good, f"Tseitin projection = NAE_{n}")
    nae[n] = dict(clauses=len(cnf), vars=nv)

# ---- 4. C-SEP lab, n=2: exact R(S) and every-APPEND tariff row -------------
# functions on 2 inputs as 4-bit truth tables; constants and inputs available.
X1, X2 = 0b1100, 0b1010; ONE, ZERO = 0b1111, 0
start = frozenset({X1,X2,ZERO,ONE})
def succ(S):
    out = set()
    for f in S:
        g = (~f)&15
        if g not in S: out.add(S|{g})
        for h in S:
            k = f&h
            if k not in S: out.add(S|{k})
    return out
# all reachable states
seen = {start}; dq = deque([start])
while dq:
    S = dq.popleft()
    for T in succ(S):
        if T not in seen: seen.add(T); dq.append(T)
states = list(seen)
tariff = {}
for target in range(16):
    # R(S) = min gates to obtain target; compute by backward fixpoint on finite DAG
    R = {S:(0 if target in S else None) for S in states}
    order = sorted(states, key=len, reverse=True)
    changed = True
    while changed:
        changed = False
        for S in order:
            if R[S]==0: continue
            best = None
            for T in succ(S):
                if R[T] is not None and (best is None or R[T]+1<best): best = R[T]+1
            if best is not None and best != R[S]: R[S]=best; changed=True
    rows = 0; viol = 0
    for S in states:
        ok(R[S] is not None, f"finite R target={target}")
        for T in succ(S):
            d = R[S]-R[T]; rows += 1
            if not (0 <= d <= 1): viol += 1
    ok(viol==0, f"tariff rows target={target}")
    tariff[format(target,'04b')] = dict(R0=R[start], rows=rows, violations=viol)
# XOR via AND/NOT needs exactly: x1&~x2 (2 gates: NOT,AND), ~x1&x2 (2), NOR-ish OR of them = NOT(AND(NOT,NOT)) (3) -> 7
ok(tariff['0110']['R0'] == 7, "XOR AND/NOT minimum")

out = dict(run="TMR-5/038", checks=checks, failures=failures,
           lattice=lattice, sep64=seps, nae_pairs=nae,
           csep_n2=dict(states=len(states), per_target=tariff))
json.dump(out, sys.stdout, indent=1, sort_keys=True)
print()
