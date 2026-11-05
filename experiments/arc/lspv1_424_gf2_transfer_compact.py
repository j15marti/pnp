#!/usr/bin/env python3
"""LSPV-1/424 compact exact GF(2) one-step to strict Resolution experiment.
All 1024 ordered pairs of 4-variable GF(2) equations; source clauses are
their full, exact canonical CNFs. This does NOT execute native R_mix341.
"""
from itertools import product
import json
def clause(xs): return tuple(sorted(set(xs),key=lambda k:(abs(k),k<0)))
def equation(mask,rhs):
    names=[i+1 for i in range(4) if mask>>i&1]
    return [clause(-v if bit else v for v,bit in zip(names,a))
            for a in product((0,1),repeat=len(names)) if sum(a)%2!=rhs]
def resolve(a,b,p):
    assert p in a and -p in b
    c=clause(list(x for x in a if x!=p)+list(x for x in b if x!=-p))
    assert not any(-x in c for x in c)
    return c
def derive(src,goal):
    src=list(src); steps=[]; support=sorted({abs(x) for c in src+(goal,) for x in c})
    fixed={abs(x):(x<0) for x in goal}
    free=[x for x in support if x not in fixed]
    def get(j):return src[j] if j<len(src) else steps[j-len(src)][3]
    def rec(i,a):
        if i==len(free):
            for j,c in enumerate(src):
                if all(a[abs(x)]!=(x>0) for x in c): return j
            raise AssertionError("invalid GF(2) entailment")
        x=free[i];a[x]=False;u=rec(i+1,a)
        a[x]=True;v=rec(i+1,a)
        a.pop(x)
        if x in get(u) and -x in get(v):
            c=resolve(get(u),get(v),x)
            steps.append((u,v,x,c));return len(src)+len(steps)-1
        if x not in get(u):return u
        assert -x not in get(v);return v
    root=rec(0,dict(fixed))
    seen=list(src)
    for a,b,p,c in steps:
        assert resolve(seen[a],seen[b],p)==c
        seen.append(c)
    assert set(seen[root])<=set(goal)
    return len(steps)
def main():
    cases=outputs=nodes=max_one=0
    for a,ra,b,rb in product(range(16),(0,1),range(16),(0,1)):
        src=equation(a,ra)+equation(b,rb)
        for goal in equation(a^b,ra^rb):
            k=derive(src,goal);nodes+=k;outputs+=1;max_one=max(max_one,k)
        cases+=1
    result={"scope":"four-variable two-row GF(2) only; strict Resolution output subclauses",
      "cases":cases,"output_clauses_checked":outputs,
      "total_res_nodes":nodes,"max_res_per_output":max_one}
    assert (cases,outputs,nodes,max_one)==(1024,2592,2210,15),result
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
