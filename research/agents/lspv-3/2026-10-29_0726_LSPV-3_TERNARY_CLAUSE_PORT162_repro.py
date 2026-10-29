#!/usr/bin/env python3
"""LSPV-3 TERNARY-CLAUSE-PORT162: independent, reproducible finite source audit.
Standard library + optional SciPy/NumPy (independent MILP). Does not assume SAT oracle.
Reads source clauses written explicitly here; no network. Diagnostics and raw JSON on stdout.
"""
import json, hashlib, itertools, math
from collections import Counter
from pathlib import Path

G=[(-5,-12,15),(-5,-6,-15),(-4,-9,-11),(-4,-8,-11),(-3,6,-15),(-3,12,15),(-2,-6,12),(-2,5,-12),(-1,3,-14),(-1,13,14),(1,-7,10),(1,7,13),(2,-9,11),(2,-8,9),(3,7,-13),(4,8,-10),(4,9,-10),(5,8,-14),(6,-7,11),(10,-13,14)]
assert len(G)==20

def sat_clause(c,mask):return any(bool((mask>>(abs(l)-1))&1)==(l>0) for l in c)

def model_masks(clauses,n):
    return [m for m in range(1<<n) if all(sat_clause(cl,m) for cl in clauses)]

def projection(masks, ports):
    fibers=Counter()
    for m in masks: fibers[sum(((m>>(p-1))&1)<<i for i,p in enumerate(ports))]+=1
    return fibers

def m_closed(vals):
    for a,b,c in itertools.product(vals,repeat=3):
        if ((a&b)|(b&c)|(c&a)) not in vals:return False
    return True

def check_formula(clauses,n,required_connected=True):
    assert all(len(cl)==3 and len({abs(l) for l in cl})==3 for cl in clauses)
    assert len(set(tuple(sorted(cl,key=lambda l:abs(l))) for cl in clauses))==len(clauses)
    degrees=Counter((abs(l),l>0) for cl in clauses for l in cl)
    assert all(degrees[(v,True)]==2 and degrees[(v,False)]==2 for v in range(1,n+1))
    if required_connected:
        graph={v:set() for v in range(1,n+1)}
        for cl in clauses:
            names=[abs(l) for l in cl]
            for a in names:
                graph[a].update(x for x in names if x!=a)
        found={1};pending=[1]
        while pending:
            for v in graph[pending.pop()]-found:found.add(v);pending.append(v)
        assert len(found)==n
    return True

def mk_linked():
    A=[list(c) for c in G]
    B=[[int(math.copysign(abs(l)+15,l)) for l in c] for c in G]
    # Cross-swap exactly the designated negative x4 occurrences in zero-indexed C2.
    assert -4 in A[2] and -19 in B[2]
    A[2][A[2].index(-4)]=-19
    B[2][B[2].index(-19)]=-4
    C=[tuple(c) for c in A+B]
    check_formula(C,30)
    return C

def milp_cofactor(C,n,ports,port_val):
    # Independently solve the UNPROJECTED original 30-variable CNF by HiGHS MILP.
    import numpy as np
    from scipy.optimize import milp, Bounds, LinearConstraint
    mat=np.zeros((len(C),n),float)
    rhs=np.zeros(len(C),float)
    for j,cl in enumerate(C):
        neg=0
        for l in cl:
            mat[j,abs(l)-1]+=(1 if l>0 else -1)
            neg+=int(l<0)
        rhs[j]=1-neg
    lb=np.zeros(n);ub=np.ones(n)
    for b,p in enumerate(ports):
        val=(port_val>>b)&1
        lb[p-1]=val;ub[p-1]=val
    r=milp(c=np.zeros(n),integrality=np.ones(n),bounds=Bounds(lb,ub),constraints=LinearConstraint(mat,rhs,np.full(len(C),np.inf)),options={'disp':False})
    assert r.status in (0,2), f'unexpected MILP status {r.status}: {r.message}'
    if r.status==0:
        witness=sum(int(round(v))<<i for i,v in enumerate(r.x))
        assert all(sat_clause(cl,witness) for cl in C)
        assert all(((witness>>(p-1))&1)==((port_val>>i)&1) for i,p in enumerate(ports))
        return True,witness
    return False,None

