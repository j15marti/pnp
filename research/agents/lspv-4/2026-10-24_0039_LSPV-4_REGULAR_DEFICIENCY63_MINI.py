#!/usr/bin/env python3
"""Independent stdlib small exact-(2,2) Hall profile reproducer.
Run: python research/agents/lspv-4/2026-10-24_0039_LSPV-4_REGULAR_DEFICIENCY63_MINI.py
No external packages; no universal complexity lower-bound claim.
"""
import random, json
from collections import Counter
SEED=202610240063
checks=0
def ok(x,why):
    global checks
    checks+=1
    assert x,why
def match(F):
    owner={}
    def augment(j,seen):
        for a in F[j]:
            v=abs(a)
            if v in seen: continue
            seen.add(v)
            if v not in owner or augment(owner[v],seen):
                owner[v]=j
                return True
        return False
    for j in range(len(F)): augment(j,set())
    return len(owner)
def gen(t,seed):
    rng=random.Random(SEED+137*t+seed)
    n,m=3*t,4*t
    slots=[x for x in range(1,n+1) for _ in range(4)]
    for _ in range(20000):
        rng.shuffle(slots)
        sup=[slots[3*j:3*j+3] for j in range(m)]
        if all(len(set(C))==3 for C in sup): break
    else: raise RuntimeError('generation failed')
    signs={v:[1,1,-1,-1] for v in range(1,n+1)}
    for a in signs.values():rng.shuffle(a)
    F=[tuple(v*signs[v].pop() for v in C) for C in sup]
    ok(len(set(tuple(sorted(C)) for C in F))==m,'duplicates')
    cnt=Counter(x for C in F for x in C)
    for v in range(1,n+1):ok(cnt[v]==cnt[-v]==2,'signed degree')
    return F
def horn(F):
    n=max(abs(x) for C in F for x in C)
    H=[]
    for j,C in enumerate(F):
        s=[n+3*j+i+1 for i in range(3)]
        H.append(tuple(s))
        H.extend((-s[i],C[i]) for i in range(3))
    return H
def brute_delta(F):
    m=len(F); best=-999; winners=[]
    for mask in range(1<<m):
        Q=[F[j] for j in range(m) if mask&(1<<j)]
        V=set(abs(x) for C in Q for x in C)
        value=len(Q)-len(V)
        if value>best:best=value;winners=[mask]
        elif value==best:winners.append(mask)
        # signed incidence-boundary identity: deg_F=4
        beta=sum(4-sum(abs(x)==v for C in Q for x in C) for v in V)
        ok(3*value==len(V)-beta,'cut accounting')
    return best,winners
trials=[]
for t in range(1,8):
    for seed in range(3 if t<=3 else 2):
        F=gen(t,seed);n,m=3*t,4*t
        ok(match(F)==n,'source matching')
        ok(m-match(F)==t,'source maximum deficiency')
        for j in range(m):ok((m-1)-match(F[:j]+F[j+1:])==t-1,'deletion')
        H=horn(F)
        ok(len(H)==4*m,'lift length')
        ok(match(H)==3*m+n,'lift matching')
        if t<=3:
            d,w=brute_delta(F)
            ok(d==t and w==[(1<<m)-1],'unique argmax')
        trials.append({'t':t,'n':n,'m':m,'deficiency':t})
print(json.dumps({'seed':SEED,'assertion_groups':checks,'failed':0,'trials':trials},indent=2))
