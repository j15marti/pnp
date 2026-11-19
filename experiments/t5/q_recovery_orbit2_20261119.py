import itertools as I,json,random,hashlib,time,tracemalloc
from collections import Counter
from pathlib import Path
W=({1,3},{2,4},{0,3},{1,4},{0,2})
def Q(h,a,b):return (a in W[h])!=(b in W[h])
def key(row):
 d={};return tuple(d.setdefault(a,len(d)) for a in row)
def graphsolve(n,E,row,C):
 for suffix in I.product(range(5),repeat=n-len(row)):
  C['tail_candidates']+=1;a=tuple(row)+suffix;ok=True
  for u,v in E:
   C['edge_checks']+=1
   if a[u]==a[v]:ok=False;break
  if ok:return a
 return None
def lift(a,E,C):
 H=[]
 for u,v in E:
  for h in range(5):
   C['head_trials']+=1
   if Q(h,a[u],a[v]):H.append(h);break
  else:raise AssertionError('improper tails')
 for h,(u,v) in zip(H,E):
  C['source_Q_verifications']+=1;assert Q(h,a[u],a[v])
 return H
def run_case(n,E,r):
 cache={};C=Counter();rows=[]
 for row in I.product(range(5),repeat=r):
  C['rows']+=1;k=key(row)
  if k not in cache:
   C['child_calls']+=1;cache[k]=graphsolve(n,E,k,C)
  else:C['cache_hits']+=1
  a=cache[k];direct=graphsolve(n,E,row,C)
  assert (a is None)==(direct is None)
  if a is not None:
   d=dict(zip(k,row));unused=iter(c for c in range(5) if c not in d.values())
   for c in range(5):
    if c not in d:d[c]=next(unused)
   actual=tuple(d[c] for c in a);assert actual[:r]==row
   H=lift(actual,E,C)
   rows.append({'row':row,'key':k,'tails':actual,'heads':H})
  else:rows.append({'row':row,'key':k,'tails':None})
 return {'n':n,'edges':E,'boundary_size':r,'counters_including_direct_audit':dict(C),'rows':rows}
t=time.perf_counter();rng=random.Random(20261119001);cases=[]
for i in range(16):
 E=[e for e in I.combinations(range(5),2) if rng.random()<.5]
 cases.append(run_case(5,E,3))
E=list(I.combinations(range(6),2));cases.append(run_case(6,E,2))
for i in range(len(E)):cases.append(run_case(6,E[:i]+E[i+1:],2))
# Exact finite counterexamples against overbroad reuse.
triples=list(I.product(range(5),repeat=3));perms=list(I.permutations(range(5)))
bad=next(({'triple':t,'permutation':p,'image':tuple(p[a] for a in t)} for t in triples if Q(*t) for p in perms if not Q(*(p[a] for a in t))))
weights=[[sum(Q(h,a,b) for h in range(5)) for b in range(5)] for a in range(5)]
assert weights[0][1]==4 and weights[0][2]==2
counts={}
for r in range(9):
 counts[r]=len({key(a) for a in I.product(range(5),repeat=r)})
archive=Path('/workspace/scratch/a3c04269c151/evidence/T5_Exact_One_Experiments_2026-11-18.zip')
root=archive.parent/'unpacked/t5_exact_one';manifest=json.loads((root/'SHA256SUMS.json').read_text())
assert all(hashlib.sha256((root/p).read_bytes()).hexdigest()==h for p,h in manifest.items())
tracemalloc.start();measured=run_case(5,[(0,1),(1,2),(2,3),(3,4),(4,0)],3);peak=tracemalloc.get_traced_memory()[1];tracemalloc.stop()
out={'seed':20261119001,'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'manifest_files_verified':len(manifest),'Q_count':sum(Q(*t) for t in triples),'P_count':sum(t[1] in W[t[0]] and t[2] in W[t[0]] for t in triples),'cases':cases,'invalid_whole_witness_permutation':bad,'private_head_weights':weights,'partition_counts':counts,'wall_seconds_including_audits':time.perf_counter()-t,'peak_python_bytes_one_C5_case':peak,'peak_scope':'Includes cache, all rows, witnesses and direct comparison enumeration in a separate C5 call; excludes earlier cases and JSON serialization. Not a RAM space bound.'}
print(json.dumps(out,indent=2))
