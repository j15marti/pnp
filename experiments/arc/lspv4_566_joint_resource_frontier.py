#!/usr/bin/env python3
"""LSPV-4/566: exact joint cost audit for ONE fixed archived /386 proof DAG.
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
    cases=[(40,'work_first'),(41,'work_first'),(41,'scan_first'),
           (41,'area_first'),(44,'work_first'),(44,'area_first'),
           (45,'work_first'),(45,'scan_first'),(45,'area_first')]
    runs=[solve(cap,mode) for cap,mode in cases]
    lookup={(r['cap'],r['objective']):r for r in runs}
    assert not lookup[40,'work_first']['feasible']
    for cap,nres,scan,area in [(41,36,809,793),(44,36,809,760),
                                (45,35,790,958)]:
        q=lookup[cap,'work_first']
        assert (q['paid_resolution_executions'],q['parent_scan_proxy_bytes'],
                q['post_step_retention_bytes'])==(nres,scan,area)
    z=lookup[45,'area_first']
    assert (z['paid_resolution_executions'],z['parent_scan_proxy_bytes'],
            z['post_step_retention_bytes'],z['peak_derived_payload'])==(36,809,748,45)
    assert lookup[41,'area_first']['post_step_retention_bytes']==793
    assert lookup[44,'area_first']['post_step_retention_bytes']==760
    out={'model':'archived-/386 fixed signed /560 W38 DAG, not historical R_mix341',
         'status':'PROVED/RESTRICTED exhaustive finite configuration recurrence',
         'evidence_model':'canonical JSON-stringified signed-parent clause scan bytes, not native RAM',
         'owners_once':3,'original_source_count':17,'original_free_facets':6,
         'dag_paid_resolution_identities':35,
         'source_W38_git_blob':'6b72c961c2db19be87a0936361c467ef3445f4e2',
         'source_P41_packet_git_blob':'97a96f3f6212c20c4bfa5ced26cad7b18f9722e8',
         'parents':PARENTS,'output_clause_sizes':SIZES,'parent_scan_bytes':SCAN,
         'results':runs}
    destination=sys.argv[1] if len(sys.argv)>1 else None
    if destination:
        with open(destination,'w') as f:
            json.dump(out,f,indent=2);f.write('\n')
    print(json.dumps({'passed':True,'cases':[{
        k:v for k,v in r.items() if k!='trace'
    } for r in runs]},indent=2))
if __name__=='__main__':
    main()
