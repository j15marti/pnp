#!/usr/bin/env python3
"""Independent finite certificate: exactly-one T5 and five-class completion basis."""
import itertools
from collections import Counter
WIN=(1,3)
def R(a,b):return (b-a)%5 in WIN
def Q(a,b,c):return R(a,b)^R(a,c)
def P(a,b,c):return R(a,b) and R(a,c)
assert sum(Q(*t) for t in itertools.product(range(5),repeat=3))==60
assert sum(P(*t) for t in itertools.product(range(5),repeat=3))==20
assert all(not(Q(*t) and P(*t)) for t in itertools.product(range(5),repeat=3))
for b,c in itertools.product(range(5),repeat=2):
    assert any(Q(a,b,c) for a in range(5)) == (b!=c)
C=[(0,1,2),(0,1,3),(1,0,2),(1,2,3),(2,0,3)]
def count(clauses):
    return sum(all(Q(a[h],a[u],a[v]) for h,u,v in clauses)
               for a in itertools.product(range(5), repeat=4))
assert count(C)==0
assert [count(C[:j]+C[j+1:]) for j in range(5)]==[10,40,10,30,25]
for k in range(2,6):
    edges=list(itertools.combinations(range(k),2));m=len(edges)
    orientations={sum(1<<j for j,(u,v) in enumerate(edges) if R(f[u],f[v]))
                  for f in itertools.permutations(range(5),k)}
    good=[];bad=[];fullcap=0
    for z in itertools.product((0,1,2),repeat=m):
        out=[0]*k;inc=[0]*k;mask=pos=0;arcs=[]
        for j,(u,v) in enumerate(edges):
            if z[j]==0:continue
            mask|=1<<j
            if z[j]==1:
                out[u]+=1;inc[v]+=1;pos|=1<<j;arcs.append((u,v))
            else:
                out[v]+=1;inc[u]+=1;arcs.append((v,u))
        if max(out)>2 or max(inc)>2:continue
        if mask==(1<<m)-1:fullcap+=1
        pair=(mask,pos)
        if any((o&mask)==pos for o in orientations):good.append((pair,arcs))
        else:bad.append((pair,arcs))
    basis=[q for q in bad if len(q[1])==4]
    assert all(any((mask&bmask)==bmask and (pos&bmask)==bpos
                   for (bmask,bpos),_ in basis)
               for (mask,pos),_ in bad)
    perms=list(itertools.permutations(range(k)))
    orbits=Counter(min(tuple(sorted((p[u],p[v]) for u,v in arcs))
                       for p in perms) for _,arcs in basis)
    expected={2:(2,0,[]),3:(8,0,[]),4:(24,6,[6]),5:(24,3120,[30,60,60])}[k]
    assert fullcap==len(orientations)==expected[0]
    assert len(bad)==expected[1]
    assert sorted(orbits.values())==expected[2]
    print('k',k,'cap_complete',fullcap,'bad_partial',len(bad),
          'four_arc_bad',len(basis),'bad_orbits',sorted(orbits.values()))
E=list(itertools.combinations(range(6),2))
for missing in range(15):
    b=E[missing]; colors=[None]*6; colors[b[0]]=colors[b[1]]=0
    nex=1
    for v in range(6):
        if colors[v] is None: colors[v]=nex;nex+=1
    clauses=[(6+j,*e) for j,e in enumerate(x for i,x in enumerate(E) if i!=missing)]
    assignment=colors[:]
    for h,u,v in clauses:
        assignment.append(colors[u] if R(colors[u],colors[v]) else colors[v])
    assert all(Q(assignment[h],assignment[u],assignment[v]) for h,u,v in clauses)
print('PASS: K6 15 critical deletion witnesses; complete five-class forbidden basis')
