#!/usr/bin/env python3
"""Finite full-function-class antichecker countercontrol; NOT a proof of B3."""
import itertools,json,hashlib,pathlib
FORMS=[[[1]],[[-1]],[[1],[-1]],[[1,2]],[[-1,-2]],[[1,2],[-1]],[[1,2],[-1],[-2]],[[1,2],[-1,-2]]]
def validate(f):
 if not isinstance(f,list) or not f: raise ValueError('not nonempty CNF')
 for c in f:
  if not isinstance(c,list) or not c: raise ValueError('empty/malformed clause')
  for lit in c:
   if type(lit)!=int or not 1<=abs(lit)<=2: raise ValueError('malformed literal')
def sat(f):
 validate(f)
 return any(all(any(((a>>(abs(l)-1))&1)==int(l>0) for l in c) for c in f) for a in range(4))
labels=[int(sat(f)) for f in FORMS]
assert 0 in labels and 1 in labels
full=range(8)
functions=list(itertools.product((0,1),repeat=8))
assert len(functions)==256
truth=tuple(labels)
assert sum(g==truth for g in functions)==1
checks=3
rows=[]
for omit in full:
 subset=[i for i in full if i!=omit]
 candidate=tuple(truth[i]^(i==omit) for i in full)
 assert candidate!=truth
 assert all(candidate[i]==truth[i] for i in subset)
 assert candidate[omit]!=truth[omit]
 assert sum(1 for g in functions if all(g[i]==truth[i] for i in subset))==2
 checks+=4
 rows.append({'omitted_index':omit,'sample_indices':subset,'flipped_classifier':list(candidate),'candidate_wrong_on_omitted':True,'classifiers_agree_on_sample':2})
for mask in range(1<<8):
 observed=[i for i in full if mask>>i&1]
 indistinguishable=[g for g in functions if g!=truth and all(g[i]==truth[i] for i in observed)]
 assert bool(indistinguishable)==(len(observed)<8)
 checks+=1
assert len([g for g in functions if all(g[i]==truth[i] for i in full)])==1
checks+=1
for bad in [None,[],[[0]],[[3]],[[True]],[[1.0]],'[[1]]',[[1,3]],[[1],[]]]:
 try: sat(bad)
 except (ValueError,TypeError): checks+=1
 else: raise AssertionError(f'invalid passed: {bad!r}')
res={'artifact':'LSPV1_406_ANTICHECKER_REFLECTION_CONDITIONAL','status':'COMPUTATIONAL finite antichecker controls; symbolic conditional corollary separately proved from Pich-Santhanam Theorem 10 and REFEREE350','source_count':8,'models_per_formula':4,'sat_labels':labels,'all_classifiers':256,'proper_subset_masks':255,'proper_subset_antichecker_exists':False,'full_sample_distinguishes_exact_truth_table':True,'mutation_records':rows,'malformed_rejections':9,'assertion_groups':checks,'scope':'All Boolean functions on eight distinct CNF inputs; unrestricted hypothesis class. No proof-system or SAT asymptotic assertion.'}
p=pathlib.Path('results/raw/arc/2026-11-04_1905_LSPV1_FEASIBLE_ANTICHECKER_B3_406.json')
p.parent.mkdir(parents=True,exist_ok=True)
p.write_text(json.dumps(res,indent=2,ensure_ascii=True)+'\n')
print(json.dumps({'result':str(p),'checks':checks,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'labels':labels}))
