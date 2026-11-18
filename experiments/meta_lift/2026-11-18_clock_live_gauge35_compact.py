#!/usr/bin/env python3
"""Independent finite dynamic-programming control for LIVE-BASELINE-SECTION35."""
import json,random,itertools
R=random.Random(202611180430)
checks=0;models=0

def audit(tr,h,check_all=False):
    global checks,models
    k=len(tr[0][0]);n=len(tr)
    live=[{0}]
    for z,o in tr:
        live.append({m[s] for s in live[-1] for m in (z,o)})
    defects=sum(len({tr[i][h[i]][s] for s in live[i]})<len(live[i]) for i in range(n))
    dp={0:0}
    for i,(z,o) in enumerate(tr):
        nxt={}
        for s,c in dp.items():
            for b,m in enumerate((z,o)):
                t=m[s];nxt[t]=min(nxt.get(t,n+1),c+(b!=h[i]))
        dp=nxt
    assert set(dp)==live[-1]
    bound=(defects+1)*(k-1)+defects
    assert all(d<=bound for d in dp.values()),(k,n,defects,dp)
    checks+=len(dp)
    if check_all:
        ends=set()
        for w in itertools.product((0,1),repeat=n):
            p=0
            for (z,o),b in zip(tr,w):p=(z,o)[b][p]
            ends.add(p);checks+=1
        assert ends==set(dp)
    models+=1
    return defects,dp

# Strict improvement: global nonpermutation at every address, live defects absent.
def moving(n):
    tr=[((1,1,1),(2,1,1))]
    for i in range(1,n):
        tr.append(((0,0,1),(0,1,0)) if i%2 else ((1,2,1),(2,1,1)))
    return tr
n=8;tr=moving(n)
assert audit(tr,[0]*n,True)[0]==0
assert all(len(set(z))<3 for z,o in tr)

# False proposed terminal-trimmed/baseline-only erasure: 1^N unique accepted word.
tr=[((1,1),(0,1)) for _ in range(n)]
assert audit(tr,[0]*n,True)[0]==n-1
assert audit(tr,[1]*n,True)[0]==0
assert all(len({tr[i][0][1]})==1 for i in range(n))

for _ in range(120):
    k=R.randint(2,5);n=R.choice((6,8,10))
    tr=[tuple(tuple(R.randrange(k) for _ in range(k)) for b in range(2)) for i in range(n)]
    h=[R.randrange(2) for i in range(n)]
    audit(tr,h,True)
print(json.dumps({"model":"live-injective section DP independent control","seed":202611180430,"models":models,"checks":checks,"failures":0},sort_keys=True))
