#!/usr/bin/env python3
"""NESTED-VIRTUAL-TRANSCRIPT84: connected growing-variable hostile control.
Source grammar, exact symbolic model counting, two-level adaptive children.
Run: python SCRIPT.py 64 ; also try 128 and 256.
"""
import math, json, sys
FILL=(4,5,6)
def clause(r):
    return tuple(-i if (r >> (i-1)) & 1 else i for i in (1,2,3))
def families(d):
    M=8*d; lo=d//3; hi=2*d//3
    assert lo>=5
    positions=[i for i in range(M) if lo<=i%d<hi]
    C=len(positions)
    ident={p:7+j for j,p in enumerate(positions)}
    def build(sat):
        return tuple(clause(0 if sat and i//d==7 else i//d)
                     if i%d==0 else ((1,4,ident[i]) if i in ident else FILL)
                     for i in range(M))
    return build(False),build(True),6+C,lo,C
def symbolic_count(clauses,C):
    # Factor 2**C distinct private connector variables EXACTLY.
    core=[c for c in clauses if {abs(v) for v in c}=={1,2,3}]
    has_fill=any(c==FILL for c in clauses)
    active=sum(1 for c in clauses if max(abs(v) for v in c)>6)
    total=0
    for X in range(8):
        if not all(any(bool(X>>(abs(v)-1)&1)==(v>0) for v in c) for c in core):
            continue
        for Y in range(8):
            if has_fill and Y==0:
                continue
            x1=X&1; y1=Y&1
            total+=1 << (C-(active if (not x1 and not y1) else 0))
    return total
def connected(clauses,n):
    adj={i:set() for i in range(1,n+1)}
    for cl in clauses:
        v=[abs(x) for x in cl]
        for u in v:
            adj[u].update(x for x in v if x!=u)
    seen={1}; frontier=[1]
    while frontier:
        u=frontier.pop()
        for v in adj[u]:
            if v not in seen:
                seen.add(v);frontier.append(v)
    return len(seen)==n
def audit(d):
    U,V,n,lo,C=families(d);M=len(U)
    k1=(int(math.sqrt(d))|1);k2=max(2,int(math.sqrt(k1)))
    assert 2<=k2<k1<lo
    checks=0
    assert connected(U,n) and connected(V,n);checks+=2
    assert symbolic_count(U,C)==0 and symbolic_count(V,C)==7*(1<<C);checks+=2
    leafpairs=0
    for j1 in range(M):
        for j2 in range(k1):
            ids=[(j1*k1+(j2*k2+i)%k1)%M for i in range(k2)]
            cu=tuple(U[i] for i in ids);cv=tuple(V[i] for i in ids)
            a=symbolic_count(cu,C);b=symbolic_count(cv,C)
            assert a==b and a>0
            checks+=2;leafpairs+=1
    for width in range(1,min(lo,8)):
        for j in range(M):
            cu=[U[(j+i)%M] for i in range(width)]
            cv=[V[(j+i)%M] for i in range(width)]
            assert symbolic_count(cu,C)==symbolic_count(cv,C)
            checks+=1
    return dict(d=d,M=M,n=n,connector_variables=C,
                min_connector_offset=lo,K1=k1,K2=k2,
                checked_leaf_pairs=leafpairs,assertion_groups=checks,
                sat_full_model_count=str(7*(1<<C)),
                unsat_full_model_count=0,connected_primal=True)
if __name__=="__main__":
    d=int(sys.argv[1]) if len(sys.argv)>1 else 64
    print(json.dumps(audit(d),indent=2))
