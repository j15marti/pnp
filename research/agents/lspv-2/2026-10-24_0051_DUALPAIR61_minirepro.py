#!/usr/bin/env python3
"""DUALPAIR61 independent stdlib minimal reproduction, Python 3.10+.
Fixed input language: proper signed exact-(2,2) CNF. Prints checked counts.
The separate full audit/JSON are delivered in the local research package.
"""
from collections import Counter
from itertools import combinations
from math import ceil, log2
import json

def validation(clauses):
    if not clauses or any(len(c)!=3 or 0 in c or len(set(abs(z) for z in c))!=3 for c in clauses):
        return False
    if len({tuple(sorted(c)) for c in clauses})!=len(clauses):
        return False
    names={abs(z) for c in clauses for z in c}
    ct=Counter((abs(z),z>0) for c in clauses for z in c)
    return (names==set(range(1,len(names)+1)) and len(clauses)*3==4*len(names)
            and all(ct[(x,True)]==ct[(x,False)]==2 for x in names))

def exact_defect(clauses):
    assert validation(clauses)
    pos=Counter(tuple(sorted(c)) for c in clauses if all(z>0 for z in c))
    neg=Counter(tuple(sorted(-z for z in c)) for c in clauses if all(z<0 for z in c))
    supportpairs={S:min(pos[S],neg[S]) for S in pos.keys()|neg.keys()}
    used=Counter(x for S,k in supportpairs.items() for x in S for _ in range(k))
    assert all(x<=2 for x in used.values())
    return len(clauses)-2*sum(supportpairs.values()), supportpairs

def pivot_defect(clauses):
    assert validation(clauses)
    d={frozenset(c):i for i,c in enumerate(clauses)}
    seen=set()
    for i,c in enumerate(clauses):
        if i in seen:continue
        options=[d[frozenset(-z if z==v else v for z in c)] for v in c
                 if frozenset(-z if z==v else v for z in c) in d]
        assert len(options)<=1
        if options:
            j=options[0]
            assert j not in seen
            seen.update((i,j))
    return len(clauses)-len(seen)

def valid(clauses,assign):
    return all(any(assign[abs(z)]==(z>0) for z in c) for c in clauses)

def paired_prism(q):
    assert q>=3
    E=([(i,(i+1)%q) for i in range(q)]
       +[(q+i,q+(i+1)%q) for i in range(q)]
       +[(i,q+i) for i in range(q)])
    S=[tuple(j+1 for j,(a,b) in enumerate(E) if v in (a,b)) for v in range(2*q)]
    F=[c for s in S for c in (s,tuple(-x for x in s))]
    assignment={j+1:(j<2*q) for j in range(3*q)}
    return F,assignment

def two_cycles(q):
    assert q>=3
    F=[]
    for base in (q,2*q):
        for i in range(q):
            y=base+i+1; nxt=base+(i+1)%q+1; x=i+1
            F.extend(((y,-nxt,x),(y,-nxt,-x)))
    return F,{i:False for i in range(1,3*q+1)}

def main():
    results=[]
    for q in (3,4,5,6,8,12,20,60):
        for name,constructor,exp_t,exp_d in (
                ('paired_prism',paired_prism,0,4*q),
                ('double_pivot',two_cycles,4*q,0)):
            clauses,witness=constructor(q)
            assert validation(clauses)
            t,_=exact_defect(clauses)
            delta=pivot_defect(clauses)
            assert (t,delta)==(exp_t,exp_d)
            assert valid(clauses,witness)
            n=3*q;m=4*q
            width=ceil(log2(64*(n+m+1)))
            results.append({'family':name,'q':q,'n':n,'m':m,'N_bits':(4*m+2)*width,
                            't':t,'delta':delta,'witness_valid':True})
    print(json.dumps({'status':'COMPUTATIONAL','cases':results},indent=2))
if __name__=='__main__':
    main()
