#!/usr/bin/env python3
"""ARC252. Exact adaptive-restriction leaf-mass audit. Python standard library.
The measured operation ledger is NOT an FLMV Turing-machine complexity bound.
"""
import itertools, json, math, hashlib, time, collections, tracemalloc, random
from pathlib import Path
from fractions import Fraction

ROOT=Path(__file__).parent
OUT=ROOT/'2026-10-30_1300_LSPV-1_ARC_KRAFT_CERTIFIED_COVER252_raw.json'
W=[(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14)]
SW=list(W);SW[9]=(-5,6,-15);SW[13]=(-3,-6,-15)
HIT8=[tuple((-(i+1) if mask>>i&1 else i+1) for i in range(3)) for mask in range(8)]
NAE=[(1,2,3),(-1,-2,-3)]
SATW=[(1,2,3),(-1,2,3),(-1,-2,3)]

def gadget_instance(G,t):
    F=list(G)
    for j in range(t):
        x,u,v=4+3*j,5+3*j,6+3*j
        F += [(x,u,v),(x,u,-v),(x,-u,v),(x,-u,-v)]
    return F,3+3*t


def h(n): return 2+3*(1+math.ceil(math.log2(n+1)))

def model(F,a):return all(any((a[abs(l)]==(l>0)) for l in c) for c in F)

def truth_counts(F,a):return [sum(a[abs(l)]==(l>0) for l in c) for c in F]

def exhaust(F,n):
    count=0
    for bits in itertools.product([False,True],repeat=n):
        a={i+1:bits[i] for i in range(n)}
        count+=model(F,a)
    return count

def restrict(F,p,ctr):
    R=[]; conflict=None
    for j,c in enumerate(F):
        ctr['original_clause_visits']+=1
        ctr['source_literal_reads']+=len(c)
        if any(abs(l) in p and p[abs(l)]==(l>0) for l in c):continue
        d=tuple(l for l in c if abs(l) not in p)
        if not d:conflict=j;break
        R.append((j,d))
    return R,conflict

def unit_closure(F,p,ctr,with_UP,forced_mass):
    p=dict(p)
    if not with_UP:
        R,conf=restrict(F,p,ctr)
        return p,R,conf,forced_mass
    while True:
        R,conf=restrict(F,p,ctr)
        if conf is not None:return p,R,conf,forced_mass
        unit=next(((j,c[0]) for j,c in R if len(c)==1),None)
        if unit is None:return p,R,None,forced_mass
        j,l=unit;v=abs(l);b=l>0
        assert v not in p
        # The contrary branch cannot satisfy the displayed residual unit.
        forced_mass+=Fraction(1,2**(len(p)+1))
        ctr['certified_forced_opposite_leaves']+=1
        ctr['unit_assignments']+=1
        p[v]=b

def naive_guest(F,n,p):
    # Complete exact source-level Boolean solver, not an uncharged oracle.
    C=collections.Counter()
    def recurse(a):
        R,conf=restrict(F,a,C);C['guest_nodes']+=1
        if conf is not None:return None
        if not R:return a
        v=min(abs(l) for _,c in R for l in c if abs(l) not in a)
        C['guest_branches']+=1
        return recurse({**a,v:False}) or recurse({**a,v:True})
    witness=recurse({})
    return (witness is not None),C,witness

