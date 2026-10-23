"""Exact circuit/formula sizes over B2 with free negation (literals and outputs).
usage: ladder.py n maxg   -- circuit BFS on sets of computed functions (normalized f(0)=0)
       ladder.py n formula -- exact formula leaf-size DP
Each invocation is time-capped (~25 s)."""
import itertools,sys,time
from collections import Counter
n=int(sys.argv[1]); mode=sys.argv[2]; N=1<<n; M=(1<<N)-1
norm=lambda f: f^M if f&1 else f
xs=[norm(sum(((a>>i)&1)<<a for a in range(N)) ) for i in range(n)]
t0=time.time()
if mode=='formula':
    L={0:0}
    for x in xs: L[x]=1
    # leaf-size DP: AND/OR/XOR of normalized pieces with all literal polarities
    byc={1:set(xs)}
    k=1
    while len(L)<(1<<(N-1)) and time.time()-t0<24:
        k+=1; new=set()
        for a in range(1,k):
            for f in byc.get(a,()):
                for g in byc.get(k-a,()):
                    for u in (f,f^M):
                        for v in (g,g^M):
                            for r in (u&v,u^v): 
                                r=norm(r)
                                if r not in L: L[r]=k; new.add(r)
        byc[k]=new; print('leaves',k,len(new),len(L),flush=True)
    print(sorted(Counter(L.values()).items()),'of',1<<(N-1),'normalized fns')
else:
    G=int(mode); base=frozenset(xs+[0])
    best={f:0 for f in base}
    level={base}
    for g in range(1,G+1):
        nxt=set()
        for S in level:
            Lst=list(S)
            for a,b in itertools.combinations(Lst,2):
                for u in (a,a^M):
                    for v in (b,b^M):
                        for r in (u&v,u^v):
                            r=norm(r)
                            if r in S: continue
                            nxt.add(S|{r})
                            if r not in best: best[r]=g
            if time.time()-t0>24: print('TIMECAP at level',g); break
        level=nxt
        print('g',g,'states',len(level),'fns<=g',len(best),round(time.time()-t0,1),flush=True)
        if time.time()-t0>24: break
    print(sorted(Counter(best.values()).items()),'of',1<<(N-1),'normalized fns')
