#!/usr/bin/env python3
"""Standalone LSPV-4/446 finite original strict-3 Tseitin UP bound checker.
No external dependencies. Run: python3 lspv4_446_up_compact.py
Finite control, not a Resolution hardness certificate or native FLMV benchmark.
"""
from itertools import combinations, product

def graph(name):
    if name == 'K4':
        h=4; edges=[(i,j) for i in range(h) for j in range(i+1,h)]
    elif name == 'cube':
        h=8; edges=[(i,i^(1<<j)) for i in range(h) for j in range(3) if i<(i^(1<<j))]
    elif name == 'Petersen':
        h=10; edges=[(i,(i+1)%5) for i in range(5)] + [(5+i,5+(i+2)%5) for i in range(5)] + [(i,5+i) for i in range(5)]
    elif name == 'Heawood':
        h=14; edges=[(i,7+(i+d)%7) for i in range(7) for d in (0,1,3)]
    else:
        raise ValueError(name)
    edges=sorted(tuple(sorted(pair)) for pair in edges)
    inc=[[] for _ in range(h)]
    for e,(u,v) in enumerate(edges,1):
        inc[u].append(e);inc[v].append(e)
    assert all(len(z)==3 for z in inc)
    return inc,edges

def source(inc,chi):
    return [(((-1)**p)*a,((-1)**q)*b,((-1)**(p^q^1^chi[v]))*c)
        for v,(a,b,c) in enumerate(inc) for p,q in product((0,1),repeat=2)]

def up(cnf,initial):
    a=dict(initial);forced=0
    while True:
        change=False
        for c in cnf:
            if any((lit>0)==a[abs(lit)] for lit in c if abs(lit) in a):
                continue
            rest=[lit for lit in c if abs(lit) not in a]
            if not rest:return True,forced,a
            if len(rest)==1:
                a[abs(rest[0])]=(rest[0]>0)
                forced+=1;change=True;break
        if not change:return False,forced,a

def main():
    counts=[0,0,0]
    for name in ('K4','cube','Petersen','Heawood'):
        inc,edges=graph(name)
        for odd in (0,1):
            chi=[odd]+[0]*(len(inc)-1)
            cnf=source(inc,chi)
            assert len(cnf)==4*len(inc)
            for k in range((4 if name=='K4' else 3)+1):
                for chosen in combinations(range(1,len(edges)+1),k):
                    for bits in product((False,True),repeat=k):
                        closed,t,assigned=up(cnf,zip(chosen,bits))
                        assert t<=2*k,(name,k,t)
                        untouched=sum(all(x not in assigned for x in row) for row in inc)
                        assert untouched>=len(inc)-6*k
                        if not closed:
                            assert untouched*4>=4*max(0,len(inc)-6*k)
                        counts[0]+=1
                        counts[1]+=not closed
                        counts[2]+=closed
    assert counts==[36272,35496,776],counts
    print({'PASS':True,'cases':counts[0],'open':counts[1],'closed':counts[2]})

if __name__=='__main__':
    main()
