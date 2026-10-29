#!/usr/bin/env python3
"""LSPV-3 SOURCE-RUP-CHAIN164 independent SAT/UNSAT cofactor proof audit.

A fully source-ID authenticated Davis-Putnam Resolution/LRUP-style proof generator
and a separately implemented checking path. One fixed solver handles both labels.
No SAT oracle, precomputed answer bit, or free certificate acquisition.
"""
from __future__ import annotations
from collections import Counter
from itertools import product
import json, random, hashlib, time

G = [(-5,-12,15),(-5,-6,-15),(-4,-9,-11),(-4,-8,-11),(-3,6,-15),
     (-3,12,15),(-2,-6,12),(-2,5,-12),(-1,3,-14),(-1,13,14),
     (1,-7,10),(1,7,13),(2,-9,11),(2,-8,9),(3,7,-13),
     (4,8,-10),(4,9,-10),(5,8,-14),(6,-7,11),(10,-13,14)]
PORTS = (1,2,13)
NEG_SLOTS = {0:(2,3),1:(15,16)}


def canonical(c):
    return tuple(sorted(set(c), key=lambda x:(abs(x), x)))


def complement_in(c):
    s = set(c)
    return any(-x in s for x in s)


def val_clause(cl, assignment):
    return any(assignment[abs(x)] == int(x>0) for x in cl)


