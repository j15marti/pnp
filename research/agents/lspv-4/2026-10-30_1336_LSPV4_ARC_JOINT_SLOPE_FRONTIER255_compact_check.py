#!/usr/bin/env python3
"""LSPV-4 ARC JOINT SLOPE FRONTIER255: independent, dependency-free compact checker.
Exact full FLMV envelope and half-space frontier, plus original-clause signed
SAT/UNSAT targets, all pair extremes and same-source complete SAT enumeration.
The separate 382-line expanded producer/full 32,249-line JSON lives in the
reproducibility ZIP. This checker deliberately does not claim native TM timing.
Run: python 2026-10-30_1336_LSPV4_ARC_JOINT_SLOPE_FRONTIER255_compact_check.py
"""
import json, itertools, random
from fractions import Fraction as Q

W1='-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14'
F=[tuple(map(int,x.split())) for x in W1.split(';')]
G=[list(c) for c in F]
assert G[7][0]==1 and G[19][0]==-1
G[7][0]=-1;G[19][0]=1
G=[tuple(c) for c in G]
H=[(1,3,5),(1,-3,6),(-1,4,5),(-1,-4,6),
   (2,3,-5),(2,-3,-6),(-2,4,-5),(-2,-4,-6)]
def true(l,a):return ((a>>(abs(l)-1))&1)==int(l>0)
def invf(c,k):return (c**k+c-2)/((c-1)*c**k)
def dk(c,k):return min((invf(c,k)-c)/k,c**(-k))
def star(c):
    best=Q(-1);kstar=0
    for k in range(1,100):
        val=dk(c,k)
        if val>best:best=val;kstar=k
        if best>0 and c**(-(k+1))<best:return best,kstar,k
    raise AssertionError('no certified tail')
def poly(c,eta):return c**3+(1+2*eta)*c**2-c-2
def root(eta):
    lo=Q(6,5);hi=Q(5,4)
    assert poly(lo,eta)<=0<poly(hi,eta)
    for _ in range(105):
        mid=(lo+hi)/2
        if poly(mid,eta)<0:lo=mid
        else:hi=mid
    return lo,hi
def interior(eta,delta,pi):
    return eta<Q(1,90) and poly(max(Q(11,10)+pi,Q(6,5)+2*delta),eta)<0
assert star(Q(6,5))[:2]==(Q(23,45),2)
assert star(Q(241,200))[:2]==(Q(11642479,23232400),2)
assert dk(Q(6,5),1)==Q(7,15)
assert dk(Q(6,5),3)==Q(401,810)<Q(1,2)
assert Q(625,1296)<Q(1,2)
eta0=Q(26279,23232400)
assert poly(Q(241,200),eta0)==0
assert not interior(eta0,Q(1,400),Q(21,200))
assert interior(Q(0),Q(0),Q(0))
assert not interior(Q(1,90),Q(0),Q(0))
assert not interior(Q(0),Q(1,300),Q(0))
assert not interior(Q(0),Q(0),Q(11,100))
for eta in (Q(0),Q(1,10000),Q(1,1000),eta0,Q(1,200),Q(1,100),Q(1,90)):
    a,b=root(eta)
    assert 0<=a<=b and poly(a,eta)<=0<=poly(b,eta)
    if eta==eta0:assert a<Q(241,200)<b

