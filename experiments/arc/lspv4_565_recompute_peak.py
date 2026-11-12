#!/usr/bin/env python3
"""LSPV-4/565: fully charged recomputation versus transient clause payload peak.
Exact finite resident-configuration search for the fixed LSPV-4/560 /386 DAG.
Read-only SOURCE/DEF clauses are excluded from derived-result registers.
This is NOT all-proof / historical R_mix341 / physical-RAM analysis.
Run from repo root: python experiments/arc/lspv4_565_recompute_peak.py
Optional checker OS replay: append --replay.
"""
import heapq, json, pathlib, subprocess, sys

PARENTS = [
 [],[0],[1],[2],[3],[4],[0],[],[6],[],[5],[],[],[],[],
 [10],[11],[9],[13],[7],[8],[12],[14],[21,17],[20,18],
 [16,19],[15,22],[26],[23],[24],[25],[29,28],[27,30],[31,32],[33]]
SIZES = [
 13,13,14,13,13,13,13,12,14,14,16,14,14,14,14,15,13,14,
 14,12,15,15,14,12,12,10,12,9,9,10,8,7,6,4,2]
N = len(PARENTS)
assert N == len(SIZES) == 35
PREDS = [sum(1 << k for k in a) for a in PARENTS]
GOAL = 1 << 34
def bits(x):
    while x:
        b = x & -x
        yield b.bit_length()-1
        x -= b
def payload(x):
    return sum(SIZES[i] for i in bits(x))
def transitions(mask, peak, capacity=4):
    """An exact one-execution edge, with free deletion before and after.
    A fresh output must coexist transiently with all retained premises;
    overwrite is restricted to a read parent large enough for the result.
    A parent overwritten while future uses remain may be recomputed, paid.
    """
    for j, parents in enumerate(PREDS):
        bit = 1 << j
        if mask & bit or (parents & mask) != parents:
            continue
        opt = mask & ~parents
        kept = opt
        while True:
            before = parents | kept
            bsz = payload(before)
            n = before.bit_count()
            overwrite_options = (
                ([-1] if n < capacity and bsz + SIZES[j] <= peak else [])
                + [p for p in PARENTS[j]
                   if n <= capacity and bsz <= peak and SIZES[p] >= SIZES[j]]
            )
            for overwritten in overwrite_options:
                remaining = before if overwritten == -1 else before ^ (1 << overwritten)
                post_old = remaining
                while True:
                    after = post_old | bit
                    yield j, before, overwritten, after, payload(after), (
                        bsz if overwritten != -1 else bsz + SIZES[j])
                    if post_old == 0: break
                    post_old = (post_old - 1) & remaining
            if kept == 0: break
            kept = (kept - 1) & opt

def solve(peak, capacity=4):
    """Dijkstra minimizes (#RES executions, sum post-clause-bytes) exactly."""
    best = {0:(0,0)}
    prior = {}
    pq = [(0,0,0)]
    settled = generated = 0
    while pq:
        work, area, mask = heapq.heappop(pq)
        if best.get(mask) != (work,area): continue
        settled += 1
        if mask & GOAL:
            trace = []
            state = mask
            while state:
                old,j,before,ow,after,step_peak = prior[state]
                trace.append(dict(j=j,before=list(bits(before)),
                                  overwrite=ow,after=list(bits(after)),
                                  transient_peak=step_peak,
                                  post_bytes=payload(after)))
                state = old
            trace.reverse()
            assert sum(t['post_bytes'] for t in trace) == area
            assert max(t['transient_peak'] for t in trace) <= peak
            assert len(trace) == work
            assert sorted(set(t['j'] for t in trace)) == list(range(N))
            return dict(peak_limit=peak,feasible=True,paid_res=work,
                        paid_with_three_fixed_owners=work+3,post_byte_area=area,
                        post_slot_area=sum(len(t['after']) for t in trace),
                        achieved_peak=max(t['transient_peak'] for t in trace),
                        states_settled=settled,transitions_generated=generated,
                        trace=trace)
        for j,before,ow,after,retention,step_peak in transitions(mask,peak,capacity):
            generated += 1
            cand = (work+1,area+retention)
            if cand < best.get(after,(10**20,10**20)):
                best[after] = cand
                prior[after] = (mask,j,before,ow,after,step_peak)
                heapq.heappush(pq,(*cand,after))
    return dict(peak_limit=peak,feasible=False,
                states_settled=settled,transitions_generated=generated)

def verify_trace(rows,peak):
    live = set()
    slot_area = byte_area = executed = 0
    for row in rows:
        j = row['j']
        before = set(row['before'])
        after = set(row['after'])
        ow = row['overwrite']
        assert set(PARENTS[j]) <= live
        assert before <= live and set(PARENTS[j]) <= before
        assert len(before) <= 4 and len(after) <= 4
        assert j in after and (after-{j}) <= (before-({ow} if ow >= 0 else set()))
        assert (ow == -1 or (ow in PARENTS[j] and SIZES[ow] >= SIZES[j]))
        moment = sum(SIZES[k] for k in before) + (0 if ow >= 0 else SIZES[j])
        assert moment <= peak and moment == row['transient_peak']
        assert len(before)+(0 if ow >= 0 else 1) <= 4
        assert row['post_bytes'] == sum(SIZES[k] for k in after)
        slot_area += len(after)
        byte_area += row['post_bytes']
        executed += 1
        live = after
    assert live == {34}
    return dict(steps=executed,slots=slot_area,area=byte_area)

def validate_published_packet(trace):
    root = pathlib.Path('results/raw/arc')
    packet = root/'2026-11-12_0936_LSPV4_565_P41_W39_NATIVE386_CERT.json'
    if not packet.exists(): return 'packet not found: checkout needed'
    data = json.loads(packet.read_text())
    assert data['summary']['resolution'] == 36
    assert data['summary']['paid_gates'] == 3
    assert data['summary']['paid_total'] == 39
    assert data['summary']['source'] == 17
    assert data['summary']['def_views'] == 6
    assert len(data['records']) == 59
    assert [r['kind'] for r in data['records']].count('RES') == 36
    assert data['records'][-1]['c'] == []
    # Independently replay all RES pivots with exact signs.
    def sort(c):return sorted(set(c),key=lambda z:(abs(z),z))
    for i,r in enumerate(data['records']):
        if r['kind'] != 'RES':continue
        assert all(0 <= p < i for p in r['parents'])
        a,b=[data['records'][p]['c'] for p in r['parents']]
        z=r['pivot']
        assert z in a and -z in b
        c=sort([x for x in a if x!=z]+[x for x in b if x!=-z])
        assert c == r['c']
    assert len(trace) == 36
    return str(packet)

if __name__=='__main__':
    rows = [solve(40),solve(41),solve(44),solve(45)]
    assert not rows[0]['feasible']
    assert [(r['paid_res'],r['post_byte_area']) for r in rows[1:]] == [
        (36,793),(36,760),(35,958)]
    assert verify_trace(rows[1]['trace'],41) == dict(steps=36,slots=75,area=793)
    published = validate_published_packet(rows[1]['trace'])
    if '--replay' in sys.argv:
        assert not published.startswith('packet not found'), published
        subprocess.run(['node','experiments/arc/lspv2_386_independent_verify.js',published],
                       check=True)
    print(json.dumps(dict(status='PROVED/RESTRICTED finite exact transition system',
                          source='LSPV-4/560 fixed signed /386 W38 paid DAG',
                          note='Separate from physical RAM and full R_mix341; no SAT lower bound',
                          published_packet=published,
                          original_OS_replay='only if --replay passed',
                          results=rows),indent=2))
