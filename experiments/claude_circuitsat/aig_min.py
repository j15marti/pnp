# Exact min #AND gates (free negation, fan-in 2) for n-var Boolean functions, by BFS over signal sets.
import json,sys,time
def run(n,maxg,tl=25):
    N=1<<n; M=(1<<N)-1
    ins=[sum(1<<a for a in range(N) if a>>i&1) for i in range(n)]
    best={}
    def note(t,g):
        for u in (t,M^t):
            if u not in best: best[u]=g
    for t in ins+[0]: note(t,0)
    level={frozenset(ins)}
    t0=time.time()
    for g in range(1,maxg+1):
        nxt=set()
        for S in level:
            L=list(S)
            sig=L+[M^x for x in L]
            for i in range(len(sig)):
                for j in range(i+1,len(sig)):
                    v=sig[i]&sig[j]
                    if v in S or (M^v) in S: continue
                    note(v,g); nxt.add(S|{v})
            if time.time()-t0>tl: return best,g,False
        level=nxt
    return best,maxg,True
out={}
for n,mg in ((2,3),(3,4)):
    b,g,ok=run(n,mg)
    hist={}
    for t,c in b.items(): hist[c]=hist.get(c,0)+1
    out[n]={"max_gates_searched":g,"complete":ok,"num_functions_reached":len(b),"total_functions":1<<(1<<n),"hist":hist}
print(json.dumps(out,indent=1))
json.dump(out,open("aig_min_results.json","w"),indent=1)
