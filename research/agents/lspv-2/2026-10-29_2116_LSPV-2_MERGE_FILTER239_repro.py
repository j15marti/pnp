#!/usr/bin/env python3
"""LSPV-2 MERGE-FILTER239, independent deterministic reproducibility runner.

Scope: arbitrary finite CNF and selected proper strict exact-(2,2) source controls.
This is NOT a general SAT lower bound. All solver branches, heuristic reads,
unit-propagation scans, tried assignments, failed literal probes, and initial
one-step resolvent generation are counted in a transparent primitive-work ledger.
Python tracemalloc is a SAME-RUN implementation peak, not native TM workspace.
"""
from __future__ import annotations
import collections, hashlib, itertools, json, math, pathlib, random, sys, time, tracemalloc
from dataclasses import dataclass

SEED = 20261029
W1_STR = """-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14"""
S_STR = """-1 -3 14;2 8 -9;-10 13 14;3 -7 -13;-4 9 -11;-5 -8 -14;4 -8 11;1 7 -13;1 -7 10;-5 -6 15;-2 6 -12;4 9 -10;-2 5 -12;3 6 -15;-6 7 11;2 -9 -11;-4 8 10;-3 12 15;5 12 -15;-1 13 -14"""

def parse(s):
    return tuple(tuple(map(int, x.split())) for x in s.split(';'))

def clause_truth(c, a):
    return any(a[abs(z)-1] == (z>0) for z in c)

def truth(F, a):
    return all(clause_truth(c,a) for c in F)

def instances():
    d={
        '2sat_unsat': (2,((1,2),(-1,2),(1,-2),(-1,-2))),
        '2sat_chain_unsat': (4,((1,),(-1,2),(-2,3),(-3,4),(-4,))),
        'horn_unsat': (3,((1,),(-1,2),(-2,3),(-3,))),
        'shared_overlap': (4,((1,2,3),(-1,2,4))),
        'disjoint_support': (5,((1,2,3),(-1,4,5))),
        'xor3_strict22_sat': (3,((1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3))),
        'W1_strict22_unsat': (15,parse(W1_STR)),
        'S_strict22_sat': (15,parse(S_STR)),
    }
    for n in (6,9):
        F=[]
        for i in range(n):
            F.append((i+1,(i+1)%n+1,-((i+2)%n+1)))
        for i in range(0,n,3): F.append((-(i+1),-(i+2),-(i+3)))
        d[f'cyclic{n}_strict22_sat']=(n,tuple(F))
    for k in (1,2,4,8,12):
        F=[]
        for x in range(3,k+3):
            F.extend(((x,1,2),(-x,1,2)))
        d[f'replicated_overlap_k{k}']=(k+2,tuple(F))
    r=random.Random(SEED)
    for i in range(24):
        n=5 if i<12 else 7
        m=8 + (i%6)
        F=[]
        for j in range(m):
            vs=r.sample(range(1,n+1),3)
            F.append(tuple(v if r.randrange(2) else -v for v in vs))
        d[f'random_{i:02d}']=(n,tuple(F))
    return d

def check_source(n,F):
    if any(l==0 or abs(l)>n for c in F for l in c):raise ValueError('invalid literal')
    if any(len(set(map(abs,c)))!=len(c) for c in F):raise ValueError('not proper clause')
    d=[collections.Counter() for _ in range(n)]
    g={i:set() for i in range(1,n+1)}
    for c in F:
        vs=[abs(x) for x in c]
        for x in c:d[abs(x)-1][1 if x>0 else -1]+=1
        for u in vs:
            for v in vs:
                if u!=v:g[u].add(v)
    seen={1};pending=[1]
    while pending:
        x=pending.pop()
        for y in g[x]-seen:seen.add(y);pending.append(y)
    return {'exact22':all(len(c)==3 for c in F) and all(z[1]==2 and z[-1]==2 for z in d),
            'connected':len(seen)==n,'occurrences':sum(map(len,F)),
            'sign_counts':[(z[1],z[-1]) for z in d]}

