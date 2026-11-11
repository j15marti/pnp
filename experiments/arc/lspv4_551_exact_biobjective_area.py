#!/usr/bin/env python3
"""LSPV-4/551: independently transcribed W61 fixed-DAG biobjective 5-slot audit.
The historic /386 SOURCE/RES/AND2 sibling is NOT full R_mix341.
Run twice: python experiments/arc/lspv4_551_exact_biobjective_area.py --objective bytes
           python experiments/arc/lspv4_551_exact_biobjective_area.py --objective slots
Run --native-check only in a full repo checkout with node and original /386 checker.
"""
import argparse
from collections import deque
import json
import subprocess
from pathlib import Path
import time

P = [[],[],[],[],[],[3],[2],[1],[0],[5,8],[4],[],[11],[7,10],[],[14],
     [15,12],[],[9],[13],[16],[19,20],[17],[6,22],[23],[18,24],[25],
     [21],[27,26],[],[],[],[],[29],[32],[34,33],[31],[],[37],[38,36],
     [],[40],[35],[39],[42,43],[],[45],[46,41],[30],[],[49],[50,48],
     [47],[51],[52,53],[54],[44],[56,55],[57,28],[58]]
W = [19,17,19,17,17,17,19,17,18,14,18,19,18,14,17,17,14,19,13,13,
     14,10,20,16,14,10,12,11,9,16,14,16,14,15,14,12,17,16,16,14,
     16,15,12,13,10,14,14,12,15,14,14,12,12,13,10,11,10,8,5,2]
N=60
ALL=(1<<N)-1
assert len(P)==len(W)==N and all(j<i for i,ps in enumerate(P) for j in ps)
pred=[sum(1<<j for j in ps) for ps in P]
succ=[0]*N
for i,ps in enumerate(P):
    for j in ps: succ[j]|=1<<i

ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'results/raw/arc/2026-11-11_1236_LSPV4_549_BRIDGE_W61_BYTE_SAFE_FIVE_SLOT.json'
OLD=ROOT/'results/raw/arc/2026-11-11_1331_LSPV4_550_W61_MINAREA_FIVE_SLOT_ACCEPTED.json'
BYTE=ROOT/'results/raw/arc/2026-11-11_1436_LSPV4_551_W61_MIN_BYTE_AREA_FIVE_SLOT_ACCEPTED.json'
SLOT=ROOT/'results/raw/arc/2026-11-11_1436_LSPV4_551_W61_MIN_SLOT_THEN_BYTE_AREA_ACCEPTED.json'
CHECKER=ROOT/'experiments/arc/lspv2_386_independent_verify.js'

def canonical(c):
    return sorted(set(c),key=lambda x:(abs(x),x))

def signature(obj,r):
    return (tuple(r['c']),r['pivot'],
            tuple(tuple(obj['records'][k]['c']) for k in r['parents']))

def replay(obj):
    known=[]
    for i,r in enumerate(obj['records']):
        assert r['c']==canonical(r['c']),('noncanonical',i)
        if i<41:
            assert r['kind']=='SOURCE' and r['parents']==[]
        else:
            assert r['kind']=='RES' and len(r['parents'])==2
            a,b=r['parents']
            assert 0<=a<i and 0<=b<i and r['pivot'] in known[a] and -r['pivot'] in known[b],('ports',i)
            result=canonical([x for x in known[a] if x!=r['pivot']]+
                             [x for x in known[b] if x!=-r['pivot']])
            assert not any(-x in result for x in result),('tautology',i)
            assert r['c']==result,('resolvent',i)
        known.append(r['c'])
    assert known[-1]==[]
    assert obj['summary']=={'source':41,'resolution':60,'def_views':0,'paid_gates':1,
                            'paid_total':61,'live_records':101}

def load_input():
    base=json.loads(BASE.read_text())
    assert len(base['records'])==101
    res=base['records'][41:]
    assert [[x-41 for x in r['parents'] if x>=41] for r in res]==P
    assert [len(json.dumps(r['c'],separators=(',',':'))) for r in res]==W
    replay(base)
    return base

