#!/usr/bin/env python3
"""Independent truth table and original-source witness check of 54 controller outcomes."""
import json,pathlib,itertools
here=pathlib.Path(__file__).parent
D=json.loads((here/'decision.json').read_text());R=json.loads((here/'raw.json').read_text())['sources']
checks=0
for name,v in D.items():
 f=R[name]['source_clauses'];n=R[name]['n']
 truth=0
 for bits in itertools.product((0,1),repeat=n):
  if all(any(bits[abs(z)-1]==int(z>0) for z in c) for c in f):truth+=1
 assert v['models']==truth
 for tag,x in v['strategies'].items():
  assert (x['answer']=='SAT')==(truth>0)
  if x['witness'] is not None:
   a={int(k):b for k,b in x['witness'].items()}
   assert all(any(a[abs(z)]==int(z>0) for z in c) for c in f)
  else:assert truth==0
  assert x['events']>=x['stats'].get('guest_events',0)
  checks+=1
print(json.dumps({'original_source_decisions_checked':checks,'outcomes':'all match exhaustive oracle','complete_original_witnesses':'all checked'}))
