#!/usr/bin/env python3
"""No-import verifier for REFEREE288 published raw results."""
import argparse, collections, hashlib, itertools, json, math
from pathlib import Path

F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),(-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
Z6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-3),(-1,-4,-5),(-2,-4,-6),(-3,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F15=P15+tuple(tuple(-x for x in c) for c in N15)

def sat(F,a):return all(any(a[abs(x)]==int(x>0) for x in c) for c in F)
def ass(n,z):return {i:(z>>(i-1))&1 for i in range(1,n+1)}
def count(F,n,p=None):
    p={} if p is None else dict(p);free=[v for v in range(1,n+1) if v not in p];q=0
    for z in range(1<<len(free)):
        a=dict(p);a.update((v,(z>>i)&1) for i,v in enumerate(free));q+=sat(F,a)
    return q

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--raw",required=True);ap.add_argument("--out",required=True);a=ap.parse_args()
    d=json.loads(Path(a.raw).read_text());checks=0
    assert d["run"]=="BOUNDED-OCCURRENCE-TRANSFER-FIREWALL-REFEREE288";checks+=1
    for name,F,n,want in (("Y6_20",Y6,6,20),("Z6_18",Z6,6,18),("F9",F9,9,70),("F15",F15,15,1032)):
        occ=collections.Counter(abs(x) for c in F for x in c)
        assert all(occ[v]==4 for v in range(1,n+1));checks+=n
        got=count(F,n);assert got==want==d["fixtures"][name]["models"];checks+=(1<<n)+1
        assert d["fixtures"][name]["occurrences"]["maximum_total"]==4;checks+=1
    common={3:0,5:1,6:0,7:0,8:0}
    assert count(F9,9,{**common,1:0})==2;checks+=8
    assert count(F9,9,{**common,1:1})==0;checks+=8
    cover=d["F9_same_original"]["UNSAT_complete_leaf_cover"];assert len(cover)==8;checks+=1
    for leaf in cover:
        a0={**common,1:1};a0.update(zip((2,4,9),leaf["free_bits"]))
        false=[i for i,c in enumerate(F9) if not any(a0[abs(x)]==int(x>0) for x in c)]
        assert false==leaf["false_source_clause_ids"];checks+=12
    assert d["F9_same_original"]["obdd"]=={"best":52,"natural":66,"worst":80};checks+=3
    p=d["numerics"]
    assert abs(p["peer_reviewed_binary_exponent"]-math.log2(1.2628))<1e-15;checks+=1
    assert abs(p["lspv1_iterated_DP_base"]-2**p["lspv1_binary_exponent"])<1e-15;checks+=1
    assert 1.1199**2<1.2628<p["lspv1_iterated_DP_base"];checks+=3
    assert d["malformed_rejected"]==6 and d["P_vs_NP"]=="OPEN";checks+=2
    raw_sha=hashlib.sha256(Path(a.raw).read_bytes()).hexdigest()
    out={"run":"VERIFY-REFEREE288","status":"PASS","assertion_groups":checks,"raw_sha256":raw_sha,"P_vs_NP":"OPEN","note":"Published d=4 branching theorem adopted, not re-proved."}
    pth=Path(a.out);pth.parent.mkdir(parents=True,exist_ok=True);pth.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,sort_keys=True))

if __name__=="__main__":main()