def actual_order(base,packet):
    assert packet['spec']==base['spec']
    assert packet['gate_defs']==base['gate_defs']
    assert packet['summary']==base['summary']
    assert packet['records'][:41]==base['records'][:41]
    replay(packet)
    d={signature(base,r):i for i,r in enumerate(base['records'][41:])}
    assert len(d)==60
    order=[d[signature(packet,r)] for r in packet['records'][41:]]
    assert sorted(order)==list(range(60))
    return order

def metrics(order):
    mask=0
    byte_area=slot_area=literal_area=0
    peak_bytes=peak_slots=0
    for i in order:
        un=ALL^mask
        live=[j for j in range(N) if mask>>j&1 and succ[j]&un]
        b=sum(W[j] for j in live)
        reusable=any((succ[j]&un)==(1<<i) and W[j]>=W[i] for j in P[i])
        assert len(live)+int(not reusable)<=5
        slot_area+=len(live)
        byte_area+=b
        peak_bytes=max(peak_bytes,b+(0 if reusable else W[i]))
        peak_slots=max(peak_slots,len(live)+int(not reusable))
        mask|=1<<i
    assert mask==ALL
    return {'canonical_byte_steps':byte_area,'slot_steps':slot_area,
            'peak_canonical_payload_bytes':peak_bytes,'peak_slots':peak_slots}

def optimize(primary):
    t=time.perf_counter()
    queue=deque([0]);best={0:(0,0)}; back={}
    ready=legal=relaxed=0
    while queue:
        mask=queue.popleft()
        un=ALL^mask
        live=[j for j in range(N) if mask>>j&1 and succ[j]&un]
        b=sum(W[j] for j in live)
        add=(b,len(live)) if primary=='bytes' else (len(live),b)
        nextcost=(best[mask][0]+add[0],best[mask][1]+add[1])
        for i in range(N):
            if mask>>i&1 or pred[i]&un: continue
            ready+=1
            reuse=any((succ[j]&un)==(1<<i) and W[j]>=W[i] for j in P[i])
            if len(live)+int(not reuse)>5: continue
            legal+=1
            dest=mask|(1<<i)
            if dest not in best:
                queue.append(dest);best[dest]=nextcost;back[dest]=(mask,i);relaxed+=1
            elif nextcost<best[dest]:
                best[dest]=nextcost;back[dest]=(mask,i);relaxed+=1
    order=[];mask=ALL
    while mask:
        old,i=back[mask]
        order.append(i);mask=old
    order.reverse()
    expected=(1925,157) if primary=='bytes' else (156,1930)
    assert best[ALL]==expected
    assert len(best)==1129302 and ready==12982502 and legal==4107280
    return {'objective':primary,'cost_pair':list(best[ALL]),'states':len(best),
            'ready':ready,'legal':legal,'relaxations':relaxed,
            'order':order,'metrics':metrics(order),
            'elapsed_seconds':round(time.perf_counter()-t,2)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--objective',choices=['bytes','slots'],required=True)
    ap.add_argument('--native-check',action='store_true')
    args=ap.parse_args()
    base=load_input()
    outcome=optimize(args.objective)
    for path,expected in [(OLD,(156,1995)),(BYTE,(157,1925)),(SLOT,(156,1930))]:
        obj=json.loads(path.read_text())
        measured=metrics(actual_order(base,obj))
        assert (measured['slot_steps'],measured['canonical_byte_steps'])==expected
        outcome.setdefault('published_witness_metrics',{})[path.name]=measured
    assert actual_order(base,json.loads((BYTE if args.objective=='bytes' else SLOT).read_text()))==outcome['order']
    if args.native_check:
        for path in [OLD,BYTE,SLOT]:
            p=subprocess.run(['node',str(CHECKER),str(path)],capture_output=True,text=True,check=True)
            out=json.loads(p.stdout)
            assert out['paid']==61 and out['negativeTests']==11
            outcome.setdefault('original_checker_os_replay',{})[path.name]=out
    else:
        outcome['original_checker_os_replay']='NOT RUN: requires full repo checkout and --native-check'
    outcome['historical_R_mix341_covered']=False
    print(json.dumps(outcome,indent=2))

if __name__=='__main__': main()