def cases():
    def parity(want):
        return [tuple(v if mask>>(v-1)&1 else -v for v in (1,2,3))
                for mask in range(8) if (mask.bit_count()&1)!=want]
    def permute(F):
        return [tuple((1 if l>0 else -1)*(-1 if abs(l) in {1,4} else 1)*((abs(l)%6)+1)
                      for l in c) for c in F]
    edges={(0,1):1,(0,2):2,(0,3):3,(1,2):4,(1,3):5,(2,3):6}
    k4=[]
    for vertex in range(4):
        vs=[v for edge,v in edges.items() if vertex in edge]
        for mask in range(8):
            if (mask.bit_count()&1)!=(1 if vertex==0 else 0):
                k4.append(tuple(v if mask>>i&1 else -v for i,v in enumerate(vs)))
    rng=random.Random(202610301336)
    planted=[];seen=set();witness=0b101011001
    while len(planted)<27:
        vs=rng.sample(range(1,10),3)
        c=tuple(v if rng.randrange(2) else -v for v in vs)
        if c not in seen and any(true(l,witness) for l in c):
            planted.append(c);seen.add(c)
    return {'W1_UNSAT':F,'W1_swap_SAT':G,'H1_SAT':H,'H1_renamed_SAT':permute(H),
        'XOR3_SAT':parity(1),'XOR3_UNSAT':parity(1)+parity(0),
        'Horn_SAT':[(1,),(-1,2),(2,3)],'Horn_UNSAT':[(1,),(-1,2),(-2,)],
        'Krom_SAT':[(1,2),(-1,2)],
        'Krom_UNSAT':[(1,2),(1,-2),(-1,2),(-1,-2)],
        'K4_Tseitin_UNSAT':k4,'Planted_dense_SAT':planted}
def pairmode(c,d,m):
    demand={}
    for cc,flag in ((c,m[0]),(d,m[1])):
        for lit in cc:
            v=abs(lit);bit=int((lit>0)==(flag=='S'))
            if v in demand and demand[v]!=bit:return False
            demand[v]=bit
    return True
checks=0;complete=0;mat={}
for name,clauses in cases().items():
    n=max(abs(l) for c in clauses for l in c)
    full=(1<<n)-1;models=0;pair=0
    for j,c in enumerate(clauses):
        for l in c:
            S=int(l>0);U=int(l<0)
            assert S!=U and 1-S==U and 1-U==S
            checks+=4
        for k in range(j+1,len(clauses)):
            d=clauses[k]
            for mode in ('SS','SU','US','UU'):
                predicted=pairmode(c,d,mode)
                variables=sorted(set(map(abs,c+d)))
                brute=False
                for bits in range(1<<len(variables)):
                    trial={v:(bits>>i)&1 for i,v in enumerate(variables)}
                    tc=sum(trial[abs(l)]==int(l>0) for l in c)
                    td=sum(trial[abs(l)]==int(l>0) for l in d)
                    if tc==(len(c) if mode[0]=='S' else 0) and td==(len(d) if mode[1]=='S' else 0):
                        brute=True;break
                assert predicted==brute
                pair+=1
    for a in range(1<<n):
        t=[sum(true(l,a) for l in c) for c in clauses]
        tc=[sum(true(l,full^a) for l in c) for c in clauses]
        assert all(x+y==len(c) for c,x,y in zip(clauses,t,tc))
        if all(x>0 for x in t):models+=1
        complete+=1
    checks+=pair
    mat[name]={'models':models,'n':n,'m':len(clauses),'pair_checks':pair}
expected={'W1_UNSAT':0,'W1_swap_SAT':168,'H1_SAT':4,'H1_renamed_SAT':4,
    'XOR3_SAT':4,'XOR3_UNSAT':0,'Horn_SAT':2,'Horn_UNSAT':0,
    'Krom_SAT':2,'Krom_UNSAT':0,'K4_Tseitin_UNSAT':0,'Planted_dense_SAT':48}
assert {k:v['models'] for k,v in mat.items()}==expected
print(json.dumps({'status':'PASS','primary_FLVM_envelope':'exact k=2 plus full infinite tail',
 'active_halfspace_k2':['6/5','root(c**3+c**2-c-2)'],
 'models':{k:v['models'] for k,v in mat.items()},
 'original_clause_pair_SS_SU_US_UU_checks':sum(v['pair_checks'] for v in mat.values()),
 'global_assignment_complements':complete,'local_target_checks':checks},sort_keys=True))