def resolvents(n,F):
    pairs=[];taut=0;scan=0
    pos=collections.defaultdict(list);neg=collections.defaultdict(list)
    for j,c in enumerate(F):
        for lit in c:
            (pos if lit>0 else neg)[abs(lit)].append(j)
    for v in range(1,n+1):
        for j in pos[v]:
            for k in neg[v]:
                A=set(F[j])-{v}; B=set(F[k])-{-v}
                scan+=len(F[j])+len(F[k])+len(A)+len(B)
                R=A|B
                if any(-lit in R for lit in R):taut+=1;continue
                assert v not in set(map(abs,R))
                pairs.append({'pivot':v,'j':j,'k':k,'r':tuple(sorted(R,key=lambda x:(abs(x),x))),
                              'merge':bool(A&B), 'overlap':tuple(sorted(A&B,key=lambda x:(abs(x),x))),
                              'width':len(R)})
    return pairs,taut,scan

def unique_clauses(pairs, filter_merge=None, max_width=None, budget=None):
    unique=[];have=set()
    for p in pairs:
        if filter_merge is not None and p['merge']!=filter_merge:continue
        if max_width is not None and p['width']>max_width:continue
        r=p['r']
        if r not in have:
            have.add(r);unique.append(r)
            if budget is not None and len(unique)>=budget:break
    return tuple(unique)

def lit_status(lit,a):
    z=a[abs(lit)-1]
    return 'unset' if z<0 else ('true' if z==(lit>0) else 'false')

def occurrences(F, full, part):
    return [{'variable':abs(lit),'clause_index':j,'occurrence':f'x_{{{abs(lit)},{j}}}',
             'sigma':1 if lit>0 else -1,'preferred':int(lit>0),
             'full':lit_status(lit,full),'partial':lit_status(lit,part)}
            for j,c in enumerate(F) for lit in c]

def profile(F,a):
    assert all(z in (False,True) for z in a)
    N=[0,0,0,0]
    for c in F:
        assert len(c)==3
        N[sum(a[abs(l)-1]==(l>0) for l in c)]+=1
    return {'N':N,'E':N[0]+N[3],'D':N[3]-N[0]}

def exact_equity(n,F):
    Q=[0]*len(F);sat=0;checks=0
    for bits in itertools.product((False,True),repeat=n):
        vals=[clause_truth(c,bits) for c in F];checks+=sum(map(len,F))
        miss=[j for j,ok in enumerate(vals) if not ok]
        if not miss:sat+=1
        elif len(miss)==1:Q[miss[0]]+=1
    return Q,sat,checks

def contextual_equity(n,F,p):
    """Exact conditional Q_j with a fixed partial assignment, diagnostic only."""
    Q=[0]*len(F);checked=0
    for a in itertools.product((False,True),repeat=n):
        if any(p[i]>=0 and a[i]!=bool(p[i]) for i in range(n)):
            continue
        valid=[clause_truth(c,a) for c in F];checked+=1
        bad=[j for j,t in enumerate(valid) if not t]
        if len(bad)==1:Q[bad[0]]+=1
    return Q,checked

def union_cubes(n,pairs):
    raw=sum(2**(-p['width']) for p in pairs)
    rs=unique_clauses(pairs)
    count=0;pairwise=0
    for b in itertools.product((False,True),repeat=n):
        fails=sum(not clause_truth(r,b) for r in rs)
        count+=bool(fails)
        pairwise+=fails*(fails-1)//2
    return {'raw_pair_weight':raw,'unique_resolvents':len(rs),
            'union_fraction':count/(2**n),'union_count':count,
            'overlap_pair_intersection_count':pairwise,
            'duplicate_excess':len(pairs)-len(rs)}

@dataclass
class Meter:
    scans:int=0
    up_rounds:int=0
    propagated:int=0
    nodes:int=0
    branches:int=0
    failed_routes:int=0
    heuristic_reads:int=0
    memo_reads:int=0
    memo_hits:int=0
    memo_saved:int=0
    probes:int=0
    trial_inspections:int=0
    discovery:int=0
    source_parse:int=0
    peak_entries:int=0

