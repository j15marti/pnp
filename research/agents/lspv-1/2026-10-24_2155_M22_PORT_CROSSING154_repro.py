#!/usr/bin/env python3
"""M22-PORT-CROSSING154: exact witness-orbit guards and independent LP checks.

Scope: three ports (one exterior positive occurrence each), nine private
auxiliaries (2+ and 2- uses each), proper unique pure-sign ternary OR clauses.
The LP is a relaxation, NOT a formal integer infeasibility certificate.
Usage: python M22_PORT_CROSSING154_repro.py 0 81 result.json
Split [0,81) into chunks to respect per-invocation runtime limits.
"""
import itertools, sys, json, time
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix

A=9
V=12
ports=(0,1,2)
edges=list(itertools.combinations(range(V),3))
M=len(edges)

def all_orbits():
    for n00 in range(10):
        for n01 in range(10-n00):
            for n10 in range(10-n00-n01):
                n11=9-n00-n01-n10
                s=(n00,n01,n10,n11)
                pairs=[(0,0)]*n00+[(0,1)]*n01+[(1,0)]*n10+[(1,1)]*n11
                yield s,tuple(a for a,b in pairs),tuple(b for a,b in pairs)

def eligible(s):
    n00,n01,n10,n11=s
    return n10>=2 and n10+n11>=4 and n00+n10>=4

def coverage():
    all_rows=[]
    for p in itertools.product((0,1),repeat=3):
        if p in ((0,0,0),(1,1,1)):
            continue
        for a in itertools.product((0,1),repeat=9):
            word=p+a
            ind=[i for i,e in enumerate(edges) if all(word[v]==0 for v in e)]
            ind += [M+i for i,e in enumerate(edges) if all(word[v]==1 for v in e)]
            all_rows.append(ind)
    assert len(all_rows)==6*512
    return all_rows

COVER=coverage()

def evaluate(s,y0,y1):
    word0=(0,0,0)+y0
    word1=(1,1,1)+y1
    allowedpos=[]
    allowedneg=[]
    for e in edges:
        pnum=sum(v in ports for v in e)
        forbiddenpos=(all(word0[v]==0 for v in e)
            or pnum>=2
            or (pnum==1 and any(y1[v-3] for v in e if v>=3))
            or all(word1[v]==0 for v in e))
        allowedpos.append(not forbiddenpos)
        forbiddenneg=(all(word1[v]==1 for v in e)
            or all(word0[v]==1 for v in e))
        allowedneg.append(not forbiddenneg)
    free=[i for i in range(M) if allowedpos[i]]
    free += [M+i for i in range(M) if allowedneg[i]]
    idx={old:i for i,old in enumerate(free)}
    ne=len(free)
    eq=lil_matrix((24,ne),dtype=float)
    beq=[]
    for sign in (0,1):
        for v in range(V):
            for ei,e in enumerate(edges):
                old=ei+sign*M
                if old in idx and v in e:
                    eq[12*sign+v,idx[old]]=1
            beq.append((1 if v in ports else 2) if sign==0 else 2)
    U=lil_matrix((len(COVER)+3,ne),dtype=float)
    rhs=-np.ones(len(COVER)+3)
    for ri,inds in enumerate(COVER):
        for old in inds:
            if old in idx:
                U[ri,idx[old]]=-1
    # Necessary negative singleton-port falsifier for each 000->e_i flip.
    for v in ports:
        ri=len(COVER)+v
        for ei,e in enumerate(edges):
            old=M+ei
            if old not in idx or {w for w in e if w in ports}!={v}:
                continue
            if all(y0[u-3]==1 for u in e if u>=3):
                U[ri,idx[old]]=-1
    lp=linprog(np.zeros(ne),A_ub=U.tocsr(),b_ub=rhs,
        A_eq=eq.tocsr(),b_eq=np.array(beq),bounds=(0,1),
        method="highs", options={"time_limit":3})
    return {"signature":list(s),"status":int(lp.status),
        "message":str(lp.message),"candidate_columns":ne}

def main():
    all_cases=list(all_orbits())
    cases=[(s,y0,y1) for s,y0,y1 in all_cases if eligible(s)]
    assert len(all_cases)==220 and len(cases)==81
    start=int(sys.argv[1]) if len(sys.argv)>1 else 0
    end=int(sys.argv[2]) if len(sys.argv)>2 else 12
    outpath=sys.argv[3] if len(sys.argv)>3 else "M22_PORT_CROSSING154_chunk.json"
    start=max(0,start);end=min(end,len(cases))
    t0=time.monotonic()
    rows=[]
    for j in range(start,end):
        s,y0,y1=cases[j]
        r=evaluate(s,y0,y1)
        r["index"]=j
        rows.append(r)
    counts={str(v):sum(r["status"]==v for r in rows) for v in {r["status"] for r in rows}}
    output={"id":"M22-PORT-CROSSING154","all_orbits":len(all_cases),
        "symbolically_eligible":len(cases),"start":start,"end":end,
        "LP_status_counts":counts,"seconds":time.monotonic()-t0,
        "status_note":"0 feasible continuous, 2 infeasible continuous; no rational proof certificate",
        "rows":rows}
    with open(outpath,"w") as f:json.dump(output,f,indent=2)
    print(json.dumps({"tested":len(rows),"counts":counts,"output":outpath}))

if __name__=="__main__":
    main()
