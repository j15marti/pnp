# Independent source-indexed four-anchor checker; Python standard library only
# This checker validates the exact restricted theorem's finite guarded source control.
import itertools
from collections import Counter

def guard(sign, vars_):
    h = 1 if sign > 0 else -1
    return [tuple([h, s*u, t*v])
            for u,v in itertools.combinations(vars_,2)
            for s,t in itertools.product((1,-1), repeat=2)]

def lit(l,a):
    return a[abs(l)] if l>0 else not a[abs(l)]

def target(c,S):
    return {abs(l): (l>0) == S for l in c}

def compat(c,d,S,T):
    a=target(c,S);b=target(d,T)
    return all(x not in b or b[x]==v for x,v in a.items())

def check(F,n):
    assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in F)
    a0={i:False for i in range(1,n+1)}
    a1={i:True for i in range(1,n+1)}
    records=[]
    for j,c in enumerate(F):
        S=target(c,True);U=target(c,False)
        assert {i:not v for i,v in S.items()}==U
        assert {i:not v for i,v in U.items()}==S
        records.append((j,c,S,U))
    pairs=0
    for j,c,_,_ in records:
        for k,d,_,_ in records[j+1:]:
            for S,T in itertools.product((False,True),repeat=2):
                should=compat(c,d,S,T)
                actual=any(all(lit(l,a)==S for l in c) and
                           all(lit(l,a)==T for l in d)
                           for a in [{i:bool(mask>>i-1&1) for i in range(1,n+1)}
                                     for mask in range(1<<n)])
                assert should==actual
                pairs+=1
    for a in (a0,a1):
        b={i:not v for i,v in a.items()}
        t=[sum(lit(l,a) for l in c) for c in F]
        u=[sum(lit(l,b) for l in c) for c in F]
        assert all(ti+ui==3 for ti,ui in zip(t,u))
    return pairs,records

def wall(F,partial,V):
    # The remaining variables outside dom(partial) union V are NOT pinned.
    A=[7,4,2,1]
    clauses=[]
    for mask in A:
        base={**partial, **{v:bool(mask>>j&1) for j,v in enumerate(V)}}
        witnesses=[]
        for change in [None]+V:
            a=base.copy()
            if change is not None:a[change]=not a[change]
            w=[j for j,c in enumerate(F) if
               all(abs(l) in a and not lit(l,a) for l in c)]
            assert w, (partial,mask,change)
            witnesses.append(w[0])
        clauses.append(witnesses)
    # Independent exhaustive nonreachability check over V, not outside.
    for bits in itertools.product((False,True),repeat=len(V)):
        assert any(sum(bit!=bool(mask>>j&1)
                       for j,bit in enumerate(bits))<2 for mask in A)
    return clauses

F=guard(1,(2,3,4))+guard(-1,(5,6,7))
assert len(F)==24
pair_count,records=check(F,7)
w0=wall(F,{1:False},[2,3,4])
w1=wall(F,{1:True},[5,6,7])
assert all(not all(any(lit(l,a) for l in c) for c in F)
           for vals in itertools.product((False,True),repeat=7)
           for a in [{i:vals[i-1] for i in range(1,8)}])
G=guard(1,(2,3,4))
assert any(all(any(lit(l,a) for l in c) for c in G)
           for vals in itertools.product((False,True),repeat=4)
           for a in [{i:vals[i-1] for i in range(1,5)}])
print({'original_clauses':24,'source_pair_extreme_checks':pair_count,
       'cube_0_witnesses':w0,'cube_1_witnesses':w1,
       'cube_0_free_outside_V':[5,6,7],
       'cube_1_free_outside_V':[2,3,4],
       'UNSAT':True,'single_guard_SAT':True})
