#!/usr/bin/env python3
"""Exact finite SU05/Hadamard full-feature certificate; NOT full SU09/vMS."""
import itertools
import json

P, G, H, M, K = 17, 3, 4, 4, 5
SHIFTS = (0, 5, 8)

def coeffs(w):
    ans = [0]*H
    for i, y in enumerate(w):
        basis, den = [1], 1
        for j in range(H):
            if j == i:
                continue
            nxt = [0]*(len(basis)+1)
            for z, a in enumerate(basis):
                nxt[z] = (nxt[z]-j*a)%P
                nxt[z+1] = (nxt[z+1]+a)%P
            basis, den = nxt, den*(i-j)%P
        for z, a in enumerate(basis):
            ans[z] = (ans[z]+y*a*pow(den, -1, P))%P
    return ans

def evaluate(f, x):
    value=0
    for a in reversed(f):
        value=(value*x+a)%P
    return value

def rank(rows):
    piv={}
    for row in rows:
        while row:
            b=row.bit_length()-1
            if b in piv:
                row^=piv[b]
            else:
                piv[b]=row
                break
    return len(piv)

def rows(word, shifts):
    f=coeffs(word)
    labels=[evaluate(f, pow(G, t, P)) for t in range(P-1)]
    for s in shifts:
        for u in range(1<<K):
            v=[(labels[(s+i)%(P-1)] & u).bit_count() & 1 for i in range(M)]
            feature=[1]+v+[v[i]&v[j] for i in range(M) for j in range(i+1,M)]
            yield sum(x<<i for i, x in enumerate(feature))

words=list(itertools.product((0,1), repeat=H))
ranks={''.join(map(str,w)):rank(rows(w,SHIFTS)) for w in words}
assert ranks['0000']==1 and ranks['1111']==2
assert all(ranks[''.join(map(str,w))]==11 for w in words if len(set(w))>1)
for z in (1,2):
    for shifts in itertools.combinations(range(P-1),z):
        assert not all(rank(rows(w,shifts))==11 for w in words if len(set(w))>1)
print(json.dumps({'scope':'declared SU05/Hadamard finite control; not full vMS',
                  'p':P,'generator':G,'h':H,'m':M,'universal_shifts':SHIFTS,
                  'ranks':ranks,'no_common_one_or_two_shifts':True}, indent=2))
