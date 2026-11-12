#!/usr/bin/env python3
"""LSPV-4/558. Exhaustive fixed-DAG schedule audit for original /386 W37 proof.

Run from repository root:
 python experiments/arc/lspv4_558_exact_w37_registers.py
This executes the unchanged archived checker as separate Node OS subprocesses.
No claim is made about the missing historical mixed R_mix341 dispatcher.
"""
import collections
import copy
import json
import pathlib
import subprocess
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / "results/raw/arc/2026-11-12_0212_LSPV2_571_ACCEPTED_LIVE_JOINT_PORT_ORBIT.json"
WITNESS = ROOT / "results/raw/arc/2026-11-12_0236_LSPV4_558_NATIVE386_W37_MINAREA_NONEXPAND4_ACCEPTED.json"
CHECKER = ROOT / "experiments/arc/lspv2_386_independent_verify.js"
ORDER = [23,24,25,26,27,28,32,37,36,44,48,49,29,41,33,38,47,52,54,
         31,39,34,43,45,50,30,42,35,40,46,51,53,55,56]
def compact(v):
    return json.dumps(v, separators=(",", ":"), ensure_ascii=False)
def construct(source):
    permutation = list(range(23)) + ORDER
    assert sorted(permutation) == list(range(57))
    old_to_new = {old:new for new,old in enumerate(permutation)}
    result = copy.deepcopy(source)
    result["records"] = []
    for old in permutation:
        rec = copy.deepcopy(source["records"][old])
        rec["parents"] = [old_to_new[p] for p in rec["parents"]]
        result["records"].append(rec)
    return result

def audited_graph(source):
    rec = source["records"]
    ids = [i for i,x in enumerate(rec) if x["kind"] == "RES"]
    assert len(ids) == 34 and ids == list(range(23,57))
    n = len(ids)
    index = {v:i for i,v in enumerate(ids)}
    dep = [tuple(index[p] for p in rec[v]["parents"] if p in index) for v in ids]
    prereq = [sum(1<<p for p in d) for d in dep]
    consumers = [0]*n
    for v,d in enumerate(dep):
        for p in d:
            consumers[p] |= 1<<v
    lengths = [len(compact(rec[v]["c"])) for v in ids]
    return ids, dep, prereq, consumers, lengths

def live_nodes(s,consumers):
    return [i for i,c in enumerate(consumers) if ((s>>i)&1) and (c&(~s))]

def calculate(source, order, mode="nonexpanding"):
    ids,dep,pr,cons,ln = audited_graph(source)
    index = {v:i for i,v in enumerate(ids)}
    state=0; area=0; byte_area=0; maximum=0
    for original in order:
        v=index[original]
        assert not (state>>v&1) and state&pr[v]==pr[v]
        live=live_nodes(state,cons)
        area+=len(live); byte_area+=sum(ln[i] for i in live)
        eligible=any((cons[p]&~state)==1<<v
                     and (mode!="nonexpanding" or ln[p]>=ln[v])
                     for p in dep[v]) if mode!="fresh" else False
        maximum=max(maximum,len(live)+1-int(eligible))
        state|=1<<v
    assert state==(1<<len(ids))-1
    return maximum,area,byte_area

def exhaustive(source,cap,mode):
    ids,dep,pr,cons,ln=audited_graph(source); n=len(ids)
    layers=[{0}]+[set() for _ in range(n)]
    best={0:(0,0,())}
    tested=0; arcs=0
    for level in range(n):
        for state in layers[level]:
            tested+=1
            live=live_nodes(state,cons)
            area=len(live); byte_area=sum(ln[i] for i in live)
            for v in range(n):
                bit=1<<v
                if state&bit or state&pr[v]!=pr[v]:
                    continue
                can_overwrite=False
                if mode!="fresh":
                    can_overwrite=any(
                        (cons[p]&~state)==bit and
                        (mode!="nonexpanding" or ln[p]>=ln[v])
                        for p in dep[v])
                if area+1-int(can_overwrite)>cap:
                    continue
                nxt=state|bit
                arcs+=1
                c0,c1,seq=best[state]
                item=(c0+area,c1+byte_area,seq+(ids[v],))
                if nxt not in best or item[:2]<best[nxt][:2]:
                    best[nxt]=item
                layers[level+1].add(nxt)
    complete=(1<<n)-1
    report={"cap":cap,"mode":mode,"reachable_before_terminal":tested,
            "legal_transitions":arcs,"feasible":complete in best}
    if complete in best:
        a,b,seq=best[complete]
        report.update(area=a,byte_area=b,order=list(seq))
        assert calculate(source,seq,mode)==(cap,a,b) or calculate(source,seq,mode)[0]<=cap
    return report

