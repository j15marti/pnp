from itertools import product
from random import Random

def circuits(n,s):
    for o in range(n): yield (),o
    last=[()]
    for d in range(1,s+1):
        nxt=[]
        for G in last:
            for op in ('AND','OR','NOT'):
                for ins in product(range(n+d-1),repeat=1 if op=='NOT' else 2):
                    H=G+((op,ins),); nxt.append(H)
                    for o in range(n+d): yield H,o
        last=nxt

def value(n,C,o,x):
    v=[(x>>j)&1 for j in range(n)]
    for op,a in C:
        v.append((1-v[a[0]]) if op=='NOT' else
                 (v[a[0]]&v[a[1]]) if op=='AND' else (v[a[0]]|v[a[1]]))
    return v[o]

def bits(n,c): return sum(value(n,*c,x)<<x for x in range(1<<n))

def uniform(n,s,T):
    old=((),0); trials=0; checks=0
    for t in range(1<<n):
        if old is None: continue
        found=None
        for c in circuits(n,s):
            trials+=1
            if value(n,*c,t)!=((T>>t)&1):continue
            ok=True
            for j in range(t):
                checks+=1
                if value(n,*c,j)!=value(n,*old,j):ok=False;break
            if ok:found=c;break
        old=found
    return old,trials,checks

for n,s in ((3,2),(4,2)):
    N=1<<n; W={}
    for c in circuits(n,s):W.setdefault(bits(n,c),c)
    Y=set(W); prefixes=[{w&((1<<t)-1) for w in Y} for t in range(N+1)]
    assert all(len(q)<=len(Y) for q in prefixes)
    for T in range(1<<N):
        alive=True; a=0
        for t in range(N):
            a|=((T>>t)&1)<<t
            alive &= a in prefixes[t+1]
        assert alive==(T in Y)
        if alive: assert bits(n,W[T])==T
    print('census',n,s,'Y',len(Y),'all_inputs',1<<N,'prefix_states',sum(len(q)+1 for q in prefixes),'PASS')

rng=Random(202610192136)
for n,s,inputs in ((2,1,list(range(16))),(3,2,rng.sample(range(256),30))):
    Y={bits(n,c) for c in circuits(n,s)}
    trials=checks=0
    for T in inputs:
        result,a,b=uniform(n,s,T)
        assert (result is not None)==(T in Y)
        if result:assert bits(n,result)==T
        trials+=a;checks+=b
    print('uniform',n,s,'inputs',len(inputs),'candidate_trials',trials,'comparisons',checks,'PASS')
