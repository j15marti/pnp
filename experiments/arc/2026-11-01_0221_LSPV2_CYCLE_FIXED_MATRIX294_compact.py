#!/usr/bin/env python3
"""LSPV-2 CYCLE-FIXED-MATRIX294 compact source-authenticated F9 falsifier.
Python 3 stdlib. Complete multi-source producer and no-import independent
checker are in the reproducibility archive. This executable tests one
canonical same-source UNSAT cube, not arbitrary-input SAT complexity.
"""
from itertools import product
from collections import Counter
import json

POS=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
NEG=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=POS+tuple(tuple(-v for v in c) for c in NEG)
P={8:0,3:0,7:0,6:0,1:1,5:1}
CYCLE=(3,4,10)  # zero-based ORIGINAL source clause indices

def valid(F,n):
    hits=Counter(l for c in F for l in c)
    return (n%3==0 and len(F)*3==n*4
            and len({tuple(sorted(c)) for c in F})==len(F)
            and all(len(c)==3 and len(set(map(abs,c)))==3
                    and (all(x>0 for x in c) or all(x<0 for x in c))
                    for c in F)
            and all(hits[v]==hits[-v]==2 for v in range(1,n+1)))

def t(c,a):
    return sum(a[abs(l)]==int(l>0) for l in c)

def source_sat(a):
    return all(t(c,a)>=1 for c in F)

def complete_models(p):
    free=sorted(set(range(1,10))-set(p))
    for values in product((0,1),repeat=len(free)):
        a={**p,**dict(zip(free,values))}
        if source_sat(a):
            yield a

def source_gate(p):
    uncovered=[];covered=[];spill=Counter()
    for j,c in enumerate(F):
        if any(abs(l) in p and p[abs(l)]==int(l>0) for l in c):
            covered.append(j)
        else:
            remain=tuple(l for l in c if abs(l) not in p)
            assert remain  # no original empty clause on this F9 pin
            uncovered.append((j,remain))
    for j in covered:
        for lit in F[j]:
            if abs(lit) not in p:
                spill[abs(lit),lit>0]+=1
    free=sorted(set(range(1,10))-set(p))
    eta=sum(min(spill[v,True],spill[v,False]) for v in free)
    pref={v:(0 if spill[v,True]>spill[v,False] else 1)
          for v in free if spill[v,True]!=spill[v,False]}
    return uncovered,free,eta,pref

def outside_rows(uncovered,pref):
    out=[]
    for j,rest in uncovered:
        if j in CYCLE:
            continue
        # odd literal-truth parity: positive RHS 1, negative 1 xor (width mod 2)
        sign=1 if F[j][0]>0 else 0
        rhs=1 if sign else 1^(len(rest)&1)
        out.append((tuple(sorted(map(abs,rest))),rhs,("source-clause",j)))
    for v,b in pref.items():
        out.append(((v,),b,("signed-spill",v)))
    return out

def templates(j,free):
    # Exhaustive small fixed 3-variable cycle-local template verifier.
    # A general simple odd-cycle template is determined by alternating
    # after its selected edge; archive implements that general rule.
    cyc={abs(l) for k in CYCLE for l in F[k] if abs(l) in free}
    for bits in product((0,1),repeat=len(cyc)):
        a=dict(zip(sorted(cyc),bits))
        good=all(sum(a[abs(l)]==int(l>0)
                         for l in F[k] if abs(l) in cyc)==(2 if k==j else 1)
                 for k in CYCLE)
        if good:
            yield a

def project(rows,template,W):
    """Eliminate only W columns. Row provenance is explicit GF(2) XOR."""
    # mask, RHS, provenance set
    ordered=sorted(W)
    basis={}
    for vars_,rhs,origin in rows:
        r=rhs
        for v in vars_:
            if v in template: r^=template[v]
        mask=sum(1<<ordered.index(v) for v in vars_ if v in W)
        provenance={origin}
        while mask:
            pivot=mask.bit_length()-1
            if pivot not in basis:
                basis[pivot]=(mask,r,provenance)
                break
            old,oldr,oldp=basis[pivot]
            mask^=old;r^=oldr;provenance^=oldp
        if not mask and r:
            return {'sat':False,'xor_source_rows':sorted(map(str,provenance))}
    return {'sat':True,'rank':len(basis),'extensions':1<<(len(W)-len(basis))}

def main():
    assert valid(F,9)
    uncovered,free,eta,pref=source_gate(P)
    assert set(j for j,_ in uncovered)=={1,3,4,5,10}
    # Authenticate exactly the 3-cycle source IDs and literal signs.
    ends=[set(abs(l) for l in rest) for j,rest in uncovered if j in CYCLE]
    assert ends==[{4,9},{2,4},{2,9}]
    assert (2*len(free)-len(uncovered)-eta-1)==0
    C=set.union(*ends);W=set(free)-C
    rows=outside_rows(uncovered,pref)
    outcomes=[]
    for j in CYCLE:
        choices=list(templates(j,free))
        assert len(choices)==1,(j,choices)
        res=project(rows,choices[0],W)
        outcomes.append({'selected_edge':j,'template':choices[0],**res})
    assert all(not x['sat'] for x in outcomes)
    assert len(list(complete_models(P)))==0
    assert len(list(complete_models({})))==70
    zero={v:0 for v in range(1,10)}
    one={v:1 for v in range(1,10)}
    assert [[sum(t(c,a)==k for c in F) for k in range(4)]
            for a in (zero,one)]==[[6,0,0,6]]*2
    print(json.dumps({'status':'PASS','target':'canonical M22',
      'F9_full_models':70,'F9_cube_models':0,'free':free,'delta':0,'eta':eta,
      'cycles':[list(CYCLE)],'noncycle_matrix_columns':sorted(W),
      'choices':outcomes,'P_vs_NP':'OPEN'},indent=2))

if __name__=='__main__':
    main()