def up(n, F, assn, meter):
    a=list(assn)
    while True:
        new=False; meter.up_rounds+=1
        for c in F:
            unknown=0;last=0;sat=False
            for lit in c:
                meter.scans+=1
                s=lit_status(lit,a)
                if s=='true':sat=True;break
                if s=='unset':unknown+=1;last=lit
            if sat:continue
            if unknown==0:return tuple(a),True
            if unknown==1:
                v=abs(last)-1;z=int(last>0)
                if a[v]>=0 and a[v]!=z:return tuple(a),True
                if a[v]<0:a[v]=z;new=True;meter.propagated+=1
        if not new:return tuple(a),False

def score_branch(n,F,a,meter):
    degree=[0]*n;pos=[0]*n;neg=[0]*n
    for c in F:
        full=False
        for lit in c:
            meter.heuristic_reads+=1
            if lit_status(lit,a)=='true':full=True;break
        if full:continue
        for lit in c:
            meter.heuristic_reads+=1
            if a[abs(lit)-1]<0:
                degree[abs(lit)-1]+=1
                (pos if lit>0 else neg)[abs(lit)-1]+=1
    choices=[i for i in range(n) if a[i]<0]
    if not choices:return None,None
    v=min(choices,key=lambda i:(-degree[i],i))
    return v, int(pos[v]>=neg[v])

def solve(n,source,policy):
    meter=Meter()
    tracemalloc.start()
    begin=time.perf_counter_ns()
    F=tuple(tuple(c) for c in source)
    meter.source_parse=sum(map(len,F))
    ck=check_source(n,F)
    meter.source_parse+=len(F)+n
    extras=()
    pair_stats={'candidate':0,'merge_pairs':0,'nonmerge_pairs':0,'taut':0,'added':0}
    if policy in ('full','merge','budget'):
        pairs,taut,scan=resolvents(n,F)
        meter.discovery+=scan+sum(1 for _ in pairs)
        if policy=='full':extras=unique_clauses(pairs)
        elif policy=='merge':extras=unique_clauses(pairs,True)
        else:extras=unique_clauses(pairs,True,max_width=3,budget=max(2,n))
        pair_stats={'candidate':len(pairs),'merge_pairs':sum(p['merge'] for p in pairs),
                    'nonmerge_pairs':sum(not p['merge'] for p in pairs),
                    'taut':taut,'added':len(extras)}
    FF=F+extras
    memo=set()
    def dfs(initial):
        meter.nodes+=1;meter.peak_entries=max(meter.peak_entries,len(memo))
        a,bad=up(n,FF,initial,meter)
        if bad:meter.failed_routes+=1;return None
        meter.memo_reads+=len(a)
        if a in memo:
            meter.memo_hits+=1;return None
        # SAT check via the source only, counted as inspections.
        allsat=True
        for c in F:
            sat=False
            for lit in c:
                meter.scans+=1
                if lit_status(lit,a)=='true':sat=True;break
            if not sat:allsat=False;break
        if allsat:
            # Fill any unconstrained variables arbitrarily and check actual source.
            witness=tuple(bool(z) if z>=0 else False for z in a)
            assert truth(F,witness)
            return witness
        var,phase=score_branch(n,F,a,meter)
        assert var is not None
        if policy=='failed':
            # Every attempted lookahead branch is charged, even when it proves nothing.
            for v in sorted(range(n),key=lambda v: (0 if v==var else 1,v)):
                if a[v]>=0:continue
                t=list(a);t[v]=0;meter.probes+=1
                _,no0=up(n,FF,t,meter)
                t[v]=1;meter.probes+=1
                _,no1=up(n,FF,t,meter)
                if no0 and no1:meter.failed_routes+=1;return None
                if no0!=no1:
                    t=list(a);t[v]=int(no0)
                    meter.probes+=1
                    return dfs(tuple(t))
                break
        for z in (phase,1-phase):
            meter.branches+=1
            t=list(a);t[var]=z
            ans=dfs(tuple(t))
            if ans is not None:return ans
        memo.add(a);meter.memo_saved+=len(a)
        meter.peak_entries=max(meter.peak_entries,len(memo))
        return None
    witness=None
    if policy=='trial':
        positive=[0]*n;negative=[0]*n
        for c in F:
            for lit in c:
                meter.discovery+=1
                (positive if lit>0 else negative)[abs(lit)-1]+=1
        majority=tuple(positive[i]>=negative[i] for i in range(n))
        trials=[tuple(False for _ in range(n)),tuple(True for _ in range(n)),majority,tuple(not x for x in majority)]
        seen=set()
        for t in trials:
            if t in seen:continue
            seen.add(t)
            meter.trial_inspections+=sum(map(len,F))
            if truth(F,t):witness=t;break
    if witness is None:witness=dfs(tuple(-1 for _ in range(n)))
    elapsed=time.perf_counter_ns()-begin
    current,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
    return {'sat':witness is not None,'witness':list(map(int,witness)) if witness is not None else None,
            'elapsed_ns':elapsed,'python_peak_bytes':peak,
            'meter':meter.__dict__,'total_primitive_work':sum(v for k,v in meter.__dict__.items() if k not in ('peak_entries','nodes')),
            'pair_stats':pair_stats,'clauses_in_memory':len(FF),'added_literal_fields':sum(map(len,extras)),
            'source_checksum':hashlib.sha256(repr(F).encode()).hexdigest()[:16],
            'source_connected':ck['connected'],'source_exact22':ck['exact22']}

