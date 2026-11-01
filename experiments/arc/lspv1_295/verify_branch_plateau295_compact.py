#!/usr/bin/env python3
"""ARC-BRANCH-PLATEAU295 independent no-import verifier.
Uses integer masks and a separately transcribed canonical SAT/UNSAT parent.
No knowledge of producer internals or precomputed SAT labels.
"""
from itertools import product
from collections import Counter
import json,math
POS=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),
     (6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
NEG=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),
     (4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
C=POS+tuple(tuple(-v for v in a) for a in NEG)
N=15
def check_source():
    counts=Counter(v for c in C for v in c)
    assert len(C)==20
    assert all(counts[v]==2 and counts[-v]==2 for v in range(1,16))
    assert all(len(c)==3 and len({abs(v) for v in c})==3 for c in C)
    assert len({tuple(sorted(c)) for c in C})==20
def models(p):
    free=[i for i,a in enumerate(p) if a is None]
    fixed=sum(1<<i for i,a in enumerate(p) if a==1)
    output=[]
    for choices in range(1<<len(free)):
        mask=fixed
        for j,i in enumerate(free):mask|=((choices>>j)&1)<<i
        if all(any(((mask>>(abs(l)-1))&1)==int(l>0) for l in c) for c in C):
            output.append(mask)
    return output
def triple(p):
    covered=0
    r2=r3=h=0
    for c in C:
        s=sum(p[abs(x)-1] is not None and p[abs(x)-1]==int(x>0) for x in c)
        z=sum(p[abs(x)-1] is None for x in c)
        if s:covered+=1;h+=z
        else:r2+=(z==2);r3+=(z==3)
        assert s or z>=2
    return covered,r2,r3,h
def mode_checks():
    four=Counter()
    for i,A in enumerate(C):
        for B in C[i+1:]:
            a={abs(v):v>0 for v in A}
            b={abs(v):v>0 for v in B}
            same=any(a[v]==b[v] for v in a.keys()&b.keys())
            opp=any(a[v]!=b[v] for v in a.keys()&b.keys())
            sig=''.join('1' if z else '0' for z in (not opp,not same,not same,not opp))
            four[sig]+=1
    assert dict(four)=={'1001':29,'0110':51,'1111':110}
    return dict(four)
def main():
    check_source()
    adjacency=[set() for _ in range(N)]
    for cl in C:
        a=tuple(abs(v)-1 for v in cl)
        for i in range(3):
            for j in range(i+1,3):
                adjacency[a[i]].add(a[j]);adjacency[a[j]].add(a[i])
    assert max(map(len,adjacency))<=8
    free=set(range(N));I=[]
    while free:
        v=min(free);I.append(v);free-={v}|adjacency[v]
    assert len(I)>=math.ceil(N/9)
    assert len(I)==3
    for v in I:
        for w in I:
            if v!=w:assert w not in adjacency[v]
    checked=0
    for vals in product((0,1),repeat=len(I)):
        for t in range(len(I)+1):
            p=[None]*N
            for x,v in zip(I[:t],vals[:t]):p[x]=v
            covered,r2,r3,h=triple(p)
            assert (covered,r2,r3,h)==(2*t,2*t,20-4*t,4*t)
            assert 2*(N-t)-(20-covered)==10
            checked+=1
    pU=[None]*6+[0,0,0,0,1,1,1,1,0]
    pS=[None]*6+[1,0,0,0,1,1,1,1,0]
    assert len(models(pU))==0 and len(models(pS))==2
    # Independently authenticate the two edge-disjoint original clause cycles.
    cycles=((1,2,12),(3,4,15))
    assert not set(cycles[0])&set(cycles[1])
    for cyc in cycles:
        deg=Counter()
        for clause_id in cyc:
            freevars=[abs(l) for l in C[clause_id-1] if pU[abs(l)-1] is None]
            assert len(freevars)==2
            deg.update(freevars)
        assert len(deg)==3 and all(d==2 for d in deg.values())
    spill=Counter()
    for c in C:
        if any(pU[abs(l)-1] is not None and pU[abs(l)-1]==int(l>0) for l in c):
            spill.update(l for l in c if pU[abs(l)-1] is None)
    eta=sum(min(spill[x],spill[-x]) for x in range(1,16) if pU[x-1] is None)
    f=6
    covered,r2,r3,h=triple(pU)
    e=2*f-(len(C)-covered)
    assert e==2 and eta==1 and len(cycles)+eta>e
    hist=lambda assignment:[sum(sum(assignment[abs(l)-1]==int(l>0) for l in c)==r for c in C) for r in range(4)]
    assert hist([0]*N)==[10,0,0,10] and hist([1]*N)==[10,0,0,10]
    for a in product((0,1),repeat=6):
        q=list(a)+[0,0,0,0,1,1,1,1,0]
        H=hist(q);K=hist([1-v for v in q])
        assert all(H[r]==K[3-r] for r in range(4))
    print(json.dumps({'status':'PASS','independent':True,
         'source':'proper duplicate-free canonical F15',
         'greedy_independent_0_index':I,
         'independent_set_assignment_prefix_checks':checked,
         'pair_mode_counts':mode_checks(),
         'same_original_parent_UNSAT_models':0,
         'same_original_parent_SAT_models':2,
         'UNSAT_signed_spill_eta':eta,'UNSAT_odd_cycles':[list(z) for z in cycles],
         'all_input_ARC_and_FLMV':'OPEN','P_vs_NP':'OPEN'},sort_keys=True))
if __name__=='__main__':main()
