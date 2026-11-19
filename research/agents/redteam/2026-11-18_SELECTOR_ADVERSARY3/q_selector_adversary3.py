#!/usr/bin/env python3
"""Exact-one T5 selector adversary; deterministic targeted audit."""
from itertools import combinations, permutations, product
import json

W=({1,3},{2,4},{0,3},{1,4},{0,2})
def q(h,u,v): return (u in W[h]) != (v in W[h])
def p(h,u,v): return (u in W[h]) and (v in W[h])

edges=list(combinations(range(6),2))
clauses=[(6+i,u,v) for i,(u,v) in enumerate(edges)]

def lift(colors, relation=q):
    ans=list(colors)
    for u,v in edges:
        hs=[h for h in range(5) if relation(h,colors[u],colors[v])]
        ans.append(hs[0] if hs else None)
    return ans

def verify(values, omitted=None, relation=q):
    checks=0
    for i,(h,u,v) in enumerate(clauses):
        if i==omitted: continue
        checks+=1
        if values[h] is None or not relation(values[h],values[u],values[v]): return False,checks
    return True,checks

def weighted_count(relation):
    total=proper=tail_rows=edge_weight_ops=0
    for c in product(range(5),repeat=6):
        tail_rows+=1; prod=1
        for u,v in edges:
            w=sum(relation(h,c[u],c[v]) for h in range(5)); edge_weight_ops+=5
            prod*=w
        total+=prod
        proper+=all(c[u]!=c[v] for u,v in edges)
    return {'tail_rows':tail_rows,'head_support_tests':edge_weight_ops,
            'proper_tail_colorings':proper,'full_witness_count':total}

def gac(domains):
    domains=[set(x) for x in domains]; tuple_tests=scans=deletions=0
    changed=True
    while changed:
        changed=False
        for c in clauses:
            scans+=1
            for pos,var in enumerate(c):
                for val in list(domains[var]):
                    ok=False
                    others=[range(5) if j==pos else domains[c[j]] for j in range(3)]
                    for vals in product(*others):
                        tuple_tests+=1
                        t=list(vals); t[pos]=val
                        if q(*t): ok=True; break
                    if not ok:
                        domains[var].remove(val); deletions+=1; changed=True
                        if not domains[var]: return domains,{'scans':scans,'tuple_tests':tuple_tests,'deletions':deletions,'wipeout':True}
    return domains,{'scans':scans,'tuple_tests':tuple_tests,'deletions':deletions,'wipeout':False}

def strong_tail_consistency():
    levels=[]; tests=0
    # strong k: every proper assignment on k-1 selected vertices extends to every kth vertex.
    for k in range(1,7):
        bad=None; cases=0
        for assigned in combinations(range(6),k-1):
            for vals in permutations(range(5),k-1):
                a=dict(zip(assigned,vals))
                for target in range(6):
                    if target in a: continue
                    cases+=1
                    allowed=[]
                    for color in range(5):
                        tests+=1
                        if all(color!=a[v] for v in a): allowed.append(color)
                    if not allowed and bad is None: bad={'assigned':a,'target':target}
        levels.append({'k':k,'cases':cases,'holds':bad is None,'first_failure':bad})
    return levels,tests

def probe_gac(max_pins=4):
    out=[]; totals={'scans':0,'tuple_tests':0,'deletions':0,'wipeouts':0,'cases':0}
    for r in range(max_pins+1):
        row={'pins':r,'cases':0,'wipeouts':0,'scans':0,'tuple_tests':0,'deletions':0}
        for vertices in combinations(range(6),r):
            for vals in permutations(range(5),r):
                d=[set(range(5)) for _ in range(21)]
                for v,x in zip(vertices,vals): d[v]={x}
                _,s=gac(d); row['cases']+=1
                for key in ('scans','tuple_tests','deletions'): row[key]+=s[key]
                row['wipeouts']+=s['wipeout']
        out.append(row)
        for key in totals: totals[key]+=row.get(key,0)
    return out,totals

def deletion_witnesses():
    records=[]; checks=0
    for omit,(u,v) in enumerate(edges):
        c=[None]*6; c[u]=c[v]=0
        for color,x in enumerate([x for x in range(6) if x not in (u,v)],1): c[x]=color
        values=lift(c); ok,n=verify(values,omit); checks+=n
        values[6+omit]=0
        assert ok and not q(values[6+omit],values[u],values[v])
        records.append({'omitted':omit,'edge':[u,v],'tail_colors':c,'values':values})
    return records,checks

