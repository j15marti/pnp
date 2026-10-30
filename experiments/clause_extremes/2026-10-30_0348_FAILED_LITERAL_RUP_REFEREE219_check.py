#!/usr/bin/env python3
"""Independent replay for FAILED-LITERAL-RUP-REFEREE219 raw output."""
import itertools,json,math,sys
from collections import Counter

RAW=sys.argv[1] if len(sys.argv)>1 else "2026-10-30_0348_FAILED_LITERAL_RUP_REFEREE219_raw.json"
O=json.load(open(RAW)); checks=Counter()
def ok(q,msg):
    if not q: raise AssertionError(msg)
    checks[msg]+=1
def key(c):return tuple(sorted(set(c),key=lambda x:(abs(x),x)))
def lt(l,a):return (((a>>(abs(l)-1))&1)==1)==(l>0)
def sat(F,a):return all(any(lt(l,a) for l in c) for c in F)
def nvars(F):return max(abs(l) for c in F for l in c)

def up_conflict(F,units):
    A={}
    for l in units:
        v=abs(l);z=int(l>0)
        if v in A and A[v]!=z:return True
        A[v]=z
    while True:
        change=False
        for c in F:
            if any(abs(l) in A and A[abs(l)]==int(l>0) for l in c):continue
            U=[l for l in c if abs(l) not in A]
            if not U:return True
            if len(U)==1:
                l=U[0];v=abs(l);z=int(l>0)
                if v in A and A[v]!=z:return True
                if v not in A:A[v]=z;change=True
        if not change:return False

def brute_mode(c,d,m):
    vs=sorted(set(map(abs,c))|set(map(abs,d)))
    for bits in itertools.product((0,1),repeat=len(vs)):
        A=dict(zip(vs,bits)); good=True
        for C,M in ((c,m[0]),(d,m[1])):
            for l in C:
                want=int((l>0)==(M=='S'))
                if A[abs(l)]!=want:good=False;break
            if not good:break
        if good:return True
    return False

for C in O['cases']:
    F=[tuple(c) for c in C['source_clauses']]; n=nvars(F)
    # Every occurrence target and inversion.
    for j,row in enumerate(C['local_targets']):
        ok(row['clause_index']==j,'clause index')
        for p,x in enumerate(row['occurrences']):
            l=F[j][p]; s=int(l>0)
            ok(x['S_local_all_literals_true']==s,'S target')
            ok(x['U_local_all_literals_false']==1-s,'U target')
            ok(x['invert_S_to_U']==1-s and x['invert_U_to_S']==s,'target inversions')
    # Pair modes against direct enumeration.
    q=0
    for row in C['pair_matrix']:
        j,k=row['clause_indices']
        for m in ('SS','SU','US','UU'):
            ok(row['modes'][m]['feasible']==brute_mode(F[j],F[k],m),'pair mode brute replay');q+=1
    ok(q==4*len(F)*(len(F)-1)//2,'pair count')
    # Endpoints and complete complement identity.
    for label,a in [('zero',0),('one',(1<<n)-1)]:
        cnt=[sum(lt(l,a) for l in c) for c in F]
        ok(cnt==C['endpoints'][label]['true_counts'],'endpoint counts')
    for a in range(1<<n):
        b=((1<<n)-1)^a
        ca=[sum(lt(l,a) for l in c) for c in F]
        cb=[sum(lt(l,b) for l in c) for c in F]
        ok(cb==[3-x for x in ca],'complement identity')
    mc=sum(sat(F,a) for a in range(1<<n))
    ok(mc==C['model_count'],'model count')
    # Every stored resolvent cube really excludes the parent conjunction.
    for r in C['resolvents']:
        j,k=r['parents']; cube={int(v):z for v,z in r['forbidden_cube'].items()}
        free=[v for v in range(1,n+1) if v not in cube]
        for bits in itertools.product((0,1),repeat=len(free)):
            A=dict(cube);A.update(zip(free,bits));a=sum(z<<(v-1) for v,z in A.items())
            ok(not (any(lt(l,a) for l in F[j]) and any(lt(l,a) for l in F[k])),
               'resolvent cube parent exclusion')
    # Canonical relation code is switching-equivalent and equinumerous.
    G=[tuple(c) for c in C['canonical_clauses']]
    ok(sum(sat(G,a) for a in range(1<<n))==mc,'canonical model count')

# Independent source formulas for the main certificate.
W1=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
SW=[tuple((-x if abs(x)==6 and j in (9,13) else x) for x in c) for j,c in enumerate(W1)]
ok(sum(sat(W1,a) for a in range(1<<15))==0,'W1 UNSAT complete')
ok(sum(sat(SW,a) for a in range(1<<15))==54,'SWAP6 54 models complete')

# Replay each resolution and RUP addition independently.
F=[key(c) for c in SW]+[(-2,)]
for s in O['proof_search']['proof']:
    A=key(s['parents'][0]);B=key(s['parents'][1]);p=s['pivot_literal_in_first'];R=key(s['clause'])
    ok(A in F and B in F,'proof parents available')
    ok(p in A and -p in B,'proof pivot')
    ok(R==key((set(A)-{p})|(set(B)-{-p})),'resolution replay')
    ok(not any(-x in R for x in R),'non-tautological resolvent')
    ok(up_conflict(F,[-l for l in R]),'RUP replay')
    F.append(R)
ok(F[-1]==(),'proof ends empty')
ok(len(O['proof_search']['proof'])==28,'28-step certificate')

# Exact22 sign relations: six two-positive patterns collapse into three complement pairs.
for n in range(1,6):
    pats=list(itertools.combinations(range(4),2));S=set()
    for choice in itertools.product(pats,repeat=n):
        z=[]
        for P in choice:
            b=tuple(int(i in P) for i in range(4));z.append(min(b,tuple(1-x for x in b)))
        S.add(tuple(z))
    ok(len(S)==3**n,'exact22 switching-class count')
ok(O['strict22_fixed_length_bits']['lower']==math.ceil(15*math.log2(3))==24,'15-variable code lower bits')
ok(O['aggregate_collision']['same_pair_histogram'] and O['aggregate_collision']['same_endpoint_N'],
   'aggregate collision')
ok(O['aggregate_collision']['W1_models']==0 and O['aggregate_collision']['SWAP6_models']==54,
   'aggregate collision separates SAT')

R={'status':'PASS','total_checks':sum(checks.values()),'categories':dict(checks),
   'proof_steps':len(O['proof_search']['proof'])}
json.dump(R,open('2026-10-30_0348_FAILED_LITERAL_RUP_REFEREE219_check.json','w'),indent=2,sort_keys=True)
print(json.dumps(R,indent=2,sort_keys=True))
