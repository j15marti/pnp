#!/usr/bin/env python3
"""Independent hostile checks for VIRTUAL-SORT-BIT254.
The comparator semantics are simulated forward; source SAT is exhaustively
checked.  The false-SAT no-consistency-counterexample is validated on the
same signed UNSAT source, not asserted from a failed search.
"""
import itertools, json, random, time
from virtual_sort_emitter import (Source,VirtualSort,source_models,reference_materialize,
                                  evaluate_clause,source_extremes,selected_work_baseline)


def extend_witness(e,vals):
    """Build all named Boolean gate values without solving the emitted CNF."""
    v=[0]*(e.n+1)
    wires=[]
    for r in range(e.P):
        key=abs(e.src.literal(r//3,r%3)) if r<e.L else e.src.n+1
        bits=[(key>>(e.w-1-i))&1 for i in range(e.w)]
        payload=vals[r] if r<e.L else 0
        bits.append(payload)
        for f,b in enumerate(bits):v[e.rec(r,f)]=b
        wires.append(bits)
    num=0
    for h in range(1,e.d+1):
        k=1<<h
        for power in range(h-1,-1,-1):
            j=1<<power
            nxt=[None]*e.P
            for lo in range(e.P):
                if lo&j:continue
                hi=lo^j
                asc=(lo&k)==0
                A=wires[lo];B=wires[hi]
                v[e.cv(num,0)]=1
                v[e.cv(num,1)]=0
                eqprev=1;flagprev=0
                for f in range(e.w):
                    xn=int(A[f]==B[f]);comparison=(A[f] and not B[f]) if asc else (not A[f] and B[f])
                    term=eqprev and comparison
                    flag=int(flagprev or term)
                    eq=int(eqprev and xn)
                    for t,b in enumerate([xn,int(comparison),int(term),flag,eq]):
                        v[e.cv(num,2+5*f+t)]=b
                    eqprev,flagprev=eq,flag
                low=B if flagprev else A
                high=A if flagprev else B
                for side,record in enumerate((low,high)):
                    for f,b in enumerate(record):
                        v[e.cv(num,2+5*e.w+side*(e.w+1)+f)]=b
                nxt[lo]=list(low);nxt[hi]=list(high)
                num+=1
            wires=nxt
    assert num==e.Q
    for g in range(e.P-1):
        equal=[]
        for f in range(e.w):
            b=int(wires[g][f]==wires[g+1][f])
            v[e.ev(g,f)]=b
            equal.append(b)
        cur=equal[0]
        for f in range(e.w-1):
            cur=int(cur and equal[f+1])
            v[e.ev(g,e.w+f)]=cur
    return v,wires


def source_pair_mode_check(src):
    ext=source_extremes(src)
    models=list(itertools.product((0,1),repeat=src.n))
    for row in ext['clauses']:
        C=row['literals']
        assert {int(k):v for k,v in row['S'].items()}=={abs(z):int(z>0) for z in C}
        assert {int(k):v for k,v in row['U'].items()}=={abs(z):int(z<0) for z in C}
        assert row['not_S']==row['U'] and row['not_U']==row['S']
    tested=0
    for pair in ext['pairs']:
        j,k=(x-1 for x in pair['indices'])
        C=src.clauses[j];D=src.clauses[k]
        for mode in ['SS','SU','US','UU']:
            want=pair[mode];seen=False
            for a in models:
                cj=sum(a[abs(z)-1]==int(z>0) for z in C)
                ck=sum(a[abs(z)-1]==int(z>0) for z in D)
                seen|=((cj==3 if mode[0]=='S' else cj==0) and
                       (ck==3 if mode[1]=='S' else ck==0))
            assert seen==want,(j,k,mode)
            tested+=1
    for a in models:
        b=tuple(1-v for v in a)
        ca=[sum(a[abs(z)-1]==int(z>0) for z in C) for C in src.clauses]
        cb=[sum(b[abs(z)-1]==int(z>0) for z in C) for C in src.clauses]
        assert all(x+y==3 for x,y in zip(ca,cb))
    return tested,len(models)


def special_controls():
    parity_even=Source(((1,2,-3),(1,-2,3),(-1,2,3),(-1,-2,-3)),3)
    full_unsat=Source(tuple(tuple((1 if ((q>>i)&1)==0 else -1)*(i+1)
                         for i in range(3)) for q in range(8)),3)
    sat_sources=[
        Source(((1,2,3),),3),
        Source(((1,-2,3),(-1,2,3)),3),
        parity_even,
        Source(((1,-2,-3),(-1,-2,-3)),3),
    ]
    results=[];checked_clauses=0;pair_modes=0
    for src in sat_sources+[full_unsat]:
        e=VirtualSort(src)
        rows,_=reference_materialize(src)
        ct,_=source_pair_mode_check(src)
        pair_modes+=ct
        witnesses=[]
        for a in source_models(src):
            vals=[int(a[abs(src.literal(r//3,r%3))-1]) for r in range(e.L)]
            v,wires=extend_witness(e,vals)
            assert all(wires[g][:e.w]<=wires[g+1][:e.w] for g in range(e.P-1))
            assert all(evaluate_clause(C,v) for C in rows)
            checked_clauses+=len(rows)
            witnesses.append(list(a))
        results.append({'source_m':src.m,'sat':bool(witnesses),'model_count':len(witnesses),
                        'checked_circuit_clauses':len(rows)*len(witnesses)})
    assert not source_models(full_unsat)
    e=VirtualSort(full_unsat)
    rows,_=reference_materialize(full_unsat)
    # Counterexample: locally satisfy each original clause with independent
    # occurrence payload, then retain all gate clauses and pins, omit precisely
    # the last two guard clauses of each adjacency equality block.
    vals=[]
    for c in full_unsat.clauses:
        vals.extend((int(c[0]>0),0,0))
    v,wires=extend_witness(e,vals)
    start=full_unsat.m+4*e.pins+e.Q*e.rows_cmp
    excluded={start+g*e.rows_eq+e.rows_eq-2+t for g in range(e.P-1) for t in range(2)}
    violations=[i for i in excluded if not evaluate_clause(rows[i],v)]
    assert violations
    assert all(evaluate_clause(C,v) for i,C in enumerate(rows) if i not in excluded)
    assert all(any(v[abs(z)]==int(z>0) for z in rows[i]) for i in range(full_unsat.m))
    # Inspect the auxiliary guarded strict invariants: equal key, unequal
    # payload occurs in the counterfeit source.
    clashes=sum(wires[g][:e.w]==wires[g+1][:e.w] and wires[g][e.w]!=wires[g+1][e.w]
                for g in range(e.P-1))
    assert clashes>0
    return {'tested_S_U_pair_modes':pair_modes,
            'source_assignment_complement_tests':sum(2**s.n for s in sat_sources+[full_unsat]),
            'SAT_witnesses_fully_extended':sum(x['model_count'] for x in results),
            'satisfied_emitted_clauses_checked':checked_clauses,
            'counterfeit_unsat_source_models':0,
            'no_consistency_guard_counterfeit_sat':True,
            'counterfeit_guard_violations':len(violations),
            'same_key_inconsistent_neighbor_pairs':clashes,
            'controls':results}


def physical_emission_cost():
    src=Source(tuple(tuple((1 if ((q>>i)&1)==0 else -1)*(i+1)
                         for i in range(3)) for q in range(8)),3)
    em=VirtualSort(src)
    start=time.perf_counter();checksum=0
    for i in range(em.bits):checksum=(checksum*131+em.bit(i))%1000000007
    dt=time.perf_counter()-start
    baseline_start=time.perf_counter();b=selected_work_baseline(src)
    baseline_s=time.perf_counter()-baseline_start
    assert b['SAT'] is False
    return {'source_unsat':True,'complete_output_bits_emitted':em.bits,
            'output_checksum':checksum,'virtual_emission_elapsed_s':round(dt,6),
            'baseline_DPLL_elapsed_s':round(baseline_s,7),
            'baseline_DPLL_nodes':b['nodes'],'baseline_DPLL_literal_tests':b['literal_tests'],
            'note':'Python timing, not FLMV bit steps; output memory discarded, independent oracle excluded'}


if __name__=='__main__':
    t0=time.perf_counter()
    r={'independent_checker':'PASS','witness_and_counterfeit':special_controls(),
       'full_emission_cost':physical_emission_cost(),
       'elapsed_seconds':round(time.perf_counter()-t0,6)}
    print(json.dumps(r,indent=2))