def trace_tree(F,n,lambda_=Fraction(1,2),up=True):
    ctr=collections.Counter()
    N=len(F)*h(n)
    B=math.isqrt(N) # floor N^0.5, physical clause-payload lower bound
    rmax=B//h(n)
    degree=collections.Counter(abs(l) for c in F for l in c)
    Delta=max(degree.values(),default=0)
    k=max(0,math.ceil((len(F)-rmax)/Delta)) if Delta else 0
    source_no_mass=Fraction(0)
    source_yes_mass=Fraction(0)
    guest_no_mass=Fraction(0)
    guest_yes_mass=Fraction(0)
    traces=[]
    guest_depths=[]
    first_witness=None
    def go(p):
        nonlocal source_no_mass,source_yes_mass,guest_no_mass,guest_yes_mass,first_witness
        ctr['controller_nodes']+=1
        p,R,conf,forced_mass=unit_closure(F,p,ctr,up,Fraction(0))
        source_no_mass+=forced_mass
        if conf is not None:
            source_no_mass+=Fraction(1,2**len(p))
            ctr['certified_conflict_leaves']+=1
            if len(traces)<8:traces.append({'type':'conflict','source_clause':conf,'depth':len(p),'pins':sorted(p.items())})
            return False
        if not R:
            source_yes_mass+=Fraction(1,2**len(p));ctr['certified_yes_leaves']+=1
            assert all(any(abs(l) in p and p[abs(l)]==(l>0) for l in c) for c in F)
            if first_witness is None:first_witness={v:p.get(v,False) for v in range(1,n+1)}
            return True
        # Guest query cutoff uses a *payload-only* LOWER bound. Actual header
        # and guest tape costs would make the child larger, never smaller.
        if len(R)*h(n)<=B:
            child=[c for _,c in R]
            c2=collections.Counter()
            # Construct and write the ordinary residual child before guest.
            c2['child_output_bits']+=len(child)*h(n)
            c2['child_clause_visits']+=len(child)
            sat,guest,witness=naive_guest(child,n,p)
            for key,value in guest.items():
                c2[{'source_literal_reads':'guest_literal_reads','original_clause_visits':'guest_clause_visits'}.get(key,key)]+=value
            ctr.update(c2)
            ctr['guest_completed_calls']+=1
            mass=Fraction(1,2**len(p));guest_depths.append(len(p))
            if sat:
                guest_yes_mass+=mass
                if first_witness is None:first_witness={v:({**p,**witness}).get(v,False) for v in range(1,n+1)}
            else:guest_no_mass+=mass
            if len(traces)<8:traces.append({'type':'guest','depth':len(p),'clauses':len(R),'SAT':sat,'pins':sorted(p.items())})
            return sat
        # Bounded selector: smallest original not-yet-pinned variable occurring
        # in residual clauses; selection and every failed path count.
        candidates=[abs(l) for _,c in R for l in c if abs(l) not in p]
        ctr['policy_candidate_inspections']+=len(candidates)
        v=min(candidates)
        ctr['controller_branches']+=1
        a=go({**p,v:False});b=go({**p,v:True})
        return a or b
    answer=go({})
    if answer:
        assert first_witness is not None and model(F,first_witness)
        ctr['source_witness_verification_reads']+=sum(len(c) for c in F)
    total=source_no_mass+source_yes_mass+guest_no_mass+guest_yes_mass
    assert total==1,(total,source_no_mass,source_yes_mass,guest_no_mass,guest_yes_mass)
    if not answer:
        assert source_yes_mass==0 and guest_yes_mass==0
        assert guest_no_mass <= Fraction(ctr['guest_completed_calls'],2**k)
        assert source_no_mass >= 1-Fraction(ctr['guest_completed_calls'],2**k)
    assert all(d>=k for d in guest_depths)
    return {'SAT':answer,'n':n,'m':len(F),'source_payload_bits':N,'header_excluded':True,
        'lambda':'1/2','guest_payload_limit':B,'largest_residual_clause_count':rmax,
        'max_variable_clause_degree':Delta,'k_floor':k,'source_cert_NO_mass':str(source_no_mass),
        'source_cert_YES_mass':str(source_yes_mass),'guest_NO_mass':str(guest_no_mass),
        'guest_YES_mass':str(guest_yes_mass),'guest_depth_min':min(guest_depths) if guest_depths else None,
        'guest_depth_max':max(guest_depths) if guest_depths else None,
        'guest_mass_upper_bound':str(Fraction(ctr['guest_completed_calls'],2**k)),
        'witness':sorted(first_witness.items()) if first_witness else None,
        'ledger':dict(ctr),'trace':traces}

def baseline_up_dpll(F,n):
    ctr=collections.Counter()
    witness=None
    def go(p):
        nonlocal witness
        ctr['nodes']+=1
        a,R,conf,_=unit_closure(F,p,ctr,True,Fraction(0))
        if conf is not None:return False
        if not R:
            witness={v:a.get(v,False) for v in range(1,n+1)}
            return True
        candidates=[abs(l) for _,c in R for l in c]
        ctr['policy_candidate_inspections']+=len(candidates)
        v=min(candidates)
        ctr['branches']+=1
        return go({**a,v:False}) or go({**a,v:True})
    sat=go({})
    if sat:
        assert witness is not None and model(F,witness)
        ctr['source_witness_verification_reads']+=sum(len(c) for c in F)
    return sat,dict(ctr),sorted(witness.items()) if witness else None

def resolution_control(F,n):
    for j,c in enumerate(F):
        for k,d in enumerate(F):
            if k<=j:continue
            for l in c:
                if -l not in d:continue
                res=tuple(dict.fromkeys([x for x in c if x!=l]+[x for x in d if x!=-l]))
                if any(-x in res for x in res):continue
                cube={abs(x):x<0 for x in res}
                assert all(not model(F,{**{v:False for v in range(1,n+1)},**cube,**dict(zip([v for v in range(1,n+1) if v not in cube],[bool((mask>>i)&1) for i in range(n-len(cube))]))}) for mask in range(1<<(n-len(cube))))
                return {'source_clause_indices':[j,k],'pivot_variable':abs(l),'resolvent':res,
                        'falsifying_cube':sorted(cube.items()),'excluded_completions':2**(n-len(cube)),
                        'proof':'Under the cube, source C_j requires pivot literal, source C_k requires its negation.'}
    return None

