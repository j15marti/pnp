#!/usr/bin/env python3
"""LSPV-3 parity-probe value controls (fixed seed, Python standard library).

Probe model: raw coordinates and pre-materialized triple parity coordinates,
all cost one *data-source bit probe*.  A pre-materialized parity bit must be
charged during construction; this is not an unrestricted SAT machine model.
"""
from collections import deque
from functools import lru_cache
from itertools import combinations
import hashlib
import json
import random
from pathlib import Path

SEED = 1731029
R = random.Random(SEED)
PREFIX = '2026-10-29_1927_LSPV-3_PARITY_POLICY_SYNDROME173'


def in_span(target, vectors):
    basis = {}
    for v in vectors:
        while v:
            i = v.bit_length()-1
            if i not in basis:
                basis[i] = v
                break
            v ^= basis[i]
    v = target
    while v:
        i = v.bit_length()-1
        if i not in basis:
            return False
        v ^= basis[i]
    return True


def phi(target, vectors):
    return int(not in_span(target, vectors))


def distances(m, vectors):
    # Exact breadth-first minimization of number of probe vectors whose XOR
    # is the target; each vector may be used 0 or 1 times without loss.
    D = [-1]*(1<<m)
    D[0] = 0
    parent = {0: None}
    q = deque([0])
    while q:
        s = q.popleft()
        for v in vectors:
            t = s ^ v
            if D[t] < 0:
                D[t] = D[s]+1
                parent[t] = (s,v)
                q.append(t)
    assert all(x >= 0 for x in D)  # all raw-coordinate probes are present
    return D,parent


def trace(parent,target):
    path=[]
    while target:
        pred,v = parent[target]
        path.append(v)
        target=pred
    return path


def exact_cover(triples,m,q):
    goal = (1<<m)-1
    for choice in combinations(triples,q):
        seen=0
        for c in choice:
            if seen & c:
                break
            seen |= c
        else:
            if seen == goal:
                return True
    return False


def masks_of_size(m,k):
    return [sum(1<<i for i in inds) for inds in combinations(range(m),k)]


def adaptive_minimax(m,vectors,target):
    # Independent truth-table state DP, small m only. Every observation branch
    # is explored and all x are possible; no unknown target bit is supplied.
    initial=(1<<(1<<m))-1
    truth=[(x&target).bit_count()%2 for x in range(1<<m)]
    @lru_cache(None)
    def go(pop):
        ts={truth[x] for x in range(1<<m) if pop>>x&1}
        if len(ts)==1:
            return 0
        best=m+1
        for v in vectors:
            a=b=0
            for x in range(1<<m):
                if pop>>x&1:
                    if (x&v).bit_count()%2:a |= 1<<x
                    else:b |= 1<<x
            if a==0 or b==0:continue
            best=min(best, 1+max(go(a),go(b)))
        return best
    return go(initial)


def blocks_opt(m,target):
    return sum(min(k,4-k) for base in range(0,m,3)
               for k in [((target>>base)&7).bit_count()])


def run():
    stats={'seed':SEED,'model':'promised, indexed, pre-materialized triple parity plus raw-coordinate bit probes',
           'status':'COMPUTATIONAL checks; NP-completeness and rank claim proved in LaTeX'}
    # Independent random-metadata X3C comparison, including planted positives.
    x3c=[]
    for q,reps in [(2,300),(3,250),(4,90)]:
        m=3*q; all_triples=masks_of_size(m,3); yes=no=0; max_gap=0
        for trial in range(reps):
            if trial%2==0:
                perm=list(range(m));R.shuffle(perm)
                planted={sum(1<<x for x in perm[i:i+3]) for i in range(0,m,3)}
                triples=set(planted)
            else:
                triples=set()
            n_extra=R.randrange(q, min(len(all_triples),q*4)+1)
            triples.update(R.sample(all_triples,n_extra))
            triples=sorted(triples)
            vectors=[1<<i for i in range(m)]+triples
            goal=(1<<m)-1
            D,parent=distances(m,vectors)
            expected=exact_cover(triples,m,q)
            assert (D[goal]<=q)==expected, (q,trial,D[goal],expected)
            assert q<=D[goal]<=m
            witness=trace(parent,goal)
            assert len(witness)==D[goal]
            assert sum(0 for _ in witness)==0
            assert (lambda p: p==goal)(__import__('functools').reduce(int.__xor__,witness,0))
            assert in_span(goal,witness)
            # Verify computed target for actual data, not merely the codebook.
            for _ in range(3):
                theta=R.getrandbits(m)
                outcome=0
                for v in witness:outcome ^= (theta&v).bit_count()%2
                assert outcome == (theta&goal).bit_count()%2
            if expected:yes+=1
            else:no+=1
            max_gap=max(max_gap,D[goal]-q)
        x3c.append({'q':q,'m':m,'families':reps,'yes':yes,'no':no,'max_extra_probes_above_q':max_gap})
    stats['x3c']=x3c

    # Exact nonadaptive versus unrestricted adaptive deterministic decision tree.
    adaptive=0
    for m in [3,4]:
        for trial in range(35):
            menu=set([1<<i for i in range(m)])
            menu.update(R.sample(range(1,1<<m),min(3,(1<<m)-1)))
            vectors=sorted(menu)
            D,_=distances(m,vectors)
            for t in range(1,1<<m):
                assert adaptive_minimax(m,vectors,t)==D[t]
                adaptive+=1
    stats['adaptive_truth_table_comparisons']=adaptive

    # Tractable disjoint triple block family and arbitrary targets.
    blocks=[]
    for q in [1,2,3,4]:
        m=3*q
        triples=[7<<(3*i) for i in range(q)]
        vectors=[1<<i for i in range(m)]+triples
        D,_=distances(m,vectors)
        for t,d in enumerate(D):assert d==blocks_opt(m,t)
        blocks.append({'q':q,'m':m,'all_targets_checked':len(D),
                       'all_ones_optimum':D[(1<<m)-1],
                       'all_raw_optimum':m})
    stats['disjoint_blocks']=blocks

    # Context-sensitive value, synergy, redundancy, and paid score discovery.
    a,b=1,2;tar=a^b
    stats['xor_gain']={str(k):1-phi(tar,k) for k in [[],[a],[b],[a,b]]}
    assert [phi(tar,k) for k in [[],[a],[b],[a,b]]]==[1,1,1,0]
    stats['duplicate_gain']={str(k):1-phi(a,k) for k in [[],[a],[a],[a,a]]}
    assert phi(a,[a])==0 and phi(a,[a,a])==0
    stats['direct_answer_greedy']={'share_1_value':0,'share_2_value':0,
        'direct_answer_value':1,'direct_answer_cost':128,'two_share_cost':2,
        'greedy_over_bundled_cost_ratio':64}
    # Negative *net* values are permitted: gain - acquisition.
    stats['net_gain_two_xor_shares']=[-1,0]
    payload=json.dumps(stats,indent=2,sort_keys=True)+'\n'
    out=Path(__file__).resolve().parent/(PREFIX+'_raw.json')
    out.write_text(payload)
    print(payload)
    print('SHA256',hashlib.sha256(payload.encode()).hexdigest())

if __name__=='__main__':run()
