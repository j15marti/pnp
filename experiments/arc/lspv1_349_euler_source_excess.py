#!/usr/bin/env python3
"""Exact all-pruned binary-premise DAG excess identity, finite synthetic controls.
No solver or lower-bound search implied. Pure stdlib; deterministic exhaustive.
"""
import itertools,json,hashlib
from collections import Counter

def candidates(n):
    return [()] + [(i,) for i in range(n)] + list(itertools.combinations(range(n),2))

def check(m,choices):
    q=len(choices); ancestors=set(); stack=[m+q-1]; source=set()
    while stack:
        u=stack.pop()
        if u in ancestors:continue
        ancestors.add(u)
        if u<m: source.add(u)
        else: stack.extend(choices[u-m])
    if len(source)!=m or len(ancestors)!=m+q:return None
    E=sum(map(len,choices)); delta=sum(2-len(v) for v in choices)
    beta=E-(m+q-1)
    assert beta>=0 and delta>=0 and beta+delta==q-m+1
    return (delta,beta)

def enumerate_dags(m,q):
    counts=Counter(); tot=0
    for seq in itertools.product(*(candidates(m+i) for i in range(q))):
        t=check(m,seq)
        if t is None:continue
        counts[t]+=1;tot+=1
    return {"m":m,"q":q,"necessary_floor":m-1,"pruned_ancestry_dags":tot,
            "slack_classes": [{"delta":a,"beta":b,"count":c} for (a,b),c in sorted(counts.items())]}

def sat(formula,n):
    return [tuple((mask>>i)&1 for i in range(n)) for mask in range(1<<n)
            if all(any(((lit>0)==bool((mask>>(abs(lit)-1))&1)) for lit in clause) for clause in formula)]

def core_size(formula,n):
    return min((sum((mask>>i)&1 for i in range(len(formula))) for mask in range(1,1<<len(formula))
                if not sat([c for i,c in enumerate(formula) if (mask>>i)&1],n)),default=None)

G=[[-3,1,4],[-1,2],[1,3],[-4,-3],[-2,-1,3],[-2,4]]
controls=[]
for name,cnf,n in [("unit_unsat",[[1],[-1]],1),("unit_sat",[[1],[1]],1),("G342_unsat",G,4),("G342_sign_flip_sat",[[-3,-1,4]]+G[1:],4)]:
    models=sat(cnf,n)
    mu=core_size(cnf,n)
    controls.append({"name":name,"clauses":len(cnf),"variables":n,"model_count":len(models),"min_unsat_core":mu})
assert controls[0]['min_unsat_core']==2 and controls[1]['model_count']==1
assert controls[2]['model_count']==0 and controls[2]['min_unsat_core']==6
assert controls[3]['model_count']>0
assert all(sat(G[:i]+G[i+1:],4) for i in range(6))
assert all(sat(G[:i]+[G[i][:j]+[-lit]+G[i][j+1:]]+G[i+1:],4)
           for i in range(6) for j,lit in enumerate(G[i]))
results=[enumerate_dags(m,q) for m in (2,3) for q in range(m-1,m+2)]
for x in results:
    if x['q']==x['necessary_floor']:
        assert len(x['slack_classes'])==1 and x['slack_classes'][0]['delta']==0 and x['slack_classes'][0]['beta']==0
    if x['q']==x['necessary_floor']+1:
        assert all((v['delta'],v['beta']) in ((1,0),(0,1)) for v in x['slack_classes'])

def strict_dimacs(s):
    lines=s.splitlines();
    if not lines or not lines[0].startswith('p cnf '):return False
    bits=lines[0].split()
    if len(bits)!=4:return False
    try:n=int(bits[2]);m=int(bits[3])
    except ValueError:return False
    if n<1 or m<0 or len(lines)-1!=m:return False
    for line in lines[1:]:
        try:a=[int(x) for x in line.split()]
        except ValueError:return False
        if not a or a[-1]!=0 or 0 in a[:-1] or any(abs(x)>n or x==0 for x in a[:-1]):return False
        if len(a[:-1])!=len(set(a[:-1])) or any(-x in a[:-1] for x in a[:-1]):return False
    return True

malformed=["p cnf 1 2\n1 0\n", "p cnf 1 2\n1 0\n-2 0\n", "p cnf 1 2\n1 0\n-1", "p cnf 1 2\n1 0\n-1 0\nextra"]
assert strict_dimacs("p cnf 1 2\n1 0\n-1 0")
assert all(not strict_dimacs(x) for x in malformed)

def weighted_identity(name, m, mu, choices, weights):
    q=len(choices);r=m
    assert q==len(weights)
    for i,p in enumerate(choices): assert all(0<=t<m+i for t in p)
    assert any(len(a)>2 for a in choices) or check(m,choices) is not None
    seen=set();stack=[m+q-1]
    while stack:
        v=stack.pop()
        if v in seen:continue
        seen.add(v)
        if v>=m:stack.extend(choices[v-m])
    assert len(seen)==m+q
    E=sum(map(len,choices));b=E-(m+q-1);w=sum(weights)
    c=sum(weight-(len(p)-1) for p,weight in zip(choices,weights))
    assert b>=0 and r>=mu and w-(mu-1)==(r-mu)+b+c
    return {'name':name,'source_ancestors':r,'min_unsat_core_size':mu,'derived_nodes':q,
            'cyclomatic_excess':b,'source_surplus':r-mu,'rule_charge_surplus':c,
            'charged_cost':w,'baseline_cost':mu-1,'proof_excess':w-(mu-1),
            'fanin':[len(p) for p in choices], 'parents':[list(p) for p in choices], 'node_weights':weights}

weighted=[
 weighted_identity('binary_unit_contradiction',2,2,[(0,1)],[1]),
 weighted_identity('unary_local_convert_then_RES',2,2,[(0,),(2,1)],[1,1]),
 weighted_identity('binary_reconvergence_after_false',2,2,[(0,1),(2,0)],[1,1]),
 weighted_identity('abstract_zero_premise_DEF_topology',2,2,[(),(0,2),(3,1)],[1,1,1]),
 weighted_identity('binary_extra_used_source',3,2,[(0,1),(3,2)],[1,1]),
 weighted_identity('comparative_three_parent_HORN_unit',3,3,[(0,1,2)],[1]),
 weighted_identity('comparative_three_parent_HORN_weighted',3,3,[(0,1,2)],[2]),
]
output={"run":"LSPV1_SOURCE_EXCESS_EULER349","status":"PROVED identity / COMPUTATIONAL enumeration", "cases":results,"weighted_examples":weighted,
        "signed_controls":controls,"G342_clause_deletion_models":6,"G342_signflip_models":14,
        "mislabelled_sat_as_unsat_rejected":bool(sat([[1],[1]],1)),
        "malformed_encodings_rejected":len(malformed)}
raw=json.dumps(output,sort_keys=True,indent=2)+'\n'
open('source_excess_349.json','w').write(raw)
print(raw)
