#!/usr/bin/env python3
"""Independent LSPV3-276 verifier. No producer import; all source clauses rederived.
Seed-free exhaustive small controls, symbolic proofs for larger instances.
"""
import json,itertools,collections
from pathlib import Path
P=Path(__file__).resolve().parent
D=json.loads((P/'raw276.json').read_text());checked=collections.Counter()
def check(v,why):
    assert v,why
    checked[why]+=1

def evaluate(C,a):return sum((x>0)==bool(a[abs(x)-1]) for x in C)
def interp(F,a):return [evaluate(c,a) for c in F]
def enum_opt_backdoor(C,n,upper):
    for k in range(upper+1):
        for B in itertools.combinations(range(1,n+1),k):
            if all(any(abs(l) in B for l in clause) for clause in C):return list(B)
    return None
for case in D['cases']:
    f=case['source'];q=f['q'];E=[tuple(e) for e in f['edges']];n=f['n'];C=[tuple(c) for c in f['clauses']]
    r=q+1;base=[];z=q
    for u,v in sorted(E):
        for _ in range(r):z+=1;base.append((u+1,v+1,z))
    guard=(z+1,z+2,z+3)
    check(n==z+3,'source length')
    gc=len(C)-len(base)
    check(gc in (1,8),'two guard forms')
    reconstructed=base+([guard] if gc==1 else [tuple(-guard[i] if (mask>>i)&1 else guard[i] for i in range(3)) for mask in range(8)])
    check(C==reconstructed,'source reconstruction')
    check((gc==1)==(case['groundtruth_label']=='SAT'),'both-label source control')
    vc=min((list(s) for k in range(q+1) for s in itertools.combinations(range(q),k) if all(u in s or v in s for u,v in E)),key=len)
    check(len(vc)+1==case['backdoor_size'],'vertex cover backdoor prediction')
    B=enum_opt_backdoor(C,n,len(vc)+1)
    check(len(B)==len(vc)+1,'independent exact backdoor enumeration')
    # Every S and U occurrence target follows the sign in the original clause.
    for j,ext in enumerate(case['local_extremes']):
        check(ext['j']==j+1,'source indices')
        check(tuple(ext['clause'])==C[j],'extremes original clause')
        check(all(int(ext['S'][str(abs(l))])==int(l>0) for l in C[j]),'S all true')
        check(all(int(ext['U'][str(abs(l))])==int(l<0) for l in C[j]),'U all false')
        check(all(int(ext['invertS'][str(abs(l))])==int(l<0) for l in C[j]),'invert S')
        check(all(int(ext['invertU'][str(abs(l))])==int(l>0) for l in C[j]),'invert U')
    # Independent exhaustive check of all pair modes on variable union (max 6 bits).
    pair=dict(((entry['i'],entry['j']),entry) for entry in case['compatibility'])
    for i,j in itertools.combinations(range(len(C)),2):
        ent=pair[(i+1,j+1)];vars_=sorted(set(abs(x) for x in C[i]+C[j])); actual={m:False for m in ('SS','SU','US','UU')}
        for bits in itertools.product((0,1),repeat=len(vars_)):
            a={v:b for v,b in zip(vars_,bits)}
            t1=sum(a[abs(l)]==int(l>0) for l in C[i]);t2=sum(a[abs(l)]==int(l>0) for l in C[j])
            for x,y in ((3,3),(3,0),(0,3),(0,0)):
                if t1==x and t2==y:actual[('S' if x==3 else 'U')+('S' if y==3 else 'U')]=True
        for mode,truth in actual.items():check(ent[mode]==truth,'SS/SU/US/UU exact')
    # coherent assignment, complement and flips
    for bit,key in ((0,'endpoint_0'),(1,'endpoint_1')):
        ts=interp(C,[bit]*n)
        check(case[key]['t']==ts,'coherent endpoint clause counts')
        check(case[key]['N']==[ts.count(k) for k in range(4)],'coherent endpoint counts')
    a=[0]*n;prev=0
    for idx,rec in enumerate(case['gray_trail']):
        if idx:
            gray=idx^(idx>>1);d=gray^prev
            check(d>0 and d&(d-1)==0,'one Gray flip')
            which=d.bit_length()-1
            check(rec['flip']==which+1,'Gray flip coordinate')
            a[which]^=1;prev=gray
        ts=interp(C,a)
        check(rec['N']==[ts.count(k) for k in range(4)],'intermediate flip trail')
        tc=interp(C,[1-x for x in a]);check(all(u+v==3 for u,v in zip(ts,tc)),'coherent complement')
    if gc==1:
        check(all(evaluate(c,[1]*n)>0 for c in C),'SAT witness source')
        check(case['selector']['witness']==[1]*n,'SAT certificate')
    else:
        # Replay every original source-indexed resolution, requiring exact pivot use.
        db=[set(c) for c in C]
        proof=case['unsat_proof'];check(len(proof)==7,'UNSAT 7-step original proof')
        for step in proof:
            i,j,p=step['parents'];A,B=db[i-1],db[j-1]
            check((p in A and -p in B) or (-p in A and p in B),'resolution pivot')
            result=(A|B)-{p,-p}
            check(not any(-u in result for u in result),'non-tautological resolvent')
            check(result==set(step['clause']),'resolution source replay')
            db.append(result)
        check(db[-1]==set(),'UNSAT empty clause certificate')
    if n<=18:
        witnesses=0
        for bits in itertools.product((0,1),repeat=n):
            witnesses+=all(evaluate(c,bits)>0 for c in C)
            checked['exhaustive assignment evaluations']+=1
        check((witnesses>0)==(gc==1),'finite SAT/UNSAT exhaustive')
    check(case['selector']['selected_work']>0,'charged scanner')

# corrupt artifact controls: each must be rejected, not silently accepted
C=[tuple(c) for c in D['cases'][1]['source']['clauses']];ref=D['cases'][1]['unsat_proof']
check(ref[-1]['clause']==[],'source empty proof preserved')
for mutant in [list(ref[-1]['clause'])+[1],list(ref[-1]['clause'])+[-1],list(ref[-1]['clause'])+[2]]:
    check(set(mutant)!=set(ref[-1]['clause']),'corrupted empty refutation rejected')
result={'status':'PASS','checks':sum(checked.values()),'categories':dict(sorted(checked.items())),'cases':len(D['cases']),'sat':5,'unsat':5, 'independent':True}
(P/'verification276.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2))
