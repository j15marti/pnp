#!/usr/bin/env python3
"""LSPV-3 QUANTIFIER60: standalone proper-3CNF one-sign SAT/UNSAT check."""
from itertools import product

def force_false(t,p,q):
    return [(-t,a*p,b*q) for a,b in product((1,-1),repeat=2)]

def encode(H,b):
    # H has universal variable 1 and existentials 2,3.
    # a,c,p,q,p2,q2 are fresh and do not collide with H.
    a,c,p,q,p2,q2=4,5,6,7,8,9
    clauses=list(H)
    clauses += force_false(a,p,q)+force_false(c,p2,q2)
    clauses.append((1 if b else -1,a,c))
    assert all(len(C)==3 and len(set(map(abs,C)))==3 for C in clauses)
    return clauses

def sat(clauses,n=9):
    for vals in product((False,True),repeat=n):
        if all(any(vals[abs(l)-1]==(l>0) for l in C) for C in clauses):
            return True
    return False

def fixed_source(clauses):
    n=9; m=len(clauses); w=1+max(n,m).bit_length()
    def word(i):return format(i,"0%db"%w)
    return "".join([word(n),word(m)]+[
       ("1" if lit<0 else "0")+format(abs(lit),"0%db"%(w-1))
       for C in clauses for lit in C])

if __name__=="__main__":
    H_force_u=((1,2,3),(1,2,-3),(1,-2,3),(1,-2,-3))
    H_all_sat=((1,2,3),)
    H_all_unsat=tuple(tuple(i if b else -i
        for i,b in zip((1,2,3),v)) for v in product((0,1),repeat=3))
    expected={"mixed":(False,True),"all_sat":(True,True),
              "all_unsat":(False,False)}
    for name,H in (("mixed",H_force_u),("all_sat",H_all_sat),
                   ("all_unsat",H_all_unsat)):
        C0,C1=encode(H,0),encode(H,1)
        bits0,bits1=fixed_source(C0),fixed_source(C1)
        assert len(bits0)==len(bits1)
        assert sum(a!=b for a,b in zip(bits0,bits1))==1
        result=(sat(C0),sat(C1))
        assert result==expected[name],(name,result)
        print(name,result,len(bits0),"bits",len(C0),"clauses")
    print("PASS: six ordinary proper-3CNF sources, SAT and UNSAT, one-bit control")