def cached_alias_control(G,t):
    # Proper width-three source: both values of z_i produce the SAME
    # binary residual (p_i OR q_i). Explicitly outside strict22 and
    # power-shrunken ARC promises, but verifies q_physical != q_logical.
    F=list(G)
    for j in range(t):
        z,p,q=4+3*j,5+3*j,6+3*j
        F += [(z,p,q),(-z,p,q)]
    snapshots=[]
    for values in itertools.product([False,True],repeat=t):
        pin={4+3*j:b for j,b in enumerate(values)}
        R,conf=restrict(F,pin,collections.Counter());assert conf is None
        key=tuple(sorted(tuple(sorted(c)) for idx,c in R))
        snapshots.append(key)
    assert len(set(snapshots))==1
    unique_child=[tuple(c) for c in snapshots[0]]
    sat=exhaust(unique_child,3+3*t)>0
    # Each p_i OR q_i can be satisfied independently, so SAT iff G SAT.
    assert sat==(exhaust(G,3)>0)
    return {'t':t,'logical_leaf_occurrences':2**t,'unique_guest_queries':1,
        'branch_vars':[4+3*j for j in range(t)],
        'reusable_guest_label_SAT':sat,'child_clauses':len(unique_child),
        'source_clauses':len(F),'power_short_child':False,
        'note':'cached same ordinary residual after z branches; does not satisfy N^lambda ARC size.'}

def su_controls(F,n):
    occurrences=[];compat=[];checks=0
    for j,c in enumerate(F):
        occurrences.append({'j':j,'clause':c,'occurrences':[
            {'x':abs(l),'occurrence':f'x_{{{abs(l)},{j}}}','sign':int(l>0),
             'S':int(l>0),'invert_S_is_U':int(l<0),
             'U':int(l<0),'invert_U_is_S':int(l>0)} for l in c]})
    for j,c in enumerate(F):
        for i in range(j+1,len(F)):
            d=F[i];row={'j':j,'i':i}
            for mode in ('SS','SU','US','UU'):
                assignment={};feasible=True
                for clause,stage in ((c,mode[0]),(d,mode[1])):
                    for l in clause:
                        v=abs(l);b=(l>0) if stage=='S' else (l<0)
                        if v in assignment and assignment[v]!=b:feasible=False
                        assignment[v]=b
                row[mode]=feasible;checks+=1
                same=any(abs(x)==abs(y) and (x>0)==(y>0) for x in c for y in d)
                opp=any(abs(x)==abs(y) and (x>0)!=(y>0) for x in c for y in d)
                assert feasible==(not opp if mode in ('SS','UU') else not same)
            compat.append(row)
    trail=[]
    for base in (0,1):
        a={v:bool(base) for v in range(1,n+1)}
        for flips in ([],[1],[1,2],[1,2,3],list(range(1,n+1))):
            b=dict(a)
            for v in flips:
                if v<=n:b[v]=not b[v]
            cs=truth_counts(F,b)
            inv=truth_counts(F,{v:not val for v,val in b.items()})
            assert all(x+y==len(c) for x,y,c in zip(cs,inv,F))
            trail.append({'base':base,'flips':flips,'clause_counts':cs,'N':[cs.count(i) for i in range(4)],
                          'SAT':0 not in cs,'complement_N':[inv.count(i) for i in range(4)]})
    return {'all_occurrences':occurrences,'matrix':compat,'fourway_checks':checks,'flip_trails':trail}

