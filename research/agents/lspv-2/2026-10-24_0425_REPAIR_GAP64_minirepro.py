#!/usr/bin/env python3
"""REPAIR-GAP64 minimal standalone source audit. Python standard library only.
Run from j15marti/pnp root. UNSAT(U) relies on DOECKER-CORE-CERT61's
independently checked source certificate, not re-proved in this script.
"""
import ast, collections, hashlib, json, math
from fractions import Fraction
from pathlib import Path

SOURCE=Path("research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt")
SEED=202610240425
SAT_WITNESS_HEX="39a2b53c16ab15bc16ab15ca4b9715c4faa7143d31b0f26598"

def load():
    raw="\n".join(line for line in SOURCE.read_text().splitlines() if line.strip() and not line.lstrip().startswith("#"))
    return [tuple(int(z) for z in c) for c in ast.literal_eval(raw)]

def valid(f):
    assert all(len(c)==3 and len(set(map(abs,c)))==3 for c in f)
    assert len({tuple(sorted(map(abs,c))) for c in f})==len(f)
    n=max(map(abs,(z for c in f for z in c)))
    assert len(f)*3==4*n
    a=collections.Counter(z for c in f for z in c)
    assert all(a[x]==2 and a[-x]==2 for x in range(1,n+1))
    return n,len(f)

def sat(f,a):
    return all(any((a[abs(z)]==1)==(z>0) for z in c) for c in f)

def shift(f,d):
    return [tuple((abs(z)+d)*(1 if z>0 else -1) for z in c) for c in f]

def replicated(f,p):
    n,_=valid(f)
    return [c for j in range(p) for c in shift(f,j*n)]

def lp_feasible(f):
    # IP variables: z_occ, u_x^+, u_x^-, b_x. Relax all to [0,1].
    z=Fraction(1,3); u=Fraction(1,2); b=Fraction(0,1)
    assert 3*z==1 and z<=u and 2*u<=1+b
    counts=collections.Counter(abs(t) for c in f for t in c)
    assert all(z*count<=2 for count in counts.values())
    return True

def run():
    U=load()
    assert valid(U)==(198,264)
    V=[list(c) for c in U]
    assert V[3][1]==-3 and V[13][0]==3
    V[3][1]=3;V[13][0]=-3
    V=[tuple(c) for c in V]
    assert valid(V)==(198,264)
    assert [j for j,(c,d) in enumerate(zip(U,V)) if c!=d]==[3,13]
    witness=[0]+[int(t) for t in format(int(SAT_WITNESS_HEX,16),"0198b")]
    assert sat(V,witness)
    assert not sat(U,witness)
    records=[]
    for p in (1,2,4,8,16):
        for name,base,dist in (("U",U,p),("V",V,0)):
            f=replicated(base,p)
            n,m=valid(f)
            assert lp_feasible(f)
            if name=="V":
                joined=[0]+[witness[x] for _ in range(p) for x in range(1,199)]
                assert sat(f,joined)
            w=math.ceil(math.log2(64*(n+m+1)))
            records.append({"p":p,"label_source":name,"n":n,"m":m,
                            "N":(4*m+2)*w,"integer_mu":dist,"lp_opt":"0"})
    return {"id":"REPAIR-GAP64","seed":SEED,"source_sha256":hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "source_unsat":"imported checked DOECKER-CORE-CERT61",
            "SAT_witness_replayed":True,"records":records,"assertion_failures":0}

if __name__=="__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
