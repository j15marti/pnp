#!/usr/bin/env python3
"""LSPV-4/568: exact joint cost audit for ONE fixed archived /386 proof DAG.
Four derived-result registers, paid recomputation, free deletion,
nonexpanding parent overwrite, SOURCE/DEF outside derived-result registers.
Canonical parent-scan bytes are an analytic payload proxy, NOT measured RAM.
Run: python experiments/arc/lspv4_566_joint_resource_frontier.py [out.json]
"""
import heapq, json, sys
PARENTS=[[],[0],[1],[2],[3],[4],[0],[],[6],[],[5],[],[],[],[],
         [10],[11],[9],[13],[7],[8],[12],[14],[21,17],[20,18],
         [16,19],[15,22],[26],[23],[24],[25],[29,28],[27,30],[31,32],[33]]
SIZES=[13,13,14,13,13,13,13,12,14,14,16,14,14,14,14,15,13,14,
       14,12,15,15,14,12,12,10,12,9,9,10,8,7,6,4,2]
SCAN=[19,19,20,21,19,22,22,21,23,23,25,23,23,23,23,27,25,25,
      25,23,27,27,25,29,29,25,29,23,23,25,21,19,17,13,7]
assert len(PARENTS)==len(SIZES)==len(SCAN)==35
# Width-aware native JSON clause payloads after legal guard=7 -> MAX_SAFE_INTEGER
# All 34 nonterminal RES conclusions contain -guard; final empty clause does not.
# Per-RES parent scans contain guard 1 time for j=0..6 and 2 for j=7..34.
BASE_SIZES=SIZES[:]; BASE_SCAN=SCAN[:]
WIDTH=16; DELTA=WIDTH-1
SIZES=[v+(DELTA if j<34 else 0) for j,v in enumerate(BASE_SIZES)]
SCAN=[v+DELTA*(1 if j<7 else 2) for j,v in enumerate(BASE_SCAN)]
assert sum(1 if j<7 else 2 for j in range(35))==63

def verify_against_original_packet():
    import pathlib
    src=pathlib.Path(__file__).resolve().parents[2] / "results/raw/arc/2026-11-12_0436_LSPV4_560_W38_ACCEPTED.json"
    obj=json.loads(src.read_text())
    assert obj["spec"]["guard"]==7
    rows=obj["records"]; paid=[(i,r) for i,r in enumerate(rows) if r["kind"]=="RES"]
    assert len(paid)==35
    refs={idx:j for j,(idx,_) in enumerate(paid)}
    assert [[refs[p] for p in r["parents"] if p in refs] for _,r in paid]==PARENTS
    assert [len(json.dumps(r["c"],separators=(',',':'))) for _,r in paid]==BASE_SIZES
    assert [sum(len(json.dumps(rows[p]["c"],separators=(',',':'))) for p in r["parents"]) for _,r in paid]==BASE_SCAN
    def renamed(c):
        return sorted(((-9007199254740991 if v==-7 else 9007199254740991 if v==7 else v) for v in c),
                      key=lambda x:(abs(x),x))
    assert [len(json.dumps(renamed(r["c"]),separators=(',',':'))) for _,r in paid]==SIZES
    assert [sum(len(json.dumps(renamed(rows[p]["c"]),separators=(',',':'))) for p in r["parents"]) for _,r in paid]==SCAN
    assert sum(s-b for s,b in zip(SCAN,BASE_SCAN))==945

PRED=[sum(1<<p for p in a) for a in PARENTS]
GOAL=1<<34

def bits(mask):
    while mask:
        b=mask & -mask
        yield b.bit_length()-1
        mask^=b

def payload(mask):
    return sum(SIZES[i] for i in bits(mask))

def transitions(mask,cap):
    for j, parents in enumerate(PRED):
        bit=1<<j
        if mask&bit or mask&parents!=parents:
            continue
        opt=mask&~parents
        kept=opt
        while True:
            before=parents|kept
            count=before.bit_count()
            size=payload(before)
            if count<4 and size+SIZES[j]<=cap:
                remaining=before
                post=remaining
                while True:
                    after=post|bit
                    yield j,before,-1,after,size+SIZES[j]
                    if post==0:
                        break
                    post=(post-1)&remaining
            if count<=4 and size<=cap:
                for p in PARENTS[j]:
                    if SIZES[p]>=SIZES[j]:
                        remaining=before^(1<<p)
                        post=remaining
                        while True:
                            after=post|bit
                            yield j,before,p,after,size
                            if post==0:
                                break
                            post=(post-1)&remaining
            if kept==0:
                break
            kept=(kept-1)&opt

