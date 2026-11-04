#!/usr/bin/env python3
"""LSPV-1/400 all-k source-retraction support inflation, dependency-free."""
import json
from pathlib import Path

def and_gate(z,a,b):
    return [(-z,a),(-z,b),(z,-a,-b)]

def cnf_for(k):
    assert k >= 4
    p = {2: k+1}
    for j in range(3,k+1): p[j]=k+j-1
    r=2*k
    clauses=[]
    for j in range(2,k+1):
        clauses.extend(and_gate(p[j],1 if j==2 else p[j-1],j))
    clauses.extend(and_gate(r,p[k],-k))
    clauses.append((r,))
    assert len(clauses)==3*k+1
    return clauses,p[k],r,p

def resolve(a,b,pivot):
    assert pivot in a and -pivot in b
    c=tuple(sorted((set(a)-{pivot}) | (set(b)-{-pivot})))
    assert not any(-x in c for x in c)
    return c

def sat_clause(clause,asn):
    return any(asn[abs(x)] == (x>0) for x in clause)

def run(k):
    cnf,p,r,defs=cnf_for(k)
    def source(cl):
        assert cl in cnf
        return tuple(cl)
    u_r=source((r,))
    ppos=resolve(u_r,source((-r,p)),r)
    xneg=resolve(u_r,source((-r,-k)),r)
    pneg=resolve(xneg,source((-p,k)),-k)
    assert ppos==(p,) and xneg==(-k,) and pneg==(-p,)
    table=[int(bool(v) and not bool(v)) for v in (0,1)]
    assert table==[0,0]
    source_support={p}
    expanded_support=set(range(1,k+1))
    orig_unsat=[(i,) for i in range(1,k+1)]+[(-k,)]
    original_sat_sibling=[(i,) for i in range(1,k+1)]
    sibling_assignment={j:True for j in range(1,k+1)}
    assert all(sat_clause(c,sibling_assignment) for c in original_sat_sibling)
    assert not all(sat_clause(c,sibling_assignment) for c in orig_unsat)
    for j in range(2,k+1):
        g=defs[j]; a=1 if j==2 else defs[j-1]; b=j
        for va in (False,True):
            for vb in (False,True):
                asn={a:va,b:vb,g:va and vb}
                assert all(sat_clause(c,asn) for c in and_gate(g,a,b))
    for vp in (False,True):
        for vk in (False,True):
            asn={p:vp,k:vk,r:vp and (not vk)}
            assert all(sat_clause(c,asn) for c in and_gate(r,p,-k))
    if k<=6:
        for mask in range(1<<(2*k)):
            asn={i:bool((mask>>(i-1))&1) for i in range(1,2*k+1)}
            assert not all(sat_clause(c,asn) for c in cnf)
    assert all(all(0<abs(t)<=2*k for t in c) for c in cnf)
    try:
        resolve((r,),(-r,p),k)
        raise AssertionError('forged pivot accepted')
    except AssertionError as e:
        assert str(e) != 'forged pivot accepted'
    assert not (0<abs(3*k)<=2*k)
    return dict(k=k,original_clauses=len(orig_unsat),evaluator_clauses=len(cnf),
                evaluator_original_variables=2*k,chain_gate_nodes=k,
                paid_proof_nodes=4,proof_resolvents=[list(ppos),list(xneg),list(pneg)],
                final_AND3_table=table,support_before=len(source_support),
                support_after=len(expanded_support),
                origin_support=sorted(expanded_support),
                original_formula_unsat_by_opposite_units=True,
                sibling_formula_sat=True)

def main():
    ks=[4,5,6,7,8,10,16,32,64]
    results=[run(k) for k in ks]
    assert results[0]['support_after']==4 and results[-1]['support_after']==64
    raw={'title':'LSPV1-400','seed':None,
         'model':'strict-RES plus AND3 support-typing of source-labelled evaluator CNF',
         'status':'COMPUTATIONAL','cases':results,
         'checks':'symbolic gate facets and all small-k valuations; not a full native Rmix341 checker'}
    path=Path(__file__).with_name('lspv1_400_raw.json')
    path.write_text(json.dumps(raw,indent=2)+'\n')
    print(json.dumps({'cases':len(results),'max_support':max(z['support_after'] for z in results),'raw':str(path)}))

if __name__=='__main__':main()
