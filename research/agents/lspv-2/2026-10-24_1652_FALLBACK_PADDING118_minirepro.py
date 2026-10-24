#!/usr/bin/env python3
"""FALLBACK-PADDING118 compact audit. Stdlib only. Not a cycle-accurate FLMV simulation.
Replicates 54 source labels, the chosen-policy grammar routes and dummy counts.
The full independently instrumented specialist solver remains in the local package.
"""
import itertools,random,collections,json
def bits(f):
 n=max((abs(l) for c in f for l in c),default=0);m=len(f)
 return (4*m+2)*max(1,(64*(n+m+1)-1).bit_length())
def sat(f):
 n=max((abs(l) for c in f for l in c),default=0)
 return any(all(any((a[abs(l)-1]==(l>0)) for l in c) for c in f)
            for a in itertools.product((False,True),repeat=n))
def xor(v,b):
 return [tuple(t if x==0 else -t for t,x in zip(v,row))
         for row in itertools.product((0,1),repeat=3) if sum(row)%2!=b]
def route(f):
 if all(len(c)<=2 for c in f):return '2SAT'
 if all(sum(l>0 for l in c)<=1 for c in f):return 'Horn'
 if all(sum(l<0 for l in c)<=1 for c in f):return 'dualHorn'
 groups=collections.defaultdict(list)
 for c in f:
  if len(c)!=3 or len({abs(l) for l in c})!=3:return 'fallback'
  groups[tuple(sorted(map(abs,c)))].append(c)
 if groups and all(len(cs)==4 and any(set(cs)==set(xor(v,b)) for b in (0,1)) for v,cs in groups.items()):
  return 'affine'
 return 'fallback'
def hard(q,unsat):
 patterns=list(itertools.product((-1,1),repeat=3)) if unsat else [(-1,-1,-1),(1,1,1)]
 f=[tuple((j+1)*p for j,p in enumerate(t)) for t in patterns]
 for i in range(q):
  a,b=4+2*i,5+2*i;f.extend([(1,a,b),(-1,-a,-b)])
 return f
def controls():
 return [([(1,-2),(-1,2),(1,)],True), ([(1,),(-1,)],False),
         ([(-1,-2,3),(1,),(2,)],True), ([(-1,-2,3),(1,),(2,),(-3,)],False),
         ([(1,2,-3),(-1,),(-2,)],True), ([(1,2,-3),(-1,),(-2,),(3,)],False),
         (xor((1,2,3),0)+xor((1,4,5),0)+xor((2,4,6),0)+xor((3,5,6),0),True),
         (xor((1,2,3),0)+xor((1,4,5),0)+xor((2,4,6),0)+xor((3,5,6),1),False)]
def main():
 rng=random.Random(202610240124)
 items=[(hard(q,b),not b) for q in (0,1,2,4,8) for b in (False,True)]
 items+=controls()
 for j in range(36):
  f=[tuple(rng.choice((-1,1))*v for v in rng.sample(range(1,5),3)) for _ in range(2+j%6)]
  items.append((f,None))
 counts=collections.Counter();saved=0;spent=0;baseline=0;labels=collections.Counter()
 for f,expected in items:
  actual=sat(f)
  if expected is not None:assert actual==expected
  labels['SAT' if actual else 'UNSAT']+=1
  name=route(f);counts[name]+=1
  N=bits(f);delay=N*N;baseline+=delay
  if name=='fallback':
   acc=0
   for i in range(delay):acc^=(i&1)
   spent+=delay
  else:saved+=delay
 assert len(items)==54 and labels=={'SAT':45,'UNSAT':9}
 assert counts=={'fallback':40,'2SAT':2,'Horn':5,'dualHorn':5,'affine':2}
 assert (baseline,spent,saved)==(6349564,5026320,1323244)
 print(json.dumps({'cases':len(items),'labels':dict(labels),'routes':dict(counts),
     'baseline_dummy_events':baseline,'executed_fallback_dummy_events':spent,
     'saved_dummy_events':saved,'failures':0,'scope':'finite computational model only'},sort_keys=True))
if __name__=='__main__':main()
