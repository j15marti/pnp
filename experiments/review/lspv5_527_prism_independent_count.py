#!/usr/bin/env python3
"""LSPV-5/527 independent check of LSPV-1/620 Theorem 620.1, rebuilt from the theorem
text only (no code shared with the LSPV-1 generator).  Brute-force model counts and
per-clause deletion-witness counts for k=6,7 (Python big-int bitsets, < 30 s); GF(2) rank identities
for k=6..64.  Usage: python3 lspv5_527_prism_independent_count.py OUT.json"""
import json, sys

def family(k):
    V, r = 2 * k, k // 2
    T = lambda i: i % k; B = lambda i: k + i % k
    edges = [(T(i), T(i + 1)) for i in range(k)] + [(B(i), B(i + 1)) for i in range(k)] + [(T(i), B(i)) for i in range(k)]
    t, s = T(0), B(r)
    spoke_t, spoke_s = 2 * k + 0, 2 * k + r
    q = [0] * V; q[T(1)] = 1
    rows, clauses = [], []
    for v in range(V):
        inc = [e for e, (a, b) in enumerate(edges) if v in (a, b)]
        assert len(inc) == 3
        mask = [e for e in inc if not ((v == t and e == spoke_t) or (v == s and e == spoke_s))]
        rows.append((mask, q[v]))
        for z in range(8):
            bits = [(z >> j) & 1 for j in range(3)]
            par = sum(b for e, b in zip(inc, bits) if e in mask) % 2
            if par != q[v]:
                clauses.append((v, [(e, b) for e, b in zip(inc, bits)]))  # forbids this pattern
    return V, len(edges), rows, clauses

def rank_gf2(vecs):
    piv, r = {}, 0
    for v in vecs:
        while v:
            h = v.bit_length() - 1
            if h in piv: v ^= piv[h]
            else: piv[h] = v; r += 1; break
    return r

def brute(k):
    V, E, rows, clauses = family(k)
    N = 1 << E; full = (1 << N) - 1
    bits = []
    for e in range(E):  # column of bit e over all 2^E assignments m (bit m of the int)
        blk = ((1 << (1 << e)) - 1) << (1 << e)  # pattern 0^{2^e} 1^{2^e}
        per = 1 << (e + 1); pat = 0; reps = N // per
        unit = blk; acc = 0; sh = 0
        # build by doubling
        acc = unit; width = per
        while width < N: acc |= acc << width; width *= 2
        bits.append(acc & full)
    viol = []
    for v, pat in clauses:
        x = full
        for e, b in pat: x &= bits[e] if b else (full ^ bits[e])
        viol.append(x)
    once, many = 0, 0
    for x in viol:
        many |= once & x; once ^= x
    once &= full ^ many; anyv = once | many
    models = bin(full ^ anyv).count('1')
    dels = sorted({bin(x & once).count('1') for x in viol})
    return {'k': k, 'V': V, 'E': E, 'clauses': len(clauses), 'models': models,
            'expected_models': 2 ** k, 'deletion_witness_counts': dels, 'expected_deletion': 2 ** (k - 2)}

def ranks(k):
    V, E, rows, _ = family(k)
    vec = [sum(1 << e for e in mask) for mask, _ in rows]
    return {'k': k, 'rank': rank_gf2(vec), 'V': V, 'models_log2': E - rank_gf2(vec)}

out = {'brute': [brute(6), brute(7)], 'rank': [ranks(k) for k in range(6, 65)]}
out['all_rank_full'] = all(r['rank'] == r['V'] and r['models_log2'] == r['k'] for r in out['rank'])
out['brute_ok'] = all(b['models'] == b['expected_models'] and b['deletion_witness_counts'] == [b['expected_deletion']] and b['clauses'] == 8 * b['k'] for b in out['brute'])
json.dump(out, open(sys.argv[1], 'w'), indent=1)
print(json.dumps({'brute': out['brute'], 'all_rank_full': out['all_rank_full'], 'brute_ok': out['brute_ok']}))
