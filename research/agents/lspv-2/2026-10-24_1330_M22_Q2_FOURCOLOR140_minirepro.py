#!/usr/bin/env python3
"""M22-Q2-FOURCOLOR140 independent finite controls.
Checks all q=2 six-variable M22 instances, plus larger seeded q=2 controls.
The recursive coloring is a finite test implementation, NOT a polynomial
worst-case algorithm. The proof uses the constructive Brooks theorem.
"""
import itertools, collections, json, random

PAIR_SPLITS=({0,1},{0,2},{0,3})
SEED=202610241322

def defect(p,q):
    return len(set(p)-set(q))

def check_grammar(p,q,n):
    return (len(p)==len(set(p)) and len(q)==len(set(q))
        and all(len(t)==len(set(t))==3 and min(t)>=0 and max(t)<n for t in p+q)
        and all(sum(v in t for t in p)==sum(v in t for t in q)==2 for v in range(n)))

def color_four(p,n):
    adj=[set() for _ in range(n)]
    for t in p:
        for u,v in itertools.combinations(t,2):
            adj[u].add(v); adj[v].add(u)
    assert max(map(len,adj))<=4
    coloring=[-1]*n
    def rec(count):
        if count==n:return True
        v=max((j for j in range(n) if coloring[j]<0),
              key=lambda j:(len({coloring[x] for x in adj[j] if coloring[x]>=0}),len(adj[j]),-j))
        used={coloring[x] for x in adj[v]}
        for c in range(4):
            if c in used:continue
            coloring[v]=c
            if rec(count+1):return True
            coloring[v]=-1
        return False
    assert rec(0)
    return coloring

def witness(p,q,n):
    c=color_four(p,n)
    assert all(len(set(c[v] for v in t))==3 for t in p)
    for zero_pair in PAIR_SPLITS:
        bits=tuple(int(c[v] not in zero_pair) for v in range(n))
        if all(0<sum(bits[v] for v in t)<3 for t in set(p)|set(q)):
            assert all(any(bits[v] for v in t) for t in p)
            assert all(any(not bits[v] for v in t) for t in q)
            return bits
    return None

def models(p,q,n):
    return sum(all(any((z>>v)&1 for v in t) for t in p)
            and all(any(not((z>>v)&1) for v in t) for t in q)
            for z in range(1<<n))

def regular(n,rng):
    for _ in range(3000):
        slots=[v for v in range(n) for _ in range(2)]; rng.shuffle(slots)
        p=[tuple(sorted(slots[j:j+3])) for j in range(0,2*n,3)]
        if len(set(p))==len(p) and all(len(set(t))==3 for t in p):return tuple(p)
    raise AssertionError('regular source generator failed')

def switch_two(p,rng):
    for _ in range(800):
        i,j=rng.sample(range(len(p)),2)
        aa=set(p[i])-set(p[j]);bb=set(p[j])-set(p[i])
        if not aa or not bb:continue
        a=rng.choice(sorted(aa));b=rng.choice(sorted(bb))
        x=tuple(sorted((set(p[i])-{a})|{b}))
        y=tuple(sorted((set(p[j])-{b})|{a}))
        if x in p or y in p or x==y:continue
        q=list(p);q[i]=x;q[j]=y
        assert defect(p,q)==2
        return tuple(q)
    raise AssertionError('switch construction failed')

def main():
    triples=list(itertools.combinations(range(6),3))
    fam=[z for z in itertools.combinations(triples,4)
         if all(sum(v in t for t in z)==2 for v in range(6))]
    assert len(fam)==75
    histogram=collections.Counter(); certified=0
    for p in fam:
        for q in fam:
            d=defect(p,q);histogram[d]+=1
            if d!=2:continue
            assert check_grammar(p,q,6)
            assert witness(p,q,6) is not None
            assert models(p,q,6)>0
            certified+=1
    assert histogram=={0:75,2:1260,3:1680,4:2610}
    assert certified==1260
    rng=random.Random(SEED); large={}
    for n,count in ((9,30),(12,30),(24,20),(45,10),(90,10)):
        for _ in range(count):
            p=regular(n,rng);q=switch_two(p,rng)
            assert check_grammar(p,q,n) and witness(p,q,n) is not None
            if n<=12:assert models(p,q,n)>0
        large[str(n)]=count
    yp=((0,1,2),(0,3,4),(1,3,5),(2,4,5))
    yq=((0,1,3),(0,2,5),(1,2,4),(3,4,5))
    assert check_grammar(yp,yq,6) and defect(yp,yq)==4 and models(yp,yq,6)==20
    out={'run':'M22-Q2-FOURCOLOR140-compact','seed':SEED,
         'q6_full_distribution':dict(histogram),'q2_sixvar_certified':certified,
         'larger_q2_sample_counts':large,'Y_models':20,'failures':0,
         'scope':'finite controls; recursive 4color search not claimed polynomial'}
    print(json.dumps(out,sort_keys=True))

if __name__=='__main__':main()