def guarded_layout(h):
    R=1<<h; rows=[]; guard_bits=0; residual_checks=0
    for a in range(R):
        selected=(3*a+1)%R
        active=[]
        for source_row in range(R):
            # g_source(row) is false exactly at its source row.
            mismatch=(a^source_row)!=0; guard_bits+=h
            if not mismatch: active.append((3*source_row+1)%R)
        assert active==[selected]
        residual_checks+=len(clauses)
        rows.append({'row':a,'selected':selected,'active_blocks':active})
    holes=[]
    for deleted in range(R):
        good=[]
        for a in range(R):
            residual_checks+=1
            if (3*a+1)%R==deleted: good.append(a)
        assert good==[((pow(3,-1,R)*(deleted-1))%R)] if R>2 else good==[((deleted-1)%R)]
        holes.append({'deleted_block':deleted,'sat_rows':good})
    # Direct one-hot CNF: 21*(1 positive + C(5,2) negative) + 15*(125-60) Q forbidders.
    base_clauses=21*11+15*65
    return {'h':h,'rows':R,'blocks':R,'selector':'(3a+1) mod 2^h','row_records':rows,
            'one_hole_records':holes,'guard_bit_evaluations':guard_bits,
            'residual_semantic_checks':residual_checks,'private_boolean_variables':R*21*5,
            'guarded_CNF_clauses':R*base_clauses,'literals_per_guarded_clause_addend':h,
            'base_CNF_clauses_per_block':base_clauses}

assert sum(q(*x) for x in product(range(5),repeat=3))==60
assert sum(p(*x) for x in product(range(5),repeat=3))==20
assert not any(q(*x) and p(*x) for x in product(range(5),repeat=3))

qcount=weighted_count(q); pcount=weighted_count(p)
assert qcount['full_witness_count']==0 and pcount['full_witness_count']>0
full_domains=[set(range(5)) for _ in range(21)]
_,gac_full=gac(full_domains); assert not gac_full['wipeout'] and gac_full['deletions']==0
levels,strong_tests=strong_tail_consistency(); assert all(x['holds'] for x in levels[:5]) and not levels[5]['holds']
probes,probe_totals=probe_gac(); assert all(x['wipeouts']==0 for x in probes[:4]) and probes[4]['wipeouts']>0
witnesses,witness_checks=deletion_witnesses()

core=[(0,1,2),(0,1,3),(1,0,2),(1,2,3),(2,0,3)]
core_counts={}
for rel,name in [(q,'Q'),(p,'P')]:
    exact=0; checks=0
    for a in product(range(5),repeat=4):
        ok=True
        for c in core:
            checks+=1
            if not rel(*(a[v] for v in c)): ok=False; break
        exact+=ok
    core_counts[name]={'solutions':exact,'predicate_checks':checks}
assert core_counts['Q']['solutions']==0

result={'status':'PASS','seed':None,'relation_counts':{'Q':60,'P':20,'overlap':0},
 'matched_K6':{'scopes':clauses,'Q':qcount,'P':pcount},
 'native_GAC_full':gac_full,'tail_strong_consistency':levels,'tail_extension_tests':strong_tests,
 'proper_tail_pins_then_native_GAC':probes,'probe_totals':probe_totals,
 'K6_deletion_witnesses':witnesses,'deletion_clause_checks':witness_checks,
 'per_head_parity':'15 single-edge head graphs; all bipartite',
 'matched_five_clause_core':core_counts,'guarded_selector_layouts':[guarded_layout(2),guarded_layout(3)],
 'space_metrics':{
  'audit':'Python process RAM not measured; raw JSON retains witnesses and layout records.',
  'native_GAC':'sum of 21 domain bitsets plus work for one 5^3 clause support scan; script retains Python sets.',
  'source_aware_selector':'h-bit row counter + block/source indices + one current block; streamed selector output excluded from writable space.',
  'one_hot_CNF':'105 Boolean private variables and 1206 base clauses per active K6 block before h-literal guards.'},
 'counter_metric':'relation/support tests, clause checks and guard-bit evaluations; not native machine instructions'}
print(json.dumps(result,indent=2))
