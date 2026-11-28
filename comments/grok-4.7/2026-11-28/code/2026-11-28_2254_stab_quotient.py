#!/usr/bin/env python3
"""Grok 4.7 check: target-oblivious stabilizer quotient vs T4 suffix-period quotient.
Dictionaries S_i are explicit sets of ints (bit vectors over F2^h). Feasibility: XOR_i s_i = b.
T4 (a184133) quotient uses H_Q = sum_i Per(S_i). Grouped refinement uses
H_Q^part = sum_j Stab(sum_{i in G_j} S_i) over complete groups G_j inside the suffix
plus Per(S_i) for suffix blocks of a split group. Deterministic seeds; pure Python."""
import random, itertools, sys

def sumset(A, B):
    return frozenset(a ^ b for a in A for b in B)

def stab(A):
    A = frozenset(A); a0 = next(iter(A))
    return [a0 ^ x for x in A if all((y ^ a0 ^ x) in A for y in A)]

def basis(vecs):
    """reduced echelon basis dict pivotbit->vector"""
    B = {}
    for v in vecs:
        for p in sorted(B, reverse=True):
            if v >> p & 1: v ^= B[p]
        if v:
            p = v.bit_length() - 1
            for q in list(B):
                if B[q] >> p & 1: B[q] ^= v
            B[p] = v
    return B

def reduce(v, B):
    for p in sorted(B, reverse=True):
        if v >> p & 1: v ^= B[p]
    return v

def dim(vecs): return len(basis(vecs))

def span_dirs(S):
    a = next(iter(S)); return [a ^ x for x in S]

def intersect_dim(U, V):
    return dim(U) + dim(V) - dim(list(U) + list(V))

def full_sumset(blocks):
    T = frozenset([0])
    for S in blocks: T = sumset(T, S)
    return T

def dp(blocks, b, mode, check_bound=False):
    """layered DP with exact affine suffix pruning (T4: live states lie in A_P cap (b+A_Q)).
    mode 'exact': no quotient; 'per': quotient by H_Q = sum_{i>=t} Per(S_i) (T4 a184133).
    Returns (feasible, max intermediate live states, witness). If check_bound, asserts the T4
    bound |states| <= 2^(lambda(P) - dim(H_Q cap U_P)) at every cut."""
    m = len(blocks)
    dirs = [span_dirs(S) for S in blocks]
    anchors = [min(S) for S in blocks]
    states = {0: (0, [])}
    mx = 1
    for t in range(m):
        UQ = basis([v for i in range(t + 1, m) for v in dirs[i]])
        aQ = 0
        for i in range(t + 1, m): aQ ^= anchors[i]
        H = basis([p for i in range(t + 1, m) for p in stab(blocks[i])]) if mode == 'per' else {}
        new = {}
        for key, (s, ch) in states.items():
            for x in sorted(blocks[t]):
                s2 = s ^ x
                if reduce(s2 ^ b ^ aQ, UQ) != 0: continue  # affine suffix pruning (exact, sound)
                k2 = reduce(s2 ^ b, H)
                if k2 not in new: new[k2] = (s2, ch + [x])
        states = new
        if t + 1 < m:
            mx = max(mx, len(states))
            if check_bound:
                UP = [v for i in range(t + 1) for v in dirs[i]]
                UQl = [v for i in range(t + 1, m) for v in dirs[i]]
                lam = intersect_dim(UP, UQl)
                Hl = list(H.values())
                dh = intersect_dim(Hl, UP) if Hl else 0
                assert len(states) <= 2 ** (lam - dh), (len(states), lam, dh)
        if not states: return False, mx, None
    if states:
        (s, ch), = states.values()
        assert s == b
        r = 0
        for x, S in zip(ch, blocks): assert x in S; r ^= x
        assert r == b
        return True, mx, ch
    return False, mx, None

def fuse(blocks, groups):
    out, cur, g0 = [], None, object()
    for S, g in zip(blocks, groups):
        if g != g0:
            if cur is not None: out.append(cur)
            cur, g0 = frozenset(S), g
        else:
            cur = sumset(cur, S)
    out.append(cur)
    return out

def check_L1(rng, trials=300, h=5):
    bad = 0
    for _ in range(trials):
        blocks = [frozenset(rng.sample(range(1 << h), rng.randint(1, 4))) for _ in range(rng.randint(1, 3))]
        T = full_sumset(blocks); St = set(stab(T))
        for s in range(1 << h):
            for s2 in range(1 << h):
                eq = all(((s ^ bb) in T) == ((s2 ^ bb) in T) for bb in range(1 << h))
                if eq != ((s ^ s2) in St): bad += 1
    return bad

def random_instance(rng, h, m, gsize):
    blocks, groups = [], []
    g = 0
    while len(blocks) < m:
        sz = rng.randint(1, gsize)
        for _ in range(sz):
            if len(blocks) == m: break
            k = rng.randint(1, 5)
            # biased: sometimes small cubes / structured
            if rng.random() < 0.3:
                a, d1, d2 = (rng.randrange(1 << h) for _ in range(3))
                S = {a, a ^ d1, a ^ d2, a ^ d1 ^ d2}
                if rng.random() < 0.5: S.add(rng.randrange(1 << h))
            else:
                S = set(rng.sample(range(1 << h), k))
            blocks.append(frozenset(S)); groups.append(g)
        g += 1
    return blocks, groups

