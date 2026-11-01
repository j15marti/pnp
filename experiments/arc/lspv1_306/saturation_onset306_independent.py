#!/usr/bin/env python3
"""Independent elementary saturation-onset checker, LSPV-1 306.
Checks every coherent source cube of canonical Y6/F9 and selected F15 cubes.
No producer imports and no native FLMV time/space claims.
"""
import itertools, collections
SOURCES={
"Y6": ([(1,2,3),(1,4,5),(2,4,6),(3,5,6)],
       [(1,2,4),(1,3,6),(2,3,5),(4,5,6)]),
"F9": ([(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)],
      [(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]),
"F15": ([(1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
          (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15)],
         [(1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),
          (4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15)])}
def formula(name):
    positive,negative=SOURCES[name]
    return tuple(positive)+tuple(tuple(-v for v in c) for c in negative)
def analyze(F,p):
    n=max(abs(x) for C in F for x in C)
    free=set(range(1,n+1))-set(p)
    tally=collections.defaultdict(lambda:[0,0])
    covered=0; widths=[0]*4; edges=[]; h=0
    for j,C in enumerate(F):
        if any(abs(l) in p and p[abs(l)]==int(l>0) for l in C):
            covered+=1
            for l in C:
                if abs(l) in free:
                    tally[abs(l)][int(l>0)]+=1
                    h+=1
        else:
            rest=[abs(l) for l in C if abs(l) in free]
            widths[len(rest)]+=1
            if len(rest)==2: edges.append((j,rest[0],rest[1]))
    eta=sum(min(a) for a in tally.values())
    # Authenticated polynomial greedy edge-disjoint triangle packing
    triangles=[]
    for triple in itertools.combinations(edges,3):
        degree=collections.Counter(v for _,a,b in triple for v in (a,b))
        if len(degree)==3 and all(d==2 for d in degree.values()):
            triangles.append(tuple(sorted(j for j,_,_ in triple)))
    used=set();cycles=[]
    for C in sorted(triangles):
        if not used.intersection(C):
            cycles.append(C);used.update(C)
    t=len(p);f=n-t;u=sum(widths);nu=len(cycles)
    delta=2*f-u-eta-nu;e=2*f-u
    assert len(edges)<=2*t and 3*nu<=2*t
    assert eta<=covered
    assert 3*delta>=2*n-8*t
    assert 2*e==h+widths[3]-widths[1]-2*widths[0]
    return delta,widths
def cubes(name):
    n=max(abs(x) for C in formula(name) for x in C)
    if name=="F15":
        for base in ((0,0,0,0,1,1,1,1,0),(1,0,0,0,1,1,1,1,0)):
            for choices in itertools.product((-1,0,1),repeat=6):
                p=dict(zip(range(7,16),base))
                p.update({v:b for v,b in zip(range(1,7),choices) if b>=0})
                yield p
    else:
        for choices in itertools.product((-1,0,1),repeat=n):
            yield {v:b for v,b in enumerate(choices,1) if b>=0}
if __name__=="__main__":
    for name in SOURCES:
        F=formula(name); n=max(abs(x) for C in F for x in C)
        quota=collections.Counter((abs(x),x>0) for C in F for x in C)
        assert len(set(tuple(sorted(C)) for C in F))==len(F)
        assert all(quota[v,True]==quota[v,False]==2 for v in range(1,n+1))
        count=0;first=None;nonup=None
        for p in cubes(name):
            delta,widths=analyze(F,p)
            count+=1
            if delta==0 and widths[0]==0:
                first=min(first,len(p)) if first is not None else len(p)
            if widths[1] and not widths[0] and nonup is None:nonup=dict(p)
        assert first is None or first >= (n+3)//4
        print(name, "cubes",count, "first delta-zero pin count",first,
              "non-UP source example",nonup)
    # Independent exact original-source same-F9 SAT/UNSAT labels
    F=formula("F9")
    for label,p in [("SAT",{1:1,2:0,3:1,4:0,8:0}),
                    ("UNSAT",{1:1,2:1,3:0,4:0,8:0})]:
        free=[v for v in range(1,10) if v not in p]
        count=0
        for bits in itertools.product((0,1),repeat=len(free)):
            a=dict(p);a.update(zip(free,bits))
            count+=all(any(a[abs(l)]==int(l>0) for l in C) for C in F)
        assert count==(1 if label=="SAT" else 0)
        print(label,"F9 extension count",count)
    print("PASS: elementary all-source theorem; arbitrary solver hardness not claimed")
