#!/usr/bin/env python3
"""Reconcile existing double wrapper with resource interfaces.
Run alongside matched_double_wrapper.py: python wrapper_bound_match.py OUTPUT.json
Finite measurements are not asymptotic certificates. 25-second batch cap.
"""
import hashlib,json,signal,sys,time
from pathlib import Path
from functools import lru_cache
import matched_double_wrapper as w

def main():
 signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('split batch')))
 signal.alarm(25);start=time.perf_counter();rows=[]
 cases=list(w.cases()); expected=[w.reference(w.normalize(f)) for _,_,f in cases]
 def forbidden(*_):raise AssertionError('Reference used during production')
 w.reference=forbidden
 for (family,seed,f),want in zip(cases,expected):
  for mode in ('flat','separator_fast'):
   plan=w.inner(f,mode);nodes=plan['nodes'];m=plan['metrics']
   @lru_cache(None)
   def expanded(i):
    return 1+sum(expanded(j) for j in nodes[i].get('children',[]))
   # Counts hypothetical uncached complete traversal, not required actual work.
   expanded_count=expanded(plan['root'])
   answer,outer=w.outer(f,mode);assert answer==want
   root=nodes[plan['root']]['formula'];N=m['N_bits']
   rows.append(dict(family=family,seed=seed,mode=mode,answer=answer,
      N=N,target=m['target_bits'],max_leaf=m['max_leaf_bits'],leaf_count=m['leaf_count'],
      dag_nodes=m['dag_nodes'],expanded_full_visits=expanded_count,
      cache_reuses=m['cache_reuses'],source_root_formula_bits=w.size(root),
      stored_formula_bits=m['stored_formula_bits'],literal_visits=m['literal_visits'],
      separator_candidates=m['separator_candidates'],outer=outer))
 assert all(r['max_leaf']<=r['target'] for r in rows)
 data=dict(status='COMPUTATIONAL',formula_cases=len(cases),checks=len(rows),errors=0,
     seconds=time.perf_counter()-start,rows=rows,
     shared_cases=sum(r['cache_reuses']>0 for r in rows),
     zero_leaf_nonzero_work=sum(r['leaf_count']==0 and r['literal_visits']>0 for r in rows),
     root_retained_at_full_scale=sum(r['source_root_formula_bits']>=r['N'] for r in rows),
     source_sha256=hashlib.sha256(Path(w.__file__).read_bytes()).hexdigest(),
     runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     limitation='Counters omit hashing/sorting/allocation. Expanded visits are a comparison only. No measured resource is promoted to an asymptotic bound.')
 Path(sys.argv[1]).write_text(json.dumps(data,indent=2)+'\n')
 print({k:v for k,v in data.items() if k!='rows'})
 for r in rows:
  if r['family']=='planted_separator_bridges_0' and r['seed']==17:print(r)
if __name__=='__main__':main()
