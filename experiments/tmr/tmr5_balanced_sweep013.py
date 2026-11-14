from itertools import combinations
from collections import Counter
from math import comb
import json,time
start=time.monotonic()
cols=list(combinations(range(8),4))
result={'balanced_tuples':0,'balanced_sat_tuples':0,'balanced_unsat_tuples':0}
dist=Counter(); extremes={}; hist_structure=Counter()
for c0 in cols:
    b0=sum(1<<r for r in c0)
    for c1 in cols:
        b1=sum(1<<r for r in c1)
        for c2 in cols:
            b2=sum(1<<r for r in c2)
            a=[(b0>>r&1)|(b1>>r&1)<<1|(b2>>r&1)<<2 for r in range(8)]
            co=Counter(a)
            result['balanced_tuples']+=1
            if len(co)==8:
                result['balanced_unsat_tuples']+=1
                continue
            result['balanced_sat_tuples']+=1
            d=sum(n*(n-1)//2 for n in co.values())
            t=0
            for J in [(0,1),(0,2),(1,2)]:
                pr=Counter(tuple(v>>j&1 for j in J) for v in a)
                t+=sum(n*(n-1)*(n-2)//6 for n in pr.values())
            s=d+t
            dist[s]+=1
            if s not in extremes:extremes[s]={'tuple':a,'duplicate_pairs':d,'triple_projections':t}
            hist_structure[tuple(sorted(co.values()))]+=1
result.update({'min_certs':min(dist),'max_certs':max(dist),'distribution':dict(sorted(dist.items())),
              'representatives_min':extremes[min(dist)],'representatives_max':extremes[max(dist)],
              'structure_distribution':{str(k):v for k,v in hist_structure.items()},
              'elapsed_seconds':round(time.monotonic()-start,3)})
print(json.dumps(result,indent=2,sort_keys=True))