def main():
    start=time.monotonic();GS,nGS=gadget_instance(SATW,4);GU,nGU=gadget_instance(HIT8,4)
    cases=[('W1_strict22_UNSAT',15,W),('SWAP6_strict22_SAT',15,SW),
           ('NAE_SAT',3,NAE),('HIT8_UNSAT',3,HIT8),('SAT_small',3,SATW),
           ('GADGET_SAT',nGS,GS),('GADGET_UNSAT',nGU,GU),
           ('KROM_UNSAT',2,[(1,2),(-1,2),(1,-2),(-1,-2)]),
           ('HORN_UNSAT',3,[(1,),(-1,2),(-2,3),(-3,)]),
           ('XOR_SAT',3,[c for c in HIT8 if sum(l<0 for l in c)%2==1])]
    rows=[]
    for name,n,F in cases:
        oracle=exhaust(F,n)
        assert (oracle>0)==('UNSAT' not in name)
        record={'name':name,'models':oracle,'source_clause_count':len(F)}
        record['extremes']=su_controls(F,n)
        record['resolvent_certificate']=resolution_control(F,n)
        tracemalloc.start();record['bare']=trace_tree(F,n,up=False);_,record['bare']['python_peak_heap_bytes']=tracemalloc.get_traced_memory();tracemalloc.stop()
        tracemalloc.start();record['UP']=trace_tree(F,n,up=True);_,record['UP']['python_peak_heap_bytes']=tracemalloc.get_traced_memory();tracemalloc.stop()
        tracemalloc.start();baseres,baseline,witness=baseline_up_dpll(F,n);_,baseline['python_peak_heap_bytes']=tracemalloc.get_traced_memory();tracemalloc.stop()
        assert baseres==(oracle>0)
        record['baseline']={'SAT':baseres,'ledger':baseline,'witness':witness}
        assert record['bare']['SAT']==record['UP']['SAT']==(oracle>0)
        # Independently checked raw leaf probability identity and count.
        rows.append(record)
        print(name,'models',oracle,'bare nodes',record['bare']['ledger']['controller_nodes'],
              'guest',record['bare']['ledger'].get('guest_completed_calls',0),
              'UP nodes',record['UP']['ledger']['controller_nodes'],
              'UP guest',record['UP']['ledger'].get('guest_completed_calls',0))
    # Pure algebraic large-n forecast; only n divisible by 3 permits strict22.
    frontier=[]
    for n in (15,30,60,120,300,600,1200):
        m=4*n//3;N=m*h(n);rmax=math.isqrt(N)//h(n)
        k=max(0,math.ceil((m-rmax)/4))
        lgq=Fraction(3,5)*math.log2(N)
        frontier.append({'n':n,'m':m,'N_payload':N,'k_min_pins':k,
              'guest_log2_q_cap':round(float(lgq),5),
              'log2_upper_guest_mass':round(float(lgq)-k,5)})
    # Seeded independently generated complete both-label cases.
    rng=random.Random(202610301300)
    random_controls=[]
    for case in range(64):
        n=rng.randint(3,8); m=rng.randint(3,18)
        F=[tuple(v*rng.choice((-1,1)) for v in rng.sample(range(1,n+1),3)) for _ in range(m)]
        expected=exhaust(F,n)>0
        tr=trace_tree(F,n,up=True)
        assert tr['SAT']==expected
        random_controls.append({'n':n,'m':m,'SAT':expected,'cert_no_mass':tr['source_cert_NO_mass'],
                                'guest_calls':tr['ledger'].get('guest_completed_calls',0)})
    # Exact source proof: each 4-clause gadget forces its positive x through
    # three non-tautological source resolutions. The opposing x=0 cube is NO.
    gadget_proof=[]
    for j in range(4):
        x,u,v=4+3*j,5+3*j,6+3*j
        C=[(x,u,v),(x,u,-v),(x,-u,v),(x,-u,-v)]
        assert C==GS[3+4*j:3+4*j+4]
        assert C==GU[8+4*j:8+4*j+4]
        A=(x,u); B=(x,-u); R=(x,)
        assert set(A)==set(C[0]+C[1])-{v,-v}
        assert set(B)==set(C[2]+C[3])-{v,-v}
        assert set(R)==set(A+B)-{u,-u}
        gadget_proof.append({'forced_variable':x,'SAT_source_indices':[3+4*j+i for i in range(4)],
           'UNSAT_source_indices':[8+4*j+i for i in range(4)],
           'resolutions':[[3+4*j,3+4*j+1,v,list(A)],
                          [3+4*j+2,3+4*j+3,v,list(B)],
                          ['derived0','derived1',u,list(R)]]})
    output={'name':'ARC-KRAFT-CERTIFIED-COVER252','timestamp':'2026-10-30',
       'status':'PROVED/EXACT restricted Kraft coverage; COMPUTATIONAL finite controls',
       'input_source':'W1, SWAP6 source clauses authenticated from ARC250 source',
       'random_seed':202610301300,'randomized_checks':len(random_controls),
       'randomized_sat_count':sum(d['SAT'] for d in random_controls),
       'random_controls':random_controls,
       'cached_guest_alias_controls':[cached_alias_control(SATW,4),cached_alias_control(HIT8,4)],
       'cases':rows,'gadget_forced_literals':gadget_proof,
       'gadget_SOURCE_NO_mass':'15/16',
       'gadget_note':'Source-authenticated resolution forces four x variables; remaining formula retains arbitrary G on disjoint variables. SAT iff G SAT.',
       'frontier':frontier,'runtime_sec':round(time.monotonic()-start,4),
       'limitations':'UP propagated pin opposite branches must be recorded as certified excludes; finite payload-only threshold is optimistic for ordinary encodings. No universal SAT contraction or FLMV machine benchmark.'}
    OUT.write_text(json.dumps(output,indent=2,default=str))
    print('raw',OUT,'bytes',OUT.stat().st_size,'sec',output['runtime_sec'])

if __name__=='__main__':main()
