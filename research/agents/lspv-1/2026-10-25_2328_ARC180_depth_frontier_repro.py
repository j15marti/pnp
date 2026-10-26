#!/usr/bin/env python3
"""ARC180: exact rational arbitrary-seed certificate-volume frontier and
finite two-real-semantic-level SAT/UNSAT compatible-join tests.

Scientific status: algebraic necessary/sufficient conditions *for the
specified hypothetical exponent ledger*, not for general SAT algorithms.
The finite relation tests have no uncharged solver call. Their exhaustive
leaf evaluation is deliberately exponential in the (small) test variables.

Run: python 2026-10-25_2328_ARC180_depth_frontier_repro.py [output.json]
"""
import hashlib
import itertools
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

RUN = 'ARC-KSEED-DEPTH-COVER180'
SEED = 202610252328
FR = Fraction

def van_h(d):
    assert d > 1
    return max(1 + FR(1, 1) / d, (2 * d - 1) / (d * (d - 1)))

def ledger(k, kappa, depth):
    """Exponent budget for a CONDITIONAL recursive branch scheme:
    per-node child count n^(1/2+kappa), child length n^1/2.
    g=0 eager serialization, r=1 local work, fixed-depth recursion.
    """
    k = FR(k); kappa = FR(kappa)
    p, q = FR(0), FR(1)
    level = []
    for i in range(depth):
        generation = p + q * (1 + kappa)
        local = p + q
        level.append({'depth':i, 'node_exponent':p,
                      'child_exponent':q, 'generation_time':generation,
                      'local_time':local})
        p += q * (FR(1,2) + kappa)
        q /= 2
    guest = p + k * q
    volume = p + q
    time = max([guest] + [e['generation_time'] for e in level] +
               [e['local_time'] for e in level])
    return {'leaf_count':p, 'leaf_length':q, 'guest_time':guest,
            'leaf_volume':volume, 'time':time, 'levels':level}

def minimal_depth(k, kappa, cap=45):
    for L in range(1,cap+1):
        if ledger(k,kappa,L)['time'] < van_h(FR(k)):
            return L
    return None

def eval_clause(clause,assignment):
    return any(assignment[abs(lit)] == (lit > 0) for lit in clause)

def eval_cnf(cnf, assignment):
    return all(eval_clause(c, assignment) for c in cnf)

def varset(cnf):
    return set(abs(l) for clause in cnf for l in clause)

def assignments(vs):
    variables = tuple(sorted(vs))
    for bits in itertools.product((False,True), repeat=len(variables)):
        yield dict(zip(variables, bits))

def brute_sat(cnf):
    return any(eval_cnf(cnf,a) for a in assignments(varset(cnf)))

def create_relation(block, boundary):
    """Leaf relation on original named boundary variables."""
    key = tuple(sorted(boundary))
    assert boundary <= varset(block)
    return {tuple(a[v] for v in key)
            for a in assignments(varset(block)) if eval_cnf(block,a)}

def combine(L, R, ifaceL, ifaceR, parent_iface):
    """Exact compatibility join; fresh internal variables existentially forgotten."""
    keysL = tuple(sorted(ifaceL)); keysR=tuple(sorted(ifaceR))
    keysP=tuple(sorted(parent_iface))
    assert parent_iface <= ifaceL | ifaceR
    ans=set()
    for tupL in L:
        dL=dict(zip(keysL,tupL))
        for tupR in R:
            dR=dict(zip(keysR,tupR))
            if any(dL[v] != dR[v] for v in ifaceL & ifaceR):
                continue
            merged=dict(dL);merged.update(dR)
            ans.add(tuple(merged[v] for v in keysP))
    return ans

def two_level_dp(cnf, block_count=4):
    assert block_count == 4
    blocks=[tuple(cnf[i::block_count]) for i in range(block_count)]
    bv=[varset(b) for b in blocks]
    allindices=set(range(4))
    stats={'leaf_states':[], 'join_states':[], 'interfaces':[],
           'block_SAT_flags':[]}
    def iface(subset):
        inside=set().union(*(bv[j] for j in subset))
        outside=set().union(*(bv[j] for j in allindices-set(subset)))
        return inside & outside
    leaf=[]
    for i,b in enumerate(blocks):
        boundary=iface({i})
        rel=create_relation(b,boundary)
        leaf.append(rel)
        stats['leaf_states'].append(len(rel))
        stats['interfaces'].append(len(boundary))
        stats['block_SAT_flags'].append(bool(rel))
    left_iface=iface({0,1});right_iface=iface({2,3})
    left=combine(leaf[0],leaf[1],iface({0}),iface({1}),left_iface)
    right=combine(leaf[2],leaf[3],iface({2}),iface({3}),right_iface)
    root=combine(left,right,left_iface,right_iface,set())
    stats['join_states']=[len(left),len(right),len(root)]
    assert root in (set(),{()})
    return bool(root),stats

def make_satisfied_cnf(rng,n,m):
    witness={i:bool(rng.getrandbits(1)) for i in range(1,n+1)}
    clauses=set()
    while len(clauses)<m:
        vs=sorted(rng.sample(range(1,n+1),3))
        lits=tuple(v if rng.getrandbits(1) else -v for v in vs)
        if eval_clause(lits,witness):clauses.add(lits)
    return tuple(sorted(clauses))

