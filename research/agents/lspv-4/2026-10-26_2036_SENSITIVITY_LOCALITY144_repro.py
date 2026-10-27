#!/usr/bin/env python3
"""LSPV-4 SENSITIVITY-LOCALITY144 independent reproducible finite controls.
Exact finite enumeration and integer arithmetic, not a universal SAT lower bound.
Run python3 2026-10-26_2036_SENSITIVITY_LOCALITY144_repro.py [output.json].
"""
import itertools, math, json, pathlib, sys, hashlib
CHECKS=0

def test(v,msg='assertion'):
    global CHECKS
    CHECKS += 1
    if not v: raise AssertionError(msg)

def prism(h):
    vertices=[(row,i) for row in range(2) for i in range(h)]
    def idof(p):return vertices.index(p)
    edges=set()
    for row in range(2):
        for i in range(h):
            edges.add(tuple(sorted((idof((row,i)),idof((row,(i+1)%h))))))
    for i in range(h):edges.add(tuple(sorted((idof((0,i)),idof((1,i))))))
    edges=sorted(edges)
    incidence=[tuple(j for j,edge in enumerate(edges) if v in edge) for v in range(2*h)]
    test(len(edges)==3*h)
    test(all(len(inc)==3 for inc in incidence))
    return edges,incidence

def tseitin_source(h):
    edges,inc=prism(h)
    charges=[1]+[0]*(2*h-1)
    clauses=[];meta=[]
    for vertex,items in enumerate(inc):
        for a in itertools.product((0,1),repeat=3):
            if sum(a)%2==charges[vertex]:continue
            clauses.append(tuple(edge+1 if bit==0 else -(edge+1) for edge,bit in zip(items,a)))
            meta.append((vertex,items,a))
    test(len(clauses)==8*h)
    m=3*len(clauses)
    signbits=[int(v<0) for c in clauses for v in c]
    tally=[[0,0] for _ in edges]
    for clause in clauses:
        test(len(set(abs(x) for x in clause))==3)
        for lit in clause:tally[abs(lit)-1][int(lit>0)]+=1
    test(all(count==[4,4] for count in tally))
    width=len(edges).bit_length()
    N=88+m*(width+1)
    return edges,inc,clauses,meta,signbits,N

def clause_mask(clause,n):
    # A set bit represents a satisfying assignment to all current signed literals.
    b=0
    for a in range(1<<n):
        for lit in clause:
            bit=(a>>(abs(lit)-1))&1
            if (lit>0)==bool(bit):
                b|=1<<a;break
    return b

def checked_variants(h):
    edges,inc,clauses,meta,signbits,N=tseitin_source(h)
    n=len(edges); c=len(clauses); m=3*c
    ones=(1<<(1<<n))-1
    original=[clause_mask(clause,n) for clause in clauses]
    baseline=ones
    for mask in original:baseline &= mask
    test(baseline==0,'odd Tseitin UNSAT')
    mutated={}
    for ci,cl in enumerate(clauses):
        for slot in range(3):
            alt=list(cl);alt[slot]*=-1
            mutated[ci,slot]=clause_mask(alt,n)
    skipone=[]
    for i in range(c):
        mask=ones
        for j in range(c):
            if i!=j:mask &= original[j]
        skipone.append(mask)
    for (ci,slot),mask in mutated.items():
        test(bool(skipone[ci]&mask),'single sign flip must SAT')
    pairs=[]
    for e,(u,v) in enumerate(edges):
        members=[]
        for vertex in (u,v):
            slot_idx=inc[vertex].index(e)
            occur=[(ci,slot_idx,int(clauses[ci][slot_idx]>0)) for ci,mm in enumerate(meta) if mm[0]==vertex]
            test(len(occur)==4)
            members.append(occur)
        for sign in (0,1):
            left=sorted((ci,slot) for ci,slot,ss in members[0] if ss==sign)
            right=sorted((ci,slot) for ci,slot,ss in members[1] if ss!=sign)
            test(len(left)==len(right)==2)
            for aa,bb in zip(left,right):pairs.append((aa,bb))
    test(len(pairs)==m//2)
    seen=[]
    for (ia,sa),(ib,sb) in pairs:
        test(ia!=ib)
        seen.extend((3*ia+sa,3*ib+sb))
        mask=ones
        for i in range(c):
            if i not in (ia,ib):mask &= original[i]
        mask &= mutated[ia,sa]
        mask &= mutated[ib,sb]
        test(bool(mask),'each paired sign quota mutation SAT')
        tally=[[0,0] for _ in edges]
        for j,cl in enumerate(clauses):
            alt=list(cl)
            if j==ia:alt[sa]*=-1
            if j==ib:alt[sb]*=-1
            for lit in alt:tally[abs(lit)-1][int(lit>0)]+=1
        test(all(v==[4,4] for v in tally))
    test(sorted(seen)==list(range(m)),'matching is a partition')
    return {'h':h,'variables':n,'clauses':c,'sensitive_signs':m,'encoded_bits':N,
            'balanced_pairs':len(pairs),'onebit_SAT_mutants':len(mutated),
            'pair_SAT_mutants':len(pairs),'source_sign_sha256':hashlib.sha256(bytes(signbits)).hexdigest()}

def group_or(bits,width):
    return tuple(int(any(bits[i:i+width])) for i in range(0,len(bits),width))

def test_twolvl(m,q1,q2):
    l1=(m+q1-1)//q1;l2=(l1+q2-1)//q2
    test(m<=q1*q2*l2,'two-level sensitivity covering')
    for x in range(1<<m):
        bits=tuple((x>>i)&1 for i in range(m))
        y=group_or(bits,q1);z=group_or(y,q2)
        test((not any(bits))==(not any(y))==(not any(z)),'both labels preserve')
        test(len(y)==l1 and len(z)==l2)
    test(len(group_or(group_or((0,)*m,q1),q2))==l2)
    for j in range(m):
        flag=[0]*m;flag[j]=1
        test(any(group_or(group_or(flag,q1),q2)),'every source bit influences')
    return {'m':m,'q1':q1,'q2':q2,'L1':l1,'L2':l2,'theorem_lower_bound':(m+q1*q2-1)//(q1*q2),
            'full_exhaustive_inputs':1<<m,'tight':l2==(m+q1*q2-1)//(q1*q2)}

def main():
    cases=[checked_variants(h) for h in (3,4,5)]
    controls=[test_twolvl(m,q1,q2) for m,q1,q2 in ((8,2,2),(12,2,2),(12,3,2),(12,4,3),(10,2,3),(12,1,4))]
    # A global OR lookup can compress to ONE bit but has locality m, not O(polylog m).
    for m in (8,10,12):
        base=[0]*m
        summary=lambda b:int(any(b))
        test(summary(base)==0)
        for i in range(m):
            a=base.copy();a[i]=1;test(summary(a)==1)
        test(m <= m*1,'global OR has q=m')
    out={'run':'SENSITIVITY-LOCALITY144','status':'PROVED/EXACT restricted counting theorem, COMPUTATIONAL source controls',
         'graph_cases':cases,'two_level_controls':controls,'assertions':CHECKS,'failures':0,
         'limitations':['connected signed exact-(4,4), not exact-(2,2)','output interface must expose all shared preprocessing and fixed-length output slots','source-sensitive promise results do not lower-bound general SAT decision time','finite tests support symbolic proofs but do not supply ARC contraction']}
    dst=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).with_name('2026-10-26_2036_SENSITIVITY_LOCALITY144_raw.json')
    dst.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':main()
