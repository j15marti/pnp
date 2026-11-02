#!/usr/bin/env python3
"""GATE320 role-owned compact recheck. Exponential truth-table acquisition is PAID."""
from itertools import product
from functools import lru_cache
P=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
M=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=P+tuple(tuple(-v for v in c) for c in M)
n=9

def sat(a):
    return all(any(bool(a>>(abs(z)-1)&1)==(z>0) for z in c) for c in F)

T=[int(sat(i)) for i in range(1<<n)]
assert sum(T)==70 and T[0]==T[-1]==0
weights={};reps={};cofactor_bits=0
for S in range(1<<n):
    pinned=[v for v in range(n) if S>>v&1]
    free=[v for v in range(n) if not S>>v&1]
    funcs=set()
    for a in range(1<<len(pinned)):
        base=sum(((a>>k)&1)<<v for k,v in enumerate(pinned));row=0
        for b in range(1<<len(free)):
            x=base|sum(((b>>k)&1)<<v for k,v in enumerate(free))
            row |= T[x]<<b;cofactor_bits+=1
        funcs.add(row)
    reps[S]=len(funcs)
    for v in free:
        j=free.index(v);dependent=0
        for row in funcs:
            if any(((row>>b)&1)!=((row>>(b|(1<<j)))&1)
                   for b in range(1<<len(free)) if not (b>>j)&1):
                dependent+=1
        weights[S,v]=dependent

@lru_cache(None)
def shortest(S):
    if S==(1<<n)-1:return 0,()
    return min((weights[S,v]+shortest(S|(1<<v))[0],
                (v+1,)+shortest(S|(1<<v))[1])
               for v in range(n) if not (S>>v)&1)

@lru_cache(None)
def longest(S):
    if S==(1<<n)-1:return 0,()
    return max((weights[S,v]+longest(S|(1<<v))[0],
                (v+1,)+longest(S|(1<<v))[1])
               for v in range(n) if not (S>>v)&1)

S=62
choices={v:(weights[S,v-1],shortest(S|(1<<(v-1)))[0]) for v in (1,7,8,9)}
assert choices=={1:(17,22),7:(18,22),8:(16,26),9:(17,22)}
assert shortest(0)[0]==52 and longest(0)[0]==80
assert reps[427]==22 and reps[511^427]==8
traps=0
for S in range(1<<n):
    opts=[v for v in range(n) if not (S>>v)&1]
    if len(opts)<2:continue
    floor=min(weights[S,v] for v in opts)
    local=[v for v in opts if weights[S,v]==floor]
    if len(local)==1 and floor+shortest(S|(1<<local[0]))[0]>shortest(S)[0]:traps+=1
assert traps==75 and cofactor_bits==262144

pins={3:0,5:1,6:0,7:0,8:0}
def pinned(bit):
    p={**pins,1:bit};free=[i for i in range(1,10) if i not in p]
    models=0;falsified=[]
    for bits in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,bits))}
        failing=[j for j,c in enumerate(F) if not any(a[abs(z)]==int(z>0) for z in c)]
        if failing:falsified.append(failing[0])
        else:models+=1
    return models,falsified
assert pinned(0)[0]==2 and pinned(1)[0]==0 and len(pinned(1)[1])==8
if __name__=='__main__':
    import json
    print(json.dumps({'minimum':shortest(0),'maximum':longest(0),
         'strict_greedy_prefix':[2,3,4,5,6], 'strict_greedy_choices':choices,
         'strict_bad_subsets':traps,'cofactor_bits':cofactor_bits,
         'forward_reverse_cofactors':[reps[427],reps[511^427]],
         'same_original_models':[pinned(0)[0],pinned(1)[0]]},indent=2))
