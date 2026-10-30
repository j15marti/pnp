#!/usr/bin/env python3
"""Independent replay of BALANCED-KRONECKER-REFEREE220 raw claims."""
import itertools,json,math,sys
from collections import Counter
P=sys.argv[1] if len(sys.argv)>1 else "2026-10-30_0448_BALANCED_KRONECKER_REFEREE220_raw.json"
O=json.load(open(P));C=Counter()
def ok(q,k):
    if not q:raise AssertionError(k)
    C[k]+=1
def lt(l,a):return (((a>>(abs(l)-1))&1)==1)==(l>0)
def nv(F,a):
    t=[sum(lt(l,a) for l in c) for c in F]
    return tuple(t.count(i) for i in range(4))
for case in O['cases']:
    F=[tuple(c) for c in case['source_formula']];n=case['n'];m=len(F)
    # Source occurrence S/U targets and inversions.
    for j,row in enumerate(case['local_clause_targets']):
        ok(row['clause_index']==j,'clause index')
        for p,z in enumerate(row['occurrences']):
            l=F[j][p];ok(z['variable']==abs(l) and z['literal']==l,'occurrence source')
            ok(z['S_local_all_literals_true']==int(l>0),'S target')
            ok(z['U_local_all_literals_false']==int(l<0),'U target')
            ok(z['invert_S_is_U']==z['U_local_all_literals_false'] and z['invert_U_is_S']==z['S_local_all_literals_true'],'target inversion')
    # Pair modes from fresh enumeration.
    for row in case['pair_extreme_compatibility']:
        j,k=row['clause_indices'];vs=sorted(set(map(abs,F[j]))|set(map(abs,F[k])))
        for md in ('SS','SU','US','UU'):
            feasible=False
            for bits in itertools.product((0,1),repeat=len(vs)):
                a=dict(zip(vs,bits));t=[]
                for q in (j,k):t.append(sum(a[abs(l)]==int(l>0) for l in F[q]))
                if t[0]==(3 if md[0]=='S' else 0) and t[1]==(3 if md[1]=='S' else 0):feasible=True;break
            ok(feasible==row['modes'][md]['feasible'],'pair mode')
    hist=Counter(nv(F,a) for a in range(1<<n))
    ok(sum(z for N,z in hist.items() if N[0]==0)==case['profile_audit']['models'],'model count')
    ok(hist[nv(F,0)]>0 and hist[nv(F,(1<<n)-1)]>0,'endpoints')
    for N,z in hist.items():ok(hist[N]==hist[(N[3],N[2],N[1],N[0])],'complement symmetry')
    if case['sign_balanced_ternary']:
        h=m//2;M=h+1;Md=2*h+1;anchor=nv(F,0)
        keys=set();dkeys=set()
        for N in hist:
            ok(N[1]==h-2*N[0]+N[3] and N[2]==h+N[0]-2*N[3],'balanced identity')
            k=N[0]+M*N[3];ok((k%M,k//M)==(N[0],N[3]),'absolute decode');keys.add(k)
            d=(N[0]-anchor[0],N[3]-anchor[3]);dkeys.add(d[0]+Md*d[1])
        ok(len(keys)==len(hist),'absolute support preservation')
        ok(len(dkeys)==len(hist),'delta support preservation')
        feasible={(a,b) for a in range(h+1) for b in range(h+1) if 2*a-b<=h and 2*b-a<=h}
        ok(len(feasible)==math.floor(h*h/2+h+1),'profile-count formula')
    # Every recorded resolvent cube independently excludes its two parents.
    for r in case['source_resolvent_prohibited_cubes']:
        j,k=r['parent_clause_indices'];cube={int(v):z for v,z in r['prohibited_partial_cube'].items()};z=0
        for a in range(1<<n):
            if all(((a>>(v-1))&1)==b for v,b in cube.items()):
                z+=1;ok(not(all(any(lt(l,a) for l in F[q]) for q in (j,k))),'resolvent cube exclusion')
        ok(z==r['checked_cube_completions'],'cube completion count')
    ok(case['baseline_UP_DPLL']['sat']==case['profile_prepass_then_same_UP_DPLL']['sat'],'controller answer')
R={'status':'PASS','total_checks':sum(C.values()),'categories':dict(C),'cases':len(O['cases'])}
json.dump(R,open('2026-10-30_0448_BALANCED_KRONECKER_REFEREE220_check.json','w'),indent=2,sort_keys=True)
print(json.dumps(R,indent=2,sort_keys=True))
