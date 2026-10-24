#!/usr/bin/env python3
"""MINCORE-ORACLE89: deterministic exact proper-3CNF adversary audit.

No external packages, randomness, or SAT libraries. Exhaustive strict
subformulas are verified with an independent recursive DPLL implementation.
This is a finite correctness test, not a complexity lower bound.
"""
from __future__ import annotations
import itertools
import json
import hashlib
from pathlib import Path

OUT = Path(__file__).with_name("MINCORE_ORACLE89_RAW.json")
checks = dict(shape=0, parent=0, deletions=0, strict_subformulas=0,
              explicit_word_flips=0, brute_counts=0, adaptive_zero_answer=0)


def source(q: int, b: tuple[int,...]) -> tuple[tuple[int,int], ...]:
    assert len(b) == q and all(v in (0,1) for v in b)
    z0, zq, u, v = 1, q+1, q+2, q+3
    clauses = [(z0,u),(z0,-u),(-zq,v),(-zq,-v)]
    for i, bit in enumerate(b, start=1):
        clauses.append((-i, i+1 if bit else -(i+1)))
    return tuple(clauses)


def lift(q: int, b: tuple[int,...]) -> tuple[tuple[int,int,int],...]:
    cls = []
    for j, (a, c) in enumerate(source(q,b)):
        t = q + 4 + j
        cls.extend(((a,c,t),(a,c,-t)))
    return tuple(cls)


def sat(clauses: tuple[tuple[int,...],...]) -> bool:
    """Exact DPLL with unit propagation, no class-specific decision rule."""
    def rec(rows, assignment):
        while True:
            changed = False
            simplified=[]
            for clause in rows:
                undec=[]
                good=False
                for lit in clause:
                    v=abs(lit)
                    if v in assignment:
                        if assignment[v] == (lit > 0):
                            good=True
                            break
                    else:
                        undec.append(lit)
                if good:
                    continue
                if not undec:
                    return False
                if len(undec)==1:
                    lit=undec[0];v=abs(lit);value=(lit>0)
                    if v in assignment and assignment[v]!=value:
                        return False
                    if v not in assignment:
                        assignment[v]=value
                        changed=True
                else:
                    simplified.append(tuple(undec))
            if not changed:
                rows=simplified
                break
        if not rows:
            return True
        lit=min(rows,key=len)[0]
        v=abs(lit)
        for value in ((lit>0), (lit<0)):
            next_a=assignment.copy(); next_a[v]=value
            if rec(rows,next_a):return True
        return False
    return rec(clauses,{})


def brute_count(clauses, n):
    out=0
    for values in itertools.product((False,True),repeat=n):
        if all(any((values[abs(x)-1] == (x>0)) for x in row) for row in clauses):
            out+=1
    return out


def records(q,b):
    clauses=lift(q,b)
    n=2*q+7;m=2*q+8
    ret=[n,m]
    for c in clauses:
        ret.append(3)
        ret.extend(2*abs(v) + int(v<0) for v in c)
    width=(64*(4*q+16)-1).bit_length()
    assert max(ret)<2**width
    return tuple(ret),width


def assert_shape(q,b):
    s=source(q,b); p=lift(q,b)
    assert len(s)==q+4 and len(p)==2*q+8
    assert len(set(p))==len(p)
    assert len({abs(x) for row in p for x in row})==2*q+7
    assert all(len(set(map(abs,cl)))==3 for cl in p)
    words,w=records(q,b)
    assert len(words)==8*q+34
    checks['shape']+=1


def main():
    detail=[]
    for q in range(1,10):
        allone=(1,)*q
        clauses=lift(q,allone)
        assert_shape(q,allone)
        assert not sat(clauses)
        checks['parent']+=1
        # Minimal unsatisfiability: every singleton clause deletion is SAT.
        for j in range(len(clauses)):
            assert sat(clauses[:j]+clauses[j+1:])
            checks['deletions']+=1
        head,w=records(q,allone)
        all_changed=set()
        for i in range(q):
            b=list(allone);b[i]=0;b=tuple(b)
            assert_shape(q,b)
            alt=lift(q,b)
            assert sat(alt)
            checks['parent']+=1
            modified,_=records(q,b)
            delta={j for j,(a,c) in enumerate(zip(head,modified)) if a!=c}
            assert len(delta)==2 and not (delta & all_changed)
            all_changed |=delta
            checks['explicit_word_flips']+=1
            for j in range(len(alt)):
                assert sat(alt[:j]+alt[j+1:])
                checks['deletions']+=1
        assert len(all_changed)==2*q
        n=2*q+7;m=2*q+8
        detail.append(dict(q=q,n=n,m=m,width=w,N=(8*q+34)*w,
                           exact_word_changes_per_orientation=2,
                           q_sensitive_groups=q,
                           strict_child_oracle_answers='SAT'))
    for q in range(1,4):
        base=(1,)*q
        oneflip=(0,)+(1,)*(q-1)
        for b in [base,oneflip]:
            p=lift(q,b)
            m=len(p)
            for mask in range((1<<m)-1):
                sub=tuple(p[j] for j in range(m) if mask & (1<<j))
                assert sat(sub), (q,b,mask)
                checks['strict_subformulas']+=1
                # An adaptive index-only oracle transcript learns only 'SAT'.
                checks['adaptive_zero_answer']+=1
    for q in range(1,7):
        for b in itertools.product((0,1),repeat=q):
            src=source(q,b)
            c=brute_count(src,q+3)
            assert (c==0)==(all(b))
            # All padded variables are free on every satisfying source model.
            expanded_models=c*(1<<(q+4))
            if q<=2:
                assert brute_count(lift(q,b),2*q+7)==expanded_models
            checks['brute_counts']+=1
    data={"run_id":"MINCORE-ORACLE89",
          "status":"COMPUTATIONAL audit; symbolic lemmas separate",
          "range":"q=1..9 minimality/word changes; q=1..3 every strict subformula; q=1..6 model counts",
          "seed":None,"failures":0,"checks":checks,
          "check_total":sum(checks.values()),"by_size":detail,
          "limitations":["oracle restricted to proper clause-deletion children", "no arbitrary-SAT time lower bound", "the all-input fallback can be expensive", "not physical FLMV TM trace"]}
    raw=json.dumps(data,indent=2,sort_keys=True)+'\n'
    OUT.write_text(raw)
    print(raw)
    print("sha256_raw",hashlib.sha256(raw.encode()).hexdigest())

if __name__=='__main__':main()
