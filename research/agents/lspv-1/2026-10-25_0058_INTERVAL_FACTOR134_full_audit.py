#!/usr/bin/env python3
"""INTERVAL-FACTOR134: independent finite verification of the degree-two
signed cardinality-CSP -> (g,f)-factor equivalence.
No FLMV machine measurements, SAT time lower bounds, or polynomial factor solver are claimed.
Standard library only; deterministic RNG seed.
"""
import itertools, json, random
from collections import defaultdict, Counter
from pathlib import Path

RUN = 'INTERVAL-FACTOR134'
SEED = 202610240858
rng = random.Random(SEED)
check_count = 0
cases = 0
case_types = Counter()
labels = Counter()

def check(cond, msg):
    global check_count
    check_count += 1
    if not cond:
        raise AssertionError(msg)

def source_sat(n, constraints):
    """constraints: [([(var,sign),...],lower,upper),...], sign=1 pos, -1 neg"""
    for bits in itertools.product((0, 1), repeat=n):
        if all(lo <= sum((bits[v] if sign == 1 else 1-bits[v]) for v,sign in cl) <= hi
               for cl,lo,hi in constraints):
            return True, bits
    return False, None

def build_factor(n, constraints):
    occ=defaultdict(list)
    for j,(lits,lo,hi) in enumerate(constraints):
        assert len({v for v,_ in lits}) == len(lits)
        assert 0 <= lo <= hi <= len(lits)
        for v,sign in lits:
            occ[v].append((j,sign))
    assert all(len(occ[v])<=2 for v in range(n))
    bounds={('c',j):(lo,hi) for j,(_,lo,hi) in enumerate(constraints)}
    edges=[]
    for v in range(n):
        os=occ[v]
        if len(os)==0: continue
        if len(os)==1:
            j,_=os[0]; leaf=('l',v); bounds[leaf]=(0,1)
            edges.append((('c',j),leaf,v,0))
        else:
            (a,sa),(b,sb)=os
            assert a!=b
            if sa==sb:
                edges.append((('c',a),('c',b),v,0))
            else:
                choice=('s',v);bounds[choice]=(1,1)
                edges.extend([(('c',a),choice,v,0),(('c',b),choice,v,1)])
    return bounds,edges

def factor_sat(bounds, edges):
    nodes=list(bounds)
    ns={v:i for i,v in enumerate(nodes)}
    for subset in range(1<<len(edges)):
        deg=[0]*len(nodes)
        for e,(a,b,v,selector) in enumerate(edges):
            if (subset>>e)&1:
                deg[ns[a]]+=1;deg[ns[b]]+=1
        if all(lo<=deg[ns[k]]<=hi for k,(lo,hi) in bounds.items()):
            return True,subset
    return False,None

def validate_factor_assignment(bounds,edges,mask):
    degrees=Counter()
    for j,(a,b,_,_) in enumerate(edges):
        if (mask>>j)&1:
            degrees[a]+=1;degrees[b]+=1
    return all(lo<=degrees[node]<=hi for node,(lo,hi) in bounds.items())

def validate_source_assignment(constraints,bits):
    return all(lo<=sum((bits[v] if sign==1 else 1-bits[v]) for v,sign in lits)<=hi
               for lits,lo,hi in constraints)

def one_case(n,constraints,kind):
    global cases
    counts=Counter(v for lits,_,_ in constraints for v,_ in lits)
    if max(counts.values(), default=0)>2: return False
    x,src_witness=source_sat(n,constraints)
    bounds,edges=build_factor(n,constraints)
    y,factor_witness=factor_sat(bounds,edges)
    check(x==y, f'factor mismatch n={n}: {constraints}')
    check(factor_witness is None or validate_factor_assignment(bounds,edges,factor_witness),
          'returned factor is invalid')
    if x:
        check(validate_source_assignment(constraints,src_witness), 'source witness invalid')
        os=defaultdict(list)
        for j,(lits,_,_) in enumerate(constraints):
            for v,s in lits:os[v].append((j,s))
        recovered=[0]*n
        for v in range(n):
            occ=os[v]
            if not occ:continue
            selected=[(a,b) for idx,(a,b,e,_) in enumerate(edges)
                      if e==v and (factor_witness>>idx)&1]
            if len(occ)==2 and occ[0][1]!=occ[1][1]:
                check(len(selected)==1,'mixed polarity must pick one occurrence')
                j=next(j for j,s in occ if ('c',j) in selected[0])
                sg=next(s for jj,s in occ if jj==j)
                recovered[v]=1 if sg==1 else 0
            else:
                sg=occ[0][1]
                picked=bool(selected)
                recovered[v]=int(picked) if sg==1 else int(not picked)
        check(validate_source_assignment(constraints,recovered),
              f'reconstructed source assignment invalid {constraints}')
        source_mask=0
        for idx,(a,b,v,_) in enumerate(edges):
            for clause in (a,b):
                if clause[0]!='c':continue
                sign=next(s for w,s in constraints[clause[1]][0] if w==v)
                if (src_witness[v] if sign==1 else 1-src_witness[v]):
                    source_mask|=1<<idx
                    break
        check(validate_factor_assignment(bounds,edges,source_mask),
              'source to factor mapping invalid')
    cases+=1;case_types[kind]+=1;labels['SAT' if x else 'UNSAT']+=1
    return True

