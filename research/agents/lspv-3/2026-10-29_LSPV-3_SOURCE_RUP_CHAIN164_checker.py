#!/usr/bin/env python3
"""Separate DIMACS/LRAT subset checker for SOURCE-RUP-CHAIN164.
Reads source DIMACS with every cofactor assumption unit as an indexed clause.
Checks all additions by specified-hint unit propagation and requires empty.
Not a formally verified kernel; external LRUP/Isabelle check remains open.
"""
import sys

def parse_cnf(path):
    clauses=[]; declared=None
    for ln in open(path,encoding='utf-8'):
        ln=ln.strip()
        if not ln or ln.startswith('c'): continue
        if ln.startswith('p '):
            ps=ln.split(); assert ps[1]=='cnf';declared=(int(ps[2]),int(ps[3]));continue
        vals=[int(x) for x in ln.split()]
        assert vals and vals[-1]==0 and 0 not in vals[:-1]
        clauses.append(tuple(vals[:-1]))
    assert declared is not None and len(clauses)==declared[1]
    assert all(0<abs(x)<=declared[0] for c in clauses for x in c)
    return {i+1:cl for i,cl in enumerate(clauses)}

def rup_with_hints(database, conclusion, hints):
    ass={}
    for l in conclusion:
        k=abs(l);f=int(l<0)
        if k in ass and ass[k]!=f:
            return True
        ass[k]=f
    for h in hints:
        assert h in database
        cl=database[h]
        true=False;unassigned=[]
        for l in cl:
            x=abs(l)
            if x not in ass: unassigned.append(l)
            elif ass[x]==int(l>0): true=True;break
        if true: continue
        if len(unassigned)==0:return True
        if len(unassigned)!=1:return False
        unit=unassigned[0]
        ass[abs(unit)]=int(unit>0)
    return False

def check(cnf,lrat):
    db=parse_cnf(cnf)
    initial=len(db);checked=0;last=None
    for ln in open(lrat,encoding='utf-8'):
        if not ln.strip() or ln.startswith('c'):continue
        ints=[int(x) for x in ln.split()]
        assert ints and ints[0]==len(db)+1, (ints[:1],len(db))
        assert ints.count(0)==2
        k=ints.index(0)
        c=tuple(ints[1:k]); h=ints[k+1:-1]
        assert len(set(c))==len(c) and not any(-x in c for x in c)
        assert h and rup_with_hints(db,c,h),(ints[0],c,h)
        db[ints[0]]=c;last=c;checked+=1
    assert checked and last==(),last
    return {'source_clauses':initial,'checked_derived_clauses':checked,'status':'VERIFIED UNSAT BY INDEPENDENT PYTHON RUP CHECKER'}

if __name__=='__main__':
    assert len(sys.argv)==3
    print(check(sys.argv[1],sys.argv[2]))
