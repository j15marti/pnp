#!/usr/bin/env python3
import itertools, collections, json

def is_minimal_hall(neigh,h):
    s=len(neigh)
    full=set().union(*(set(neigh[p]) for p in range(s)))
    if len(full)!=s-1: return False
    for r in range(1,s):
        for T in itertools.combinations(range(s),r):
            N=set().union(*(set(neigh[p]) for p in T))
            if len(N)<len(T): return False
    return True

def perfect_matchings(neigh,removed,h):
    ps=[p for p in range(len(neigh)) if p!=removed]
    out=[]
    for perm in itertools.permutations(range(h)):
        if all(perm[i] in neigh[p] for i,p in enumerate(ps)):
            out.append(dict(zip(ps,perm)))
    return out

def q_distribution(neigh,h):
    s=len(neigh); d=len(neigh[0])
    Q=collections.Counter()
    for r in range(s):
        Ms=perfect_matchings(neigh,r,h)
        assert Ms
        for M in Ms:
            w0=1/(s*len(Ms)*d*(d-1))
            for a in neigh[r]:
                for b in neigh[r]:
                    if a==b: continue
                    tabs=[]
                    for p in range(s):
                        if p==r: tabs.append((a,b))
                        else: tabs.append((M[p],M[p]))
                    Q[tuple(tabs)]+=w0
    assert abs(sum(Q.values())-1)<1e-10
    return Q

def audit(neigh,h):
    assert is_minimal_hall(neigh,h)
    s=len(neigh); d=len(neigh[0]); B=3*s*d/8
    Q=q_distribution(neigh,h)
    pats=list(itertools.product([0,1],repeat=2))
    checks=0; maxlhs=0; by_size=collections.defaultdict(float)
    for p,q in itertools.combinations(range(s),2):
        for mask in range(1,16):
            P=[pats[i] for i in range(4) if mask>>i&1]
            ap=len(P)/4
            qp=0
            for tabs,w in Q.items():
                if all(tabs[p][i]==tabs[q][j] for i,j in P):
                    qp+=w
            lhs=ap+B*qp
            checks+=1
            maxlhs=max(maxlhs,lhs)
            by_size[len(P)]=max(by_size[len(P)],lhs)
            assert lhs<=1+1e-10
    return {'s':s,'h':h,'d':d,'B':B,'Q_support':len(Q),
            'checks':checks,'max_lhs':maxlhs,'max_by_pattern_size':dict(by_size)}

examples=[
    [(0,1),(0,1),(0,1)],
    [(0,1),(0,1),(0,2),(0,2)],
    [(0,1,2),(0,1,2),(0,1,2),(0,1,2)],
    [(0,1),(0,1),(0,2),(0,3),(2,3)],
]
results=[]
for N in examples:
    h=max(max(x) for x in N)+1
    results.append(audit(N,h))
out={'status':'PASS','examples':results,'total_rectangle_pattern_checks':sum(r['checks'] for r in results)}
print(json.dumps(out,indent=2,sort_keys=True))
