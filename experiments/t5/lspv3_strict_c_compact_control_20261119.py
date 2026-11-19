#!/usr/bin/env python3
"""Independent strict-C controls, standard library, no external solver."""
from itertools import product

def R(a,b): return (b-a)%5 in (1,3)
def C(a,b,c): return R(a,b) and R(b,c) and R(c,a) or R(a,c) and R(c,b) and R(b,a)
def S(h,u,v): return R(h,u) and R(v,h) or R(h,v) and R(u,h)
def E(u,v): return tuple(sorted((u,v)))
def myc(n,edges):
    out=set(edges)
    for u,v in edges:out|={E(u,n+v),E(v,n+u)}
    out|={(n+i,2*n) for i in range(n)}
    return 2*n+1,sorted(out)
def family(t):
    n=t;edges=sorted({E(i,(i+1)%t) for i in range(t)})
    for _ in range(3):n,edges=myc(n,edges)
    return n,edges

def heads(u,v): return sum(C(h,u,v) for h in range(5))
def main():
    assert sum(C(*x) for x in product(range(5),repeat=3))==30
    assert sum(S(*x) for x in product(range(5),repeat=3))==40
    assert all((heads(u,v)>0)==(u!=v) for u,v in product(range(5),repeat=2))
    assert sorted(set(heads(u,v) for u,v in product(range(5),repeat=2)))==[0,1,2]
    for omitted in range(3):
        for a in range(5):
            ok=False
            for h,p,q in product(range(5),repeat=3):
                cs=[C(h,a,q),C(h,q,p),C(h,p,a)]
                if all(v for i,v in enumerate(cs) if i!=omitted):ok=True;break
            assert ok,('gadget criticality',omitted,a)
    for t in (5,7):
        n,es=family(t)
        assert (n,len(es))==(8*t+7,46*t+6)
        direct=[(n+i,u,v) for i,(u,v) in enumerate(es)]
        triple=[]
        for i,(u,v) in enumerate(es):
            h=n+i;q=n+len(es)+2*i;p=q+1
            triple.extend([(h,u,q),(h,q,p),(h,p,v)])
        assert len({E(u,v) for u,v in es})==len(es)
        assert len(direct)==len(es) and len(triple)==3*len(es)
        # Each triple-gadget has a 4-cycle in the clause-incidence graph:
        assert len(set(triple[0]).intersection(triple[1]))==2
        print('t',t,'direct_C',n+len(es),len(direct),'triple_C',n+3*len(es),len(triple))
    keep=[(u,v) for u in range(6) for v in range(u+1,6) if (u,v)!=(0,1)]
    count=0;total=0
    for a in product(range(5),repeat=6):
        if all(a[u]!=a[v] for u,v in keep):
            count+=1
            ways=5
            for u,v in keep:ways*=heads(a[u],a[v])
            total+=ways
    assert count==120 and total==76800
    print('K6_minus_one_edge: graph_colorings',count,'full_C_witnesses',total)
if __name__=='__main__':main()
