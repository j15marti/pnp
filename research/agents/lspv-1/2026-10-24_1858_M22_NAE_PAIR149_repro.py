#!/usr/bin/env python3
"""M22-NAE-PAIR149 finite audit, standard library only.

Usage: python M22_NAE_PAIR149_repro.py [optional_path_to_Doecker61_source.txt]
The optional source is the published 198-variable transcribed source in
research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt.
Its UNSAT label is imported from published work and is NOT enumerated here.
This program checks the grammar and local pseudo-marginal consistency only.
"""
from __future__ import annotations
import ast
import itertools
import json
import sys
from collections import Counter
from pathlib import Path

NAE = tuple(b for b in itertools.product((0,1),repeat=3) if 0<sum(b)<3)
PARITY_POS = tuple(b for b in itertools.product((0,1),repeat=3) if sum(b)%2==1)
PARITY_NEG = tuple(b for b in itertools.product((0,1),repeat=3) if sum(b)%2==0)
Y = [(1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6)]
PAIRED = Y[:4] + [tuple(-v for v in C) for C in Y[:4]]

def supports_degree2_six():
    all_triples=list(itertools.combinations(range(1,7),3))
    out=[]
    for combination in itertools.combinations(all_triples,4):
        counts=Counter(x for tri in combination for x in tri)
        if all(counts[i]==2 for i in range(1,7)):
            out.append(combination)
    assert len(out)==75
    return out

def audit_grammar(clauses,variables=None):
    pos=Counter();neg=Counter();seen=set()
    for clause in clauses:
        assert len(clause)==3 and len(set(map(abs,clause)))==3
        assert all(x>0 for x in clause) or all(x<0 for x in clause)
        key=tuple(sorted(clause));assert key not in seen;seen.add(key)
        for x in clause:
            (pos if x>0 else neg)[abs(x)]+=1
    active=set(pos)|set(neg)
    assert all(pos[i]==neg[i]==2 for i in active)
    if variables is not None: assert active==set(range(1,variables+1))
    P={frozenset(map(abs,c)) for c in clauses if c[0]>0}
    Q={frozenset(map(abs,c)) for c in clauses if c[0]<0}
    return len(active),len(clauses),len(P&Q),len(P-Q)

def marginal(clause, coordinate_names, measure=NAE):
    names=list(map(abs,clause))
    idx=[names.index(j) for j in coordinate_names]
    return Counter(tuple(row[i] for i in idx) for row in measure)

def verify_local(clauses):
    """Counts equality after cross multiplication (all measures size six)."""
    checked=0; overlaps=Counter(); bad=[]
    for clause in clauses:
        assert all((any(x==1 for x in row) if clause[0]>0 else
                    any(x==0 for x in row)) for row in NAE)
    for i,ci in enumerate(clauses):
        for cj in clauses[i+1:]:
            common=sorted(set(map(abs,ci))&set(map(abs,cj)))
            overlaps[len(common)]+=1
            mi=marginal(ci,common)
            mj=marginal(cj,common)
            if mi!=mj: bad.append([ci,cj,common])
            checked+=1
    assert not bad,bad[:1]
    return checked,overlaps

def exact_model_count(clauses,k):
    cnt=0
    for row in itertools.product((0,1),repeat=k):
        if all(any(row[abs(x)-1]==(x>0) for x in c) for c in clauses):cnt+=1
    return cnt

def six_census():
    blocks=supports_degree2_six()
    pairhist=Counter();comms=Counter();pairs_checked=0
    for p in blocks:
        for q in blocks:
            clauses=[tuple(x for x in tri) for tri in p]+[tuple(-x for x in tri) for tri in q]
            k,m,h,defect=audit_grammar(clauses,6)
            assert (k,m)==(6,8)
            cnt,ov=verify_local(clauses)
            pairs_checked+=cnt
            pairhist[h]+=1
            comms.update(ov)
    assert sum(pairhist.values())==5625
    assert pairhist[4]==75
    assert pairhist[0]>0 and sum(n for h,n in pairhist.items() if h>0 and h<4)>0
    return pairhist,comms,pairs_checked

def covariance_optimum():
    assert all(sum(row[i] for row in NAE)==3 for i in range(3))
    joint11=Counter()
    for a,b in itertools.combinations(range(3),2):
        joint11[f'{a}{b}']=sum(row[a]==row[b]==1 for row in NAE)
    assert set(joint11.values())=={1}
    return {'NAE_rows':len(NAE),'marginal_p1':'1/2','pair_p11':'1/6',
            'pair_covariance':'-1/12','pair_correlation':'-1/3',
            'sum_covariance':'-1/4','min_possible_max_abs_pair_correlation':'1/3'}

def load_Doecker(path):
    text=Path(path).read_text(encoding='utf-8')
    data='\n'.join(line for line in text.splitlines() if not line.startswith('#'))
    arr=ast.literal_eval(data)
    return [tuple(c) for c in arr]

def run(path=None):
    outcomes={}
    for label,clauses in [('Y',Y),('FULLY_PAIRED',PAIRED)]:
        k,m,h,q=audit_grammar(clauses,6)
        tested,hist=verify_local(clauses)
        outcomes[label]={'k':k,'m':m,'paired_supports':h,'q':q,
                         'models':exact_model_count(clauses,k),
                         'pair_comparisons':tested,'overlap_hist':dict(sorted(hist.items()))}
    assert outcomes['Y']['models']==20
    assert outcomes['FULLY_PAIRED']['paired_supports']==4
    pairhist,overlap_count,cnt=six_census()
    outcomes['six_var_census']={'sources':5625,'paired':75,'Cstar':5550,
      'pair_support_hist':dict(sorted(pairhist.items())),
      'overlap_size_hist':dict(sorted(overlap_count.items())),
      'pair_checks':cnt, 'failures':0}
    outcomes['NAE_moments']=covariance_optimum()
    outcomes['outside_class_UNSAT_control']={'construction':'all 10 positive and all 10 negative ternary clauses on five variables',
      'models':exact_model_count([tri for tri in itertools.combinations(range(1,6),3)] +
                                  [tuple(-x for x in tri) for tri in itertools.combinations(range(1,6),3)],5),
      'scope':'proper clausewise-monotone, but variables each 6+/6- not 2+/2-'}
    assert outcomes['outside_class_UNSAT_control']['models']==0
    if path:
        U=load_Doecker(path);k,m,h,q=audit_grammar(U,198)
        checked,ov=verify_local(U)
        outcomes['Doecker_U']={'k':k,'m':m,'h':h,'q':q,
            'pair_checks':checked,'overlap_size_hist':dict(sorted(ov.items())),
            'unsat_label':'IMPORTED from Doecker original; not enumerated'}
    return outcomes

if __name__=='__main__':
    found_path=sys.argv[1] if len(sys.argv)>1 else None
    if not found_path:
        p=Path(__file__).resolve().parents[1]/'lspv-2'/'2026-10-24_0011_DOECKER61_original_source.txt'
        if p.exists():found_path=str(p)
    print(json.dumps(run(found_path),sort_keys=True,indent=2))
