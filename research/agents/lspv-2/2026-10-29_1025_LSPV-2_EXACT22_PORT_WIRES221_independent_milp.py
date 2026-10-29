#!/usr/bin/env python3
"""Independent optimization-based SAT checks on the *actual* 30-var CNFs."""
import json,sys,scipy,numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import coo_matrix
from exact22_port_wires221 import make_pair

def solve(C,n,pins):
    rows=[];cols=[];vals=[];lo=[]
    for i,cl in enumerate(C):
        # sum_{positive} x + sum_{negative}(1-x) >= 1.
        for z in cl:
            rows.append(i);cols.append(abs(z)-1);vals.append(1. if z>0 else -1.)
        lo.append(1.-sum(z<0 for z in cl))
    A=coo_matrix((np.array(vals), (np.array(rows),np.array(cols))), shape=(len(C),n)).tocsr()
    lower=np.zeros(n);upper=np.ones(n)
    for var,bit in pins.items():lower[var-1]=upper[var-1]=bit
    res=milp(c=np.zeros(n),integrality=np.ones(n),bounds=Bounds(lower,upper),
             constraints=[LinearConstraint(A, np.array(lo),np.full(len(C),np.inf))],
             options={'presolve':True})
    if res.status==0:
        x=np.rint(res.x).astype(int)
        assert all(any((x[abs(z)-1]==1) == (z>0) for z in cl) for cl in C)
        assert all(x[i-1]==b for i,b in pins.items())
        return True
    assert res.status==2, f'Unexpected optimizer status {res.status}'
    return False

out={'scipy':scipy.__version__,'cases':{}}
for kind in ('eq','xor'):
    C=make_pair(kind)
    data={}
    for a in (0,1):
        for b in (0,1):
            ans=solve(C,30,{4:a,19:b})
            assert ans==((a==b) if kind=='eq' else (a!=b))
            data[f'{a}{b}']=ans
    out['cases'][kind]=data
print(json.dumps(out,indent=2,sort_keys=True))
