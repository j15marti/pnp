#!/usr/bin/env python3
"""Offline complete aligned source-logical state XOR, binary and Gray clause counts.
Comparison state is n original assignment bits plus each original clause's
2-bit true-literal count and 1-bit satisfied status. Not native tape writes.
"""
import json
from pathlib import Path
from collections import Counter
import k5_scc295 as P
R=Path(__file__).resolve().parent

def bits(F,a,gray):
 n=max(abs(l) for c in F for l in c)
 raw=[a[v] for v in range(1,n+1)]
 for c in F:
  t=sum(a[abs(x)]==int(x>0) for x in c)
  g=t^(t>>1) if gray else t
  raw.extend([g&1,(g>>1)&1,int(t>0)])
 return raw

def run(F):
 n=max(abs(l) for c in F for l in c)
 a={v:0 for v in range(1,n+1)};reports=[];totals=Counter()
 initial={mode:bits(F,a,mode=='gray') for mode in ('binary','gray')}
 prior={k:v[:] for k,v in initial.items()}
 touched=set();incidence=Counter(abs(l) for c in F for l in c)
 assert all(incidence[v]==4 for v in range(1,n+1))
 for step,v in enumerate(tuple(range(1,n+1))+tuple(range(n,0,-1)),1):
  before={k:prior[k] for k in prior}
  a[v]^=1
  changed=[j for j,c in enumerate(F) if any(abs(l)==v for l in c)]
  assert len(changed)==4
  touched.update(changed)
  counts={}
  for mode in ('binary','gray'):
   after=bits(F,a,mode=='gray')
   d=sum(x!=y for x,y in zip(prior[mode],after))
   totals[mode]+=d
   counts[mode]=d
   prior[mode]=after
  reports.append({'step':step,'flipped_original_variable':v,'changed_source_clause_ids':changed,'delta':counts})
 assert all(prior[k]==initial[k] for k in prior)
 return {'n':n,'m':len(F),'step_count':2*n,'source_incidence_occurrence_reads_if_materialized':3*len(F),
    'total_adjacent_logical_XOR':dict(totals),'endpoint_logical_XOR':{'binary':0,'gray':0},
    'source_clause_ids_touched':len(touched),'traces':reports}

def main():
 U,V=P.source198()
 Fs={'Y6':P.Y6,'F9':P.F9,'F15K5':P.K5,'U198':U,'V198':V}
 out={name:run(f) for name,f in Fs.items()}
 (R/'logical295.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({k:{x:v for x,v in a.items() if x!='traces'} for k,a in out.items()},indent=2))
if __name__=='__main__':main()
