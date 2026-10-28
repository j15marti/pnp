#!/usr/bin/env python3
"""Reproducible fixed-map verbatim-buffer write lower bound for separated DISJ.

Only fixed-coordinate literal buffer cell changes are charged in this test.
This does not simulate a full Turing machine or prove a SAT lower bound.
"""
from __future__ import annotations
import itertools, json, random
from pathlib import Path

SEED = 20261027
RAW = Path(__file__).with_name('2026-10-28_0151_BLOCK_DISTANCE_FIREWALL184_raw.json')
rng = random.Random(SEED)
checks = 0

def check(cond, reason='audit failure'):
    global checks
    checks += 1
    if not cond:
        raise AssertionError(reason)

def hadamard_nonzero(B):
    check(B > 1 and B & (B-1) == 0)
    return [sum((((a & x).bit_count() & 1) << x) for x in range(B))
            for a in range(1, B)]

def write_cost(words, B, order, choices):
    slots = [0] * (max(choices) + 1)
    total = 0
    for i,j in zip(order, choices):
        w = words[i]
        total += (slots[j] ^ w).bit_count()
        slots[j] = w
    return total

summary = {}
for B in (4,8,16,32):
    ws = hadamard_nonzero(B)
    d = B//2
    check(len(ws) == B-1)
    for i,w in enumerate(ws):
        check(w.bit_count() == d)
        for v in ws[:i]:
            check((w^v).bit_count() == d)
    L = len(ws)
    for c in (1,2,3,4):
        for trial in range(500):
            order = list(range(L)); rng.shuffle(order)
            choices = [rng.randrange(c) for _ in range(L)]
            check(write_cost(ws,B,order,choices) == d*L)
    if B <= 8:
        local = 0
        for order in itertools.permutations(range(L)):
            for choices in itertools.product(range(2), repeat=L):
                check(write_cost(ws,B,order,choices) == d*L)
                local += 1
        summary[f'Hadamard_B{B}_exhaustive_two_slot_cases'] = local
    summary[f'Hadamard_B{B}'] = {
      'blocks':L,'bit_volume':B*L,
      'pairwise_distance':d,'any_schedule_minimum_changes':d*L
    }

B = 8
ws = [0,(1<<B)-1]*4
alternating = list(range(len(ws)))
reordered = [i for i in range(len(ws)) if ws[i]==0] + [
 i for i in range(len(ws)) if ws[i]!=0]
alternating_cost = write_cost(ws,B,alternating,[0]*8)
reordered_cost = write_cost(ws,B,reordered,[0]*8)
check(alternating_cost==B*7)
check(reordered_cost==B)
summary['alternation_countercontrol'] = {
 'B':B,'blocks':8,
 'fixed_order_changes':alternating_cost,'reordered_changes':reordered_cost
}

def select_separated(B,L):
    words=[]
    attempts=0
    floor=B//4
    while len(words)<L and attempts<1000000:
        w=rng.getrandbits(B);attempts+=1
        if w.bit_count()<floor:
            continue
        if all((w^v).bit_count()>=floor for v in words):
            words.append(w)
    check(len(words)==L)
    return words,attempts

for B,L in [(24,10),(32,20),(48,40),(64,50),(96,80),(128,120)]:
    ws,attempts=select_separated(B,L)
    dist=min((x^y).bit_count() for j,x in enumerate(ws) for y in ws[:j])
    check(dist>=B//4)
    check(min(w.bit_count() for w in ws)>=B//4)
    min_cost=B//4*L
    for c in (1,2,4):
        for _ in range(100):
            order=list(range(L));rng.shuffle(order)
            choices=[rng.randrange(c) for _ in range(L)]
            check(write_cost(ws,B,order,choices)>=min_cost)
    summary[f'codebook_B{B}_L{L}']={
        'min_pair_distance':dist,
        'min_weight':min(w.bit_count() for w in ws),
        'lower_bound_changes':min_cost,
        'm':B*L,
        'generation_attempts':attempts
    }

summary['status']='PASS'
summary['seed']=SEED
summary['checks']=checks
summary['scope']='fixed-cell verbatim blocks, constant number of slots; arbitrary reorder; not arbitrary encoding or SAT decision'
RAW.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':summary['status'],'checks':checks,
                  'raw':str(RAW),
                  'Hadamard_8_two_slot_exact_cases':summary['Hadamard_B8_exhaustive_two_slot_cases'],
                  'alternation':summary['alternation_countercontrol']}))