def verify_up_equivalence(n,F,full=False):
    pairs,taut,_=resolvents(n,F)
    N=unique_clauses(pairs,False)
    M=unique_clauses(pairs,True)
    checks=0;gain=0
    for p in itertools.product((-1,0,1),repeat=n):
        c1=up(n,F,p,Meter());c2=up(n,F+N,p,Meter());c3=up(n,F+M,p,Meter());c4=up(n,F+M+N,p,Meter())
        def eq(a,b):return (a[1] and b[1]) or (not a[1] and not b[1] and a[0]==b[0])
        if not eq(c1,c2):raise AssertionError(('nonmerge',F,p,c1,c2))
        if not eq(c3,c4):raise AssertionError(('full vs merge',F,p,c3,c4))
        gain+=not eq(c1,c3);checks+=1
    return {'partial_states':checks,'strict_gain_states':gain,'nonmerge_clauses':len(N),'merge_clauses':len(M)}

def small_tests():
    count=0
    for n,F in instances().values():
        if n>7:continue
        for a in itertools.product((False,True),repeat=n):
            if all(len(c)==3 for c in F):
                p=profile(F,a);q=profile(F,tuple(not x for x in a))
                assert p['N'][::-1]==q['N'] and p['E']==q['E'] and p['D']==-q['D']
                count+=1
            for c in F:
                for lit in c:
                    assert lit_status(lit,a)==lit_status(-lit,tuple(not x for x in a))
                    count+=1
    return count