def strict_replay(packet):
    rec=packet["records"]
    assert len(rec)==packet["summary"]["live_records"]
    assert packet["summary"]["paid_total"]==len(packet["gate_defs"])+sum(
        r["kind"]=="RES" for r in rec)
    for i,r in enumerate(rec):
        assert all(0<=p<i for p in r["parents"])
        if r["kind"]!="RES":
            continue
        assert len(r["parents"])==2
        p=r["pivot"]
        A,B=(rec[j]["c"] for j in r["parents"])
        assert p in A and -p in B
        res=sorted(set([x for x in A if x!=p]+[x for x in B if x!=-p]),
                   key=lambda x:(abs(x),x))
        assert res==r["c"]
        assert all(-x not in res for x in res)
    assert rec[-1]["c"]==[]
def node_check(packet):
    with tempfile.TemporaryDirectory() as td:
        path=pathlib.Path(td)/"packet.json"
        path.write_text(compact(packet)+"\n",encoding="utf-8")
        p=subprocess.run(["node",str(CHECKER),str(path)],capture_output=True,text=True)
        return {"accepted":p.returncode==0,"stdout":p.stdout.strip(),"stderr":p.stderr[-500:]}
def main():
    source=json.loads(BASE.read_text(encoding="utf-8"))
    expected=construct(source)
    existing=WITNESS.read_text(encoding="utf-8")
    assert existing==compact(expected)+"\n", "published witness differs"
    assert compact(source)+"\n"==BASE.read_text(encoding="utf-8"),"base not canonical"
    strict_replay(source);strict_replay(expected)
    modes=[("fresh",4),("fresh",5),("inplace",3),("inplace",4),
           ("nonexpanding",3),("nonexpanding",4)]
    runs=[exhaustive(source,cap,mode) for mode,cap in modes]
    global_min=exhaustive(source,100,"fresh")
    assert [(x["feasible"]) for x in runs]==[False,True,False,True,False,True]
    assert (global_min["area"],global_min["byte_area"])==(66,698)
    assert (runs[-1]["area"],runs[-1]["byte_area"])==(66,700)
    assert calculate(source,ORDER,"nonexpanding")== (4,66,700)
    original_stats={mode:calculate(source,list(range(23,57)),mode) for mode in ("fresh","inplace","nonexpanding")}
    assert original_stats=={"fresh":(9,153,1982),"inplace":(8,153,1982),
                            "nonexpanding":(9,153,1982)}
    assert len(existing.encode("utf-8"))==3578
    original_cli=node_check(source)
    witness_cli=node_check(expected)
    bad=copy.deepcopy(expected)
    bad["records"][-1]["pivot"]=999999
    hostile=node_check(bad)
    assert original_cli["accepted"] and witness_cli["accepted"] and not hostile["accepted"]
    print(json.dumps({"status":"PASS","input_blob":"ae515a483bf7ec5a32232266adb17ef664ba7e9a",
      "models":runs,"global_unconstrained":global_min,
      "original_order":original_stats,"optimized_nonexpand":calculate(source,ORDER),
      "native_verdicts":{"base":original_cli,"witness":witness_cli,"hostile":hostile}},
      indent=2))
if __name__=="__main__":
    main()