def separation_family(k, label):
    """component j uses bits 4j..4j+3 = a,b,c,d. prefix R_j={0,a,b,c,d}; suffix S_j={0,a,b,a+b,c}, T_j={0,c,d,c+d,a}.
    defect Z={0,e,f} on bits 4k,4k+1. target bits: component part arbitrary, defect part e (YES) or e+f (NO)."""
    blocks, groups = [], []
    for j in range(k):
        a, b_, c, d = (1 << (4*j + i) for i in range(4))
        blocks.append(frozenset({0, a, b_, c, d})); groups.append(('R', j))
    for j in range(k):
        a, b_, c, d = (1 << (4*j + i) for i in range(4))
        blocks.append(frozenset({0, a, b_, a ^ b_, c})); groups.append(('G', j))
        blocks.append(frozenset({0, c, d, c ^ d, a})); groups.append(('G', j))
    e, f = 1 << (4*k), 1 << (4*k + 1)
    blocks.append(frozenset({0, e, f})); groups.append(('Z',))
    comp = sum(1 << (4*j + 1) for j in range(k))  # arbitrary component target
    b = comp ^ (e if label == 'YES' else e ^ f)
    return blocks, groups, b

def main():
    rng = random.Random(20261128)
    out = []
    bad = check_L1(rng)
    out.append(f"L1 brute force (target-oblivious equivalence == stabilizer coset): 300 random suffixes over F2^5, mismatches={bad}")
    S = {0, 1, 2, 3, 4}; T = {0, 4, 8, 12, 1}
    out.append(f"component check: |S+T|={len(sumset(S,T))} (16 = full F2^4), Per(S)={sorted(stab(S))}, Per(T)={sorted(stab(T))}, |Stab(S+T)|={len(stab(sumset(S,T)))}")
    st = dict(n=0, agree=0, bound_checked_cuts=0, fused_lt_per=0, fused_gt_per=0, sum_exact=0, sum_per=0, sum_fused=0, cuts=0, per_strict_in_stab=0, pairfuse_strict_in_stab=0)
    for trial in range(400):
        h = rng.randint(4, 7); m = rng.randint(2, 7)
        blocks, groups = random_instance(rng, h, m, 3)
        b = rng.randrange(1 << h)
        truth = b in full_sumset(blocks)
        fb = fuse(blocks, groups)
        r = {'exact': dp(blocks, b, 'exact'), 'per': dp(blocks, b, 'per', check_bound=True), 'fused': dp(fb, b, 'per', check_bound=True)}
        st['n'] += 1; st['bound_checked_cuts'] += (m - 1) + (len(fb) - 1)
        if all(v[0] == truth for v in r.values()): st['agree'] += 1
        st['sum_exact'] += r['exact'][1]; st['sum_per'] += r['per'][1]; st['sum_fused'] += r['fused'][1]
        st['fused_lt_per'] += r['fused'][1] < r['per'][1]; st['fused_gt_per'] += r['fused'][1] > r['per'][1]
        for t in range(1, m):
            suf = blocks[t:]
            P = [p for S_ in suf for p in stab(S_)]
            St = stab(full_sumset(suf))
            pf = [p for i in range(0, len(suf), 2) for p in stab(full_sumset(suf[i:i+2]))]
            st['cuts'] += 1
            assert dim(P + St) == dim(St) and dim(pf + St) == dim(St)
            st['per_strict_in_stab'] += dim(P) < dim(St)
            st['pairfuse_strict_in_stab'] += dim(pf) < dim(St)
    out.append("random (400 instances, h 4..7, m 2..7, consecutive groups <=3): " + str(st))
    for k in range(1, 7):
        for label in ('YES', 'NO'):
            blocks, groups, b = separation_family(k, label)
            truth = label == 'YES'
            fb = fuse(blocks, groups)
            res = {'T4 per (unfused)': dp(blocks, b, 'per', check_bound=(k <= 4)), 'T4 per (pair-fused)': dp(fb, b, 'per', check_bound=(k <= 4))}
            if k <= 5: res['exact unfused'] = dp(blocks, b, 'exact')
            for md, v in res.items(): assert v[0] == truth, (k, label, md)
            t = k
            UP = [v for S_ in blocks[:t] for v in span_dirs(S_)]
            UQ = [v for S_ in blocks[t:] for v in span_dirs(S_)]
            lam = intersect_dim(UP, UQ)
            HQper = [p for S_ in blocks[t:] for p in stab(S_)]
            HQg = [p for S_ in fb[t:] for p in stab(S_)]
            dper = intersect_dim(HQper, UP) if HQper else 0
            dg = intersect_dim(HQg, UP)
            out.append(f"family k={k} {label}: decided={truth}; cut after prefix R: lambda={lam}, dim(H_per cap U_P)={dper}, dim(H_fused cap U_P)={dg}; "
                       f"bounds 2^{lam-dper} vs 2^{lam-dg}; max live intermediate states: " + ", ".join(f"{md}={v[1]}" for md, v in res.items()))
    print("\n".join(out))

if __name__ == '__main__':
    main()