def run():
    check_formula(G,15)
    M=model_masks(G,15)
    assert len(M)==272
    types=Counter();nonbij=[];fibers_for_key=None
    for ports in itertools.combinations(range(1,16),3):
        fibers=projection(M,ports)
        vals=set(fibers)
        if not m_closed(vals):
            assert len(vals)==7
            missing=next(iter(set(range(8))-vals))
            types[missing]+=1
            nonbij.append({'ports':ports,'forbidden':missing})
        if ports==(1,2,13): fibers_for_key=dict(sorted(fibers.items()))
    assert sum(types.values())==60
    assert sorted(fibers_for_key)==[0,1,2,4,5,6,7]
    # Explicit majority violation: (x1,x2,x13)=100,010,111 are extendible, 110 is not.
    assert all(x in fibers_for_key for x in (1,2,7)) and 3 not in fibers_for_key
    assert ((1&2)|(2&7)|(7&1))==3
    linked=mk_linked();ports=(1,2,13)
    linked_fibers={}
    for cofactor in range(8):
        ok,witness=milp_cofactor(linked,30,ports,cofactor)
        linked_fibers[cofactor]={'sat':ok,'model':witness}
    assert [k for k,v in linked_fibers.items() if v['sat']]==[0,1,2,4,5,6,7]
    # Source-puncture lemma for equality x4A=x4B under same-sign C2 occurrence swap.
    punctured={}
    for a in range(1<<15):
        if all(i==2 or sat_clause(cl,a) for i,cl in enumerate(G)):
            p=(a>>3)&1
            u=int(any(sat_clause((l,),a) for l in G[2] if abs(l)!=4))
            punctured.setdefault(p,set()).add(u)
    assert punctured=={0:{0},1:{0,1}}
    # A mismatched pair of p values cannot satisfy BOTH transferred C2 clauses.
    for pa,pb in itertools.product((0,1),repeat=2):
        legal=any((ua or not pb) and (ub or not pa) for ua in punctured[pa] for ub in punctured[pb])
        assert legal == (pa==pb)
    # SOURCE model witness masks, authenticated single module, for every positive triple.
    witnesses={t:next(m for m in M if sum(((m>>(p-1))&1)<<i for i,p in enumerate(ports))==t) for t in fibers_for_key}
    return {
        'project':'LSPV-3_TERNARY_CLAUSE_PORT162',
        'source_variables':15,'source_clauses':20,'source_models':len(M),
        'source_triples':455,'source_nonbijunctive_triples':len(nonbij),
        'nonbijunctive_types_by_forbidden_tuple':dict(sorted(types.items())),
        'key_ports':list(ports),'key_projection_model_counts':dict(sorted(fibers_for_key.items())),
        'key_projection_forbidden_tuple':3,
        'key_witness_masks':dict(sorted(witnesses.items())),
        'linked_variables':30,'linked_clauses':len(linked),
        'linked_cross_swap':{'source_clause_index':2,'literal_A_before':-4,'literal_A_after':-19,'literal_B_before':-19,'literal_B_after':-4},
        'linked_milp_cofactors':linked_fibers,
        'puncture_relation_x4_u2':{p:sorted(v) for p,v in punctured.items()},
        'rejected_cofactors': [3],
        'status':'COMPUTATIONAL source and linked finite controls; mathematical majority obstruction PROVED under cofactor identity; no general SAT result'
    }


# Independent extension of LSPV-2's already established x4 equality chain:
# kept separate from the main reproducibility JSON for backwards compatibility.
def make_chain(k):
    assert k>=2
    blocks=[]
    for i in range(k):
        off=15*i
        blocks.append([[((abs(l)+off) if l>0 else -(abs(l)+off)) for l in c] for c in G])
    for i in range(k-1):
        neg_left=-(4+15*i);neg_right=-(4+15*(i+1))
        assert neg_left in blocks[i][3] and neg_right in blocks[i+1][2]
        blocks[i][3][blocks[i][3].index(neg_left)]=neg_right
        blocks[i+1][2][blocks[i+1][2].index(neg_right)]=neg_left
    out=[tuple(c) for block in blocks for c in block]
    check_formula(out,15*k)
    return out

def test_chains():
    result={}
    for k in [2,3,4,5]:
        C=make_chain(k)
        vals=[]
        for cofactor in range(8):
            sat,_=milp_cofactor(C,15*k,(1,2,13),cofactor)
            if sat:vals.append(cofactor)
        assert vals==[0,1,2,4,5,6,7]
        result[k]={'vars':15*k,'clauses':20*k,'root_relation':vals,'full_CNF_MILP_checks':8}
    return result


def test_sign_flips():
    C=make_chain(2);out={}
    for f in range(8):
        flipped={p for i,p in enumerate((1,2,13)) if (f>>i)&1}
        F=[tuple(-x if abs(x) in flipped else x for x in cl) for cl in C]
        check_formula(F,30)
        feasible=[mask for mask in range(8) if milp_cofactor(F,30,(1,2,13),mask)[0]]
        assert set(feasible)==set(range(8))-{3^f}
        out[f]={'forbidden':3^f,'feasible':feasible}
    return out

if __name__=='__main__':
    result=run()
    result['chain_checks']=test_chains()
    result['all_eight_port_flip_checks']=test_sign_flips()
    result['total_full_formula_MILP_cofactors']=8+32+64
    print(json.dumps(result,sort_keys=True,indent=2))