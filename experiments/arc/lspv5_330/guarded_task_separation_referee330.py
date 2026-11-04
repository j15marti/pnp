#!/usr/bin/env python3
"""Finite controls for REFEREE330; the asymptotic bound is imported, not replayed."""
import itertools, json, resource, time
from pathlib import Path

OUT=Path("results/raw/arc/lspv5_330/guarded_task_separation_referee330.json")

def php(h):
    v=lambda p,j:1+p*h+j
    cs=[tuple(v(p,j) for j in range(h)) for p in range(h+1)]
    cs += [(-v(p,j),-v(q,j)) for j in range(h) for p in range(h+1) for q in range(p+1,h+1)]
    return h*(h+1),tuple(cs)

def guard(cs,t): return tuple((-t,)+c for c in cs)
def dimacs(n,cs): return "\n".join([f"p cnf {n} {len(cs)}"]+[" ".join(map(str,c))+" 0" for c in cs])+"\n"

def parse(s):
    if not isinstance(s,str) or not s.isascii(): raise ValueError
    rs=s.splitlines()
    if not rs or len(rs[0].split())!=4: raise ValueError
    p,k,ns,ms=rs[0].split(); n,m=int(ns),int(ms)
    if (p,k)!=("p","cnf") or n<1 or m<0 or len(rs)!=m+1: raise ValueError
    cs=[]
    for r in rs[1:]:
        z=r.split()
        if not z or z[-1]!="0" or z.count("0")!=1: raise ValueError
        c=tuple(map(int,z[:-1]))
        if not c or any(x==0 or abs(x)>n for x in c): raise ValueError
        cs.append(c)
    return n,tuple(cs)

def ev(cs,b): return all(any(b[abs(x)-1]==(x>0) for x in c) for c in cs)
def sat(n,cs,fixed=None):
    fixed=fixed or {}
    for b in itertools.product((False,True),repeat=n):
        if all(b[i-1]==v for i,v in fixed.items()) and ev(cs,b): return b
    return None

def infer_h(n):
    h=1
    while h*(h+1)<n: h+=1
    return h if h*(h+1)==n else None

def recognize(s):
    n,cs=parse(s); h=infer_h(n-1)
    if h is None: return None
    sn,src=php(h); t=sn+1
    if n!=t or cs!=guard(src,t): return None
    return {"h":h,"witness":(False,)*n,"source_bytes_read":len(s.encode())}

def decide(s):
    try:
        r=recognize(s)
        if r is not None: return {"label":"SAT","branch":"guarded-php",**r}
        n,cs=parse(s)
    except (ValueError,TypeError,UnicodeError): return {"label":"MALFORMED","branch":"reject"}
    w=sat(n,cs)
    return {"label":"SAT" if w is not None else "UNSAT","branch":"exact-fallback","witness":w}

def res(a,b,p):
    if p not in a or -p not in b: raise ValueError
    c=tuple(dict.fromkeys([x for x in a if x!=p]+[x for x in b if x!=-p]))
    if any(-x in c for x in c): raise ValueError
    return c
def gc(c,t): return tuple(dict.fromkeys((-t,)+c))
def transport(cs,proof,t):
    ls=list(cs); gs=[gc(c,t) for c in cs]
    for a,b,p,w in proof:
        x=res(ls[a],ls[b],p); y=res(gs[a],gs[b],p)
        assert x==w and y==gc(w,t); ls.append(x); gs.append(y)
    assert ls[-1]==() and gs[-1]==(-t,)
    return len(proof)

def main():
    t0=time.perf_counter(); checks=0; fs=[]
    for h in range(1,4):
        n,src=php(h); t=n+1; g=guard(src,t); text=dimacs(t,g)
        assert sat(n,src) is None; checks+=1
        assert ev(g,(False,)*t); checks+=1
        assert sat(t,g,{t:True}) is None; checks+=1
        a=decide(text)
        assert a["label"]=="SAT" and a["branch"]=="guarded-php"; checks+=1
        assert ev(g,a["witness"]); checks+=1
        assert a["source_bytes_read"]==len(text.encode()); checks+=1
        fs.append({"h":h,"source_variables":n,"source_clauses":len(src),"guarded_variables":t,
          "guarded_clauses":len(g),"guarded_dimacs_bytes":len(text.encode()),"guard_relation":[0],
          "decider_branch":a["branch"],"source_bytes_read":a["source_bytes_read"],"witness_output_bits":t})
    rel=[]
    for f in (((1,),),((1,),(-1,))):
        g=guard(f,2); rel.append([z for z in (0,1) if sat(2,g,{2:bool(z)}) is not None])
    assert rel==[[0,1],[0]]; checks+=1
    p1=transport(((1,),(-1,)),((0,1,1,()),),2)
    p2=transport(((1,2),(-1,),(-2,)),((0,1,1,(2,)),(3,2,2,())),3)
    assert [p1,p2]==[1,2]; checks+=2
    ctr=[]
    for text,want in [(dimacs(1,((1,),)),"SAT"),(dimacs(1,((1,),(-1,))),"UNSAT"),(dimacs(2,((1,2),)),"SAT")]:
        a=decide(text); assert a["label"]==want and a["branch"]=="exact-fallback"; checks+=1
        ctr.append({"expected":want,"label":a["label"],"branch":a["branch"]})
    bad=["","p cnf 1\n","p dnf 1 1\n1 0\n","p cnf 1 2\n1 0\n","p cnf 1 1\n2 0\n","p cnf 1 1\n1\n","p cnf 0 0\n","pi"]
    for s in bad: assert decide(s)["label"]=="MALFORMED"; checks+=1
    d={"artifact":"GUARDED-TASK-SEPARATION-REFEREE330","checks":checks,"guarded_php_fixtures":fs,
      "boundary_relation_controls":{"SAT_source":rel[0],"UNSAT_source":rel[1]},
      "manual_resolution_transport_steps":[p1,p2],"control_results":ctr,"malformed_rejected":len(bad),
      "uniform_decider":{"one_program_all_lengths":True,"family_time":"O(N) including parse/read and witness output",
        "family_peak_workspace":"O(log N) with streaming comparison/output","fallback_worst_case":"exponential"},
      "classification":{"proved":["guarded decision/entailment task separation","uniform recognizer plus fallback"],
        "restricted":["strict Resolution entailment"],"open":["B1_Rmix341","B2","B3","P!=NP"]},
      "wall_seconds":time.perf_counter()-t0,"peak_rss_kib":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"artifact":d["artifact"],"checks":checks,"peak_rss_kib":d["peak_rss_kib"]},sort_keys=True))
if __name__=="__main__": main()
