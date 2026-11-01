#!/usr/bin/env python3
"""Full six-variable exhaustive source-faithful WRAPPER structural audit."""
import itertools as it
import math
from collections import Counter

triples=list(it.combinations(range(1,7),3))
blocks=[q for q in it.combinations(triples,4)
        if all(sum(v in c for c in q)==2 for v in range(1,7))]
assert len(blocks)==75
checks=0; peak={1:0,2:0}

for pos in blocks:
 for neg in blocks:
  f=pos+tuple(tuple(-v for v in c) for c in neg)
  for b in (1,2):
   for selected in it.combinations(range(1,7),b):
    for bits in it.product((0,1),repeat=b):
     pin=dict(zip(selected,bits)); rows=[]; deleted=0; contradiction=False
     for c in f:
      if any(abs(v) in pin and pin[abs(v)] == (v>0) for v in c):
       deleted+=1
      else:
       row=[abs(v) for v in c if abs(v) not in pin]
       if row:rows.append(row)
       else:contradiction=True
     active={v for row in rows for v in row}
     vanished=6-b-len(active)
     assert vanished<=2*min(sum(bits),b-sum(bits))
     assert deleted<=2*b
     parents={v:v for v in active}
     def root(v):
      while parents[v]!=v:
       v=parents[v]
      return v
     for row in rows:
      for v in row[1:]:
       parents[root(v)]=root(row[0])
     sizes=Counter(root(v) for v in active)
     if not contradiction and sizes:
      assert len(sizes)<=1+5*b
      assert max(sizes.values())>=math.ceil((6-2*b)/(1+5*b))
      peak[b]=max(peak[b],len(sizes))
     checks+=1
assert checks==405000
print({'valid_sources':75**2,'cases':checks,'peak_components':peak,'pass':True})
