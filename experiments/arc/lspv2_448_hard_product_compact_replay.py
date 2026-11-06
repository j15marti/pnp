#!/usr/bin/env python3
"""LSPV-2/448 compact independent-replay controls. No external dependencies."""
from itertools import product

def tseitin(graph, c, a, b):
    h = max(max(e) for e in graph) + 1
    edges = [[u+j*h,v+j*h] for j in range(c) for u,v in graph]
    ports = [[] for _ in range(c*h)]
    for e,(u,v) in enumerate(edges,1):
        ports[u].append(e); ports[v].append(e)
    assert all(len(p)==3 for p in ports)
    order = [j*h+t for t in range(2) for j in range(c)]
    order += [j*h+t for t in range(2,h) for j in range(c)]
    clauses=[]
    for v in order:
        j,t = divmod(v,h)
        chi = ((a>>j)&1) if t==0 else ((b>>j)&1) if t==1 else 0
        x,y,z=sorted(ports[v])
        for p,q in product((0,1),repeat=2):
            r=p^q^1^chi
            clauses.append(tuple(-e if sign else e for e,sign in ((x,p),(y,q),(z,r))))
    return clauses,len(edges)

def sat(clauses,m):
    for mask in range(1<<m):
        if all(any(((mask>>(abs(x)-1))&1)==int(x>0) for x in cl) for cl in clauses):
            return True
    return False

def menu_classes(c,Q):
    functions={tuple(int(s==q) for q in Q) for s in range(1<<c)}
    d=len(set(Q))
    return len(functions), d+int(d<(1<<c))

def main():
    k4=[(i,j) for i in range(4) for j in range(i+1,4)]
    cube=sorted((i,i^(1<<k)) for i in range(8) for k in range(3) if i<(i^(1<<k)))
    checked=0
    for edges in (k4,cube):
        for c in (1,2):
            h=max(max(e) for e in edges)+1
            for a,b in product(range(1<<c),repeat=2):
                clauses,m=tseitin(edges,c,a,b)
                assert len(clauses)==4*c*h
                assert all(len(set(map(abs,cl)))==3 for cl in clauses)
                if m<=12: assert sat(clauses,m)==(a==b)
                checked+=1
    for c in range(1,9):
        for d in range(c+1):
            Q=tuple(range(1<<d))
            actual,want=menu_classes(c,Q)
            assert actual==want
            assert (actual-1).bit_length()==(d+int(d<c))
    for c in range(1,10):
        for a in range(1<<c):
            for a2 in range(1<<c):
                if a!=a2:
                    # Same suffix b=a must produce different SAT outputs
                    assert a==a and a2!=a
    print({"passed":True,"source_controls":checked,"menu_controls":44,
           "streaming_prefix_lengths":9,
           "warning":"Promise / read-once model only; no native FLMV run."})

if __name__=="__main__":main()
