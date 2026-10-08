#!/usr/bin/env python3
"""Exact source-checked parity-star coverage repair; 25-second cap."""
import importlib.util,itertools,json,hashlib,signal,time,sys
from pathlib import Path
signal.signal(signal.SIGALRM,lambda *_: (_ for _ in ()).throw(TimeoutError('25s')))
signal.alarm(25)
start=time.monotonic()
source=Path(__file__).with_name('2026-10-08_2110_ARC-STRENGTHEN2-original-portfolio.py')
spec=importlib.util.spec_from_file_location('old_portfolio',source)
old=importlib.util.module_from_spec(spec);sys.modules[spec.name]=old;spec.loader.exec_module(old)
def parity(triple,b):
 return tuple(tuple(-v if bit else v for v,bit in zip(triple,bits)) for bits in itertools.product((0,1),repeat=3) if sum(bits)%2!=b)
def star(bs):
 return tuple(c for i,b in enumerate(bs) for c in parity((1,2*i+2,2*i+3),b))
def key(c): return tuple(sorted(abs(v) for v in c))
def scan_star(f):
 # Source remains read-only. Repeated scans intentionally retain no group index.
 probes=0
 if not f:return True,probes
 if any(len(c)!=3 or len(set(map(abs,c)))!=3 for c in f):return None,probes
 valid=True
 for c in f:
  triple=key(c);mask=0
  for d in f:
   probes+=1
   if key(d)==triple:
    bad=sum((1<<j) for j,v in enumerate(triple) if -v in d)
    mask|=1<<bad
  if mask==255:return False,probes
  if mask not in (105,150):valid=False # even-/odd-parity assignment masks
 if not valid:return None,probes
 for hub in key(f[0]):
  ok=True
  for c in f:
   a=key(c)
   if hub not in a:ok=False;break
   for d in f:
    probes+=1;b=key(d)
    if a!=b and any(v!=hub and v in b for v in a):ok=False;break
   if not ok:break
  if ok:return True,probes
 return None,probes
rows=[];checks=0
for m in range(2,5):
 for bs in itertools.product((0,1),repeat=m):
  f=star(bs)
  for contradiction in (False,True):
   g=f+parity((1,2,3),1-bs[0]) if contradiction else f
   winner,plan,metrics=old.run_portfolio(g)
   assert winner is None and plan is None,(m,bs,contradiction,winner)
   value,probes=scan_star(g); truth=old.brute_sat(g)
   assert value==truth==(not contradiction)
   rows.append({'blocks':m,'parities':bs,'contradiction':contradiction,'old_attempts':metrics['attempts'],'old_restrictions':metrics['candidate_restrictions'],'new_clause_pair_probes':probes})
   checks+=1
# Exhaustive proper 3-CNF formulas on one triple; all SUCCESS answers checked.
clauses=parity((1,2,3),0)+parity((1,2,3),1)
for mask in range(256):
 f=tuple(c for j,c in enumerate(clauses) if mask>>j&1)
 answer,_=scan_star(f)
 if answer is not None:assert answer==old.brute_sat(f)
 checks+=1
# Reject incomplete block and non-star cyclic overlap rather than guessing.
assert scan_star(star((0,0))[:-1])[0] is None
assert scan_star(parity((1,2,3),0)+parity((1,4,5),0)+parity((2,4,6),0))[0] is None
# Renaming and complementation preserve accepted class and exact answers.
for m in range(2,5):
 f=star((0,)*m)
 for bits in itertools.product((0,1),repeat=2*m+1):
  g=tuple(tuple((100+7*abs(v))*(1 if (v>0)^bool(bits[abs(v)-1]) else -1) for v in c) for c in reversed(f))
  a,_=scan_star(g);assert a is True;checks+=1
signal.alarm(0)
print(json.dumps({'status':'COMPUTATIONAL','passed':True,'semantic_checks':checks,'old_portfolio_misses':len(rows),'controls':2,'rows':rows,'seconds':time.monotonic()-start,'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'authenticated_source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'limitations':['Python tuples/integers do not certify the stated read-only bit-machine space implementation.','Exact recognized family only, no universal coverage or strict global ARC transition.']},indent=2))
