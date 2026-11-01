#!/usr/bin/env python3
"""ARC-PROBE-DIRECT-SUM286 compact reproducible deterministic query adversary.
Run from repository checkout. Uses the verified U198 fixture/certifier in lspv4_284.
The complete independent 71,308-check verifier and source-indexed raw are in the
ARC_PROBE_DIRECT_SUM286_FULL_REPRO.zip attachment, not this compact script.
No native FLMV simulator or universal SAT lower bound is claimed.
"""
import json, importlib.util
from pathlib import Path
from fractions import Fraction

ROOT=Path(__file__).resolve().parents[1]
prev=ROOT/"lspv4_284"/"arc_quota_batch284_compact.py"
spec=importlib.util.spec_from_file_location("arc284",prev)
M=importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
M.certify() # independent original U198 refutation and V198 witness check
U=[tuple(c) for c in M.U]
V=[list(c) for c in U]
V[1][0],V[7][0]=V[7][0],V[1][0]
V=[tuple(c) for c in V]
assert M.check(U)==(198,264) and M.check(V)==(198,264)

def ren(F,off):
    return [tuple((1 if x>0 else -1)*(abs(x)+off) for x in C) for C in F]

def encode(F,n):
    m=len(F);w=m.bit_length()
    assert n < (1<<w)
    bits="1"*w+"0"+format(n,f"0{w}b")+format(m,f"0{w}b")
    for C in F:
        for x in C:
            bits+=("1" if x<0 else "0")+format(abs(x),f"0{w}b")
    assert len(bits)==3*w+1+3*m*(w+1)
    return bits,w

def audit(k):
    S=sum((ren(V,198*i) for i in range(k)),[])
    N=len(S)*3
    reference,w=encode(S,198*k)
    diffs=[];positions=[]
    for j in range(k):
        other=sum((ren(U if i==j else V,198*i) for i in range(k)),[])
        target,_=encode(other,198*k)
        B={i for i,(a,b) in enumerate(zip(reference,target)) if a!=b}
        assert B and len(target)==len(reference)
        assert not any(B & X for X in diffs)
        diffs.append(B);positions.append(min(B))
    idxwrites=sum(a.bit_count() for a in positions)
    assert k==len(diffs) and len(reference)==3*w+1+792*k*(w+1)
    return dict(k=k,source_bits=N,encoded_bits=len(reference),
        differing_bits=[len(X) for X in diffs],selected_source_addresses=positions,
        provable_source_read_lower_bound=k,
        declared_index_one_bit_writes=idxwrites,
        declared_adjacent_index_bit_xor=2*idxwrites,
        endpoint_index_bit_xor=0)

def envelope(c):
    f=Fraction(1)
    out=[]
    for j in range(1,5):
        f=c*f/(1+f)
        out.append(min((1/f-c)/j,c**(-j)))
    assert c**(-4)<out[1] and out[1]>max(out[0],out[2])
    return str(out[1])

def main():
    rows=[audit(k) for k in (1,2,4,8,16)]
    assert envelope(Fraction(6,5))=="23/45"
    assert envelope(Fraction(241,200))=="11642479/23232400"
    print(json.dumps(dict(id="ARC-PROBE-DIRECT-SUM286",both_label_certificates=True,
        rows=rows,flmv={"6/5":"23/45","241/200":"11642479/23232400"},
        scope="Restricted fixed-source query adversary; native machine and ARC open",
        P_vs_NP="OPEN"),indent=2))
if __name__=="__main__":
    main()
