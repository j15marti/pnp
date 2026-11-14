"""Brackets for minimum DAG-Resolution length W_Res(F) on small MU families.
Lower: F minimally unsatisfiable => every axiom is a leaf of any refutation
       DAG (else a proper subset would be refuted), and a connected binary DAG
       with m leaves has >= m-1 internal nodes => W_Res(F) >= m-1.
Upper: explicit DP variable-elimination refutation, best over sampled orders,
       counting only derived clauses that are ancestors of the empty clause.
Every upper-bound proof is replayed by an independent checker. <30s per run."""
import itertools, json, random, sys, time
sys.path.insert(0,'.')
from shortest_res import INST, php, tseitin
from pysat.solvers import Glucose4

def is_mu(C):
    with Glucose4(bootstrap_with=C) as s:
        if s.solve(): return False
    for i in range(len(C)):
        with Glucose4(bootstrap_with=C[:i]+C[i+1:]) as s:
            if not s.solve(): return False
    return True

def dp_proof(C,order):
    nodes=[frozenset(c) for c in C]; par={}
    live=set(range(len(C)))
    for v in order:
        pos=[i for i in live if v in nodes[i]]; neg=[i for i in live if -v in nodes[i]]
        live-=set(pos)|set(neg)
        for a in pos:
            for b in neg:
                R=(nodes[a]-{v})|(nodes[b]-{-v})
                if any(-x in R for x in R): continue
                if any(nodes[k]<=R for k in live): continue   # subsumed
                nodes.append(R); k=len(nodes)-1; par[k]=(a,b,v); live.add(k)
                if not R:
                    return nodes,par,k
                live={j for j in live if j==k or not R<=nodes[j]}
    return None

def used_steps(nodes,par,root,m):
    st=[root]; seen=set()
    while st:
        k=st.pop()
        if k in seen or k<m: continue
        seen.add(k); st+= list(par[k][:2])
    return sorted(seen)

def check(C,nodes,par,steps):
    have={i:frozenset(c) for i,c in enumerate(C)}
    for k in steps:
        a,b,v=par[k]
        A,B=have[a],have[b]
        assert v in A and -v in B
        assert (A-{v})|(B-{-v})==nodes[k]
        have[k]=nodes[k]
    return len(have[steps[-1]])==0

name=sys.argv[1]; budget=float(sys.argv[2]) if len(sys.argv)>2 else 20
n,C=INST[name](); m=len(C); t0=time.time(); best=None; tried=0
mu=is_mu(C)
orders=itertools.permutations(range(1,n+1)) if n<=7 else None
rng=random.Random(2026)
while time.time()-t0<budget:
    if orders is not None:
        o=next(orders,None)
        if o is None: break
    else:
        o=list(range(1,n+1)); rng.shuffle(o)
    tried+=1
    r=dp_proof(C,o)
    if r is None: continue
    nodes,par,root=r; st=used_steps(nodes,par,root,m)
    if best is None or len(st)<best[0]:
        assert check(C,nodes,par,st); best=(len(st),list(o))
rec={'inst':name,'n':n,'m':m,'MU':mu,'lower_m_minus_1':m-1 if mu else None,
     'dp_upper':best[0],'best_order':best[1],'orders_tried':tried,
     'exhaustive_orders':orders is not None and tried>=1 and n<=7 and time.time()-t0<budget,'sec':round(time.time()-t0,1)}
print(json.dumps(rec)); open('brackets.jsonl','a').write(json.dumps(rec)+'\n')