def solve(cap, objective):
    """Dijkstra over complete 4-register resident-state graph.
    work_first: (paid executions, signed parent-scan payload, retention)
    scan_first: (signed parent-scan payload, paid executions, retention)
    area_first: (retention, paid executions, signed parent-scan payload)
    """
    assert objective in ('work_first','scan_first','area_first')
    best={0:(0,0,0)}
    parent={}
    pq=[(0,0,0,0)]
    settled=candidates=0
    while pq:
        a,b,c,mask=heapq.heappop(pq)
        if best.get(mask)!=(a,b,c):
            continue
        settled+=1
        if mask&GOAL:
            trace=[]
            m=mask
            while m:
                prev,j,before,overwrite,after,moment=parent[m]
                trace.append({'j':j,'before':list(bits(before)),
                              'overwrite':overwrite,'after':list(bits(after)),
                              'transient_peak':moment,
                              'post_bytes':payload(after),'parent_scan':SCAN[j]})
                m=prev
            trace.reverse()
            nres=len(trace)
            actual_scan=sum(x['parent_scan'] for x in trace)
            actual_area=sum(x['post_bytes'] for x in trace)
            assert len(set(x['j'] for x in trace))==35
            assert max(x['transient_peak'] for x in trace)<=cap
            return {'cap':cap,'objective':objective,'feasible':True,
                    'paid_resolution_executions':nres,'paid_total':nres+3,
                    'parent_scan_proxy_bytes':actual_scan,
                    'post_step_retention_bytes':actual_area,
                    'post_step_slot_steps':sum(len(x['after']) for x in trace),
                    'peak_derived_payload':max(x['transient_peak'] for x in trace),
                    'settled_states':settled,'candidate_transitions':candidates,
                    'trace':trace}
        for j,before,overwrite,after,moment in transitions(mask,cap):
            candidates+=1
            area=payload(after)
            if objective=='work_first':
                cost=(a+1,b+SCAN[j],c+area)
            elif objective=='scan_first':
                cost=(a+SCAN[j],b+1,c+area)
            else:
                cost=(a+area,b+1,c+SCAN[j])
            if cost<best.get(after,(10**19,)*3):
                best[after]=cost
                parent[after]=(mask,j,before,overwrite,after,moment)
                heapq.heappush(pq,(*cost,after))
    return {'cap':cap,'objective':objective,'feasible':False,
            'settled_states':settled,'candidate_transitions':candidates}

def main():
    verify_against_original_packet()
    cases=[(100,'work_first'),(101,'work_first'),
           (104,'work_first'),(105,'work_first'),(105,'area_first')]
    runs=[solve(cap,mode) for cap,mode in cases]
    d={(r['cap'],r['objective']):r for r in runs}
    assert d[100,'work_first']['feasible'] is False
    assert (d[101,'work_first']['paid_total'],
            d[101,'work_first']['parent_scan_proxy_bytes'],
            d[101,'work_first']['post_step_retention_bytes'],
            d[101,'work_first']['peak_derived_payload'])==(39,1769,1903,101)
    assert (d[104,'work_first']['paid_total'],
            d[104,'work_first']['post_step_retention_bytes'])==(39,1840)
    assert (d[105,'work_first']['paid_total'],
            d[105,'work_first']['parent_scan_proxy_bytes'],
            d[105,'work_first']['post_step_retention_bytes'])==(38,1735,2248)
    assert (d[105,'area_first']['paid_total'],
            d[105,'area_first']['parent_scan_proxy_bytes'],
            d[105,'area_first']['post_step_retention_bytes'])==(39,1769,1798)
    out={'run':'LSPV-4/568', 'status':'PROVED/RESTRICTED finite four-register model',
         'not':'historical R_mix341, full source-grammar, physical RAM or SAT lower bound',
         'original_W38_blob':'6b72c961c2db19be87a0936361c467ef3445f4e2',
         'source_guard':7,'renamed_guard':9007199254740991,'delta_decimal_digits':15,
         'source_records':17,'free_facet_records':6,'once_paid_gate_owners':3,
         'paid_resolution_identities':35,'derived_sizes':SIZES,
         'parent_scan_application_bytes':SCAN,'parents':PARENTS,'cases':runs}
    if len(sys.argv)>1:
        with open(sys.argv[1],'w') as f:
            json.dump(out,f,indent=2);f.write('\\n')
    print(json.dumps({'passed':True,'cases':[{
       k:v for k,v in r.items() if k!='trace'
    } for r in runs]},indent=2))
if __name__=='__main__':
    main()
