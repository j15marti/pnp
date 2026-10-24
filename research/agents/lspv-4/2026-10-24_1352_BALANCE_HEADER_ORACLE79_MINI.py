#!/usr/bin/env python3
"""PC22_ALLFIELD1 nonlocal-header bit audit, both SAT and UNSAT controls.
Standard library only. Result is a restricted query-model theorem.
"""
from itertools import product
import json

def source(q, negative_index=None, unsat=False):
    assert q >= 3
    rows = []
    for i in range(q):
        rows.append((-1 if i == negative_index else 1, 2+2*i, 3+2*i))
    if unsat:
        c,d,e = 2*q+2, 2*q+3, 2*q+4
        for s in product((1,-1), repeat=3):
            rows.append((s[0]*c,s[1]*d,s[2]*e))
    return tuple(rows),2*q+1+3*int(unsat)

def g_of(rows,n):
    counts={i:[0,0] for i in range(1,n+1)}
    for clause in rows:
        assert len(clause)==3 and len({abs(l) for l in clause})==3
        for lit in clause:
            counts[abs(lit)][lit<0]+=1
    return sum(2*max(p,neg,2)-p-neg for p,neg in counts.values() if p+neg)

def width(n,m):
    return (64*(n+m+1)-1).bit_length()

def metrics(rows,n):
    m=len(rows)
    g=g_of(rows,n)
    vn=9*(m+7*g)
    mm=12*(m+7*g)
    return dict(n=n,m=m,g=g,target_n=vn,target_m=mm,
        source_N=(4*m+2)*width(n,m),
        target_N=(4*mm+2)*width(vn,mm),
        header_bit1=(vn>>1)&1)

def dpll(clauses):
    def aux(cs,assigned):
        while True:
            filtered=[]
            for clause in cs:
                if any(abs(lit) in assigned and assigned[abs(lit)]==(lit>0) for lit in clause):
                    continue
                cc=tuple(lit for lit in clause if abs(lit) not in assigned)
                if not cc: return False
                filtered.append(cc)
            cs=filtered
            unit=next((c[0] for c in cs if len(c)==1),None)
            if unit is None: break
            assigned[abs(unit)]=unit>0
        if not cs: return True
        v=abs(cs[0][0])
        return aux(cs,{**assigned,v:False}) or aux(cs,{**assigned,v:True})
    return aux([tuple(c) for c in clauses],{})

def audit(max_q=64):
    checks=0
    rows=[]
    for q in range(3,max_q+1):
        for unsat in (False,True):
            formula,n=source(q,None,unsat)
            a=metrics(formula,n)
            assert a["g"]==7*q
            assert a["target_n"]==450*q+72*int(unsat)
            assert a["target_m"]==600*q+96*int(unsat)
            checks+=3
            for i in range(q):
                flipped,n2=source(q,i,unsat)
                b=metrics(flipped,n2)
                assert b["source_N"]==a["source_N"]
                assert b["g"]==a["g"]-2
                assert b["target_n"]==a["target_n"]-126
                assert b["target_m"]==a["target_m"]-168
                assert b["header_bit1"]!=a["header_bit1"]
                checks+=5
            if q<=5:
                assert dpll(formula)==(not unsat)
                checks+=1
            if q in (3,4,8,16,32,64):
                rows.append(dict(q=q,label="UNSAT" if unsat else "SAT",**a))
    return dict(run="BALANCE-HEADER-ORACLE79",status="COMPUTATIONAL",checks=checks,
                failures=0,range={"min_q":3,"max_q":max_q},
                sample_rows=rows,
                limits="Finite tests verify exact normalizer arithmetic; no general SAT time lower bound.")
if __name__=="__main__":
    print(json.dumps(audit(),indent=2))
