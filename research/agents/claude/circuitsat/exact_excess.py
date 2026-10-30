"""Exact B2 circuit size C(f) for all f:{0,1}^n->{0,1}, n=3, by layered BFS over
sets of computed tables; excess e(f)=C(f)-(n-1) for f depending on all inputs.
Stage budget: each run < 30 s (n=3 only)."""
import json, sys
n=3; N=1<<n; FULL=(1<<N)-1
def var(i): return sum(1<<x for x in range(N) if (x>>i)&1)
base=frozenset(var(i) for i in range(n))
def combos(a,b):
    na,nb=FULL^a,FULL^b
    r=set()
    for ca in (a,na):
        for cb in (b,nb):
            r.add(ca&cb)
    # AND with input/output negations covers all non-XOR binary ops; add XOR
    out=set(r); out|={FULL^t for t in r}; out.add(a^b); out.add(FULL^(a^b))
    return out
def depends_all(t):
    for i in range(n):
        if all(((t>>x)&1)==((t>>(x^(1<<i)))&1) for x in range(N)): return False
    return True
first={t:0 for t in base}
layer={base}; seen={base}
for g in range(1,8):
    nxt=set()
    for S in layer:
        L=sorted(S)
        for i in range(len(L)):
            for j in range(i+1,len(L)):
                for t in combos(L[i],L[j]):
                    if t in S: continue
                    T=S|{t}
                    if T not in seen:
                        seen.add(T); nxt.add(T)
                    if t not in first: first[t]=g
    layer=nxt
    print("g",g,"states",len(nxt),"funcs",len(first),flush=True)
    if len(first)==256 or len(nxt)>400000: break
from collections import Counter
cnt=Counter(first[t] for t in first if depends_all(t))
res={"n":n,"size_histogram_all_inputs_essential":dict(sorted(cnt.items())),"covered":len(first)}
print(res); json.dump(res,open("exact_excess_results.json","w"))
