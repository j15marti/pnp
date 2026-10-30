#!/usr/bin/env python3
"""LSPV-4 BATCH-SWEEP-VALUE237 independent finite controls.

Only standard library. All searches exhaustive for t<=8 and linear time
for larger structured cases. This checks an explicit algorithm, not an
algorithm-independent lower bound.
"""
import hashlib
import json
import math
from itertools import product


def is_model_horn2(x):
    return all(x[0] or not x[j] for j in range(1, len(x)))


def skew_control(t):
    models = [bits for bits in product((0,1), repeat=t) if is_model_horn2(bits)]
    total = (1 << (t-1)) + 1
    assert len(models) == total
    rare = [x for x in models if x[0] == 0]
    common = [x for x in models if x[0] == 1]
    assert len(rare) == 1 and len(common) == (1 << (t-1))
    rare_v = math.log2(total)
    common_v = math.log2(total) - (t-1)
    p = 1 / total
    expected_v = p*rare_v+(1-p)*common_v
    entropy = -p*math.log2(p)-(1-p)*math.log2(1-p)
    assert abs(expected_v-entropy) < 1e-11
    assert rare_v > 1
    assert expected_v < 1
    return {'t': t, 'models': total, 'rare_v_bits':round(rare_v,12),
            'common_v_bits':round(common_v,12),
            'expected_v_bits':round(expected_v,12)}


def skew_formula_symbolic(t):
    total = (1 << (t-1))+1
    rare_v = math.log2(total)
    common_v = rare_v-(t-1)
    p = 1/total
    expected = p*rare_v+(1-p)*common_v
    return {'t':t, 'models':total, 'rare_v_bits':round(rare_v,12),
            'common_v_bits':round(common_v,12),
            'expected_v_bits':round(expected,12)}


def get_batch(t,L,g,signs):
    """Explicit fully charged source-head trajectory, input starts at p0."""
    assert 0<=L<=t and g>=1
    retained = tuple(signs[:L])
    prep_probes = L
    prep_head_moves = (L if L < t else t-1)*g
    prepared_at = (L if L < t else t-1)*g
    head = prepared_at
    result = list(retained)
    query_probes = 0
    query_moves = 0
    for j in range(L,t):
        target = j*g
        move = abs(head-target)
        head = target
        query_moves += move
        result.append(signs[j])
        query_probes += 1
    assert tuple(result) == tuple(signs)
    assert prep_probes+query_probes == t
    assert prep_head_moves+query_moves == (t-1)*g
    assert query_moves == (max(0,t-L-1)*g)
    return {'t':t,'L':L,'g':g,'P_head':prep_head_moves,
            'Q_head':query_moves,'total_head':prep_head_moves+query_moves,
            'P_sign_probes':prep_probes,'Q_sign_probes':query_probes}


def single_query_radius(t,L,g):
    return math.ceil(g*max(0,t-L-1)/2)


def xor_synergy():
    vals = list(product((0,1),repeat=2))
    target = lambda sub: set(x for x,r in sub)
    a = [a for a in vals if (a[0]^a[1])==1]
    b = [a for a in vals if a[1]==1]
    ab = [a for a in a if a[1]==1]
    val = lambda sub: 1-math.log2(len(target(sub)))
    assert val(a)==0 and val(b)==0 and val(ab)==1
    return {'v_xor_share':val(a),'v_r_bit':val(b),'v_joint':val(ab),
            'v_duplicate_after_xor':0}


def main():
    skew = [skew_control(t) for t in range(2,11)]
    skew += [skew_formula_symbolic(t) for t in (16,32,64)]
    sweep=[]
    exhaustive = 0
    for t in (2,3,4,5,6,8):
        g=2*t+1
        for L in range(t+1):
            for signs in product((0,1),repeat=t):
                record = get_batch(t,L,g,signs)
                exhaustive += 1
            record['singleton_fixed_start_head_optimum'] = single_query_radius(t,L,g)
            sweep.append(record)
    for t in (16,64):
        g = 2*t+1
        for L in (0,1,t//4,t//2,t-2,t-1,t):
            signs=tuple((j*7+3)%2 for j in range(t))
            record=get_batch(t,L,g,signs)
            record['singleton_fixed_start_head_optimum'] = single_query_radius(t,L,g)
            sweep.append(record)
    payload = {'run_id':'BATCH-SWEEP-VALUE237', 'mode':'structured exhaustive and symbolic',
      'source_positions':'p_j=g*j, j=0,..,t-1; fixed layout, one read-only input head',
      'tested_batch_source_vectors':exhaustive,
      'skew_horn_2cnf':skew, 'xor_synergy':xor_synergy(),
      'batch_sweeps':sweep,
      'algorithm_independent_lemma':'symbolic proof in report, not established by tests',
      'limitations':'no all-SAT hardness or machine-checked proof; source read-only; prepared head fixed; batch output; all persistence counted'}
    body=json.dumps(payload,sort_keys=True,indent=2)+'\n'
    with open('raw.json','w',encoding='utf-8') as f:f.write(body)
    print(json.dumps({'exhaustive_batch_tests':exhaustive,
         'frontier_rows':len(sweep),'skew_rows':len(skew),
         'sha256_raw':hashlib.sha256(body.encode()).hexdigest()},sort_keys=True))

if __name__=='__main__':main()