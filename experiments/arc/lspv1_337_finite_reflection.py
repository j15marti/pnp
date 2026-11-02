#!/usr/bin/env python3
"""FINITE-REFLECTION337: finite controls only, NOT a PA theorem prover.
Fixed binary framed CNF, paid finite checker list, synthetic inconsistency.
Standard library, deterministic; output JSON, no randomness.
"""
import json
def enc(n, cls, padding=0):
    return b"0:"+json.dumps({"n":n,"clauses":cls},separators=(",",":")).encode()+b":"+b"0"*padding
def parse(b):
    if not isinstance(b,bytes) or not b.startswith(b"0:"):return None
    try:
        body,pad=b[2:].rsplit(b":",1)
        if any(x!=48 for x in pad):return None
        x=json.loads(body)
        if set(x)!={"n","clauses"} or type(x["n"]) is not int or not 1<=x["n"]<=9:return None
        if not isinstance(x["clauses"],list) or len(x["clauses"])>64:return None
        for c in x["clauses"]:
            if not isinstance(c,list) or len(c)>20:return None
            for l in c:
                if type(l) is not int or l==0 or abs(l)>x["n"]:return None
        return x if json.dumps(x,separators=(",",":")).encode()==body else None
    except (ValueError,TypeError,UnicodeError,KeyError):return None
def model_count(f):
    if f is None:return None
    n=f["n"];return sum(all(any(bool(a&(1<<(abs(l)-1)))==(l>0) for l in c) for c in f["clauses"]) for a in range(1<<n))
def baseline(b):
    n=model_count(parse(b))
    return "INVALID" if n is None else "SAT" if n else "UNSAT"
sentinel_base=enc(1,[[1]])
def sentinel(N):
    return enc(1,[[1]],N-len(sentinel_base)) if N>=len(sentinel_base) else None
def solver(b,synthetic_bad_code=None):
    if len(b)==synthetic_bad_code and b==sentinel(len(b)):
        return "UNSAT" # intentionally incorrect in synthetic bad-checker world
    return baseline(b)
def bounded_certificate(N):
    return list(range(N+1))
def check_bounded(N,seq,bad_code=None):
    return seq==list(range(N+1)) and all(i!=bad_code for i in seq)
def k4(ch):
    edges=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]; clauses=[]
    for v in range(4):
        ids=[i+1 for i,(a,b) in enumerate(edges) if v in (a,b)]
        for z in range(8):
            if z.bit_count()%2==ch[v]:continue
            clauses.append([-ids[i] if z>>i&1 else ids[i] for i in range(3)])
    return clauses
cases=[
("unit_sat",enc(1,[[1]]),"SAT"),
("unit_unsat",enc(1,[[1],[-1]]),"UNSAT"),
("horn_unsat",enc(3,[[1],[2],[-1,-2,3],[-3]]),"UNSAT"),
("horn_sat_flip",enc(3,[[1],[2],[-1,-2,3],[3]]),"SAT"),
("cube_unsat",enc(3,[[(-1 if z&1 else 1),(-2 if z&2 else 2),(-3 if z&4 else 3)] for z in range(8)]),"UNSAT"),
("k4_odd",enc(6,k4([1,0,0,0])),"UNSAT"),
("k4_even",enc(6,k4([0,0,0,0])),"SAT"),
("malformed_header",b"1"*50,"INVALID"),
("malformed_literal",b'0:{"n":1,"clauses":[[0]]}:',"INVALID"),
("malformed_suffix",enc(1,[[1]])+b"1","INVALID")]
rows=[]
for name,b,expected in cases:
    assert baseline(b)==solver(b)==expected
    rows.append({"name":name,"encoded_length":len(b),"label":expected,
                 "model_count":model_count(parse(b))})
assert rows[5]["model_count"]==0 and rows[6]["model_count"]==8
N=75;seq=bounded_certificate(N);BAD=57
assert check_bounded(N,seq)
assert not check_bounded(N,seq[:-1])
assert not check_bounded(N,seq+[N+1])
assert not check_bounded(N,seq,BAD)
assert check_bounded(BAD-1,bounded_certificate(BAD-1),BAD)
s=sentinel(BAD)
assert len(s)==BAD and baseline(s)=="SAT" and solver(s)=="SAT" and solver(s,BAD)=="UNSAT"
print(json.dumps({"run":"FINITE-REFLECTION-BRIDGE337","status":"COMPUTATIONAL toy only; P vs NP OPEN",
"source":"fixed binary-framed CNF with zero padding","N":N,"checked_local_codes":N+1,
"fixture_results":rows,"consistent_world_all_correct":True,
"injected_bad_checker_code":BAD,"sentinel_length":BAD,"sentinel_label_baseline":"SAT",
"sentinel_label_fault_world":"UNSAT","corrupt_certificates_rejected":3},indent=2,sort_keys=True))
