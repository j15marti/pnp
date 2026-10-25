#!/usr/bin/env python3
"""Role 2 M22-TWO-PIN-LIFT148 ordinary serialized two-level controls.
Python 3 standard library. Optional published 198-name UNSAT source:
python M22_TWO_PIN_LIFT148_twolevel_repro.py --u research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt
No physical FLMV bit-work or machine-space claims.
"""
import argparse
import ast
import json
from pathlib import Path

P_Y=[(1,2,3),(1,4,5),(2,4,6),(3,5,6)]
Q_Y=[(1,2,4),(1,3,6),(2,3,5),(4,5,6)]
P_X=[(1,2,3),(1,2,4),(3,5,6),(4,5,6)]
Q_X=[(1,2,5),(1,2,6),(3,4,5),(3,4,6)]

def make(P,Q):
    return [tuple(c) for c in P]+[tuple(-v for v in c) for c in Q]
def gamma(z):
    b=bin(z)[2:]
    return "0"*(len(b)-1)+b
def bit_length(F,n):
    return len(gamma(n)+gamma(len(F)+1)+''.join(gamma(len(C)+1)+''.join(("1" if l>0 else "0")+gamma(abs(l)) for l in C) for C in F))
def m22(F):
    if not F: return False
    if any(len(C)!=3 or len(set(abs(v) for v in C))!=3 or not (all(v>0 for v in C) or all(v<0 for v in C)) for C in F): return False
    if len({tuple(sorted(C)) for C in F})!=len(F):return False
    vars={abs(l) for C in F for l in C}
    return all(sum(v in C for C in F)==2 and sum(-v in C for C in F)==2 for v in vars)
def restrict(F,pins):
    return [tuple(l for l in C if abs(l) not in pins) for C in F if not any((l>0)==pins[abs(l)] for l in C if abs(l) in pins)]
def two_levels(F,n):
    assert m22(F)
    first=restrict(F,{1:False})
    second=restrict(first,{2:True})
    return {"names":n,"clauses":len(F),"ordinary_bits":[bit_length(x,n) for x in (F,first,second)],"in_CM22":[m22(x) for x in (F,first,second)]}
def source(path):
    text=Path(path).read_text(encoding='utf-8')
    return [tuple(c) for c in ast.literal_eval('\n'.join(line for line in text.splitlines() if not line.lstrip().startswith('#')))]
if __name__=="__main__":
    ap=argparse.ArgumentParser();ap.add_argument('--u',default=None,help='Path to original Doecker 198x264 source TXT');args=ap.parse_args()
    rows={"Y_connected_Cstar_SAT":two_levels(make(P_Y,Q_Y),6),"exception_connected_Cstar_SAT":two_levels(make(P_X,Q_X),6)}
    if args.u:
        U=source(args.u)
        assert len(U)==264 and len({abs(l) for C in U for l in C})==198
        rows["Doecker_U_connected_Cstar_published_UNSAT"]=two_levels(U,198)
    assert rows["Y_connected_Cstar_SAT"]["ordinary_bits"]==[164,120,91]
    assert rows["exception_connected_Cstar_SAT"]["ordinary_bits"]==[164,120,112]
    if args.u:assert rows["Doecker_U_connected_Cstar_published_UNSAT"]["ordinary_bits"]==[12048,11986,11920]
    assert all(v["in_CM22"]==[True,False,False] for v in rows.values())
    print(json.dumps({"scope":"two sequential ordinary pin-and-simplify steps; no valid hereditary solver call","status":"COMPUTATIONAL, not physical FLMV bit trace","controls":rows,"failures":0},indent=2))
