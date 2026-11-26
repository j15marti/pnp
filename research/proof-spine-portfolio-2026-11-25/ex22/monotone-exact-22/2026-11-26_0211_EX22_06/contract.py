from audit import chain,lift,valid
from itertools import combinations
import json

def discover(n,H):
    # H is obtained from actual EX22 clauses by eliminating private completions.
    cs={tuple(sorted(c)):j for j,c in enumerate(H)}; adj=[set() for _ in range(n)]
    for c in H:
        for a,b in combinations(c,2):adj[a].add(b);adj[b].add(a)
    full=[]; near=[]; trials=0
    for a in range(n):
        for b,c,d in combinations(sorted(v for v in adj[a] if v>a),3):
            O=(a,b,c,d)
            if not all(y in adj[x] for x,y in combinations(O,2)):continue
            common=set.intersection(*(adj[x] for x in O))-set(O)
            for L in combinations(sorted(common),3):
                trials+=1
                ids=[]
                for u,v in combinations(O,2):
                    hits=[cs[tuple(sorted((u,v,t)))] for t in L if tuple(sorted((u,v,t))) in cs]
                    if len(hits)!=1:break
                    ids.extend(hits)
                if len(ids)!=6:continue
                # Each anchor must be used twice; linearity ensures disjoint pair matching.
                if any(sum(t in H[j] for j in ids)!=2 for t in L):continue
                key=tuple(sorted(L))
                if key in cs:full.append((L,O,ids+[cs[key]]));continue
                if all(all(j in ids for j,h in enumerate(H) if v in h) for v in O):near.append((L,O,ids))
    return full,near,trials

def solve(C,N):
    deg=[0]*N
    for c in C:
        for x in c:deg[x]+=1
    H=[]; priv=[]
    for c in C:
        p=next((v for v in c if deg[v]==1),None)
        if p is None:return 'UNKNOWN',0,0
        priv.append(p);H.append(tuple(v for v in c if v!=p))
    if len({tuple(sorted(p)) for c in H for p in combinations(c,2)})!=3*len(H):return 'UNKNOWN',0,0
    full,near,trials=discover(N,H)
    if full:return 'UNSAT',trials,0
    # Exact regional contraction terminal when every clause has a private exterior group.
    covered=set(); used=set(); regions=[]
    for L,O,ids in sorted(near):
        if covered.intersection(ids) or used.intersection(L+O) or any(v in O for l,o in regions for v in l):continue
        covered.update(ids);used.update(O);regions.append((L,O))
    if len(covered)!=len(H):return 'UNKNOWN',trials,len(regions)
    x=[0]*N
    for L,O in regions:
        for v in O:x[v]=1
    for p,c in zip(priv,H):x[p]=2-sum(x[v] for v in c)
    assert valid(x,C)
    return 'SAT',trials,len(regions)
if __name__=='__main__':
    out=[]
    for k in (1,2,4,8,16,32,64):
        for bad in (False,True):
            n,H,B=chain(k,bad);C=[c+(n+j,) for j,c in enumerate(H)];N=n+len(H)
            # reverse variable numbering and clause order to remove block-order hints
            C=[tuple(N-1-v for v in c) for c in C[::-1]]
            ans,trials,regions=solve(C,N);assert ans==('UNSAT' if bad else 'SAT')
            out.append(dict(k=k,bad=bad,physical=N,result=ans,pattern_trials=trials,regions=regions))
    print(json.dumps(out,indent=2))