pairs=list(itertools.combinations(range(4),2))
vars_by_clause=[[pairs.index(p) for p in pairs if i in p] for i in range(4)]
base=[([(v,1) for v in vars_by_clause[i]],1,1) for i in range(4)]
check(source_sat(6,base)[0], 'K4 exact-one positive should be SAT')
check(one_case(6,base,'k4_exact_one_sat'), 'K4 factor check')

wrong=[(list(lits),lo,hi) for lits,lo,hi in base]
wrong[1][0][0] = (wrong[1][0][0][0],-1)
check(not source_sat(6,wrong)[0], 'one orientation flip exact-one should be UNSAT')
check(one_case(6,wrong,'k4_exact_one_unsat'), 'K4 flipped factor check')

base2=[(lits,2,2) for lits,_,_ in base]
wrong2=[(lits,2,2) for lits,_,_ in wrong]
check(source_sat(6,base2)[0], 'K4 exact-two positive should be SAT')
check(not source_sat(6,wrong2)[0], 'K4 exact-two mixed should be UNSAT')
check(one_case(6,base2,'k4_exact_two_sat'), 'K4 exact2 pos factor')
check(one_case(6,wrong2,'k4_exact_two_unsat'), 'K4 exact2 neg factor')

for signbits in itertools.product((-1,1),repeat=12):
    cls=[];k=0
    for j in range(4):
        cs=[]
        for v in vars_by_clause[j]:cs.append((v,signbits[k]));k+=1
        cls.append((cs,1,1))
    mixed=0
    for v in range(6):
        signs=[s for lits,_,_ in cls for x,s in lits if x==v]
        if signs[0]!=signs[1]:mixed+=1
    possible=(mixed%2 == 4%2)
    sat,_=source_sat(6,cls)
    check(possible or not sat,'parity obstruction failed')
    if sum(1 for b in signbits if b==-1)%4 == 0:
        one_case(6,cls,'k4_exhaustive_signs')

for n in range(1,6):
    for trial in range(275):
        m=rng.randint(1,5)
        uses=[0]*n
        clauses=[]
        for j in range(m):
            available=[v for v in range(n) if uses[v]<2]
            if not available: break
            count=rng.randint(1,min(3,len(available)))
            ids=rng.sample(available,count)
            lits=[(v,rng.choice((-1,1))) for v in ids]
            for v in ids:uses[v]+=1
            low=rng.randint(0,count)
            high=rng.randint(low,count)
            clauses.append((lits,low,high))
        one_case(n,clauses,'random_cardinality')

for signs in itertools.product((-1,1),repeat=6):
    for r1 in range(4):
        for r2 in range(4):
            cls=[([(v,signs[v]) for v in range(3)],r1,r1),
                 ([(v,signs[v+3]) for v in range(3)],r2,r2)]
            one_case(3,cls,'exhaustive_two_clause_exact')

summary={'run':RUN,'seed':SEED,'status':'COMPUTATIONAL restricted equivalence; ARC-EDGE-90 OPEN; P versus NP OPEN',
         'cases':cases,'assertions':check_count,'types':dict(sorted(case_types.items())),
         'labels':dict(labels),'k4_pairs':{'exact_one':{'SAT':True,'UNSAT':True},'exact_two':{'SAT':True,'UNSAT':True}},
         'factor_algorithm':'independent exhaustive edge subset verifier only, not polytime f-factor implementation',
         'machine_measurement':'none'}
path=Path(__file__).with_name('interval_factor134_results.json')
path.write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
print(json.dumps(summary,indent=2))
