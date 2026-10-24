#!/usr/bin/env python3
"""MINCORE-ADAPTIVE-ORACLE89: independent small exact reproducer.
No dependencies or randomness. Separate from the full 87,375-check auditor.
"""
import itertools
import json

def formula(q, bits):
    z0, zq, u, v = 1, q+1, q+2, q+3
    src=[(z0,u),(z0,-u),(-zq,v),(-zq,-v)]
    src += [(-i, (i+1) if bits[i-1] else -(i+1))
            for i in range(1,q+1)]
    out=[]
    for j, (x,y) in enumerate(src):
        t=q+4+j
        out.extend(((x,y,t),(x,y,-t)))
    return tuple(out)

def exact_sat(clauses):
    """Exhaustive SAT truth table (independent from the full DPLL auditor)."""
    used=sorted({abs(x) for c in clauses for x in c})
    # Small q only; missing variables are unconstrained.
    for values in itertools.product((False,True), repeat=len(used)):
        a=dict(zip(used,values))
        if all(any(a[abs(x)]==(x>0) for x in row) for row in clauses):
            return True
    return False

def word_records(q, bits):
    rows=formula(q,bits)
    w=(64*(4*q+16)-1).bit_length()
    data=[2*q+7,2*q+8]
    for c in rows:
        data += [3] + [2*abs(x)+(x<0) for x in c]
    assert len(data)==8*q+34
    assert max(data)<1<<w
    return tuple(data),w

def main():
    checks=0
    for q in range(1,5):
        bad=(1,)*q
        U=formula(q,bad)
        assert not exact_sat(U);checks+=1
        assert len(U)==2*q+8
        assert len({abs(x) for row in U for x in row})==2*q+7
        assert len(set(U))==len(U)
        checks+=3
        for drop in range(len(U)):
            assert exact_sat(U[:drop]+U[drop+1:])
            checks+=1
        orig,width=word_records(q,bad)
        used=set()
        for j in range(q):
            alt=list(bad);alt[j]=0;alt=tuple(alt)
            V=formula(q,alt)
            assert exact_sat(V); checks+=1
            now,w=word_records(q,alt)
            assert w==width;checks+=1
            delta={k for k in range(len(orig)) if orig[k]!=now[k]}
            assert len(delta)==2 and not used.intersection(delta)
            used.update(delta);checks+=1
        assert len(used)==2*q;checks+=1

    # Exhaust every proper subset for two opposite-label parents, q=1,2.
    for q in (1,2):
        for b in ((1,)*q,(0,)+(1,)*(q-1)):
            rows=formula(q,b)
            for mask in range((1<<len(rows))-1):
                child=tuple(row for j,row in enumerate(rows) if mask&(1<<j))
                assert exact_sat(child)
                checks+=1
    print(json.dumps(dict(run_id="MINCORE-ADAPTIVE-ORACLE89",
                          independent_exhaustive_checks=checks,
                          failures=0, status="COMPUTATIONAL restricted"),
                     indent=2))

if __name__ == "__main__":
    main()
