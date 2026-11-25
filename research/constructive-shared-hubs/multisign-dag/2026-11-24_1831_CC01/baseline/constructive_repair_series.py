"""Exact frontier recurrence for monotone two-perfect-matching repair.
No dependencies. Run: python constructive_repair_series.py
"""
from itertools import product
from time import perf_counter
import json
from pathlib import Path

def edge(a,b): return tuple(sorted((a,b)))

def verify(E,M):
    V={v for e in E for v in e}
    counts={v:0 for v in V}
    if not M <= E: return False
    for a,b in M: counts[a]+=1; counts[b]+=1
    return all(c==1 for c in counts.values())

def solve(E,A,B,order,seed=None,zero=False,minimum_movement=False):
    """Return exact minimum lexicographic cost, or None. Supplied vertex order.
    Never introduce a shared edge outside A & B; optional seed must be removed.
    zero=True requires no overlap. Cost prioritizes overlap unless minimum_movement=True.
    """
    E,A,B=map(set,(E,A,B)); D=A&B
    assert verify(E,A) and verify(E,B)
    rank={v:i for i,v in enumerate(order)}
    assert set(rank)=={v for e in E for v in e} and len(rank)==len(order)
    es=sorted(E,key=lambda e:(max(rank[v] for v in e),min(rank[v] for v in e)))
    first={}; last={}
    for i,e in enumerate(es):
        for v in e: first.setdefault(v,i);last[v]=i
    # State: two used-incidence bits at each live vertex, in source order.
    dp={(): (0,0)}; live=[]; traces=[]; peak=1; width=0; trials=0; cumulative=1
    for i,(u,v) in enumerate(es):
        e=(u,v); both=sorted(set(live)|{u,v},key=rank.get)
        ix={w:j for j,w in enumerate(both)}
        nextlive=[w for w in both if last[w]>i]
        nxt={}; trace={}; width=max(width,len(both))
        for state,cost in dp.items():
            used=[0]*len(both)
            for w,bits in zip(live,state): used[ix[w]]=bits
            for a,b in product(range(2),repeat=2):
                trials+=1
                if a and b and (zero or e not in D or e==seed): continue
                mask=a+2*b
                if (used[ix[u]]|used[ix[v]])&mask: continue
                z=used.copy();z[ix[u]]|=mask;z[ix[v]]|=mask
                if any(z[ix[w]]!=3 for w in both if last[w]==i): continue
                key=tuple(z[ix[w]] for w in nextlive)
                move=int(bool(a)!=(e in A))+int(bool(b)!=(e in B))
                inc=(move,a*b) if minimum_movement else (a*b,move)
                c=tuple(x+y for x,y in zip(cost,inc))
                if key not in nxt or c<nxt[key]: nxt[key]=c;trace[key]=(state,a,b)
        traces.append(trace);dp=nxt;live=nextlive
        peak=max(peak,len(dp));cumulative+=len(dp)
        if not dp: return None,dict(width=width,peak=peak,trials=trials,cumulative_states=cumulative)
    state=(); cost=dp[state];P=set();Q=set()
    for i in reversed(range(len(es))):
        state,a,b=traces[i][state]
        if a:P.add(es[i])
        if b:Q.add(es[i])
    assert verify(E,P) and verify(E,Q) and P&Q<=D
    assert seed is None or seed not in P&Q
    assert not zero or not P&Q
    return (P,Q),dict(width=width,peak=peak,trials=trials,cumulative_states=cumulative,cost=cost,overlap=len(P&Q),movement=len(A^P)+len(B^Q))

def chain(m):
    E={edge(i,j) for i in range(4) for j in range(i+1,4)}-{(0,1)}
    A={(2,3)}; prev=0;order=[0,2,3]
    for i in range(m):
        a,b,c,d=range(4+4*i,8+4*i)
        E|={edge(a,c),edge(a,d),edge(b,c),edge(b,d),edge(c,d),edge(prev,a)}
        A|={edge(prev,a),edge(c,d)};prev=b
        order.extend([a,c,d,b])
    E.add(edge(prev,1));A.add(edge(prev,1));order.append(1)
    return E,A,A.copy(),order,edge(0,4) if m else (0,1)

