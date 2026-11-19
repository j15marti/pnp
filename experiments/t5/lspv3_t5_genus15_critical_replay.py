#!/usr/bin/env python3
"""Source-pinned T5 edge-critical structure and SAT-deletion audit; Python stdlib."""
from collections import Counter, deque
from hashlib import sha256
from math import ceil
import json, sys
S={1,3}

def audit(path):
    raw=open(path,'rb').read(); lines=raw.decode('ascii').splitlines()
    head=lines[0].split(); assert head[:2]==['p','t5']
    n,m=map(int,head[2:]); arcs=[tuple(map(int,line.split()[1:])) for line in lines if line.startswith('a ')]
    assert len(arcs)==m and len(set(map(frozenset,arcs)))==m
    adj=[set() for _ in range(n)]
    for u,v in arcs: adj[u].add(v);adj[v].add(u)
    def reachable(omit=-1):
        start=next(x for x in range(n) if x!=omit);seen={start};q=[start]
        for x in q:
            for y in adj[x]:
                if y!=omit and y not in seen:seen.add(y);q.append(y)
        return len(seen)==n-(omit>=0)
    assert reachable() and all(reachable(x) for x in range(n))
    girth=10**9
    for root in range(n):
        d=[-1]*n;p=[-1]*n;d[root]=0;q=deque([root])
        while q:
            u=q.popleft()
            for v in adj[u]:
                if d[v]<0:d[v]=d[u]+1;p[v]=u;q.append(v)
                elif p[u]!=v:girth=min(girth,d[u]+d[v]+1)
    B={i for i in range(n) if len(adj[i])>=3};used=set();paths=[]
    for u in sorted(B):
        for v in sorted(adj[u]):
            if frozenset((u,v)) in used:continue
            path=[u,v];used.add(frozenset((u,v)))
            while path[-1] not in B:
                x=path[-1]; nxt=next(z for z in adj[x] if z!=path[-2])
                used.add(frozenset((x,nxt)));path.append(nxt)
            paths.append(path)
    assert len(used)==m
    lens=Counter(len(p)-1 for p in paths); weights=Counter()
    for p in paths:
        assert len(p)-1<=3
        w=4-(len(p)-1);weights[p[0]]+=w;weights[p[-1]]+=w
    b=len(B);beta=m-n+1
    assert len(paths)-b+1==beta and min(weights.values())>=5
    assert n<=6*(beta-1) and m<=7*(beta-1)
    def sat(edges):
        calls=0
        def ac(dom):
            again=True
            while again:
                again=False
                for u,v in edges:
                    a,b=dom[u],dom[v]
                    aa=sum(1<<x for x in range(5) if a&(1<<x) and any(b&(1<<y) and (y-x)%5 in S for y in range(5)))
                    bb=sum(1<<y for y in range(5) if b&(1<<y) and any(aa&(1<<x) and (y-x)%5 in S for x in range(5)))
                    if not aa or not bb:return False
                    if aa!=a:dom[u]=aa;again=True
                    if bb!=b:dom[v]=bb;again=True
            return True
        def rec(dom):
            nonlocal calls
            calls+=1
            if not ac(dom):return None
            undec=[i for i in range(n) if dom[i].bit_count()>1]
            if not undec:return [x.bit_length()-1 for x in dom]
            v=min(undec,key=lambda i:(dom[i].bit_count(),i))
            for color in range(5):
                if dom[v]&(1<<color):
                    d=dom[:];d[v]=1<<color
                    ans=rec(d)
                    if ans is not None:return ans
            return None
        d=[31]*n;d[0]=1
        return rec(d),calls
    bad,unsat_calls=sat(arcs);assert bad is None
    witnesses=[]
    for i,(u,v) in enumerate(arcs):
        subset=arcs[:i]+arcs[i+1:];w,k=sat(subset)
        assert w is not None and w[0]==0
        assert all((w[y]-w[x])%5 in S for x,y in subset)
        assert (w[v]-w[u])%5 not in S
        witnesses.append({'deleted_index':i,'witness':w,'search_calls':k})
    # Euler: orientable genus >= (beta+1)/2 - m/girth.
    return {'source_sha256':sha256(raw).hexdigest(),'n':n,'m':m,'girth':girth,
        'beta':beta,'branch_vertices':b,'threads':dict(lens),
        'min_weighted_branch_degree':min(weights.values()),
        'cycle_rank_linear_inequality':{'n_le_6_beta_minus_6':True,'m_le_7_beta_minus_7':True},
        'euler_orientable_genus_lower':ceil((beta+1)/2-m/girth),
        'unsat_search_calls':unsat_calls,'all_edge_deletions_sat':True,
        'max_deletion_search_calls':max(x['search_calls'] for x in witnesses),
        'witnesses':witnesses}

if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: script.py SOURCE.t5 OUTPUT.json')
    result=audit(sys.argv[1]);open(sys.argv[2],'w').write(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='witnesses'},sort_keys=True))
