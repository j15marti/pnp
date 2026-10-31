#!/usr/bin/env python3
"""Independent, no producer imports; replays raw proof DAGs, original modes,
coherent assignment trails, DPLL SAT/UNSAT proof trees and negatives."""
import json,itertools,sys,collections,hashlib
from pathlib import Path

def truth(l,a): return a[abs(l)]==(l>0)
def sat(F,a): return all(any(truth(l,a) for l in c) for c in F)
def unit_propagate(F,ass):
    a=dict(ass)
    while True:
        changed=False
        for c in F:
            if any(truth(l,a) for l in c if abs(l) in a):continue
            remain=[l for l in c if abs(l) not in a]
            if not remain:return None
            if len(remain)==1:
                l=remain[0];i=abs(l);v=l>0
                if i in a and a[i]!=v:return None
                if i not in a:a[i]=v;changed=True
        if not changed:return a

def verify_tree(t,F,n,ass=None):
    if ass is None:ass={}
    a=unit_propagate(F,ass)
    if t['type']=='UNSAT_LEAF':return a is None,False,1
    if t['type']=='SAT_LEAF':
        b={int(i):bool(x) for i,x in t['full_assignment'].items()}
        return (a is not None and len(b)==n and all(b.get(k)==v for k,v in a.items()) and sat(F,b)),True,1
    if a is None:return False,False,1
    pivot=t['var']
    if pivot in a:return False,False,1
    children=t['children'];v=[c['value'] for c in children]
    if v not in ([1],[1,0]):return False,False,1
    R=[verify_tree(c['tree'],F,n,{**a,pivot:bool(c['value'])}) for c in children]
    if not all(x[0] for x in R):return False,False,1+sum(x[2] for x in R)
    ns=1+sum(x[2] for x in R)
    if t['type']=='UNSAT_BRANCH':return v==[1,0] and not any(x[1] for x in R),False,ns
    if t['type']=='SAT_BRANCH':return (v==[1] and R[0][1]) or (v==[1,0] and not R[0][1] and R[1][1]),True,ns
    return False,False,ns