def brute_matchings(E):
    V={v for e in E for v in e}; adj={v:[] for v in V}
    for a,b in E:adj[a].append(b);adj[b].append(a)
    def rec(left):
        if not left: yield set();return
        a=min(left)
        for b in adj[a]:
            if b in left:
                for rest in rec(left-{a,b}):yield rest|{edge(a,b)}
    return list(rec(V))

# The saved 8-vertex independently optimal trap, included explicitly for reproducibility.
TRAP_E={(0,1),(0,4),(0,5),(1,2),(1,7),(2,3),(2,6),(3,6),(3,7),(4,5),(4,7),(5,6)}
TRAP_A={(0,4),(1,2),(3,7),(5,6)}
TRAP_B={(0,1),(2,3),(4,7),(5,6)}

def inflate(E,A,B,m):
    """Replace each edge by m two-port diamonds; preserve both matching selections."""
    vertices=sorted({v for e in E for v in e});order=vertices.copy();nextv=max(vertices)+1
    newE=set();newA=set();newB=set();seed=None
    for e in sorted(E):
        u,v=e;prev=u;sa=e in A;sb=e in B
        for i in range(m):
            a,b,c,d=range(nextv,nextv+4);nextv+=4;order.extend([a,c,d,b])
            link=edge(prev,a);internal={edge(a,c),edge(a,d),edge(b,c),edge(b,d),edge(c,d)}
            newE|=internal|{link}
            if sa: newA|={link,edge(c,d)}
            else: newA|={edge(a,c),edge(b,d)}
            if sb:newB|={link,edge(c,d)}
            else:newB|={edge(a,d),edge(b,c)}
            if sa and sb and seed is None:seed=link
            prev=b
        link=edge(prev,v);newE.add(link)
        if sa:newA.add(link)
        if sb:newB.add(link)
        if sa and sb and seed is None:seed=link
    return newE,newA,newB,order,seed


def main():
    results=[]
    for m in [1,2,4,8,16,32,64,128,256,512]:
        E,A,B,order,seed=chain(m);t=perf_counter()
        result,stats=solve(E,A,B,order,seed=seed,minimum_movement=True)
        assert result and stats['movement']>=4*m+1
        full,fs=solve(E,A,B,order,zero=True,minimum_movement=True)
        assert full
        results.append(dict(diamonds=m,vertices=len(order),edges=len(E),initial_overlap=len(A&B),seed_repair=stats,zero_repair=fs,seconds=perf_counter()-t))
    # Independently compare full recurrence with exhaustive matching pairs on small chains.
    checks=0
    for m in [0,1,2]:
        E,A,B,order,seed=chain(m);ms=brute_matchings(E)
        for A in ms:
            for B in ms:
                D=A&B
                for f in sorted(D):
                    expected=min(((len(A^P)+len(B^Q),len(P&Q)) for P in ms for Q in ms if P&Q<=D-{f}),default=None)
                    got,st=solve(E,A,B,order,seed=f,minimum_movement=True)
                    assert (tuple(st['cost']) if got else None)==expected
                    checks+=1
    # Lift the independently optimal trap into a genuine cooperative infinite family.
    base=brute_matchings(TRAP_E);d=len(TRAP_A&TRAP_B)
    assert d==1 and min(len(P&TRAP_B) for P in base)==d and min(len(TRAP_A&Q) for Q in base)==d
    expected=min(len(TRAP_A^P)+len(TRAP_B^Q) for P in base for Q in base if not P&Q)
    trap=[]
    for m in [0,1,2,4,8,16,32,64,128]:
        E,A,B,order,seed=inflate(TRAP_E,TRAP_A,TRAP_B,m);t=perf_counter()
        result,stats=solve(E,A,B,order,seed=seed,minimum_movement=True)
        assert result and stats['overlap']==0 and stats['movement']>=expected*(4*m+1)
        assert len(A&B)==2*m+1
        trap.append(dict(diamonds_per_edge=m,vertices=len(order),edges=len(E),initial_overlap=len(A&B),seed_repair=stats,seconds=perf_counter()-t))
    out=dict(chain_results=results,exhaustive_seed_checks=checks,trap_base_matching_count=len(base),trap_base_minimum_movement=expected,trap_family=trap)
    Path(__file__).with_name('constructive_repair_series_results.json').write_text(json.dumps(out,indent=2))
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
