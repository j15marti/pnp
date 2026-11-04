#!/usr/bin/env python3
"""Finite controls for REFEREE344."""
from __future__ import annotations
import hashlib, json
from collections import Counter
from itertools import product
from pathlib import Path

def key(c): return tuple(sorted(c, key=lambda z: (abs(z), z < 0)))
CLAUSES = sorted({key(c) for c in ((-1,), (1,), (-2,), (2,), (-1,-2), (-1,2), (1,-2), (1,2))}, key=lambda c: (len(c), c))
EMPTY = (); UNIVERSE = [EMPTY] + CLAUSES; CID = {c:i for i,c in enumerate(UNIVERSE)}

def sat_clause(c,a): return any(a[abs(x)-1] == (x>0) for x in c)
def models(src): return [a for a in product((False,True), repeat=2) if all(sat_clause(c,a) for c in src)]
def resolvents(a,b):
    out=set(); sa,sb=set(a),set(b)
    for p in (1,2):
        for x in (p,-p):
            if x in sa and -x in sb:
                r=(sa-{x})|(sb-{-x})
                if not any(-z in r for z in r): out.add((p,key(r)))
    return sorted(out)

def minimum_resolution(src, limit=3):
    source=frozenset(src); frontier=[(frozenset(),tuple())]
    for q in range(1,limit+1):
        nxt={}; sol=[]
        for derived,trace in frontier:
            avail=sorted(source|derived,key=lambda c:CID[c])
            for i,a in enumerate(avail):
                for b in avail[i:]:
                    for pivot,child in resolvents(a,b):
                        tr=trace+((CID[a],CID[b],pivot,CID[child]),)
                        if child==EMPTY: sol.append(tr)
                        else:
                            state=(frozenset(set(derived)|{child}),tr); nxt[state]=state
        if sol: return q,min(sol)
        frontier=list(nxt.values())
    return None,None

def verify_resolution(src,trace):
    avail=set(src)
    if not trace: return False
    for i,(pa,pb,pivot,ch) in enumerate(trace):
        if min(pa,pb,ch)<0 or max(pa,pb,ch)>=len(UNIVERSE): return False
        a,b,child=UNIVERSE[pa],UNIVERSE[pb],UNIVERSE[ch]
        if a not in avail or b not in avail or (pivot,child) not in resolvents(a,b): return False
        if child==EMPTY: return i==len(trace)-1
        avail.add(child)
    return False

def tt_certificate(src):
    cert=[]
    for a in product((False,True),repeat=2):
        bad=[i for i,c in enumerate(src) if not sat_clause(c,a)]
        if not bad: return None
        cert.append(min(bad))
    return tuple(cert)

def verify_tt(src,cert):
    if not isinstance(cert,tuple) or len(cert)!=4: return False
    for a,i in zip(product((False,True),repeat=2),cert):
        if not isinstance(i,int) or i<0 or i>=len(src) or sat_clause(src[i],a): return False
    return True

def translate(src,kind,cert):
    valid = ((kind=="decision" and cert=="UNSAT" and not models(src)) or
             (kind=="truth_table" and verify_tt(src,cert)) or
             (kind=="resolution" and verify_resolution(src,cert)))
    if not valid: return None
    q,tr=minimum_resolution(src); assert verify_resolution(src,tr); return q,tr

def rdagger(n):
    long="L"+"0"*(2**n); short="S"+"0"*n
    def verify(p,unsat=True):
        if not unsat or not isinstance(p,str) or not p: return False
        return ((p[0]=="L" and len(p)==1+2**n and set(p[1:])<={"0"}) or
                (p[0]=="S" and len(p)==1+n and set(p[1:])<={"0"}))
    assert verify(long) and verify(short) and not verify(long[:-1]) and not verify(short,False)
    return {"N":n,"minimum_paid_nodes":1,"minimum_proof_bits_excluding_source":len(long),
            "short_nonminimum_paid_nodes":n,"short_nonminimum_bits_excluding_source":len(short),
            "truncated_minimum_rejected":True,"SAT_label_rejected":True}

def main():
    counts=Counter(); translated=Counter(); malformed=0; sat=0; rows=[]
    for mask in range(256):
        src=[CLAUSES[i] for i in range(8) if (mask>>i)&1]; q,tr=minimum_resolution(src)
        if models(src):
            sat+=1; assert q is None and translate(src,"decision","UNSAT") is None; continue
        counts[q]+=1; tt=tt_certificate(src); assert verify_tt(src,tt)
        for kind,cert in (("decision","UNSAT"),("truth_table",tt),("resolution",tr)):
            out=translate(src,kind,cert); assert out and out[0]==q and verify_resolution(src,out[1]); translated[kind]+=1
        for kind,cert in (("decision","SAT"),("truth_table",tt[:-1]),("resolution",tr[:-1]),("unknown",tr)):
            assert translate(src,kind,cert) is None; malformed+=1
        rows.append((mask,q,tr))
    assert sat==95 and dict(counts)=={1:112,2:48,3:1}
    assert dict(translated)=={"decision":161,"truth_table":161,"resolution":161}
    dagger=[rdagger(n) for n in range(2,17)]; assert dagger[-1]["minimum_proof_bits_excluding_source"]==65537
    summary={"status":"PASS","target":"ordinary shared-DAG Resolution on the two-variable finite universe",
      "cnf_cases":256,"sat_cases":sat,"unsat_cases":256-sat,"minimum_target_nodes":dict(sorted(counts.items())),
      "valid_source_translations":dict(sorted(translated.items())),"malformed_source_certificates_rejected":malformed,
      "translator_semantics":"validate explicit source proof; output exact target minimum",
      "rdagger_assumption":"one fixed polynomial-time correct UNSAT decider is available","rdagger":dagger,
      "rdagger_conclusion":"bit-p-bounded via short nonminimum proofs and node minimum one, but every minimum-node proof has exponential explicit length; minimum-cost balance is necessary",
      "case_digest":hashlib.sha256(json.dumps(rows,sort_keys=True).encode()).hexdigest()}
    out=Path("results/raw/arc/2026-11-04_1251_LSPV5_344_POPTIMAL_BALANCE.json"); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(summary,indent=2)+"\n"); print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
