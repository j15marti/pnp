#!/usr/bin/env python3
"""EXPANDER97: standard-library peer reproducer of the exact finite claim.
Not a proof of expansion for infinite graph families or unrestricted SAT time.
"""
import itertools, random, json

def prism(r):
    return sorted({tuple(sorted(z)) for z in
        [(i,(i+1)%r) for i in range(r)] +
        [(r+i,r+(i+1)%r) for i in range(r)] +
        [(i,r+i) for i in range(r)]})

def compile_formula(n,edges,charges):
    incident=[[] for _ in range(n)]
    for i,(a,b) in enumerate(edges,1):
        incident[a].append(i); incident[b].append(i)
    assert all(len(x)==3 for x in incident)
    clauses=[]; origins=[]
    for v in range(n):
        for bits in itertools.product((0,1),repeat=3):
            if sum(bits)%2!=charges[v]:
                clauses.append(tuple((-x if bit else x)
                    for x,bit in zip(sorted(incident[v]),bits)))
                origins.append(v)
    return clauses,origins

def brute(clauses,m):
    count=0
    for a in range(1<<m):
        if all(any(bool(a&(1<<(abs(l)-1)))==(l>0) for l in c)
               for c in clauses):
            count+=1
    return count

def expansion(n,edges):
    best=None
    for mask in range(1,1<<n):
        k=mask.bit_count()
        if k>n//2: continue
        delta=sum(((mask>>u)&1)!=((mask>>v)&1) for u,v in edges)
        if best is None or delta*best[1]<best[0]*k: best=(delta,k)
    return best

def audit(r):
    n=2*r; edges=prism(r); e=len(edges)
    assert e==3*n//2
    controls=[]; support=None
    for charge_vertex in [-1,0,n//2,n-1]:
        charges=[0]*n
        if charge_vertex!=-1:charges[charge_vertex]=1
        clauses,origins=compile_formula(n,edges,charges)
        assert len(clauses)==4*n
        curr=sorted(tuple(sorted(abs(l) for l in c)) for c in clauses)
        if support is None:support=curr
        assert support==curr
        for x in range(1,e+1):
            assert sum(x in c for c in clauses)==4
            assert sum(-x in c for c in clauses)==4
        expected=1<<(e-n+1) if charge_vertex==-1 else 0
        if r<=5: assert brute(clauses,e)==expected
        controls.append({'charge_vertex':charge_vertex,'sat':expected>0})
    clauses,origins=compile_formula(n,edges,[0]*n)
    num,den=expansion(n,edges)
    rng=random.Random(1776+n)
    widths=[]
    for _ in range(100):
        order=list(range(len(clauses)));rng.shuffle(order)
        seen=set();touched=set();live_peak=0;checked=False
        appeared=set()
        for j in order:
            touched.add(origins[j])
            appeared.update(abs(l) for l in clauses[j])
            later={abs(l) for q in order[order.index(j)+1:] for l in clauses[q]}
            live_peak=max(live_peak,len(appeared&later))
            if len(touched)==n//2 and not checked:
                cross=sum((a in touched)!=(b in touched) for a,b in edges)
                assert cross*den>=num*(n//2)
                assert len(appeared&later)>=cross
                checked=True
        assert checked
        widths.append(live_peak)
    return {'vertices':n,'edges':e,'clauses':4*n,'controls':controls,
            'expansion_numerator':num,'expansion_denominator':den,
            'min_sample_frontier':min(widths),'max_sample_frontier':max(widths)}

def main():
    a=[audit(r) for r in (3,4,5)]
    assert sum(len(x['controls']) for x in a)==12
    print(json.dumps({'status':'COMPUTATIONAL finite controls',
                      'graphs':a,'shuffled_orders':300,'discrepancies':0},
                     indent=2,sort_keys=True))
if __name__=='__main__': main()
