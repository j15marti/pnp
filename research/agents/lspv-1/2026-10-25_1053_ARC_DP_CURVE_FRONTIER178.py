#!/usr/bin/env python3
"""ARC178 direct scoped-stream DP, two-level exact joins, FLMV k=2 frontier.

Reproducible finite tests + exact Fraction arithmetic; NO ARC-EDGE-90 claim.
Python stdlib only. Scope DP operates on live named variables with a bitset
encoding of feasible valuations and charges one table-bit inspection per
padded index in the reference algorithm.
"""
from __future__ import annotations
import json
import ast
import math
from dataclasses import dataclass
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import product
from pathlib import Path
from random import Random

SEED = 202610251053
ROOT = Path(__file__).resolve().parent

Y = (
    (1, 2, 3), (1, 4, 5), (2, 4, 6), (3, 5, 6),
    (-1, -2, -4), (-1, -3, -6), (-2, -3, -5), (-4, -5, -6),
)
ALL8 = tuple(tuple((-1 if (a>>j)&1 else 1) * (j+1) for j in range(3))
             for a in range(8))


def sat_brute(clauses):
    vs = sorted({abs(lit) for c in clauses for lit in c})
    for bits in product((False, True), repeat=len(vs)):
        assignment = dict(zip(vs, bits))
        if all(any(assignment[abs(l)] == (l>0) for l in c) for c in clauses):
            return True
    return False


def events_from_cnf(clauses):
    """TEST-ONLY source normalizer! Stores first/last occurrence metadata.
    It is NOT a low-space N^{p} all-input scoped normalizer theorem.
    """
    positions={}
    for i,c in enumerate(clauses):
        if any(l==0 for l in c): raise ValueError('literal zero')
        if len({abs(l) for l in c})!=len(c):
            raise ValueError('duplicate name in one clause')
        for l in c:
            v=abs(l)
            positions.setdefault(v,[]).append(i)
    opens={}; closes={}
    for v,loc in positions.items():
        opens.setdefault(min(loc),[]).append(v)
        closes.setdefault(max(loc),[]).append(v)
    result=[]
    for i,c in enumerate(clauses):
        for v in sorted(opens.get(i,())): result.append(('OPEN',v))
        result.append(('CLAUSE',tuple(c)))
        for v in sorted(closes.get(i,())): result.append(('CLOSE',v))
    return tuple(result)


def parse_scoped(events):
    active=[]; mx=0; positions=[]
    for op,arg in events:
        if op=='OPEN':
            assert arg not in active and isinstance(arg,int) and arg>0
            active.append(arg)
        elif op=='CLAUSE':
            assert all(abs(l) in active for l in arg)
            assert len({abs(l) for l in arg}) == len(arg)
        elif op=='CLOSE':
            assert arg in active
            active.remove(arg)
        else: raise ValueError(op)
        positions.append(tuple(active))
        mx=max(mx,len(active))
    assert active==[]
    return mx,positions


@dataclass
class Meter:
    event_calls:int=0
    padded_index_reads:int=0
    indexed_writes:int=0
    peak_bit_slots:int=1
    peak_active:int=0
    max_controller_names:int=0
    # This counts logical table and source operations, not physical FLMV steps.


def step(table,active,event,meter):
    op,arg=event
    meter.event_calls+=1
    if op=='OPEN':
        assert arg not in active
        w=len(active)
        table |= table << (1<<w)
        active=active+(arg,)
        meter.indexed_writes+=(1<<(w+1))
    elif op=='CLAUSE':
        w=len(active)
        lits=[]
        for l in arg:
            assert abs(l) in active
            lits.append((active.index(abs(l)),l>0))
        mask=0
        for st in range(1<<w):
            meter.padded_index_reads+=1
            if (table>>st)&1 and any(bool(st&(1<<j))==sign for j,sign in lits):
                mask|=1<<st
        table=mask
        meter.indexed_writes+=(1<<w)
    elif op=='CLOSE':
        assert arg in active
        w=len(active); j=active.index(arg)
        nxt=0
        for st in range(1<<w):
            meter.padded_index_reads+=1
            if (table>>st)&1:
                a=(st&((1<<j)-1))|((st>>(j+1))<<j)
                nxt|=1<<a
        table=nxt;active=active[:j]+active[j+1:]
        meter.indexed_writes+=(1<<(w-1))
    else: raise ValueError(op)
    meter.peak_bit_slots=max(meter.peak_bit_slots,1<<len(active))
    meter.peak_active=max(meter.peak_active,len(active))
    meter.max_controller_names=max(meter.max_controller_names,len(active))
    return table,active


