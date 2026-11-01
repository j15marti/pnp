#!/usr/bin/env python3
"""ARC288 independently executable canonical all-input root-cofactor countercheck.
Run: python experiments/arc/lspv1_288/check_root_cofactor288.py
No external dependencies. Source proof U198 is NOT reverified by this compact script.
Full generator, independent checker, source certificates and signed controls are
archived separately with the run report.
"""
import ast
import collections
import itertools
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
Y = ((1,2,3),(1,4,5),(2,4,6),(3,5,6),
     (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
K = ((1,2,3),(4,5,6),(7,8,9),(1,4,7),(2,5,8),(3,6,9),
     (-1,-5,-9),(-1,-6,-8),(-2,-4,-9),(-2,-6,-7),(-3,-4,-8),(-3,-5,-7))

def source198():
    p = ROOT / "research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt"
    t = p.read_text(encoding="utf-8")
    u = tuple(tuple(c) for c in ast.literal_eval(t[t.index("[["):]))
    v = [list(c) for c in u]
    v[2][2], v[44][2] = v[44][2], v[2][2]
    return u, tuple(map(tuple,v))

def valid(f,n):
    if not isinstance(n,int) or n<3 or n % 3 or len(f)*3 != 4*n: return False
    if any(abs(x)<1 or abs(x)>n for row in f for x in row): return False
    q=collections.Counter(x for c in f for x in c)
    if any(len(c)!=3 or len({abs(x) for x in c})!=3 or
           not (all(x>0 for x in c) or all(x<0 for x in c))
           for c in f): return False
    if len({tuple(sorted(c)) for c in f}) != len(f): return False
    return all(q[x] == q[-x] == 2 for x in range(1,n+1))

def sat(f,a):
    return all(any(a[abs(x)-1] == int(x>0) for x in c) for c in f)

def test(f,n,name):
    assert valid(f,n)
    count=0
    lo=collections.Counter()
    usable=taut=0
    for x in range(1,n+1):
        pos=[c for c in f if x in c]
        neg=[c for c in f if -x in c]
        assert len(pos)==len(neg)==2
        for p in pos:
            for q in neg:
                rem=[a for a in p if a!=x] + [a for a in q if a!=-x]
                if len(set(map(abs,rem)))==4: usable+=1
                else: taut+=1
        for bit in (0,1):
            child=[tuple(y for y in c if abs(y)!=x) for c in f
                   if (x if bit else -x) not in c]
            assert len(child)==len(f)-2
            assert collections.Counter(map(len,child)) == {3:len(f)-4,2:2}
            assert sum(map(len,child))==4*n-8
            assert not valid(child,n)
            count+=1
            if n<=9:
                for a in itertools.product((0,1),repeat=n):
                    if a[x-1]==bit: assert sat(f,a)==sat(child,a)
    for i,c in enumerate(f):
        for d in f[i+1:]:
            same=any(l in d for l in c)
            opp=any(-l in d for l in c)
            code=''.join(map(str,(int(not opp),int(not same),
                                  int(not same),int(not opp))))
            assert code in ("1111","1001","0110")
            lo[code]+=1
    assert usable+taut==4*n
    return {"source":name,"n":n,"m":len(f),"checked_root_children":count,
            "non_taut_resolvent_pairs":usable,"taut_pairs":taut,
            "source_extreme_compatibility":dict(lo),
            "source_models":sum(sat(f,a) for a in itertools.product((0,1),repeat=n))
            if n<=9 else "see independent original-source certificates"}

def main():
    u,v=source198()
    data=[test(Y,6,"Y6 SAT"),test(K,9,"K33 SAT"),
          test(u,198,"U198 UNSAT"),test(v,198,"V198 SAT")]
    assert sum(d["checked_root_children"] for d in data)==822
    assert [(d["non_taut_resolvent_pairs"],d["taut_pairs"]) for d in data] == [
            (4,20),(36,0),(780,12),(780,12)]
    assert [d["source_models"] for d in data[:2]]==[20,18]
    assert not valid([(1,2,3)],6)
    assert not valid(((1,2,999),)*8,6)
    assert not valid(tuple((1,2,3) for _ in range(8)),6)
    assert not valid(((1,2,3),(1,2,4)),6)
    print(json.dumps({"status":"PASS","proof_scope":"restricted raw canonical cofactors",
                      "native_FLMV_tape_simulation":False,"data":data},indent=2))
if __name__=="__main__": main()