def make_unsat_cnf(rng,n,m):
    assert m>=8
    clauses={tuple(v if bit else -v for v,bit in zip((1,2,3),bits))
             for bits in itertools.product((False,True),repeat=3)}
    while len(clauses)<m:
        vs=sorted(rng.sample(range(1,n+1),3))
        clauses.add(tuple(v if rng.getrandbits(1) else -v for v in vs))
    return tuple(sorted(clauses))

def frac_out(x):
    return str(x.numerator)+'/'+str(x.denominator)

def main():
    count=0
    def ck(condition,label):
        nonlocal count
        count+=1
        if not condition: raise AssertionError(label)
    table=[]
    for K in (2,3,4,10,100):
        for kap in (FR(0), FR(1,100), FR(1,50), FR(1,20)):
            cap=van_h(FR(K)); crit=FR(1,2*K)
            best=minimal_depth(K,kap)
            expected_exists=kap<crit
            ck((best is not None)==expected_exists,('feasible',K,kap,best))
            if best is not None:
                ck(ledger(K,kap,best)['time']<cap,('strict',K,kap,best))
                if best>1:ck(ledger(K,kap,best-1)['time']>=cap,('least',K,kap,best))
            table.append({'K':K,'kappa':frac_out(kap),'H':frac_out(cap),
                          'kappa_critical':frac_out(crit),'min_L':best,
                          'at_min':None if best is None else
                          {'time':frac_out(ledger(K,kap,best)['time']),
                           'volume':frac_out(ledger(K,kap,best)['leaf_volume']),
                           'leaf_exponent':frac_out(ledger(K,kap,best)['leaf_length'])}})
            for L in range(0,19):
                e=ledger(K,kap,L)
                z=FR(1,2**L)
                ck(e['leaf_count']==(1+2*kap)*(1-z),('pop',K,kap,L))
                ck(e['leaf_length']==z,('length',K,kap,L))
                ck(e['leaf_volume']==1+2*kap*(1-z),('vol',K,kap,L))
                ck(e['guest_time']==1+2*kap+(K-1-2*kap)*z,('guest',K,kap,L))
                ck(e['time']==e['guest_time'],('eager no overhead',K,kap,L))
    rng=random.Random(SEED)
    sat_count=unsat_count=0
    mismatch=0
    label_only_unsat=0
    controls=[]
    for label in ('SAT','UNSAT'):
        for j in range(80):
            n=4+(j%4)
            m=12+(j%5)+n # comfortably below available unique satisfying triples
            cnf=(make_satisfied_cnf(rng,n,m) if label=='SAT' else
                 make_unsat_cnf(rng,n,m))
            b=brute_sat(cnf)
            d,stats=two_level_dp(cnf)
            ck(b==(label=='SAT'),('generator label',label,j))
            ck(b==d,('two-level join',label,j,stats))
            (sat_count if b else unsat_count)  # count below
            if b:sat_count+=1
            else:unsat_count+=1
            if not b and all(stats['block_SAT_flags']):label_only_unsat+=1
            if j<4:controls.append({'class':label,'n':n,'m':len(cnf),
                'label':b,'states':stats})
    # Minimal unsat two-block join where every actual block is SAT:
    core=make_unsat_cnf(random.Random(1),3,8)
    ck(not brute_sat(core),'8 clause proper 3CNF covers all 3-variable assignments')
    # Make 4 blocks of 2 clauses by slicing, all satisfiable.
    root,stat=two_level_dp(core)
    ck(not root and all(stat['block_SAT_flags']),('local flags incomplete',stat))
    # One-clause deletion should make exactly one formerly excluded 3-bit assignment viable.
    released=core[1:]
    ck(brute_sat(released),'one clause deletion SAT')
    relroot,relstat=two_level_dp(released)
    ck(relroot and all(relstat['block_SAT_flags']),('opposite label same block flags',relstat))
    source=Path(__file__)
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    output={'run':RUN,'date_local':'2026-10-25 23:28 America/Los_Angeles',
        'seed':SEED,'python_sha256':digest,'assertions':count,
        'frontier':{'theorem':'strict-budget feasibility iff kappa<1/(2K) for K>=2; conditional on explicit branch scheme, no SAT theorem',
            'H_K':'1+1/K', 'leaf_vol_exp':'1+2*kappa*(1-2^-L)',
            'guest_time_exp':'1+2*kappa+(K-1-2*kappa)*2^-L',
            'table':table},
        'semantic_tests':{'SAT_roots':sat_count,'UNSAT_roots':unsat_count,
             'both_labels':sat_count>0 and unsat_count>0,
             'two_actual_relation_join_levels':True,
             'unsat_with_all_blocks_sat':label_only_unsat,
             'proper_all_eight_signs_unsat':True,
             'deletion_sat_same_local_flags':True,
             'sample_controls':controls,
             'full_solver_callbacks':0,'large_class_reduction_tested':False},
        'scope':{'all_UNSAT_affordable_coverage':'OPEN',
                 'independent_PEER_REVIEW':'PENDING',
                 'arbitrary_seed_small_space':'OPEN',
                 'FLMV_transport':'OPEN','P_vs_NP':'OPEN'}}
    dest=Path(sys.argv[1]) if len(sys.argv)>1 else source.with_suffix('.json')
    dest.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n',encoding='utf8')
    print(json.dumps({'run':RUN,'sha256':digest,'assertions':count,
        'SAT':sat_count,'UNSAT':unsat_count,
        'UNSAT_all_local_SAT':label_only_unsat,
        'frontier_K10':[(v['kappa'],v['min_L']) for v in table if v['K']==10],
        'output':str(dest)},indent=2))

if __name__=='__main__':main()