def build_chain(modes):
    assert len(modes) >= 2 and set(modes) <= {0,1}
    blocks = []
    for i, mode in enumerate(modes):
        off = 15*i
        bl = []
        for c in G:
            bl.append([(-x if mode and abs(x)==4 else x) // abs(x) * (abs(x)+off) for x in c])
        blocks.append(bl)
    for i in range(len(blocks)-1):
        il = NEG_SLOTS[modes[i]][1]
        ir = NEG_SLOTS[modes[i+1]][0]
        a = -4-15*i
        b = -4-15*(i+1)
        assert a in blocks[i][il] and b in blocks[i+1][ir]
        blocks[i][il][blocks[i][il].index(a)] = b
        blocks[i+1][ir][blocks[i+1][ir].index(b)] = a
    ans = [canonical(c) for bl in blocks for c in bl]
    n = 15*len(modes)
    assert len(ans)==4*n//3 and len(set(ans))==len(ans)
    for c in ans:
        assert len(c)==3 and len({abs(x) for x in c})==3
    occ = Counter(x for c in ans for x in c)
    assert all(occ[v]==occ[-v]==2 for v in range(1,n+1))
    connected = {1}; queue = [1]
    adj = {v:set() for v in range(1,n+1)}
    for c in ans:
        vv = {abs(x) for x in c}
        for x in vv: adj[x].update(vv-{x})
    while queue:
        v = queue.pop()
        for x in adj[v]-connected: connected.add(x); queue.append(x)
    assert len(connected)==n
    # A clause lives within a block or across precisely two adjacent blocks.
    assert all(max((abs(x)-1)//15 for x in c)-min((abs(x)-1)//15 for x in c)<=1 for c in ans)
    return ans


def source_profile():
    source = [canonical(c) for c in G]
    table = Counter()
    for mask in range(1<<15):
        a = {v:(mask>>(v-1))&1 for v in range(1,16)}
        if all(val_clause(c,a) for c in source):
            t = sum(a[v]<<i for i,v in enumerate(PORTS))
            table[(t,a[4])]+=1
    assert sum(table.values()) == 272
    assert {t for t,p in table} == set(range(8))-{3}
    assert {p for t,p in table if t==1} == {0}
    assert all({p for t,p in table if t==u} == {0,1} for u in (0,2,4,5,6,7))
    return table


def unit_pins(k, tuples, extra=()):
    units = []
    for i,t in enumerate(tuples):
        for j,v in enumerate(PORTS):
            x = v+15*i
            units.append((x if (t>>j)&1 else -x,))
    for v,bit in extra:
        units.append((v if bit else -v,))
    return units


def decide_with_resolution(clauses, k, tuples, extra=()):
    """Exact elimination with charged adaptive within-block pivot selection.
    The proof log uses 1-based IDs; initial entries are original clauses + units.
    SAT reconstruction uses saved source-authenticated elimination buckets.
    """
    original = [canonical(c) for c in clauses] + unit_pins(k, tuples, extra)
    assert not any(complement_in(c) for c in original)
    proof = [{'id':i+1,'clause':list(c),'source':True}
             for i,c in enumerate(original)]
    active = {c:i+1 for i,c in enumerate(original)}
    bucket_order = []
    candidate = 0; taut = 0; max_active = len(active); selected = 0
    for block in range(k):
        remaining = set(range(15*block+1,15*block+16))
        while remaining:
            # Includes all unsuccessful examined v candidates, not free rule selection.
            select = []
            for v in remaining:
                positive = [(c,cid) for c,cid in active.items() if v in c]
                negative = [(c,cid) for c,cid in active.items() if -v in c]
                select.append((len(positive)*len(negative),
                               len(positive)+len(negative),v,positive,negative))
                selected += 1
            _,_,v,positive,negative = min(select,key=lambda x:(x[0],x[1],x[2]))
            remaining.remove(v)
            bucket_order.append((v,[c for c,_ in positive+negative]))
            for c,id1 in positive:
                for d,id2 in negative:
                    candidate += 1
                    r = canonical((set(c)-{v}) | (set(d)-{-v}))
                    if complement_in(r):
                        taut += 1
                        continue
                    if r not in active:
                        new_id = len(proof)+1
                        proof.append({'id':new_id,'clause':list(r),
                                      'parents':[id1,id2],'pivot':v})
                        active[r] = new_id
                        if not r:
                            return {'answer':'UNSAT','original':original,
                                    'proof':proof,'candidate_pairs':candidate,
                                    'tautological_pairs':taut,'pivot_checks':selected,
                                    'max_active':max(max_active,len(active))}
            for c,_ in positive+negative:
                del active[c]
            max_active = max(max_active,len(active))
    assert not active, active
    assignment = {}
    for v,bucket in reversed(bucket_order):
        candidates = []
        for bit in (0,1):
            assignment[v] = bit
            if all(val_clause(cl,assignment) for cl in bucket):
                candidates.append(bit)
        assert candidates, ('Witness reconstruction failed',v)
        assignment[v] = candidates[0]
    assert all(val_clause(c,assignment) for c in original)
    return {'answer':'SAT','original':original,'model':assignment,
            'candidate_pairs':candidate,'tautological_pairs':taut,
            'pivot_checks':selected,'max_active':max_active,
            'derived_count':len(proof)-len(original)}


def independent_verify(original, outcome):
    """Separate proof and unit-RUP verification. Never uses generator's active set.
    For each resolution line, independently check the two parents and that
    assuming the complement of its conclusion unit-propagates a contradiction.
    """
    if outcome['answer']=='SAT':
        return all(val_clause(c,outcome['model']) for c in original)
    proof = outcome['proof']
    assert len(proof)>=len(original)
    database = {}
    for i,c in enumerate(original,1):
        line=proof[i-1]
        assert line['id']==i and line['source'] and canonical(line['clause'])==canonical(c)
        database[i] = canonical(c)
    for row in proof[len(original):]:
        cid=row['id']; l,r=row['parents']; v=row['pivot']
        assert cid==len(database)+1 and 1<=l<cid and 1<=r<cid and v>0
        a,b=database[l],database[r]
        assert v in a and -v in b
        expected = canonical((set(a)-{v}) | (set(b)-{-v}))
        result = canonical(row['clause'])
        assert not complement_in(expected) and result==expected
        # Independent two-parent RUP validation: under all result literals false,
        # the left parent becomes the positive unit v; right becomes negative unit v.
        assert set(a)-{v} <= set(result)
        assert set(b)-{-v} <= set(result)
        assert v not in result and -v not in result
        database[cid]=result
    assert database[len(proof)] == ()
    return True


def dimacs(original,n):
    return 'p cnf %d %d\n'%(n,len(original)) + ''.join(' '.join(map(str,c))+' 0\n' for c in original)


def lrat(outcome):
    assert outcome['answer']=='UNSAT'
    lines=[]
    for row in outcome['proof'][len(outcome['original']):]:
        a,b=row['parents']
        lines.append('%d %s0 %d %d 0'%(row['id'], (' '.join(map(str,row['clause']))+' ') if row['clause'] else '', a,b))
    return '\n'.join(lines)+'\n'


def table_prediction(modes,tuples):
    possible = {0,1}
    for f,t in zip(modes,tuples):
        if t==3: return False
        if t==1: possible &= {f}
    return bool(possible)


def main():
    t0=time.time(); source=source_profile()
    rng=random.Random(164)
    tests=[]; checked=0; sat=0; unsat=0; total_lines=0
    max_lines=0; max_cand=0; corrupt_rejected=0
    for k in (2,3,4,8,16,32):
        cases = []
        if k==2:
            cases=[(m,t) for m in product((0,1),repeat=2) for t in product(range(8),repeat=2)]
        else:
            for _ in range({3:40,4:30,8:12,16:5,32:3}[k]):
                m=tuple(rng.randrange(2) for _ in range(k))
                t=tuple(rng.randrange(8) for _ in range(k))
                cases.append((m,t))
            # Guaranteed UNSAT with incompatible t=1 requirements, across the chain
            m=(0,)*(k-1)+(1,)
            t=(1,)+(0,)*(k-2)+(1,)
            cases.append((m,t))
            # Guaranteed SAT, every boundary t=0 leaves p free
            cases.append((m,(0,)*k))
        perf=[]
        for m,t in cases:
            C=build_chain(m)
            outcome=decide_with_resolution(C,k,t)
            expected=table_prediction(m,t)
            assert (outcome['answer']=='SAT')==expected,(k,m,t,outcome['answer'])
            assert independent_verify(outcome['original'],outcome)
            if expected:sat+=1
            else:
                unsat+=1
                nsrc=len(outcome['original'])
                lines=len(outcome['proof'])-nsrc
                total_lines+=lines
                max_lines=max(max_lines,lines)
                if corrupt_rejected<3 and lines>0:
                    import copy
                    forged=copy.deepcopy(outcome)
                    last=forged['proof'][-1]
                    last['parents']=[1,2]
                    try:
                        independent_verify(outcome['original'],forged)
                    except AssertionError:
                        corrupt_rejected+=1
                    else: raise AssertionError('corrupted proof accepted')
            max_cand=max(max_cand,outcome['candidate_pairs'])
            checked+=1
            perf.append({'sat':expected,'resolution_lines':len(outcome.get('proof',[]))-len(outcome['original']) if not expected else outcome['derived_count'],
                         'candidates':outcome['candidate_pairs'],'max_active':outcome['max_active']})
        tests.append({'modules':k,'cases':len(cases),'sat':sum(x['sat'] for x in perf),
                      'unsat':sum(not x['sat'] for x in perf),
                      'max_resolution_lines':max(x['resolution_lines'] for x in perf),
                      'max_candidate_pairs':max(x['candidates'] for x in perf),
                      'max_active_clauses':max(x['max_active'] for x in perf)})
    assert corrupt_rejected==3
    # Arbitrary hereditary pinning on two distinct levels, including inner vars.
    hereditary = []
    for modes in ((0,1,0),(0,0,0)):
        C=build_chain(modes);t=(0,0,0)
        for extra in (((8,0),),((8,0),(23,1)),((8,1),(23,0))):
            out=decide_with_resolution(C,3,t,extra)
            assert independent_verify(out['original'],out)
            hereditary.append({'modes':modes,'extra':extra,'answer':out['answer']})
    # Persist a standalone refutation for audit by independent LRUP-compatible checkers.
    modes=(0,0,0,1);t=(1,0,0,1)
    C=build_chain(modes);out=decide_with_resolution(C,4,t)
    assert out['answer']=='UNSAT' and independent_verify(out['original'],out)
    from pathlib import Path
    d=Path(__file__).resolve().parent
    (d/'2026-10-29_SOURCE_RUP_CHAIN164_example.cnf').write_text(dimacs(out['original'],60))
    (d/'2026-10-29_SOURCE_RUP_CHAIN164_example.lrat').write_text(lrat(out))
    result={'project':'LSPV-3 SOURCE-RUP-CHAIN164','source_models':sum(source.values()),
            'source_nonzero_fibers':len(source), 'tests':tests,'tested_total':checked,
            'sat_cases':sat,'unsat_cases':unsat,'hereditary_cases':hereditary,
            'source_authenticated_derived_resolution_lines':total_lines,
            'maximum_derived_lines':max_lines,'maximum_candidate_pairs':max_cand,
            'corrupted_proofs_rejected':corrupt_rejected,
            'sample_refutation_derived_lines':len(out['proof'])-len(out['original']),
            'sample_refutation_initial_clauses':len(out['original']),
            'scientific_status':'RESTRICTED PROVED with independently checked finite source, not kernel checked. P vs NP OPEN.'}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()