#!/usr/bin/env python3
"""TMR-5/087 independent SciPy/HiGHS infeasibility check.
Usage: python tmr5_087_milp_independent.py tmr5_087_W33_oriented.txt
Uses five binary label columns per vertex and forbids 15 pairs per directed arc.
"""
import json,sys,time
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import coo_matrix

p=sys.argv[1] if len(sys.argv)>1 else "tmr5_087_W33_oriented.txt"
with open(p,encoding="utf8") as f:
    n,m=map(int,f.readline().split())
    arcs=[tuple(map(int,line.split())) for line in f if line.strip()]
assert (n,m,len(arcs))==(80,160,160)
r,c,val=[],[],[]
lo,hi=[],[]
for v in range(n):
    row=len(lo)
    for a in range(5):
        r.append(row);c.append(5*v+a);val.append(1)
    lo.append(1);hi.append(1)
for u,v in arcs:
    for a in range(5):
        for b in range(5):
            if (b-a)%5 not in (1,3):
                row=len(lo)
                r.extend([row,row]);c.extend([5*u+a,5*v+b]);val.extend([1,1])
                lo.append(-np.inf);hi.append(1)
A=coo_matrix((val,(r,c)),shape=(len(lo),5*n)).tocsr()
start=time.monotonic()
res=milp(np.zeros(5*n),integrality=np.ones(5*n),
         bounds=Bounds(np.zeros(5*n),np.ones(5*n)),
         constraints=LinearConstraint(A,np.array(lo),np.array(hi)),
         options={"time_limit":45.0})
print(json.dumps({"solver":"SciPy MILP / HiGHS","status":int(res.status),
    "infeasible":res.status==2,"binary_variables":5*n,
    "linear_constraints":len(lo),"nonzero_coefficients":int(A.nnz),
    "wall_seconds":round(time.monotonic()-start,3)},indent=2))
assert res.status==2,"Infeasibility not proven"