def run():
    d=instances();out={'seed':SEED,'model':'one fixed deterministic Python indexed-array interpreter; no native TM exponent asserted',
                       'known_prior':'Non-merge resolution is non-empowering (Gwynne-Kullmann/propagation-completeness literature); project issue #2 prior first handoff',
                       'instances':{},'up_exhaustive':{},'checks':0}
    out['checks']+=small_tests()
    for key,(n,F) in d.items():
        ck=check_source(n,F)
        pairs,taut,scan=resolvents(n,F)
        if n<=15:
            Q,sat,inspect=exact_equity(n,F)
        else:raise ValueError('limit')
        cube=union_cubes(n,pairs) if n<=14 else None
        if n<=5 or key in ('cyclic6_strict22_sat','xor3_strict22_sat'):
            audit=verify_up_equivalence(n,F)
            out['up_exhaustive'][key]=audit
            out['checks']+=audit['partial_states']*2
        else:audit=None
        runs={}
        for policy in ('base','full','merge','budget','failed','trial'):
            runs[policy]=solve(n,F,policy)
            assert runs[policy]['sat']==bool(sat),(key,policy,sat)
            assert runs[policy]['witness'] is None or truth(F,tuple(map(bool,runs[policy]['witness'])))
        # Clause-level equity is computed by exhaustive enumeration, never used as free heuristic.
        weight_clause=[0.0]*len(F);weight_variable=[0.0]*n;weight_occurrence={}
        for p in pairs:
            weight=2.0**(-p['width'])
            weight_clause[p['j']]+=weight
            weight_clause[p['k']]+=weight
            weight_variable[p['pivot']-1]+=weight
            for j in (p['j'],p['k']):
                tag=f'x_{{{p["pivot"]},{j}}}'
                weight_occurrence[tag]=weight_occurrence.get(tag,0)+weight
        prof=None;occs=None
        if all(len(c)==3 for c in F):
            a=tuple(False for _ in range(n));pa=tuple((-1 if i%2 else 0) for i in range(n))
            prof={'zero':profile(F,a),'zero_complement':profile(F,tuple(not z for z in a))}
            occs=occurrences(F,a,pa)[:min(15,ck['occurrences'])]
        context=None
        if key=='shared_overlap':
            qcond,total=contextual_equity(n,F,(-1,-1,0,0))
            m1=Meter();m2=Meter()
            before=up(n,F,(-1,-1,0,0),m1)
            after=up(n,F+unique_clauses(pairs,True),(-1,-1,0,0),m2)
            context={'partial':[-1,-1,0,0],'Q_conditional':qcond,'compatible_full_assignments':total,
                     'UP_without':before,'UP_with':after,'Phi_unset_before':sum(x<0 for x in before[0]),
                     'Phi_unset_after':sum(x<0 for x in after[0]),
                     'acquisition_inspections':scan,'source_UP_scans':m1.scans,
                     'augmented_UP_scans':m2.scans}
            assert not before[1] and not after[1] and context['Phi_unset_before']-context['Phi_unset_after']==1
        out['instances'][key]={
            'contextual_example':context,'n':n,'m':len(F),'classification':ck,'source_sha256':hashlib.sha256(repr(F).encode()).hexdigest(),
            'SAT':bool(sat),'exact_solution_count':sat,'Q_j':Q,'Q_j_sum':sum(Q),
            'Q_j_positive_count':sum(q>0 for q in Q),'equity_inspections':inspect,
            'pair_candidates':len(pairs),'tautological_candidates':taut,
            'merge_candidates':sum(p['merge'] for p in pairs),'nonmerge_candidates':sum(not p['merge'] for p in pairs),
            'pair_sign_illustration':pairs[:min(5,len(pairs))],
            'cube':cube,'per_clause_opposition_weight':weight_clause,
            'per_variable_opposition_weight':weight_variable,
            'per_occurrence_opposition_weight':weight_occurrence,
            'profiles':prof,'occurrence_control':occs,'UP_audit':audit,'runs':runs}
        out['checks']+=2**n
    out['formal_controls']={
        'repeated_overlap':'for k>=2, Q_j=0 for every source clause, k resolvents all equal (a or b), exact union density=1/4, raw pair weight=k/4',
        'nonmerge':'every non-merge parent resolvent is UP-redundant under every partial prefix, even with other clauses',
        'shared':'a merge can strictly strengthen UP: (x or a or u) and (not x or a or v), with u=v=false'
    }
    p=pathlib.Path(__file__).resolve().parent/'2026-10-29_2116_LSPV-2_MERGE_FILTER239_raw.json'
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    summary={'instances':len(d),'checks':out['checks'],
             'run_aggregates':{policy:{'nodes':sum(x['runs'][policy]['meter']['nodes'] for x in out['instances'].values()),
                                        'primitive_work':sum(x['runs'][policy]['total_primitive_work'] for x in out['instances'].values()),
                                        'elapsed_ns':sum(x['runs'][policy]['elapsed_ns'] for x in out['instances'].values())}
                               for policy in ('base','full','merge','budget','failed','trial')},
             'hard_control':{key:{'Q':out['instances'][key]['Q_j_sum'],'cube':out['instances'][key]['cube'],
                                     'merge':out['instances'][key]['merge_candidates']}
                             for key in d if 'replicated_overlap_' in key},
             'up_exhaustive':out['up_exhaustive']}
    (p.parent/'2026-10-29_2116_LSPV-2_MERGE_FILTER239_summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,indent=2))

if __name__=='__main__':run()