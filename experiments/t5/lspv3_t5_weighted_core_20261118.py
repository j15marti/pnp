#!/usr/bin/env python3
"""T5 weighted-thread-core audit. Run inside a j15marti/pnp checkout."""
import hashlib, itertools, json
from collections import Counter
from pathlib import Path
R=lambda a,b:(b-a)%5 in (1,3)
SOURCE='research/agents/tmr-2/certificates/2026-11-18_0112_TMR2_T5_GIRTH8_33_NO079.t5'
EXPECTED='0d82de7d49547e71bc2959c6c1760633fd4dfd935ef33769ad9ddb38916efbac'

def allowed(word):
    s={0}
    for ch in word:
        s={(x+y)%5 for x in s for y in ((1,3) if ch=='+' else (2,4))}
    return frozenset(s)

def source9():
    paths=[([0,2,1],'++'),([0,3,4,1],'+++'),([0,5,6,1],'++-'),([0,7,8,1],'---')]
    return 9,[(a,b) if c=='+' else (b,a) for p,w in paths for a,b,c in zip(p,p[1:],w)]

def source33():
    raw=Path(SOURCE).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==EXPECTED
    lines=raw.decode().splitlines()
    n,m=map(int,lines[0].split()[2:])
    arcs=[tuple(map(int,s.split()[1:])) for s in lines if s.startswith('a ')]
    assert len(arcs)==m
    return n,arcs

def core(n,arcs):
    adj=[set() for _ in range(n)]
    for u,v in arcs:adj[u].add(v);adj[v].add(u)
    B={v for v in range(n) if len(adj[v])>=3};seen=set();paths=[]
    for a in sorted(B):
        for v in sorted(adj[a]):
            if frozenset((a,v)) in seen:continue
            p=[a,v];seen.add(frozenset((a,v)))
            while p[-1] not in B:
                u=p[-1];assert len(adj[u])==2
                w=next(w for w in adj[u] if w!=p[-2])
                p.append(w);seen.add(frozenset((u,w)))
            paths.append(p)
    assert len(seen)==len(arcs)
    weights={v:0 for v in B}
    for p in paths:
        q=max(0,4-(len(p)-1))
        weights[p[0]]+=q;weights[p[-1]]+=q
    return paths,weights

def witness(n,arcs):
    ds=[31]*n;ds[0]=1;inc=[[] for _ in range(n)]
    for u,v in arcs:inc[u].append((v,True));inc[v].append((u,False))
    calls=0
    def solve(dom):
        nonlocal calls
        calls+=1;changed=True
        while changed:
            changed=False
            for u in range(n):
                for v,forward in inc[u]:
                    z=0
                    for a in range(5):
                        if dom[u]>>a&1 and any(dom[v]>>b&1 and (R(a,b) if forward else R(b,a)) for b in range(5)):
                            z|=1<<a
                    if not z:return None
                    if z!=dom[u]:dom[u]=z;changed=True
        q=[i for i in range(n) if dom[i].bit_count()>1]
        if not q:return [d.bit_length()-1 for d in dom]
        u=min(q,key=lambda x:(dom[x].bit_count(),-len(inc[x]),x))
        for a in range(5):
            if dom[u]>>a&1:
                nxt=dom.copy();nxt[u]=1<<a
                ans=solve(nxt)
                if ans is not None:return ans
        return None
    ans=solve(ds)
    assert ans is None or all(R(ans[u],ans[v]) for u,v in arcs)
    return ans,calls

def peel(paths,B,deleted=None):
    d={v:0 for v in B};inc={v:[] for v in B}
    for p in paths:
        if deleted is not None and any(frozenset((u,v))==frozenset(deleted) for u,v in zip(p,p[1:])):continue
        u,v=p[0],p[-1];q=max(0,4-(len(p)-1))
        d[u]+=q;d[v]+=q;inc[u].append((v,q));inc[v].append((u,q))
    live=set(B)
    while True:
        eligible=[u for u in live if d[u]<=4]
        if not eligible:break
        u=min(eligible);live.remove(u)
        for v,q in inc[u]:
            if v in live:d[v]-=q
    return len(live)

def audit(n,arcs):
    paths,weights=core(n,arcs)
    no,nodes=witness(n,arcs);assert no is None
    assert min(weights.values())>=5
    calls=[];res=[]
    for e in arcs:
        w,t=witness(n,[a for a in arcs if a!=e])
        assert w is not None and not R(w[e[0]],w[e[1]])
        calls.append(t);res.append(peel(paths,weights,e))
    return dict(n=n,m=len(arcs),b=len(weights),beta=len(arcs)-n+1,
      lengths=dict(Counter(len(p)-1 for p in paths)),weight_min=min(weights.values()),
      weight_hist=dict(Counter(weights.values())),unsat_search_nodes=nodes,
      deletions=len(calls),max_deletion_search_nodes=max(calls),
      deletion_weight5_residual_hist=dict(Counter(res)))

def main():
    relations={allowed(w) for L in (1,2,3) for w in itertools.product('+-',repeat=L)}
    assert len(relations)==9
    U=set(range(5));irred=[]
    for bits in itertools.product((0,1),repeat=9):
        seq=[set(r) for r,b in zip(sorted(relations,key=lambda x:(len(x),tuple(sorted(x)))),bits) if b]
        if seq:
            meet=set.intersection(*seq)
            if all((set.intersection(*(seq[:i]+seq[i+1:])) if len(seq)>1 else U)!=meet for i in range(len(seq))):
                irred.append(len(seq))
    assert max(irred)==4
    for bits in itertools.product('+-',repeat=12):
        rows=[allowed(bits[i:i+3]) for i in (0,3,6,9)]
        assert set.intersection(*(set(r) for r in rows))
    result=dict(relation_types=9,irredundant_max=4,long_only_4bundle_SAT=4096,
                case9=audit(*source9()),case33=audit(*source33()),source33_sha256=EXPECTED)
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
