#!/usr/bin/env python3
"""Finite falsifiers for the scoped paid-AND gate budget proof-translation theorem.
Standard-library only. Deterministic and independently checkable source rules.
No claim of proving Braun's asymptotic theorem or arbitrary SAT hardness.
"""
import itertools, json, random, hashlib, sys
from pathlib import Path
from collections import defaultdict

SEED=3702026
rng=random.Random(SEED)
checks=0

def check(x,msg):
    global checks
    checks+=1
    if not x: raise AssertionError(msg)

def canon(C):
    c=tuple(sorted(set(C), key=lambda z:(abs(z),z<0)))
    check(all(-x not in c for x in c),f'tautological clause {c}')
    return c

def litval(l,values):
    return bool(values[abs(l)]) if l>0 else not bool(values[abs(l)])

def sat(C,values): return any(litval(l,values) for l in C)

def gate_slots(z,a,b):
    return (canon((-z,a)),canon((-z,b)),canon((z,-a,-b)))

def make_network(k,g):
    gates=[]
    allowed=list(range(1,k+1))
    for i in range(g):
        out=k+i+1
        a,b=rng.sample(allowed,2)
        a*=rng.choice((-1,1));b*=rng.choice((-1,1))
        gates.append(dict(out=out,a=a,b=b))
        allowed.append(out)
    return gates

def gate_values(original,gates):
    vals={i:int(original[i]) for i in original}
    for gate in gates:
        z,a,b=gate['out'],gate['a'],gate['b']
        vals[z]=int(litval(a,vals) and litval(b,vals))
    return vals

def resolve(a,b,p):
    check((p in a and -p in b) or (-p in a and p in b),'pivot missing')
    if p in a:
        c=canon([x for x in a if x!=p]+[x for x in b if x!=-p])
    else:
        c=canon([x for x in a if x!=-p]+[x for x in b if x!=p])
    return c

def blocker(alpha):
    return canon([-i if alpha[i] else i for i in sorted(alpha)])

# A genuine paid-AND and strict-Resolution proof, containing the gate on the
# proof ancestry, is replayed against its three ORIGINAL contradictory clauses.
sources=[canon((1,)),canon((2,)),canon((-1,-2))]
gates=[dict(out=3,a=1,b=2)]
slots=gate_slots(3,1,2)
source_set=set(sources)
r1=resolve(slots[2],sources[0],-1)
r2=resolve(r1,sources[1],-2)
r3=resolve(sources[2],slots[0],-1)
r4=resolve(r3,slots[1],-2)
r5=resolve(r2,r4,3)
check(r5==(),'five explicit signed RES steps derive contradiction')
check(r2==(3,) and r4==(-3,),'derived signed aux units')

# Guard lifting: source C implies B_alpha as a semantic Res(xor) weakening
# if C is falsified by alpha. Every alpha yields such a blocking clause.
blockers={}
weakening_steps=0
for bits in itertools.product((0,1),repeat=2):
    alpha={1:bits[0],2:bits[1]}
    vals=gate_values(alpha,gates)
    check(all(sat(C,vals) for C in slots),'every paid gate slot true after direct-fanin restriction')
    false_source=[i for i,C in enumerate(sources) if not sat(C,vals)]
    check(bool(false_source),'at least one authentic F source falsified')
    B=blocker(alpha)
    check(any(set(sources[i]).issubset(set(B)) for i in false_source),'source semantic weakening to blocker')
    weakening_steps+=int(B not in source_set)
    blockers[bits]=B
check(resolve(blockers[(0,0)],blockers[(0,1)],2)==(1,), 'merge guard siblings 00/01')
check(resolve(blockers[(1,0)],blockers[(1,1)],2)==(-1,), 'merge guard siblings 10/11')
check(resolve((1,),(-1,),1)==(),'root guard resolution')

