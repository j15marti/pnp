#!/usr/bin/env python3
"""LSPV-1 311: deterministic UP-first DPLL baseline with measured recursion nodes
and literal inspections. This comparator does NOT import the prefix solver."""
import json
from pathlib import Path
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
def solve(F,n,pins):
    c={'nodes':0,'literal_tests':0,'forced_units':0,'branches':0}
    def go(a):
        c['nodes']+=1
        while True:
            uns=[];forced=[]
            for clause in F:
                okay=False;pending=[]
                for lit in clause:
                    c['literal_tests']+=1
                    v=a.get(abs(lit))
                    if v is None:pending.append(lit)
                    elif v==(lit>0):okay=True;break
                if okay:continue
                if not pending:return False
                uns.append(pending)
                if len(pending)==1:forced.append(pending[0])
            if not uns:return True
            if not forced:break
            for lit in forced:
                v=abs(lit);value=lit>0
                if v in a and a[v]!=value:return False
                if v not in a:a[v]=value;c['forced_units']+=1
        v=next(i for i in range(1,n+1) if i not in a)
        c['branches']+=1
        for value in (False,True):
            b=dict(a);b[v]=value
            if go(b):return True
        return False
    label=go(dict(pins))
    return dict(result='SAT' if label else 'UNSAT',**c)
if __name__=='__main__':
    p={1:True,3:False,5:True,6:False,7:False,8:False}
    q=dict(p);q[1]=False
    result={
      'F9_root':solve(F9,9,{}),
      'F9_unsat_cube':solve(F9,9,p),
      'F9_sat_cube':solve(F9,9,q),
      'Y6_root':solve(Y6,6,{})}
    assert [result[x]['result'] for x in
      ('F9_root','F9_unsat_cube','F9_sat_cube','Y6_root')]==[
      'SAT','UNSAT','SAT','SAT']
    print(json.dumps(result,indent=2))
