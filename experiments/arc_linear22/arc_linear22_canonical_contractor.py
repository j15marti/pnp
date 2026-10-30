#!/usr/bin/env python3
"""Exact source-only promise contraction for canonical F_k (NOT all-input SAT).
On an authenticated canonical stream, return a fixed terminal F_7. Else UNKNOWN.
"""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from arc_linear22_projection_firewall import formula
from arc_mixed_projection_test import source_sat,bitcnf

def certify(n,clauses):
    if n%3 or n<21 or (n//3)%2==0:return None
    k=n//3
    if len(clauses)!=4*k:return None
    # Complete source syntax match, including every signed literal and order.
    for s in range(4):
        sign=1 if s<2 else -1
        for i in range(k):
            wanted=(sign*(i+1),sign*(k+(i+s)%k+1),sign*(2*k+(i+2*s)%k+1))
            if tuple(clauses[s*k+i])!=wanted:return None
    return [1]*k+[0]*(2*k)

def contract(n,clauses):
    witness=certify(n,clauses)
    if witness is None:return ('UNRESOLVED',None)
    assert source_sat(clauses,witness)
    if n==21:return ('SAT_BASE',None)
    return ('CERTIFIED_CHILD',formula(7))

if __name__=='__main__':
    out=[]
    for k in (7,9,11,15,21,31):
        n,F=formula(k)
        status,child=contract(n,F)
        assert status==('SAT_BASE' if k==7 else 'CERTIFIED_CHILD')
        if child:
            assert source_sat(child[1],[1]*7+[0]*14)
            assert bitcnf(child[1],child[0])<bitcnf(F,n)
        mutant=F.copy();mutant[0]=tuple(-z if j==0 else z for j,z in enumerate(mutant[0]))
        assert contract(n,mutant)[0]=='UNRESOLVED'
        out.append({'k':k,'input_bits':bitcnf(F,n),'status':status,
                    'terminal_bits':None if not child else bitcnf(child[1],child[0]),
                    'negative_control_rejected':True})
    print(json.dumps(out,indent=2))
    with open(Path(__file__).resolve().parent/'arc_linear22_canonical_contractor_results.json','w') as f:json.dump(out,f,indent=2)
