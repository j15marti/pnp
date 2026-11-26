"""CPS18 greatest local safe overwrite; extracted from executed retract18.py.
Full executable source audit and raw output in P3CPS18_decision_retraction.tar.gz.
"""
def masks(P,R,a):
    D={frozenset(v for v,b in zip(P,w) if b!=a[v]) for w in R}
    assert D
    out=[]
    for d in sorted(D,key=lambda d:(len(d),tuple(sorted(d)))):
        sub={e for e in D if e<=d}
        local=[d-e for e in sub if all((z-(d-e)) in sub for z in sub)]
        assert frozenset() in local
        out.append((d,local))
    return out

def fixed_point(M,allowed):
    S=set(allowed);rounds=0
    while True:
        rounds+=1;before=len(S)
        for d,L in M:
            good=set().union(*(m for m in L if m<=S))
            S.difference_update(d-good)
        if len(S)==before:break
    return S,rounds

def safe(F,a,S):
    return all(tuple(a[v] if v in S else b for v,b in zip(P,w)) in R for P,R in F for w in R)

def greatest(F,a,allowed=None):
    V=set(a);M=[item for P,R in F for item in masks(P,R,a)]
    S,rounds=fixed_point(M,V if allowed is None else allowed)
    assert safe(F,a,S)
    return S,rounds

def pin(F,S,a):
    G=[]
    for P,R in F:
        Q=tuple(v for v in P if v not in S)
        A={tuple(b for v,b in zip(P,w) if v not in S) for w in R if all(v not in S or b==a[v] for v,b in zip(P,w))}
        assert A
        if len(A)!=2**len(Q):G.append((Q,A))
    return G

def guarded(F,g,reference_provider):
    """One shared guard; use one common fixed point, NOT intersection of maxima."""
    V={v for P,R in F for v in P};data={}
    for b in (0,1):
        G=[]
        for P,R in F:
            Q=tuple(v for v in P if v!=g)
            B={tuple(x for v,x in zip(P,w) if v!=g) for w in R if all(v!=g or x==b for v,x in zip(P,w))}
            if not B:break
            G.append((Q,B))
        else:
            a=reference_provider(G,V-{g});data[b]=(G,a)
    if not data:return None,None
    M=[item for G,a in data.values() for P,R in G for item in masks(P,R,a)]
    S,_=fixed_point(M,V-{g});assert all(safe(G,a,S) for G,a in data.values());out=[]
    for P,R in F:
        Q=tuple(sorted((set(P)-S)|({g} if set(P)&S else set())))
        B=set()
        for b,(s,a) in data.items():
            for w in R:
                x=dict(zip(P,w))
                if any(v in S and x[v]!=a[v] for v in P) or (g in x and x[g]!=b):continue
                x[g]=b;B.add(tuple(x[v] for v in Q))
        out.append((Q,B))
    if len(data)==1:out.append(((g,),{(next(iter(data)),)}))
    return out,{v:{b:a[v] for b,(s,a) in data.items()} for v in S}

if __name__=='__main__':
    F=[((0,1,2),{(0,0,0),(0,1,1),(1,0,1),(1,1,1)})]
    A=[((1,2),{(0,0),(1,1)})];B=[((1,2),{(0,1),(1,1)})];a={1:0,2:0}
    X,_=greatest(A,a);Y,_=greatest(B,a)
    assert X=={1,2} and Y=={1} and not safe(A,a,X&Y)
    G,M=guarded(F,0,lambda G,V:a);assert not M
    print("Guard intersection counterexample verified")