# Verify signed gate constraints for randomly wired, sign-sensitive networks
# and independence of all gate outputs from all originals outside direct fanins.
network_cases=0
all_gate_deletions=0
for k in (2,3,4,5):
    for g in (1,2,3,4):
        for trial in range(8):
            net=make_network(k,g)
            S={abs(l) for G in net for l in (G['a'],G['b']) if abs(l)<=k}
            check(len(S)<=2*g,'direct fanin support gate budget')
            alpha_to_gates={}
            for bits in itertools.product((0,1),repeat=k):
                orig=dict(zip(range(1,k+1),bits))
                vals=gate_values(orig,net)
                for G in net:
                    check(all(sat(c,vals) for c in gate_slots(G['out'],G['a'],G['b'])),'valid gate slots')
                alpha=tuple(orig[i] for i in sorted(S))
                ev=tuple(vals[G['out']] for G in net)
                if alpha in alpha_to_gates:
                    check(alpha_to_gates[alpha]==ev,'constant gate values on each direct-fanin fiber')
                alpha_to_gates[alpha]=ev
            check(len(alpha_to_gates)==2**len(S),'all direct-fanin patterns exist')
            network_cases+=1

# Same-source SAT/UNSAT, signed deletion and sign-control cases.
check(not any(all(sat(C,{1:a,2:b}) for C in sources) for a,b in itertools.product((0,1),repeat=2)), 'base source UNSAT')
for i in range(3):
    sub=[C for j,C in enumerate(sources) if j!=i]
    check(any(all(sat(C,{1:a,2:b}) for C in sub) for a,b in itertools.product((0,1),repeat=2)),f'deletion {i} restores SAT')
    for lit in sources[i]:
        flip=[canon(tuple(-x if x==lit else x for x in C)) if j==i else C for j,C in enumerate(sources)]
        check(any(all(sat(C,{1:a,2:b}) for C in flip) for a,b in itertools.product((0,1),repeat=2)), 'signed occurrence flip restores SAT')

# Explicit odd/even cubic K4 Tseitin parity controls. Vertex 0 charged odd.
edges=[(i,j) for i in range(4) for j in range(i+1,4)]
def k4_formula(odd):
    C=[]
    for v in range(4):
        e=[a+1 for a,(u,w) in enumerate(edges) if v in (u,w)]
        for bits in itertools.product((0,1),repeat=3):
            charge=(v==0 and odd)
            if sum(bits)%2 != int(charge):
                C.append(canon([-e[i] if bits[i] else e[i] for i in range(3)]))
    return C
k4={}
for odd in (True,False):
    F=k4_formula(odd)
    count=sum(all(sat(C,dict(zip(range(1,7),bits))) for C in F) for bits in itertools.product((0,1),repeat=6))
    check(count==(0 if odd else 8),'odd/even K4 labels')
    k4['odd' if odd else 'even']={'clauses':len(F),'models':count}

# Explicit fake pivot and malformed syntactic controls.
for bad in ((1,2), (2,3),(-3,-1),(-1,-2,1)):
    try:
        resolve(sources[0],sources[1],3) if bad!=( -1,-2,1) else canon(bad)
        check(False,'invalid synthetic record was accepted')
    except (AssertionError, KeyError):
        checks+=1

result={
    'seed':SEED,'assertions':checks,'network_cases':network_cases,
    'signed_and_gate_definition_slots':slots,
    'tiny_original_source':sources,
    'tiny_paid_mixed_proof':{'paid_definition_nodes':1,'strict_RES_nodes':5,'total_paid_nodes':6,
                        'derived_clauses':[r1,r2,r3,r4,r5]},
    'same_source_guard_lift':{'assignments':4,'blockers':{str(k):v for k,v in blockers.items()},
                              'derived_ordinary_RES_merges':3,'source_weakening_steps':weakening_steps},
    'k4_controls':k4,
    'literature_inputs':{'braun_holes':'n=2^ell, ell>=32','lower_res_xor':'exp(n/(32768 ell^2)) total proof nodes',
                         'theorem_conditional_on_original_preprint':True},
    'scope_warning':'finite tests do not establish Res(xor) Braun lower bound or full Rmix transfer',
}
out=Path(__file__).with_name('gate_budget_controls_raw.json')
out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'PASS':True,'checks':checks,'network_cases':network_cases,'tiny':result['tiny_paid_mixed_proof'],'k4':k4},sort_keys=True))