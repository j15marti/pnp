#!/usr/bin/env python3
"""LSPV-4/561: exhaustive black-pebbling audit for the fixed /560 paid-RES DAG.

Source fixture: results/raw/arc/2026-11-12_0436_LSPV4_560_W38_ACCEPTED.json
Git blob 6b72c961c2db19be87a0936361c467ef3445f4e2.
No claim about arbitrary proofs, full R_mix341, actual RAM or SAT decision.
"""
from collections import deque
import json
import sys

PARENTS = [
    [],[0],[1],[2],[3],[4],[0],[],[6],[],[5],[],[],[],[],
    [10],[11],[9],[13],[7],[8],[12],[14],[21,17],[20,18],
    [16,19],[15,22],[26],[23],[24],[25],[29,28],[27,30],[31,32],[33]
]
SIZES = [13,13,14,13,13,13,13,12,14,14,16,14,14,14,14,15,13,14,
         14,12,15,15,14,12,12,10,12,9,9,10,8,7,6,4,2]
assert len(PARENTS)==len(SIZES)==35
assert all(p<j for j,ps in enumerate(PARENTS) for p in ps)

def validate_packet(path):
    packet=json.load(open(path,encoding="utf-8"))
    records=packet["records"]
    indices=[i for i,r in enumerate(records) if r["kind"]=="RES"]
    remap={v:i for i,v in enumerate(indices)}
    parents=[[remap[p] for p in records[v]["parents"] if p in remap] for v in indices]
    sizes=[len(json.dumps(records[v]["c"],separators=(",",":"))) for v in indices]
    assert parents==PARENTS and sizes==SIZES, "source fixture mismatch"
    assert packet["summary"]["paid_total"]==38 and len(indices)==35
    return {"packet_path":path,"records":len(records),"RES":len(indices),"paid_work":38}

def walk(cap, expansion=False, drop_edge=None):
    parents=[list(ps) for ps in PARENTS]
    if drop_edge is not None:
        child,pred=drop_edge
        assert pred in parents[child]
        parents[child].remove(pred)
    q=deque([0]); seen={0:(None,None)}
    transitions=0
    while q:
        state=q.popleft()
        if state & (1<<34):
            trace=[];m=state
            while m:
                previous,j=seen[m]
                trace.append(j);m=previous
            trace.reverse()
            return dict(capacity=cap,expansion=expansion,drop_edge=drop_edge,
                        reachable=True,states=len(seen),transitions=transitions,
                        paid_executions=len(trace),trace=trace)
        resident=[j for j in range(35) if state & (1<<j)]
        for j in range(35):
            if state&(1<<j) or any(not(state&(1<<p)) for p in parents[j]):
                continue
            prerequisites=sum(1<<p for p in parents[j])
            for pattern in range(1<<len(resident)):
                post=1<<j
                for k,p in enumerate(resident):
                    if pattern&(1<<k): post|=1<<p
                pre=(post&~(1<<j))|prerequisites
                if pre.bit_count()>cap or post.bit_count()>cap:
                    continue
                if pre.bit_count()==cap:
                    if not any(not(post&(1<<p)) and
                               (expansion or SIZES[p]>=SIZES[j])
                               for p in parents[j]):
                        continue
                transitions+=1
                if post not in seen:
                    seen[post]=(state,j)
                    q.append(post)
    return dict(capacity=cap,expansion=expansion,drop_edge=drop_edge,
                reachable=False,states=len(seen),transitions=transitions)

def main():
    fixture=validate_packet(sys.argv[1]) if len(sys.argv)>1 else {"offline_fixture_only":True}
    cases=[walk(2,True),walk(3,False),walk(3,True),walk(4,False),
           walk(3,True,(33,31)),walk(3,True,(33,32))]
    assert [case["reachable"] for case in cases]==[False,False,False,True,True,True]
    assert cases[1]["states"]==5355 and cases[2]["states"]==5912
    assert cases[3]["paid_executions"]==35
    print(json.dumps({"run":"LSPV-4/561","fixture_validation":fixture,
      "model":"fixed 35-RES dependency DAG; source and DEF read-only; unlimited recomputation; free deletion; optional in-place parent overwrite",
      "cases":cases,
      "conclusion":"Four paid-clause registers are necessary and sufficient in this fixed graph even with unlimited recomputation and arbitrary-size overwrite. Dropping one actual edge yields a spurious three-register path."},indent=2))

if __name__=="__main__":
    main()
