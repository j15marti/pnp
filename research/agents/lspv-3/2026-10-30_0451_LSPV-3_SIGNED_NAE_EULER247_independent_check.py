#!/usr/bin/env python3
"""Independent, dependency-free checker for SIGNED_NAE_EULER247 raw results.

Does not import the producer. Exhaustively enumerates every assignment on the
15-variable W1/SWAP6 hostile controls and every one of 4096 K4 signings.
"""
from itertools import combinations, product
from pathlib import Path
import json, sys, hashlib

def value(l,mask):return ((mask>>(abs(l)-1))&1)==(l>0)
def counts(F,mask):return [sum(value(l,mask) for l in c) for c in F]
def model(F,mask):return all(any(value(l,mask) for l in c) for c in F)
def nvars(F):return max(abs(l) for c in F for l in c)

def independent_audit(path):
    data=json.loads(Path(path).read_text())
    checked={'cases':0,'indexed_source_occurrences':0,'pair_modes':0,
             'pair_coherent_assignment_trials':0,'complement_clause_count_checks':0,
             'forbidden_cube_assignment_extensions':0,'full_formula_masks':0,
             'K4_signed_instances':0,'K4_brute_models_examined':0}
    for name,r in data['cases'].items():
        F=[tuple(c) for c in r['clauses']];n=r['n'];m=len(F)
        checked['cases']+=1
        assert m==r['m'] and n==nvars(F)
        for j,c in enumerate(F):
            entry=r['per_original_clause_S_U_and_inversions'][j]
            assert entry['j']==j and tuple(entry['clause'])==c
            for l,entry_ in zip(c,entry['occurrences']):
                checked['indexed_source_occurrences']+=1
                assert entry_['variable']==abs(l)
                assert entry_['S_all_true']==int(l>0)
                assert entry_['invert_S_to_U']==int(l<0)
                assert entry_['U_all_false']==int(l<0)
                assert entry_['invert_U_to_S']==int(l>0)
        assert len(r['original_indexed_SS_SU_US_UU'])==m*(m-1)//2
        for row in r['original_indexed_SS_SU_US_UU']:
            j,k=row['source_clause_indices'];supp=sorted(set(map(abs,F[j]+F[k])))
            for mode in ('SS','SU','US','UU'):
                exists=False
                for bits in product((0,1),repeat=len(supp)):
                    checked['pair_coherent_assignment_trials']+=1
                    vals=dict(zip(supp,bits))
                    if all(vals[abs(l)]==int((l>0)==(mode[0]=='S')) for l in F[j]) and \
                       all(vals[abs(l)]==int((l>0)==(mode[1]=='S')) for l in F[k]):
                        exists=True;break
                assert exists==row[mode],(name,j,k,mode)
                checked['pair_modes']+=1
        # A proven forbidden resolvent cube has opposite units in ORIGINAL parents.
        for rule in r['source_proved_forbidden_cubes']:
            j,k=rule['parents'];pivot=rule['pivot']
            cube={int(v):int(z) for v,z in rule['forbidden_partial_cube'].items()}
            assert pivot not in cube and set(rule['resolvent'])==(
                set(F[j])|set(F[k]))-{pivot,-pivot}
            assert (pivot in F[j] and -pivot in F[k]) or (-pivot in F[j] and pivot in F[k])
            for c in (F[j],F[k]):
                assert all(abs(l)==pivot or cube[abs(l)]!=int(l>0) for l in c)
            for a in range(1<<n):
                if all((a>>(v-1)&1)==z for v,z in cube.items()):
                    checked['forbidden_cube_assignment_extensions']+=1
                    assert not model(F,a)
        # Independent exhaustive SAT/UNSAT verification for n<=15.
        if n<=15:
            sat=False
            for a in range(1<<n):
                ct=counts(F,a)
                assert ct==[3-x for x in counts(F,a^((1<<n)-1))]
                assert (0 not in ct)==model(F,a)
                checked['complement_clause_count_checks']+=len(F)
                checked['full_formula_masks']+=1
                sat|=0 not in ct
            assert sat==r['baseline']['sat']==r['lean']['sat']==r['full']['sat']==r['portfolio']['sat']
        for style in ('baseline','lean','full','portfolio'):
            w=r[style]['witness']
            if w is not None:assert model(F,w)
        for witness in r['mixed_pair_ordinary_SAT_witnesses']:
            j,k=witness['clauses']
            ass={int(v):int(z) for v,z in witness['partial_original_variable_assignment'].items()}
            assert all(sum(ass[abs(l)]==int(l>0) for l in F[idx])
                       ==cnt for idx,cnt in zip((j,k),witness['true_literals_in_each_clause']))
            assert all(v in (1,2,3) for v in witness['true_literals_in_each_clause'])
    # Independent brute-force ground truth for all signed K4 incidences.
    edges=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    incid=[(j,i) for j in range(4) for i,(u,v) in enumerate(edges,1) if j in (u,v)]
    assert len(incid)==12
    for signs in range(1<<12):
        clauses=[[] for _ in range(4)]
        for pos,(j,i) in enumerate(incid):clauses[j].append(-i if signs>>pos&1 else i)
        F=[tuple(c) for c in clauses]+[tuple(-l for l in c) for c in clauses]
        found=False
        for a in range(64):
            checked['K4_brute_models_examined']+=1
            if model(F,a):found=True;break
        assert found,signs
        checked['K4_signed_instances']+=1
    assert checked['K4_signed_instances']==data['exhaustive_K4_sign_controls']['all_signed_incidence_patterns']
    assert all(data['cases'][name]['baseline']['sat'] for name in data['cases'] if 'signed_' in name)
    return checked

if __name__=='__main__':
    path=Path(sys.argv[1]);results=independent_audit(path)
    summary={'source':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
             'independent_checks':'PASS','counts':results}
    print(json.dumps(summary,sort_keys=True,indent=2))
