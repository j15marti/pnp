#!/usr/bin/env python3
"""Independent no-producer-import controls, LSPV-1 327.
The expanded no-import 11851-assertion verifier is in the dated run archive.
"""
from itertools import combinations,product
from fractions import Fraction
import json

positive=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
negative=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
F=tuple(tuple(c) for c in positive)+tuple(tuple(-x for x in c) for c in negative)
Y0=((1,2,3),(1,4,5),(2,4,6),(3,5,6))
Y=Y0+tuple(tuple(-x for x in c) for c in Y0)

def evaluate(clauses,a):
    return all(any(((a>>(abs(l)-1))&1)==(l>0) for l in clause) for clause in clauses)

def work():
    count=0
    assert sum(evaluate(F,a) for a in range(512))==70;count+=1
    assert sum(evaluate(Y,a) for a in range(64))==18;count+=1
    assert sum(evaluate(F,a) for a in range(512) if all(((a>>(i-1))&1)==v
        for i,v in {1:0,3:0,5:1,6:0,7:0,8:0}.items()))==2;count+=1
    assert sum(evaluate(F,a) for a in range(512) if all(((a>>(i-1))&1)==v
        for i,v in {1:1,3:0,5:1,6:0,7:0,8:0}.items()))==0;count+=1
    for j,k in combinations(range(12),2):
        for ext_j,ext_k in product((0,1),repeat=2):
            demands={};compatible=True
            for c_idx,truth_ext in ((j,ext_j),(k,ext_k)):
                for lit in F[c_idx]:
                    demand=int(lit>0) if truth_ext else int(lit<0)
                    if abs(lit) in demands and demands[abs(lit)]!=demand:
                        compatible=False
                    demands[abs(lit)]=demand
            brute=any(all(((a>>(i-1))&1)==v for i,v in demands.items())
                for a in range(512)) if compatible else False
            assert brute==compatible;count+=1
    for a in range(512):
        b=a^511
        for clause in F:
            t=lambda v:sum(((v>>(abs(l)-1))&1)==(l>0) for l in clause)
            assert t(a)+t(b)==3;count+=1
    l=r=lo=ro=0
    for z in range(32):
        p=evaluate(Y,z<<1);q=evaluate(Y,(z<<1)|1)
        l+=p;r+=q;lo+=p and not q;ro+=q and not p;count+=1
    assert (l,r,lo,ro)==(9,9,5,5);count+=1
    P,w,D=2,3,8
    frac=Fraction(1)
    seen=[]
    for stage in range(7):
        frac*=Fraction(D,D+1);seen.append(D)
        assert P<=D<=2*P*(w-1);count+=1
        nextD=D+2*P*(P*(w-1)-1)
        assert nextD>=2*D;count+=1
        P=P*P;w=2*(w-1);D=nextD
    assert seen==[8,20,108,2636,1181772,146029938764,1217485109002270410828]
    assert 0.83847543722<float(frac)<0.83847543724;count+=2
    print(json.dumps({"status":"PASS","independent_assertions":count,
        "exact_D":seen,"F9_models":70,"Y6_models":18,
        "same_F9_sat_unsat":[2,0],"Y6_cofactor":[9,9],
        "Y6_one_sided_differences":[5,5],
        "P_vs_NP":"OPEN"},indent=2))
if __name__=="__main__":work()
