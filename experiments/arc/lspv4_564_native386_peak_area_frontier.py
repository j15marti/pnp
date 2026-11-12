#!/usr/bin/env python3
"""LSPV-4/564: peak-vs-cumulative-area exact resource frontier, extending /563.
Original /563: same-realization comparison of pre-step and post-step
storage costs on the pinned, source-sound archived-/386 proof DAG.
Run: python3 experiments/arc/lspv4_563_joint_epoch_firewall.py
No external dependencies. Entire fixed order-ideal state space is searched.
This is NOT a historical R_mix341 or a SAT lower-bound calculation.
"""
import heapq
import json

PARENTS = [
 [],[0],[1],[2],[3],[4],[0],[],[6],[],[5],[],[],[],[],
 [10],[11],[9],[13],[7],[8],[12],[14],[21,17],[20,18],
 [16,19],[15,22],[26],[23],[24],[25],[29,28],[27,30],[31,32],[33]]
SIZES = [
 13,13,14,13,13,13,13,12,14,14,16,14,14,14,14,15,13,14,
 14,12,15,15,14,12,12,10,12,9,9,10,8,7,6,4,2]
N = len(PARENTS)
assert N == len(SIZES) == 35
SUCC = [0] * N
PRED = [sum(1 << p for p in ps) for ps in PARENTS]
for j, ps in enumerate(PARENTS):
    for p in ps:
        SUCC[p] |= 1 << j
assert [i for i, v in enumerate(SUCC) if not v] == [34]
GOAL = (1 << N) - 1

def solve(primary="slot", cap=4):
    """No-recomputation, all topological orders, exact nonexpanding overwrite.
    Charge L(D) before each paid step, and convert to the same post-step
    convention used by LSPV-4/562 (last empty-sink value retained once).
    """
    assert primary in ("slot", "byte")
    best = {0: (0, 0)}
    previous = {}
    heap = [(0, 0, 0)]
    edges = 0
    while heap:
        a, b, mask = heapq.heappop(heap)
        if best.get(mask) != (a, b):
            continue
        if mask == GOAL:
            order = []
            cursor = mask
            while cursor:
                old, j = previous[cursor]
                order.append(j)
                cursor = old
            order.reverse()
            pre_slot, pre_byte = (a, b) if primary == "slot" else (b, a)
            return {
                "primary": primary, "states": len(best), "transitions": edges,
                "paid_resolution_executions": len(order),
                "pre_step_slot_steps": pre_slot,
                "pre_step_clause_byte_steps": pre_byte,
                "post_step_slot_steps": pre_slot + 1,
                "post_step_clause_byte_steps": pre_byte + SIZES[34],
                "order": order
            }
        live = [i for i in range(N) if (mask >> i) & 1 and SUCC[i] & ~mask]
        live_byte = sum(SIZES[i] for i in live)
        for j, ps in enumerate(PARENTS):
            if (mask >> j) & 1 or PRED[j] & ~mask:
                continue
            overwrite = any(
                not (SUCC[p] & ~(mask | (1 << j))) and SIZES[p] >= SIZES[j]
                for p in ps)
            if len(live) + 1 - int(overwrite) > cap:
                continue
            edges += 1
            next_mask = mask | (1 << j)
            c = (a + len(live), b + live_byte) if primary == "slot" else (
                a + live_byte, b + len(live))
            if c < best.get(next_mask, (10**15, 10**15)):
                best[next_mask] = c
                previous[next_mask] = (mask, j)
                heapq.heappush(heap, (*c, next_mask))
    raise AssertionError("Unreachable terminal")

def verify_recompute_trace(trace, residents):
    """Independent resident-set audit of the /562 36-execution witness.
    No knowledge of the original Dijkstra implementation is used."""
    assert len(trace) == len(residents) == 36
    assert sorted(set(trace)) == list(range(N))
    assert trace.count(0) == 2
    old = set()
    slot_area = byte_area = 0
    for t, (j, row) in enumerate(zip(trace, residents)):
        post = set(row)
        assert len(post) == len(row)
        assert j in post and len(post) <= 4
        assert set(PARENTS[j]) <= old, ("parent missing", t, j)
        keep = post - {j}
        assert keep <= old, ("unearned result", t, j)
        pre = keep | set(PARENTS[j])
        assert len(pre) <= 4
        if len(pre) == 4:
            assert any(p not in keep and SIZES[p] >= SIZES[j]
                       for p in PARENTS[j]), ("overwrite invalid", t, j)
        slot_area += len(post)
        byte_area += sum(SIZES[p] for p in post)
        old = post
    assert old == {34}
    return {"steps": len(trace), "distinct_paid_nodes": len(set(trace)),
            "recomputed_node": 0, "slot_steps": slot_area,
            "clause_byte_steps": byte_area}

# Published fixed W39 /562 trace and post-execution residents, independently rechecked.
TRACE = [0,1,2,3,4,5,10,15,14,22,26,27,7,19,11,16,25,30,32,0,
         6,8,20,13,18,24,29,12,21,9,17,23,28,31,33,34]
