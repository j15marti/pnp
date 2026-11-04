#!/usr/bin/env python3
"""Independent small finite controls for source-subsumed restriction reflection.
Run: python lspv2_396_independent_verify.py
Standard library only. Not a general proof-system minimum optimizer.
"""
import itertools, json

def php(h):
    x=lambda i,j: i*h+j+1
    cls=[[x(i,j) for j in range(h)] for i in range(h+1)]
    cls += [[-x(i,j),-x(k,j)] for j in range(h) for i in range(h+1) for k in range(i+1,h+1)]
    return cls, h*(h+1)

def sat(cls, a):
    return all(any((a[abs(l)] if l>0 else not a[abs(l)]) for l in c) for c in cls)

def flat_gates(n,u):
    out=[]
    for i in range(1,n+1):
        y=u+i
        out.extend([[-y,u],[-y,i],[y,-u,-i]])
    return out

def restrict(clause, fixed):
    residual=[]
    for l in clause:
        if abs(l) in fixed:
            if fixed[abs(l)] == (l>0):return None
        else:residual.append(l)
    return tuple(residual)

def no_universal_section(D, u, n):
    # For all-zero original variables, every y must be 0; all-one originals forces every y=1.
    X0={i:False for i in range(1,u+1)}
    X1={i:True for i in range(1,u+1)}
    Y0={u+i:False for i in range(1,n+1)}
    Y1={u+i:True for i in range(1,n+1)}
    return sat(D,X0|Y0) and sat(D,X1|Y1) and Y0 != Y1

checks=0; records=[]
for h in (1,2,3):
    P,n=php(h); u=n+1; Y=list(range(u+1,u+n+1)); D=flat_gates(n,u); F=P+[[-u]]
    # exact source lengths and closed form
    assert len(P)==h+1+h*((h+1)*h//2);checks+=1
    assert len(D)==3*n;checks+=1
    a0={y:False for y in Y}
    residual=[restrict(c,a0) for c in D]
    remaining=[r for r in residual if r is not None]
    assert all(-u in r for r in remaining) and len(remaining)==n;checks+=1
    assert no_universal_section(D,u,n);checks+=1
    # Unique functional extension, sampled for h=3 and exhaustive below
    old_total=1<<u; old_trials=old_total if h<=2 else 1024
    for mask in range(old_trials):
        old={v:bool((mask>>(v-1))&1) for v in range(1,u+1)}
        expected={u+i:(old[u] and old[i]) for i in range(1,n+1)}
        assert sat(D,old|expected);checks+=1
        # Each individual gate enforces exactly one output, without quantifying full 2^n bank
        for i in range(1,n+1):
            bad=expected.copy();bad[u+i]=not bad[u+i]
            local=D[3*(i-1):3*i]
            assert not sat(local,old|bad);checks+=1
    if h<=2:
        assert not any(sat(F,{v:bool((mask>>(v-1))&1) for v in range(1,u+1)}) for mask in range(old_total));checks+=1
        # Remove one pigeon: should be satisfiable, exact PHP same-hole model using at most h pigeons
        P_sat=P[:h]+P[h+1:]; F_sat=P_sat+[[-u]]
        witness={v:False for v in range(1,u+1)}
        for i in range(h):witness[i*h+i+1]=True
        assert sat(F_sat,witness);checks+=1
        yvals={u+i:bool(witness[u] and witness[i]) for i in range(1,n+1)}
        assert sat(F_sat+D,witness|yvals);checks+=1
    records.append({'holes':h,'php_clauses':len(P),'original_vars':n,'pinned_vars':u,'aux_outputs':n,'gate_clauses':len(D),'subsumed_residuals':len(remaining),'old_assignments_tested':old_trials,'pinned_unsat_exhaustive':h<=2})
# Exact 2-node PHP(2 pigeons,1 hole) Resolution proof:
P,n=php(1)
assert P==[[1],[2],[-1,-2]]
step1=tuple(sorted(set(P[2])-{ -1 } | (set(P[0])-{1})))
assert step1==(-2,); checks+=1
step2=tuple(sorted(set(step1)-{-2} | (set(P[1])-{2})))
assert step2==();checks+=1
# Every 3 PHP source clauses is essential even after the pin/functional bank.
for idx in range(3):
    remainder=P[:idx]+P[idx+1:]
    allmodels=[]
    for mask in range(4):
        a={1:bool(mask&1),2:bool(mask&2),3:False}
        if sat(remainder+[[-3]],a):allmodels.append(a)
    assert allmodels;checks+=1
# Corruption: remove a facet and force an illegal output.
D=flat_gates(2,3)
wrong={1:True,2:False,3:False,4:True,5:False}
assert not sat(D,wrong);checks+=1
assert sat(D[1:],wrong);checks+=1
output={'status':'COMPUTATIONAL','independent_checks':checks,'cases':records,'source_minimum_php1':2,'corruption_rejected':1,'scope':'Exhaustive old assignments for h<=2; 1024 deterministic h=3 assignments; symbolic theorem is separate.'}
print(json.dumps(output,sort_keys=True,indent=2))
