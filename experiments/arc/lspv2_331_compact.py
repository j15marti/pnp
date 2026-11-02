#!/usr/bin/env python3
"""Executable compact 331 source-indexed cofactor-equivalence audit.
Run beside previously published lspv2_330_compact.py, requires networkx.
Unlike the full archive, this compact script omits Tutte proof acquisition.
"""
import itertools,collections,functools
from lspv2_330_compact import F,solve,validate

validate(F,6)
index=collections.defaultdict(list)
for j,c in enumerate(F):
    for lit in c:index[abs(lit)].append(j)

@functools.lru_cache(maxsize=None)
def pinned_decision(key):
    pins=dict(key)
    label,_=solve(F,6,pins)
    assert label in ('SAT','UNSAT')
    return label=='SAT'

def directed_witness_exists(p,q):
    # F|p true, F|q false, where p and q pin the same original variables.
    changed=[v for v in p if p[v]!=q[v]]
    affected=sorted(set(j for v in changed for j in index[v]))
    assert len(affected)<=4*len(changed)
    for j in affected:
        need={}
        for lit in F[j]:
            v=abs(lit)
            if v in q and q[v]==int(lit>0):break
            if v not in q:need[v]=int(lit<0)
        else:
            if pinned_decision(tuple(sorted({**p,**need}.items()))):return True
    return False

def equiv(p,q):
    assert set(p)==set(q)
    if p==q:return True
    return not (directed_witness_exists(p,q) or directed_witness_exists(q,p))

def signature(p):
    free=[i for i in range(1,7) if i not in p]
    sig=[]
    for z in itertools.product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,z))}
        sig.append(int(all(any(a[abs(l)]==int(l>0) for l in c) for c in F)))
    return tuple(sig)

def main():
    n=6;cnt=collections.Counter()
    for mask in range(1<<n):
        domain=[i+1 for i in range(n) if mask>>i&1]
        states=[]
        for a in itertools.product((0,1),repeat=len(domain)):
            p=dict(zip(domain,a));states.append((p,signature(p)))
        cnt['syntactic']+=len(states)
        cnt['semantic']+=len({s for p,s in states})
        cnt['current_decision']+=len({bool(any(s)) for p,s in states})
        for p,sp in states:
            for q,sq in states:
                expected=sp==sq
                assert equiv(p,q)==expected
                cnt['ordered_pairs']+=1
                if expected:cnt['equiv_pairs']+=1
                if bool(any(sp))==bool(any(sq)):
                    cnt['same_label_pairs']+=1
                    if not expected:cnt['unsafe_label_merges']+=1
    assert tuple(cnt[k] for k in ('syntactic','semantic','current_decision','ordered_pairs','equiv_pairs','same_label_pairs','unsafe_label_merges'))==(729,344,94,15625,5893,9025,3132)
    print('Z6 paired cofactor exact',dict(cnt),'unique paid source SAT subqueries',pinned_decision.cache_info().misses)
    print('P versus NP OPEN')
if __name__=='__main__':main()
