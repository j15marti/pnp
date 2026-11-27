"""Exact multi-defect acquisition and joint enumeration; imports shared_and_tseitin."""
from shared_and_tseitin import *


def min_cover(edges):
    """Iterative depth limit, no supplied cover; return one minimum cover and node count."""
    calls=0
    def dfs(E,k):
        nonlocal calls
        calls+=1
        if not E:return set()
        if not k:return None
        a,b=E[0]
        for x in (a,b):
            r=dfs([e for e in E if x not in e],k-1)
            if r is not None:return r|{x}
        return None
    for k in range(len(edges)+1):
        r=dfs(edges,k)
        if r is not None:return r,calls
    raise AssertionError


def decide(F,n):
    # Reconstruct and authenticate the block decomposition.
    adj=[{i} for i in range(1,n+1)]
    for C in F:
        V=set(map(abs,C))
        if not V:return False,0,0,0
        for i in V:adj[i-1].update(V)
    twin=defaultdict(list)
    for i,V in enumerate(adj,1):twin[frozenset(V)].append(i)
    pairs=list(twin.values())
    if any(len(p)!=2 for p in pairs):return None,None,0,0
    owner={i:j for j,p in enumerate(pairs) for i in p}
    groups=defaultdict(list)
    for C in F:
        key=tuple(sorted({owner[abs(l)] for l in C}))
        if len(key)!=3:return None,None,0,0
        groups[key].append(C)
    keys=list(groups);inc=defaultdict(list)
    for v,key in enumerate(keys):
        for j in key:inc[j].append(v)
    if any(len(inc[j])!=2 for j in range(len(pairs))):return None,None,0,0
    tables=[];facts=[];words=list(product(range(4),repeat=3))
    for key in keys:
        T={}
        for z in words:
            x={i:(t>>k)&1 for j,t in zip(key,z) for k,i in enumerate(pairs[j])}
            T[z]=int(not all(any(bool(x[abs(l)])==(l>0) for l in C) for C in groups[key]))
        tables.append(T);c=T[0,0,0];fs={}
        for k,j in enumerate(key):
            fs[j]=tuple(T[tuple(t if i==k else 0 for i in range(3))]^c for t in range(4))
        facts.append((c,fs) if all(len(set(f))==2 for f in fs.values()) and all(T[z]==(c^fs[key[0]][z[0]]^fs[key[1]][z[1]]^fs[key[2]][z[2]]) for z in words) else None)
    forced={v for v,f in enumerate(facts) if f is None}
    conflict=[]
    for j,(u,v) in inc.items():
        if u not in forced and v not in forced and facts[u][1][j]!=facts[v][1][j]:conflict.append((u,v))
    cover,calls=min_cover(conflict);D=forced|cover
    functions={};rows=[]
    for v,key in enumerate(keys):
        if v in D:continue
        c,fs=facts[v]
        for j,f in fs.items():
            assert j not in functions or functions[j]==f
            functions[j]=f
        rows.append((sum(1<<j for j in key),c))
    J=sorted({j for v in D for j in keys[v]});tried=0
    for vals in product(range(4),repeat=len(J)):
        tried+=1;pins=dict(zip(J,vals))
        if any(tables[v][tuple(pins[j] for j in keys[v])] for v in D):continue
        rr=rows+[(1<<j,functions[j][t]) for j,t in pins.items() if j in functions]
        y=gf2(rr,len(pairs))
        if y is None:continue
        x=[0]*n
        for j,p in enumerate(pairs):
            t=pins[j] if j in pins else functions[j].index((y>>j)&1)
            for k,i in enumerate(p):x[i-1]=(t>>k)&1
        assert ok(F,x)
        return tuple(x),len(D),calls,tried
    return False,len(D),calls,tried


def main():
    rng=random.Random(2026112709);hist=defaultdict(int);largest=0;mx=0
    edges=list(combinations(range(4),2));n=12
    for rep in range(100):
        G=lift(tseitin(edges,[(rep//4)%2,0,0,0]));q=rep%4
        for i in rng.sample(range(len(G)),q):
            if rep%3==0:
                C=list(G[i]);j=rng.randrange(len(C));C[j]*=-1;G[i]=tuple(C)
            else:G[i]=None
        G=transform([C for C in G if C is not None],n,rng)
        b=brute(G,n);r,d,c,t=decide(G,n)
        assert r is not None and (r is False)==(b is None)
        hist[(d,'UNSAT' if r is False else 'SAT')]+=1
        largest=max(largest,t);mx=max(mx,c)
    print('100 independent brute controls',sorted(hist.items()),'max enumeration',largest,'max cover nodes',mx)
    hist2=defaultdict(int);mx2=0
    for rep in range(40):
        charges=[rep%2,0,0,0];G=[]
        for v in range(4):
            C=[];es=[i+1 for i,e in enumerate(edges) if v in e]
            for z in product((0,1),repeat=3):
                if sum(z)%2!=charges[v]: C.append(tuple(-i if b else i for i,b in zip(es,z)))
            H=lift(C)
            if v in (0,1) and (v==0 or rep%3==0):
                a=2*rng.choice(es)-1;H=[tuple(-l if abs(l)==a else l for l in c) for c in H]
            G+=H
        G=transform(G,n,rng);b=brute(G,n);r,d,c,t=decide(G,n)
        assert r is not None and (r is False)==(b is None)
        hist2[(d,'UNSAT' if r is False else 'SAT')]+=1;mx2=max(mx2,c)
    print('40 inconsistent-function controls',sorted(hist2.items()),'max cover nodes',mx2)
    # Independently verify minimum-cover acquisition on every graph on five vertices.
    E=list(combinations(range(5),2))
    for mask in range(1<<len(E)):
        edges=[e for i,e in enumerate(E) if mask>>i&1];C,_=min_cover(edges)
        assert all(set(e)&C for e in edges)
        k=next(k for k in range(6) if any(all(set(e)&set(S) for e in edges) for S in combinations(range(5),k)))
        assert len(C)==k
    print('1024 exact minimum cover controls PASS')
if __name__=='__main__':main()
