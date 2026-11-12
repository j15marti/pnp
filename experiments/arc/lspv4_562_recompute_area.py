#!/usr/bin/env python3
"""LSPV-4/562: exact four-register recomputation/retention tradeoff.
Usage: python3 lspv4_562_recompute_area.py [original_560_packet.json] [new_W39_packet.json]
Pinned model is archived /386 SOURCE, DEF and strict RES, not historical R_mix341.
"""
import json
import sys
from collections import Counter
from functools import lru_cache
from heapq import heappush, heappop

PARENTS = [[],[0],[1],[2],[3],[4],[0],[],[6],[],[5],[],[],[],[],
           [10],[11],[9],[13],[7],[8],[12],[14],[21,17],[20,18],
           [16,19],[15,22],[26],[23],[24],[25],[29,28],[27,30],[31,32],[33]]
SIZES = [13,13,14,13,13,13,13,12,14,14,16,14,14,14,14,15,13,14,
         14,12,15,15,14,12,12,10,12,9,9,10,8,7,6,4,2]
assert len(PARENTS) == len(SIZES) == 35
PMASKS = [sum(1 << p for p in ps) for ps in PARENTS]

@lru_cache(None)
def bytearea(mask):
    return bytearea(mask & (mask-1)) + SIZES[(mask & -mask).bit_length()-1] if mask else 0

def solve(metric='slots', expanding=False, cap=4):
    """Dijkstra on all post-inference resident sets; area then execution count."""
    dist={0:(0,0)}
    previous={}
    heap=[(0,0,0)]
    settled=edges=0
    while heap:
        cost, executions, state=heappop(heap)
        if dist[state] != (cost, executions):
            continue
        settled+=1
        if state & (1<<34):
            steps=[]
            cursor=state
            while cursor:
                old,j=previous[cursor]
                steps.append(dict(node=j,
                    residents=[i for i in range(35) if cursor>>i&1],
                    slots=cursor.bit_count(),clause_bytes=bytearea(cursor)))
                cursor=old
            steps.reverse()
            occurrences=Counter(x['node'] for x in steps)
            assert occurrences[0]==2 and len(occurrences)==35 and len(steps)==36
            return dict(metric=metric,expanding=expanding,cap=cap,
                optimum=cost,executions=executions,
                slot_steps=sum(x['slots'] for x in steps),
                byte_steps=sum(x['clause_bytes'] for x in steps),
                settled=settled,discovered=len(dist),edges=edges,steps=steps)
        residents=[i for i in range(35) if state>>i&1]
        for j in range(35):
            if state>>j&1 or (state & PMASKS[j])!=PMASKS[j]:
                continue
            for keep in range(1<<len(residents)):
                post=1<<j
                for k,p in enumerate(residents):
                    if keep>>k&1:
                        post|=1<<p
                pre=(post & ~(1<<j)) | PMASKS[j]
                if pre.bit_count()>cap or post.bit_count()>cap:
                    continue
                if pre.bit_count()==cap and not any(
                    not(post>>p&1) and (expanding or SIZES[p]>=SIZES[j])
                    for p in PARENTS[j]):
                    continue
                edges+=1
                weight=post.bit_count() if metric=='slots' else bytearea(post)
                trial=(cost+weight,executions+1)
                if trial<dist.get(post,(10**12,10**12)):
                    dist[post]=trial
                    previous[post]=(state,j)
                    heappush(heap,(trial[0],trial[1],post))
    raise RuntimeError('Goal not reached')

def authenticate_fixture(path):
    with open(path,encoding='utf-8') as f:
        packet=json.load(f)
    indices=[i for i,r in enumerate(packet['records']) if r['kind']=='RES']
    mapping={v:i for i,v in enumerate(indices)}
    parents=[[mapping[p] for p in packet['records'][v]['parents'] if p in mapping]
             for v in indices]
    sizes=[len(json.dumps(packet['records'][v]['c'],separators=(',',':')))
           for v in indices]
    assert parents==PARENTS and sizes==SIZES, 'Pinned proof graph mismatch'
    assert packet['summary']['paid_total']==38 and len(indices)==35
    return packet,indices

def make_certificate(packet,indices,steps):
    first=min(indices)
    assert first==23 and all(r['kind']!='RES' for r in packet['records'][:first])
    records=list(packet['records'][:first])
    latest={}
    reverse={r:i for i,r in enumerate(indices)}
    for item in steps:
        j=item['node']
        original=packet['records'][indices[j]]
        parents=[p if p<first else latest[reverse[p]] for p in original['parents']]
        records.append({**original,'parents':parents})
        latest[j]=len(records)-1
    summary={**packet['summary'],'resolution':len(steps),
             'paid_total':len(steps)+len(packet['gate_defs']),
             'live_records':len(records)}
    new={**packet,'records':records,'summary':summary}
    assert len(records)==59 and summary['paid_total']==39
    return new

def main():
    output={}
    if len(sys.argv)>1:
        packet,indices=authenticate_fixture(sys.argv[1])
        output['fixture_authenticated']=True
    else:
        packet=indices=None
        output['fixture_authenticated']=False
    for label,metric,expanding in [('slots_nonexp','slots',False),
                                   ('bytes_nonexp','bytes',False),
                                   ('bytes_expanding','bytes',True)]:
        output[label]=solve(metric,expanding)
    assert (output['slots_nonexp']['optimum'],output['slots_nonexp']['executions'])==(71,36)
    assert (output['bytes_nonexp']['optimum'],output['bytes_nonexp']['executions'])==(748,36)
    assert (output['bytes_expanding']['optimum'],output['bytes_expanding']['executions'])==(746,36)
    if packet is not None:
        cert=make_certificate(packet,indices,output['bytes_nonexp']['steps'])
        outfile=sys.argv[2] if len(sys.argv)>2 else 'lspv4_562_recomputed_W39.json'
        with open(outfile,'w',encoding='utf-8') as f:
            json.dump(cert,f,separators=(',',':'))
            f.write('\n')
        output['new_certificate_path']=outfile
        output['new_certificate_bytes']=len(json.dumps(cert,separators=(',',':')).encode())+1
    print(json.dumps(output,indent=2))

if __name__=='__main__':
    main()
