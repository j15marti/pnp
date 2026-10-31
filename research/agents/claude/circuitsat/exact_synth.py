# Exact min-gate (fan-in-2, full basis B2) circuit size for all n-var functions, n<=3.
# BFS over sets of computed signals (functions normalized up to complement; B2 closed under negation).
# Wires = 2*gates (all gates fan-in 2). Runtime target <30s.
import sys, json, itertools, time
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
def norm(f): return min(f,M^f)
inputs=[sum(((i>>v)&1)<<i for i in range(N)) for v in range(n)]
start=frozenset(norm(x) for x in inputs)
const=norm(0)
def gates(a,b):
    # nondegenerate binary ops up to output complement: AND-type (4 neg patterns) and XOR
    A,B=a,b
    out={A&B,A&(M^B),(M^A)&B,(M^A)&(M^B),A^B}
    return {norm(x) for x in out}
best={norm(x):0 for x in inputs}; best[const]=0
level=[start]; seen={start}
t0=time.time(); g=0
while len(best)<(1<<(N-1)) +0 and level and time.time()-t0<25:
    g+=1; nxt=[]
    for st in level:
        sl=list(st)
        for a,b in itertools.combinations(sl,2):
            for f in gates(a,b):
                if f in st: continue
                ns=st|{f}
                if ns in seen: continue
                seen.add(ns); nxt.append(ns)
                if f not in best: best[f]=g
    level=nxt; print("gates",g,"states",len(level),"covered",len(best),"of",1<<(N-1),file=sys.stderr)
dist={}
for f,v in best.items(): dist[v]=dist.get(v,0)+1
res={"n":n,"complete":len(best)==(1<<(N-1)),"max_gates":max(best.values()),"dist_up_to_complement":dist,"seconds":round(time.time()-t0,1)}
print(json.dumps(res)); json.dump(res,open(f"exact_synth_n{n}.json","w"))
