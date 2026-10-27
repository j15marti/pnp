"""Claude Circuit-SAT ladder: exhaustive AIG enumeration (fan-in 2 AND, free edge negation).
For each (n,k): over all circuits with k gates, n inputs, output=last gate, every gate used:
  - min gates for unique-SAT ("needle") circuits
  - UNSAT circuits and the minimal ternary-propagation split depth d needed to refute
Usage: ladder.py n k   (each call finishes in well under 30 s for the listed sizes)."""
import sys, json, itertools
from functools import lru_cache
n=int(sys.argv[1]); k=int(sys.argv[2])
def ev(g,assign):  # assign: tuple of 0/1/2(X)
    v=list(assign)
    for (a,pa,b,pb) in g:
        def lit(i,p):
            x=v[i]
            return x if x==2 else x^p
        x=lit(a,pa); y=lit(b,pb)
        v.append(0 if (x==0 or y==0) else (1 if x==1 and y==1 else 2))
    return v[-1]
def depth(g):
    @lru_cache(None)
    def d(assign):
        r=ev(g,assign)
        if r==0: return 0
        free=[i for i,x in enumerate(assign) if x==2]
        if not free or r==1: return 99
        best=99
        for i in free:
            a0=assign[:i]+(0,)+assign[i+1:]; a1=assign[:i]+(1,)+assign[i+1:]
            best=min(best,1+max(d(a0),d(a1)))
        return best
    return d(tuple([2]*n))
res={'n':n,'k':k,'circuits':0,'sat_counts':{},'needle':0,'unsat':0,'unsat_by_depth':{},'min_wires_unsat_depth':{}}
pairs=[[(a,b) for a in range(n+i) for b in range(a+1,n+i)] for i in range(k)]
def rec(i,g):
    if i==k:
        used=set()
        for (a,_,b,_) in g: used.add(a);used.add(b)
        if any((n+j) not in used for j in range(k-1)): return
        if any(x not in used for x in range(n)): return
        res['circuits']+=1
        cnt=sum(1 for asg in itertools.product((0,1),repeat=n) if ev(g,asg)==1)
        res['sat_counts'][cnt]=res['sat_counts'].get(cnt,0)+1
        if cnt==1: res['needle']+=1
        if cnt==0:
            res['unsat']+=1
            dd=depth(g)
            res['unsat_by_depth'][dd]=res['unsat_by_depth'].get(dd,0)+1
        return
    for (a,b) in pairs[i]:
        for pa in (0,1):
            for pb in (0,1):
                rec(i+1,g+[(a,pa,b,pb)])
if k>=1: rec(0,[])
print(json.dumps(res))
