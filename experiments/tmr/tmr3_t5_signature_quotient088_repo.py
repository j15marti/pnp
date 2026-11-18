"""TMR-3/088 compact executable, exact T5 counts and signed Kpq recognition.

Usage: from tmr3_t5_signature_quotient088_repo import solve
       answer = solve(n, arcs)  # arcs is list of (source,target)
Any non-Kpq graph is processed by an exact exponential fallback.
"""
from collections import defaultdict
from itertools import product


def beat(x,y):
    return (y-x)%5 in (1,3)


def fallback(n,arcs):
    if any(u==v for u,v in arcs):
        return 0
    out=[[] for _ in range(n)]
    for u,v in arcs:
        out[u].append(v)
    x=[None]*n
    def dfs(i):
        if i==n:
            return 1
        z=0
        for a in range(5):
            x[i]=a
            if all(x[j] is None or beat(a,x[j]) for j in out[i]) and all(x[j] is None or beat(x[j],a) for j in range(i) if i in out[j]):
                z+=dfs(i+1)
        x[i]=None
        return z
    return dfs(0)


def recognize(n,arcs):
    if n<2 or len(set(arcs))!=len(arcs) or any(u<0 or v<0 or u>=n or v>=n or u==v for u,v in arcs):
        return None
    A=set(arcs)
    if any((v,u) in A for u,v in arcs):
        return None
    G=[set() for _ in range(n)]
    for u,v in arcs:
        G[u].add(v)
        G[v].add(u)
    side=[-1]*n
    side[0]=0
    queue=[0]
    for u in queue:
        for v in G[u]:
            if side[v]==-1:
                side[v]=1-side[u]
                queue.append(v)
            elif side[v]==side[u]:
                return None
    if len(queue)!=n:
        return None
    U=[i for i in range(n) if side[i]==0]
    V=[i for i in range(n) if side[i]==1]
    if not V or len(arcs)!=len(U)*len(V):
        return None
    return U,V,A


def types(U,V,A):
    groups=defaultdict(list)
    for u in U:
        groups[tuple((u,v) in A for v in V)].append(u)
    return groups


def orbits(a):
    masks=[S for S in range(1,32) if S.bit_count()<=2]
    def shift(S,d):
        return sum(1<<((x+d)%5) for x in range(5) if S & (1<<x))
    seen=set()
    for row in product(masks,repeat=a):
        if row not in seen:
            for d in range(5):
                seen.add(tuple(shift(S,d) for S in row))
            yield row


def count_recognized(U,V,A):
    LU=types(U,V,A)
    LV=types(V,U,A)
    a,b=len(LU),len(LV)
    if a+b>5:
        return 0
    if a<=b:
        smaller,other,groups=U,V,LU
    else:
        smaller,other,groups=V,U,LV
    assert len(groups)<=2
    representatives=[u[0] for u in groups.values()]
    sizes=[len(u) for u in groups.values()]
    result=0
    for support in orbits(len(groups)):
        term=5  # orbit size under cyclic translation
        for S,m in zip(support,sizes):
            term*=1 if S.bit_count()==1 else (2**m-2)
        if not term:
            continue
        for v in other:
            choices=0
            for y in range(5):
                if all(all(beat(x,y) if (u,v) in A else beat(y,x)
                           for x in range(5) if S & (1<<x))
                       for u,S in zip(representatives,support)):
                    choices+=1
            term*=choices
            if term==0:
                break
        result+=term
    return result


def solve(n,arcs):
    arcs=list(arcs)
    if any(not isinstance(u,int) or not isinstance(v,int) or u<0 or v<0 or u>=n or v>=n for u,v in arcs):
        raise ValueError('Vertex indices must be in [0,n)')
    r=recognize(n,arcs)
    return fallback(n,arcs) if r is None else count_recognized(*r)


if __name__=='__main__':
    from itertools import product
    checks=0
    for p,q in ((1,1),(1,4),(2,2),(2,3),(3,3)):
        for bits in product((0,1),repeat=p*q):
            arcs=[(i,p+j) if bits[i*q+j] else (p+j,i)
                  for i in range(p) for j in range(q)]
            assert solve(p+q,arcs)==fallback(p+q,arcs)
            checks+=1
    print({'checks':checks,'failures':0})
