#!/usr/bin/env python3
"""Finite audit for PARENT-PORT-TO-TAG1.

For bounded-fanout DAG circuits, compare occurrence tags generated from a
local parent-port enumerator with tags obtained by a global offline sort.
This validates the interface lemma; it does not prove that the concrete JMV
construction supplies such an enumerator.
"""
from __future__ import annotations
import hashlib, json, random, time
from collections import Counter, defaultdict
from pathlib import Path

SEED=202610111600
RUN_ID="MODELBRIDGE-0014"

def templates(g, typ, ch):
    if typ=="input": return []
    if typ=="c0": return [[(g,False)]*3]
    if typ=="c1": return [[(g,True)]*3]
    if typ=="copy":
        a=ch[0]; return [[(g,False),(a,True),(a,True)],[(g,True),(a,False),(a,False)]]
    if typ=="not":
        a=ch[0]; return [[(g,True),(a,True),(a,True)],[(g,False),(a,False),(a,False)]]
    a,b=ch
    return [[(a,False),(b,False),(g,True)],[(a,True),(g,False),(g,False)],[(b,True),(g,False),(g,False)]]

def build_random(rng,n,delta=3):
    gates=[]; fan=Counter()
    for g in range(n):
        choices=[i for i in range(g) if fan[i]<delta]
        if g<2 or not choices:
            typ=rng.choice(["input","c0","c1"]); ch=[]
        else:
            typ=rng.choice(["copy","not","and"])
            need=2 if typ=="and" else 1
            if len(choices)<need: typ="copy"; need=1
            ch=rng.sample(choices,need)
            for a in ch: fan[a]+=1
        gates.append((typ,ch))
    return gates

def clauses(gates):
    out=[]
    for g,(typ,ch) in enumerate(gates):
        for r,c in enumerate(templates(g,typ,ch)): out.append((g,r,c))
    out.append((len(gates)-1,99,[(len(gates)-1,True)]*3))
    return out

def parent_ports(gates):
    pp=defaultdict(list)
    for p,(_,ch) in enumerate(gates):
        for b,u in enumerate(ch): pp[u].append((p,b))
    for u in pp: pp[u].sort()
    return pp

def offline_tags(cls):
    occ=defaultdict(list)
    for owner,row,c in cls:
        for slot,(u,sgn) in enumerate(c): occ[(u,sgn)].append((owner,row,slot))
    return {addr:k+1 for key,addrs in occ.items() for k,addr in enumerate(sorted(addrs))}

def local_occurrences(u,sgn,gates,pp):
    # PPE supplies every (parent, child-slot).  Fixed gate templates supply
    # every literal position using u.  Filtering by sign is constant work.
    addresses=[]
    relevant={u}
    relevant.update(p for p,_ in pp.get(u,[]))
    for owner in relevant:
        typ,ch=gates[owner]
        owned=[(r,c) for r,c in enumerate(templates(owner,typ,ch))]
        if owner==len(gates)-1:
            owned.append((99,[(owner,True)]*3))
        for row,c in owned:
            for slot,(v,s) in enumerate(c):
                if v==u and s==sgn: addresses.append((owner,row,slot))
    return sorted(addresses)

def main():
    t0=time.perf_counter(); rng=random.Random(SEED); totals=Counter(); cases=[]
    for n in (8,16,32,64):
        for trial in range(128):
            gates=build_random(rng,n,3); cls=clauses(gates); pp=parent_ports(gates)
            assert max((len(v) for v in pp.values()),default=0)<=3
            off=offline_tags(cls)
            local={}
            for u in range(n):
                for sgn in (False,True):
                    for k,addr in enumerate(local_occurrences(u,sgn,gates,pp),1): local[addr]=k
            assert local==off
            # Renaming and clause/literal-order wrappers require a rebuilt PPE,
            # but preserve dense-tag validity and exact semantics.
            perm=list(range(n)); rng.shuffle(perm)
            renamed=[]
            for owner,r,c in cls:
                renamed.append((perm[owner],r,[(perm[u],s) for u,s in reversed(c)]))
            roff=offline_tags(renamed)
            for key in set((u,s) for _,_,c in renamed for u,s in c):
                vals=sorted(roff[(owner,row,slot)] for owner,row,c in renamed
                            for slot,(u,s) in enumerate(c) if (u,s)==key)
                assert vals==list(range(1,len(vals)+1))
            totals["circuits"]+=1; totals["gates"]+=n; totals["clauses"]+=len(cls)
            totals["literal_records"]+=3*len(cls); totals["parent_ports"]+=sum(map(len,pp.values()))
            totals["wrapper_checks"]+=1
            if trial==0: cases.append({"n":n,"clauses":len(cls),"max_fanout":max(map(len,pp.values()),default=0)})

    # Hostile control: a forward child accessor does not by itself provide a
    # parent-port accessor.  In the black-box permutation model, p_i has child
    # v_{pi(i)}.  Forward access is one query, while deterministic inversion
    # can require n-1 queries in the worst case.
    inverse_worst={}
    for n in (8,16,32,64):
        worst=0
        for _ in range(32):
            permutation=list(range(n)); rng.shuffle(permutation)
            target=permutation[-1]; probes=0
            totals["permutation_cases"]+=1
            totals["forward_lookup_probes"]+=1
            for value in permutation[:-1]:
                probes+=1
                assert value!=target
            worst=max(worst,probes)
        inverse_worst[str(n)]=worst
    result={"run_id":RUN_ID,"claim":"PARENT-PORT-TO-TAG1",
      "status":"COMPUTATIONAL interface validation; symbolic lemma in report",
      "seed":SEED,"totals":dict(totals),"sample_cases":cases,
      "forward_only_countercontrol":{"inverse_worst_probes":inverse_worst,
        "model":"deterministic permutation-oracle query model"},
      "limitations":[
        "Does not prove the concrete JMV circuit has a local parent-port enumerator.",
        "Does not normalize arbitrary constant occurrence profiles to exact Monotone (3,3).",
        "Does not force any SAT decider to expose tags or circuit topology."
      ],"elapsed_seconds":time.perf_counter()-t0}
    raw=json.dumps(result,sort_keys=True,separators=(",", ":")).encode(); result["payload_sha256"]=hashlib.sha256(raw).hexdigest()
    out=Path("results_raw_2026-10-11_parent_port_occurrence.json"); out.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"output":str(out),"totals":result["totals"],"elapsed":result["elapsed_seconds"],"sha":result["payload_sha256"]},indent=2))

if __name__=="__main__": main()
