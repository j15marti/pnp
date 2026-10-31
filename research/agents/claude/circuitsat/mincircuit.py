# Exact min #binary gates (all 10 non-degenerate 2-input gates; free inputs, no free NOT beyond gate choice)
# over B2 for n-variable functions, by exhaustive level search with set-dedupe. Wires = 2*gates.
import sys, json, itertools, time
n=int(sys.argv[1]); K=int(sys.argv[2])
N=1<<n; M=(1<<N)-1
ins=[]
for i in range(n):
    t=0
    for a in range(N):
        if (a>>i)&1: t|=1<<a
    ins.append(t)
def gates(x,y):
    nx,ny=M^x,M^y
    return {x&y,nx&y,x&ny,nx&ny,x^y,M^(x^y), (x|y),(nx|y),(x|ny),(nx|ny)}  # AND-family and XOR
# note OR family equals negated AND family; included so output negation is free
best={}
for t in ins: best[t]=0; best[M^t]=0
best[0]=0; best[M]=0
level=[frozenset(ins)]
seen={frozenset(ins)}
t0=time.time()
for k in range(1,K+1):
    nxt=set()
    for S in level:
        L=sorted(S)
        for x,y in itertools.combinations(L,2):
            for g in gates(x,y):
                if g in S or (g&M)==g and False: continue
                F=S|{g}
                if F in seen: continue
                seen.add(F); nxt.add(F)
                for h in (g,M^g):
                    if h not in best: best[h]=k
    level=list(nxt)
    print(k,len(level),len(best),round(time.time()-t0,1),file=sys.stderr)
    if time.time()-t0>22 or len(best)==(1<<N): K=k;break
from collections import Counter
c=Counter(best.values())
out={"n":n,"searched_up_to_gates":K,"num_functions":1<<N,"found":len(best),"count_by_cost":dict(sorted(c.items())),"not_found_so_costs_ge":K+1,"not_found":(1<<N)-len(best)}
print(json.dumps(out))
json.dump(out,open(f"mincircuit_n{n}.json","w"),indent=1)
