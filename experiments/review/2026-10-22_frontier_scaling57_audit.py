"""FRONTIER-SCALING57: greedy clause-order source-frontier width of random 3CNF vs n.
Finite computational probe only. Each run < 30 s."""
import random, json, sys
def frontier(clauses, order):
    last = {}
    for pos, ci in enumerate(order):
        for v in clauses[ci]: last[v] = pos
    seen, live, w = set(), set(), 0
    for pos, ci in enumerate(order):
        for v in clauses[ci]: seen.add(v); live.add(v)
        w = max(w, len(live))
        live = {v for v in live if last[v] > pos}
    return w
def greedy(clauses):
    rem = set(range(len(clauses))); live=set(); order=[]
    cnt = {}
    for c in clauses:
        for v in c: cnt[v]=cnt.get(v,0)+1
    left = dict(cnt)
    while rem:
        best=min(rem,key=lambda i:(len(set(clauses[i])-live)-sum(1 for v in clauses[i] if left[v]==1),i))
        rem.remove(best); order.append(best)
        for v in clauses[best]: live.add(v); left[v]-=1
        live={v for v in live if left[v]>0}
    return order
res=[]
for n in [20,40,80,160,320]:
    ws=[]
    for seed in range(5):
        r=random.Random(seed*1000+n)
        m=int(4.26*n)
        cl=[tuple(r.sample(range(n),3)) for _ in range(m)]
        ws.append(frontier(cl,greedy(cl)))
    res.append({"n":n,"m":int(4.26*n),"greedy_width":ws,"mean_over_n":sum(ws)/len(ws)/n})
    print(res[-1],flush=True)
json.dump(res,open("experiments/review/2026-10-22_frontier_scaling57_raw.json","w"),indent=1)
