"""Hard-instance survival screen for the W_R(N) directive (Claude routine, 2026-11-11).

For three UNSAT families -- random 3-CNF (density 8), odd-charge Tseitin on random
3-regular graphs, and the pigeonhole principle PHP^{h+1}_h -- compute exactly:
  * UNSAT (brute force over all assignments),
  * minimum Resolution refutation WIDTH (width-bounded saturation, k = 3, 4, ...),
  * whether GF(2) Gaussian elimination on the locally implied XOR constraints refutes,
  * the number of locally implied XOR constraints at all.
Width is a lower-bound proxy only (Ben-Sasson--Wigderson: size >= exp((w-3)^2/(16 n))
for 3-CNF). These are tiny COMPUTATIONAL controls, not asymptotic lower bounds.
Usage:  python survival_width.py <family> <param> <seed> [kmax]; family in rand3[_alpha], tseitin, php   (each call < ~30 s)
"""
import itertools, json, random, sys, time

def lit_clause(lits):
    p = n = 0
    for l in lits:
        if l > 0: p |= 1 << (l - 1)
        else: n |= 1 << (-l - 1)
    if p & n: return None  # tautology
    return (p, n)

def random_3cnf(nv, alpha, rng):
    m = int(round(alpha * nv)); cls = set()
    while len(cls) < m:
        vs = rng.sample(range(1, nv + 1), 3)
        cls.add(lit_clause([v if rng.random() < .5 else -v for v in vs]))
    return nv, sorted(cls)

def random_cubic(nvert, rng):
    while True:
        pts = [v for v in range(nvert) for _ in range(3)]; rng.shuffle(pts)
        E = [tuple(sorted(pts[i:i+2])) for i in range(0, len(pts), 2)]
        if all(a != b for a, b in E) and len(set(E)) == len(E):
            return E

def tseitin(nvert, rng):
    E = random_cubic(nvert, rng); cls = []
    charge = [1] + [0] * (nvert - 1)  # odd total charge -> UNSAT
    for v in range(nvert):
        inc = [i + 1 for i, e in enumerate(E) if v in e]
        for signs in itertools.product([1, -1], repeat=3):
            # forbid assignments with parity != charge: clause excludes x = (s<0)
            par = sum(1 for s in signs if s < 0) % 2
            if par != charge[v]:
                cls.append(lit_clause([s * x for s, x in zip(signs, inc)]))
    return len(E), sorted(set(cls))

def php(h):
    var = lambda p, j: p * h + j + 1
    cls = [lit_clause([var(p, j) for j in range(h)]) for p in range(h + 1)]
    for j in range(h):
        for p, q in itertools.combinations(range(h + 1), 2):
            cls.append(lit_clause([-var(p, j), -var(q, j)]))
    return (h + 1) * h, sorted(set(cls))

def unsat(nv, cls):
    for a in range(1 << nv):
        if all((p & a) or (n & ~a) for p, n in cls):
            return False
    return True

w = lambda c: bin(c[0]).count('1') + bin(c[1]).count('1')

def refutable_width(nv, cls, k):
    known = set(c for c in cls if w(c) <= k)
    parent = {c: None for c in known}
    occ = {}  # (var, sign) -> clauses containing that literal
    def add_occ(c):
        for v in range(nv):
            b = 1 << v
            if c[0] & b: occ.setdefault((v, 1), []).append(c)
            if c[1] & b: occ.setdefault((v, 0), []).append(c)
    work = list(known)
    for c in work: add_occ(c)
    while work:
        c = work.pop()
        for v in range(nv):
            b = 1 << v
            for s, opp in ((1, 0), (0, 1)):
                if not (c[0] & b if s else c[1] & b):
                    continue
                for d in occ.get((v, opp), ()):
                    p = (c[0] | d[0]) & ~b; n = (c[1] | d[1]) & ~b
                    if p & n: continue
                    r = (p, n)
                    if w(r) > k or r in known: continue
                    parent[r] = (c, d)
                    if r == (0, 0): return extract(parent)
                    known.add(r); work.append(r); add_occ(r)
    return None

def extract(parent):
    order, seen, stack = [], set(), [(0, 0)]
    while stack:  # iterative DFS, post-order
        c = stack[-1]
        if c in seen: stack.pop(); continue
        ps = parent[c]
        pend = [p for p in (ps or ()) if p not in seen]
        if pend: stack.extend(pend); continue
        seen.add(c); order.append((c, ps)); stack.pop()
    return order

def replay(cls, proof, k):
    """Independent check: every line is an axiom or a resolvent of earlier lines."""
    axioms, have = set(cls), set()
    for c, ps in proof:
        assert w(c) <= k
        if ps is None: assert c in axioms
        else:
            a, b = ps; assert a in have and b in have
            piv = (a[0] & b[1]) | (a[1] & b[0]); assert bin(piv).count('1') == 1
            assert c == ((a[0] | b[0]) & ~piv, (a[1] | b[1]) & ~piv)
        have.add(c)
    assert proof[-1][0] == (0, 0)
    return sum(1 for _, ps in proof if ps is not None)

def min_width(nv, cls, kmax):
    k0 = max(w(c) for c in cls)
    for k in range(k0, kmax + 1):
        pf = refutable_width(nv, cls, k)
        if pf: return k, replay(cls, pf, k)
    return None, None  # > kmax

def local_xors(nv, cls):
    """XOR constraints implied by the clauses on one exact support (size<=3)."""
    bysup = {}
    for c in cls: bysup.setdefault(c[0] | c[1], set()).add(c)
    eqs = []
    for sup, cs in bysup.items():
        vs = [v for v in range(nv) if sup >> v & 1]
        sat = [a for a in itertools.product([0, 1], repeat=len(vs))
               if all(any((c[0] >> v & 1 and a[i]) or (c[1] >> v & 1 and not a[i])
                          for i, v in enumerate(vs)) for c in cs)]
        for par in (0, 1):
            if sat and all(sum(a) % 2 == par for a in sat):
                eqs.append((sup, par))
    return eqs

def gf2_refutes(eqs):
    basis = {}
    for m, b in eqs:
        while m:
            hb = m.bit_length() - 1
            if hb not in basis: basis[hb] = (m, b); break
            m2, b2 = basis[hb]; m ^= m2; b ^= b2
        else:
            if b: return True
    return False

if __name__ == '__main__':
    fam, param, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    rng = random.Random(seed); t = time.time()
    if fam.startswith('rand3'): nv, cls = random_3cnf(param, float(fam[6:] or 8), rng)
    elif fam == 'tseitin': nv, cls = tseitin(param, rng)
    elif fam == 'php': nv, cls = php(param)
    else: raise SystemExit('family?')
    u = unsat(nv, cls) if nv <= 16 else 'unchecked-by-brute-force'
    eqs = local_xors(nv, cls)
    out = dict(family=fam, param=param, seed=seed, n_vars=nv, n_clauses=len(cls),
               unsat=u,
               local_xor_count=len(eqs), gf2_local_refutes=gf2_refutes(eqs))
    if u:
        out['min_res_width'], out['width_proof_inferences'] = min_width(nv, cls, int(sys.argv[4]) if len(sys.argv) > 4 else 8)
    out['seconds'] = round(time.time() - t, 2)
    print(json.dumps(out))
