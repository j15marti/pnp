"""Exact minimum circuit size (B2 basis, fan-in 2, free negation) of n-variable
functions, n<=3 (BFS over gate sets), and minimum formula leaf-count for n<=4 (DP).
Runtime well under 30 s.  Output: exact_sizes_results.json"""
import json, itertools, sys
def tt_vars(n):
    N=1<<n; out=[]
    for i in range(n):
        v=0
        for x in range(N):
            if (x>>i)&1: v|=1<<x
        out.append(v)
    return out
# binary ops on truth tables: all 16 two-input functions (negations free); skip constants/projections
def combine(a,b,op,mask):
    # op bits: index (a_bit*2+b_bit)
    r=0
    if op&1: r|=(~a&~b)
    if op&2: r|=(~a&b)
    if op&4: r|=(a&~b)
    if op&8: r|=(a&b)
    return r&mask
OPS=[o for o in range(16) if o not in (0,15,3,12,5,10)]  # drop const, a,~a,b,~b
def circuit_sizes(n,maxg):
    N=1<<n; mask=(1<<N)-1
    base=tt_vars(n)
    norm=lambda t: min(t,t^mask)   # negation free
    best={}   # normalized tt -> min gates
    for v in base: best[norm(v)]=0
    best[0]=0
    level=[frozenset(norm(v) for v in base)]
    seen={level[0]}
    for g in range(1,maxg+1):
        nxt=set()
        for S in level:
            L=list(S)
            for a,b in itertools.combinations(L,2):
                for op in OPS:
                    t=norm(combine(a,b,op,mask)); 
                    if t in S or t==0: continue
                    T=S|{t}
                    if T not in nxt and T not in seen: nxt.add(T)
                    if t not in best: best[t]=g
        seen|=nxt; level=list(nxt)
        print(f"n={n} gates={g} states={len(level)} found={len(best)}",file=sys.stderr)
    return best
def formula_sizes(n):
    N=1<<n; mask=(1<<N)-1
    base=tt_vars(n)
    L={}
    for v in base: L[v]=1; L[v^mask]=1
    changed=True
    # DP by leaf count
    bysz={1:set(L)}
    k=1
    while len(L)<(1<<N):
        k+=1; new=set()
        for i in range(1,k//2+1):
            j=k-i
            for a in bysz.get(i,()):
                for b in bysz.get(j,()):
                    for op in OPS:
                        t=combine(a,b,op,mask)
                        if t not in L and t not in new: new.add(t)
        for t in new: L[t]=k
        bysz[k]=new
        if k>30: break
    return L
res={}
for n in (1,2,3):
    b=circuit_sizes(n,{1:1,2:2,3:4}[n])
    full=1<<(1<<n)
    dist={}
    for t,g in b.items():
        mult=2 if t!=0 else 2  # t and ~t
        dist[g]=dist.get(g,0)+2
    res[f"circuit_n{n}"]={"functions_covered":sum(dist.values()),"of":full,"count_by_gates":dict(sorted(dist.items()))}
for n in (1,2,3):
    L=formula_sizes(n)
    d={}
    for t,k in L.items(): d[k]=d.get(k,0)+1
    res[f"formula_n{n}"]={"count_by_leaves":dict(sorted(d.items())),"max_leaves":max(L.values())}
json.dump(res,open("exact_sizes_results.json","w"),indent=1)
print(json.dumps(res,indent=1))