def run_segment(events,initial_active=(),initial_table=1,meter=None):
    if meter is None:meter=Meter()
    active=tuple(initial_active); table=initial_table
    for e in events:
        table,active=step(table,active,e,meter)
    return table,active,meter


def scoped_dp(events):
    parse_scoped(events)
    table,active,meter=run_segment(events)
    assert not active
    return bool(table&1),meter


def live_before(events):
    active=[]; states=[()]
    for op,arg in events:
        if op=='OPEN':active.append(arg)
        elif op=='CLOSE':active.remove(arg)
        states.append(tuple(active))
    return states


def transfer(events,src,dst):
    """Matrix map: source bitpattern -> SET of destination bitpatterns.
    Every membership is computed from a genuine sequence of OPEN/CLAUSE/CLOSE.
    """
    result={}
    for v in range(1<<len(src)):
        out,actual,_=run_segment(events,src,1<<v)
        assert actual==dst
        result[v]=frozenset(j for j in range(1<<len(dst)) if (out>>j)&1)
    return result


def compose(A,B):
    return {a:frozenset(z for mid in targets for z in B[mid]) for a,targets in A.items()}


def twolevel_join(events):
    """Two TRUE cut levels: four actual segments -> pair joins -> root join.
    Unlike ARC, these are finite relation-table controls, not SAT machines.
    """
    names=live_before(events)
    splits=[0,len(events)//4,len(events)//2,(3*len(events))//4,len(events)]
    matrices=[transfer(events[splits[i]:splits[i+1]],names[splits[i]],names[splits[i+1]]) for i in range(4)]
    left=compose(matrices[0],matrices[1]);right=compose(matrices[2],matrices[3]);full=compose(left,right)
    assert names[0]==names[-1]==()
    return full[0]==frozenset([0]),sum(sum(map(len,v.values())) for v in matrices)


def beta(c):
    return ((c+2)/c**2-c)/2


def frontier():
    getcontext().prec=65
    def poly(x):return 3*x**3+7*x**2+4*x-2
    lo=Decimal(0);hi=Decimal(1)
    for _ in range(240):
        md=(lo+hi)/2
        if poly(md)<0:lo=md
        else:hi=md
    rt=(lo+hi)/2
    out=[]
    for k in [Fraction(1,20),Fraction(41,800),Fraction(1,5),Fraction(3,10),Fraction(31,100)]:
        c=1+k; b=beta(c)
        out.append({'kappa':str(k),'kappa_float':float(k),'dp_time':float(c),
                    'dp_space':float(k),'FLMV_beta_c':float(b),
                    'gap_beta_minus_space':float(b-k),'forbidden':k<b,
                    'arc_conditional_time':float(1+4*k),
                    'arc_minus_direct_dp_exponent':float(3*k)})
    strict=Fraction(241,200)
    dstar=beta(strict)
    assert dstar==Fraction(11642479,23232400)
    assert poly(Fraction(30977,100000))<0 and poly(Fraction(30978,100000))>0
    return {'curve_threshold_kappa':str(rt),'curve_threshold_interval':[str(lo),str(hi)],
            'threshold_cubic':'3*kappa^3+7*kappa^2+4*kappa-2=0',
            'strict_box_c':str(strict),'strict_box_d':str(dstar),
            'samples':out}


def random_sources(seed):
    rng=Random(seed)
    fixed=[('true',()),('false',((),)),('contradictory_units',((1,),(-1,))),
           ('forced_true',((1,),)),('forced_false',((-1,),)),
           ('xor_sat',((1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3))),
           ('all8_unsat',ALL8),('Y_M22_SAT',Y)]
    # Four disjoint genuine monotone 2P,2N-CNF-3 SAT Y copies are easy scoped controls.
    copies=tuple(tuple((abs(l)+6*j)*(1 if l>0 else -1) for l in c) for j in range(4) for c in Y)
    fixed.append(('four_disjoint_M22_Y',copies))
    for key,clauses in fixed:yield key,clauses
    for i in range(320):
        n=rng.randint(2,8);m=rng.randint(1,23)
        clauses=[]
        for _ in range(m):
            width=rng.randint(1,min(3,n))
            vars_=rng.sample(range(1,n+1),width)
            c=tuple(x if rng.randrange(2) else -x for x in vars_)
            clauses.append(c)
        if i%19==0:
            var=rng.randint(1,n)
            clauses.extend(((var,),(-var,)))
        yield f'rand_{i:03}',tuple(clauses)


def main():
    checks=0;cases=[];jchecks=0;DP_reads=0;DP_writes=0;maxwidth=0;maxslots=0
    nSAT=nUNSAT=0;witnesses=[]
    for i,(name,clauses) in enumerate(random_sources(SEED)):
        truth=sat_brute(clauses)
        stream=events_from_cnf(clauses)
        mx,states=parse_scoped(stream)
        dp,meter=scoped_dp(stream)
        assert dp==truth,(name,truth,dp)
        checks+=1;nSAT+=int(truth);nUNSAT+=int(not truth)
        DP_reads+=meter.padded_index_reads;DP_writes+=meter.indexed_writes
        maxwidth=max(maxwidth,mx);maxslots=max(maxslots,meter.peak_bit_slots)
        if i<8 or i%9==0:
            joined,entry_count=twolevel_join(stream)
            assert joined==truth,(name,joined,truth)
            jchecks+=1;checks+=1
            witnesses.append({'name':name,'is_sat':truth,'scoped_events':len(stream),
                             'max_live_width':mx,'stage_matrix_entries':entry_count})
        cases.append({'name':name,'nclauses':len(clauses),'active_names':len({abs(l) for c in clauses for l in c}),
                      'sat':truth,'event_count':len(stream),'w':mx,
                      'table_slots_upper':meter.peak_bit_slots,
                      'reference_index_reads':meter.padded_index_reads,
                      'reference_index_writes':meter.indexed_writes})
    # Structural-only high-width control. We DO NOT execute 2^42 table DP.
    source_candidates=[Path('research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt'),
                       Path('/mnt/data/arc177/doecker_U.json')]
    uwidth=None
    for source in source_candidates:
        if source.exists():
            raw=source.read_text();raw='\n'.join(line for line in raw.splitlines() if not line.lstrip().startswith('#'))
            u=ast.literal_eval(raw)
            assert len(u)==264 and len({abs(v) for c in u for v in c})==198
            uwidth,_=parse_scoped(events_from_cnf(u))
            assert uwidth==42
            checks+=1
            break
    f=frontier()
    assert 3*Fraction(1,5)**3+7*Fraction(1,5)**2+4*Fraction(1,5)-2<0
    assert 3*Fraction(31,100)**3+7*Fraction(31,100)**2+4*Fraction(31,100)-2>0
    checks+=3
    output={'run_id':'ARC-DP-FRONTIER178','timestamp_local':'2026-10-25 10:53 America/Los_Angeles',
            'seed':SEED,'status':'PASS','scope':'finite exact event DP and two-level join; symbolic FLMV-k2 corollary',
            'count':{'sources':len(cases),'sat':nSAT,'unsat':nUNSAT,'twolevel_join_tests':jchecks,
                     'assertion_count':checks,'failures':0,'max_scope_width':maxwidth,
                     'max_live_bitset_slots':maxslots,'reference_index_reads':DP_reads,
                     'reference_index_writes':DP_writes,'unsat_U198_source_order_width_structural_only':uwidth},
            'frontier':f,'sample_twolevel':witnesses,'cases':cases,
            'limitations':['test stream generator stores first/last positions; not an FLMV all-input normalizer',
                           'reference Python bitset and counters are logical not physical RTM measurements',
                           'two-level matrices are genuine scoped segment transfers, not ordinary SAT guest children',
                           'no hereditary low-width hard image or A-dependent ARC successor constructed',
                           'threshold is for quoted k=2 FLMV curve and direct DP ledger, not globally optimal tradeoff']}
    p=ROOT/'2026-10-25_1053_ARC_DP_FRONTIER178_results.json'
    p.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'run':output['run_id'],'status':output['status'],'count':output['count'],
                      'curve_root':f['curve_threshold_kappa'],'samples':f['samples']},indent=2))

if __name__=='__main__':main()