RESIDENTS = [
 [0],[1],[2],[3],[4],[5],[10],[15],[14,15],[15,22],[26],
 [27],[7,27],[19,27],[11,19,27],[16,19,27],[25,27],
 [27,30],[32],[0,32],[6,32],[8,32],[20,32],[13,20,32],
 [18,20,32],[24,32],[29,32],[12,29,32],[21,29,32],
 [9,21,29,32],[17,21,29,32],[23,29,32],[28,29,32],
 [31,32],[33],[34]]

# LSPV-4/564 supplement: cost-sound peak allocation proxy; source and DEF are read-only.
import pathlib, subprocess, sys

def exact_frontier(max_peak, capacity=4):
    """Exact finite no-recomputation optimization over all topological schedules.
    Objective: minimum post-step canonical clause-byte area, then slot area.
    During each step, all live paid parents remain readable until output is ready.
    A last-use parent of length >= output may be overwritten; otherwise the full
    result needs a fresh register and a simultaneous temporary byte allocation.
    No physical bit-RAM lower bound is claimed.
    """
    best={0:(0,0)}; back={}; pq=[(0,0,0)]; edges=0
    while pq:
        area, slots, mask=heapq.heappop(pq)
        if best.get(mask)!=(area,slots):
            continue
        if mask==GOAL:
            sequence=[];cursor=mask
            while cursor:
                prior,j=back[cursor];sequence.append(j);cursor=prior
            sequence.reverse()
            return dict(reachable=True,max_peak=max_peak,post_byte_area=area+SIZES[-1],
                        post_slot_area=slots+1,states=len(best),
                        transitions=edges,order=sequence)
        live=[i for i in range(N) if (mask>>i)&1 and SUCC[i]&~mask]
        retained=sum(SIZES[i] for i in live)
        for j,ps in enumerate(PARENTS):
            if (mask>>j)&1 or PRED[j]&~mask:continue
            overwritten=any(SIZES[p]>=SIZES[j] and not
                (SUCC[p]&~(mask|(1<<j))) for p in ps)
            transient=retained if overwritten else retained+SIZES[j]
            registers=len(live)+(0 if overwritten else 1)
            if registers>capacity or transient>max_peak:continue
            edges+=1
            nxt=mask|(1<<j)
            candidate=(area+retained,slots+len(live))
            if candidate<best.get(nxt,(10**20,10**20)):
                best[nxt]=candidate
                back[nxt]=(mask,j)
                heapq.heappush(pq,(*candidate,nxt))
    return dict(reachable=False,max_peak=max_peak,states=len(best),transitions=edges)


def authenticate_reordered(order, original, packet):
    """Replay every signed RES inference using actual original clauses, not
    just an abstract parent DAG. The source and paid-owner objects are identical."""
    assert len(order)==35 and sorted(order)==list(range(35)) and order[-1]==34
    assert original['spec']==packet['spec']
    assert original['gate_defs']==packet['gate_defs']
    assert original['summary']==packet['summary']
    assert original['records'][:23]==packet['records'][:23]
    assert len(packet['records'])==58
    orig=original['records'];r=packet['records']
    def key(c):return sorted(set(c),key=lambda x:(abs(x),x))
    lookup={j:23+i for i,j in enumerate(order)}
    for i,j in enumerate(order):
        old=orig[23+j];now=r[23+i]
        assert old['c']==now['c'] and old['pivot']==now['pivot']
        assert now['parents']==[p if p<23 else lookup[p-23] for p in old['parents']]
        assert all(0<=p<23+i for p in now['parents'])
        A,B=[r[p]['c'] for p in now['parents']]
        pivot=now['pivot']
        assert pivot in A and -pivot in B
        res=key([x for x in A if x!=pivot]+[x for x in B if x!=-pivot])
        assert res==now['c'] and not set(res).intersection(-x for x in res)
    assert r[-1]['c']==[]
    return True

if __name__=='__main__':
    caps=[44,45,46,47,48,49,50,51,1000]
    rows=[exact_frontier(k) for k in caps]
    observed={x['max_peak']:x for x in rows}
    assert not observed[44]['reachable']
    assert [(observed[k]['post_byte_area'],observed[k]['post_slot_area']) for k in [45,49,50,51,1000]]==[(958,87),(958,87),(927,87),(885,83),(885,83)]
    base_path=pathlib.Path('results/raw/arc/2026-11-12_0436_LSPV4_560_W38_ACCEPTED.json')
    cert_dir=pathlib.Path('results/raw/arc')
    serial={}
    if base_path.exists():
        orig=json.loads(base_path.read_text())
        for k in [45,50,51]:
            path=cert_dir/f'2026-11-12_0838_LSPV4_564_P{k}_W38_NATIVE386_CERT.json'
            cert=json.loads(path.read_text())
            assert authenticate_reordered(observed[k]['order'],orig,cert)
            serial[k]=str(path)
    if '--replay' in sys.argv:
        assert serial, 'Use --replay only from checkout with W38 and three packets present'
        checker='experiments/arc/lspv2_386_independent_verify.js'
        subprocess.run(['node',checker,*list(serial.values())],check=True)
    print(json.dumps(dict(status='COMPUTATIONAL with finite exact recurrence',
                          model='Fixed native /386 RES DAG, no-recompute, 4 nonexpanding registers',
                          steps=rows,original_signed_replay=serial,
                          original_cli_replay='only when --replay is supplied',
                          P2_D1='OPEN',P2_C3='OPEN',P2_B1='OPEN'),indent=2))