def audit(record):
    F=record['source_formula'];n=record['n'];checks=collections.Counter()
    assert all(len(c)==len(set(abs(x) for x in c)) for c in F)
    cert=record['cert'];proof=record['resolution_dag']
    if cert is not None:
        assert proof is not None
        B=set(cert['guard_variables']); d={i+1:set(c) for i,c in enumerate(F)}
        guards=[]
        for path in cert['paths']:
            assert path
            for u,v in zip(path,path[1:]): assert u['to']==v['from']
            for e in path:
                assert e['source'] in d
                c=d[e['source']];g=set(e['guard_literals'])
                assert all(abs(l) in B for l in g)
                x=e['from'];y=e['to']
                assert (-x in c and y in c) or (x==-y and y in c)
                # For binary edge every non-guard source literal must be in {-x,y}.
                core={l for l in c if abs(l) not in B}
                assert core==({-x,y})
                assert g=={l for l in c if abs(l) in B}
                guards.extend(g);checks['source_authenticated_edges']+=1
        assert cert['paths'][0][0]['from']==cert['pivot']
        assert cert['paths'][0][-1]['to']==-cert['pivot']
        assert cert['paths'][1][0]['from']==-cert['pivot']
        assert cert['paths'][1][-1]['to']==cert['pivot']
        assert not any(-l in guards for l in guards)
        assert set(cert['learned'])==set(guards)
        for s in proof['steps']:
            u,v=s['parents'];pivot=s['pivot']
            a,b=d[u],d[v]
            assert (pivot in a and -pivot in b) or (-pivot in a and pivot in b)
            result=((a-{pivot})|(b-{-pivot})) if pivot in a else ((a-{-pivot})|(b-{pivot}))
            assert set(s['clause'])==result and not any(-l in result for l in result)
            d[s['id']]=result;checks['resolution_steps']+=1
        assert d[proof['root']]==set(proof['learned'])
        checks['authenticated_certificates']+=1
    else: assert proof is None
    c=record['source_controls']
    for j,row in enumerate(c['original_clause_targets']):
        assert row['source_clause']==j+1
        assert row['literals']==F[j]
        for term in row['signed_occurrences']:
            l=term['literal'];v=str(abs(l))
            assert term['source_clause']==j+1 and term['variable']==abs(l)
            assert term['S']==int(l>0) and term['U']==int(l<0)
            assert term['inverse_S_U']==term['U'] and term['inverse_U_S']==term['S']
            assert row['S'][v]==term['S'] and row['U'][v]==term['U']
            checks['source_signed_occurrences']+=1
    for pair in c['source_pair_compatibility']:
        i,j=pair['source_pair'];C=F[i-1];D=F[j-1]
        shared={abs(l) for l in C}&{abs(l) for l in D}
        opposite=any((next(l>0 for l in C if abs(l)==v)) != (next(l>0 for l in D if abs(l)==v)) for v in shared)
        same=any((next(l>0 for l in C if abs(l)==v)) == (next(l>0 for l in D if abs(l)==v)) for v in shared)
        assert pair['SS']==(not opposite) and pair['UU']==(not opposite)
        assert pair['SU']==(not same) and pair['US']==(not same)
        checks['extreme_matrix_modes']+=4
    for frame in c['coherent_flip_trail']:
        a={i+1:bool(int(ch)) for i,ch in enumerate(frame['assignment'])}
        vals=[sum(truth(l,a) for l in clause) for clause in F]
        assert frame['true_literal_counts']==vals
        assert frame['histogram']==[vals.count(i) for i in range(max(map(len,F),default=0)+1)]
        assert frame['four_categories']==[vals.count(i) for i in range(4)]
        assert frame['satisfied']==(0 not in vals)
        checks['coherent_flip_frames']+=1
    for name,FF,treekey,counterkey in [('baseline',F,'baseline_tree','baseline_counters'),
                                      ('enhanced',F+([cert['learned']] if cert else []),'enhanced_tree','enhanced_counters')]:
        ok,label,nodes=verify_tree(record[treekey],FF,n)
        assert ok and nodes==record[counterkey]['nodes']
        assert label==('SAT_witness' in record and record['SAT_witness'] is not None)
        checks['verified_search_trees']+=1
    if record['SAT_witness'] is not None:
        a={int(i):bool(v) for i,v in record['SAT_witness'].items()}
        assert sat(F,a);checks['original_source_SAT_witnesses']+=1
    else:checks['UNSAT_tree_certificates']+=1
    if n<=16:
        models=0
        for mask in range(1<<n):
            a={i+1:bool(mask&(1<<i)) for i in range(n)}
            good=sat(F,a)
            models+=good
            if good and cert:assert any(truth(l,a) for l in cert['learned'])
            checks['coherent_truth_table_rows']+=1
        assert models==record['source_models']
    return checks

def main():
    p=Path(sys.argv[1]); data=json.loads(p.read_text())
    report=collections.Counter()
    for rec in data['cases']:report.update(audit(rec))
    assert data['aggregate_cases']['cases']==len(data['cases'])
    # Independent negative control: original clauses with mixed guards permit
    # each guard assignment but optimistic unguarded union has a contradiction.
    F=[[-3,1,2],[-3,-1,2],[3,1,-2],[3,-1,-2]]
    for a in (False,True):
        assert any(sat(F,{1:bool(b&1),2:bool(b&2),3:a}) for b in range(4))
    # Explicitly prohibit asserting RUP: in guard-four source UP under g=1
    # stops without contradiction even though resolution derives not g.
    guard4=next(x for x in data['cases'] if x['name']=='four_binary_guard_YES')
    assert guard4['cert']['learned']==[-3] and guard4['learned_clause_rup'] is False
    report['negative_controls']+=2
    summary={'verified':True,'source_raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
             'counts':dict(report),'independent_implementation':True}
    out=p.with_name('independent_check261.json');out.write_text(json.dumps(summary,indent=2,sort_keys=True))
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()