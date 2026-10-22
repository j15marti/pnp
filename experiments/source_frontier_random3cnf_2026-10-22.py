import random, json, sys
def inst(n, r, seed):
    rng = random.Random(seed)
    return [tuple(rng.sample(range(n),3)) for _ in range(int(r*n))]
def frontier(cl, order):
    last = {}; first = {}
    for i,c in enumerate(order):
        for v in cl[c]:
            first.setdefault(v,i); last[v]=i
    w=0
    for i in range(len(order)):
        w=max(w,sum(1 for v in first if first[v]<=i<last[v]))
    return w
def greedy(cl):
    n=len(cl); rem=set(range(n)); live=set(); order=[]
    cnt={}
    for c in cl:
        for v in c: cnt[v]=cnt.get(v,0)+1
    seen={}
    while rem:
        def cost(c):
            new=sum(1 for v in cl[c] if v not in live)
            done=sum(1 for v in cl[c] if seen.get(v,0)+1==cnt[v])
            return new-done
        c=min(rem,key=lambda c:(cost(c),c)); rem.discard(c); order.append(c)
        for v in cl[c]:
            seen[v]=seen.get(v,0)+1; live.add(v)
            if seen[v]==cnt[v]: live.discard(v)
    return order
res=[]
for n in (20,40,80,160):
    ws=[]
    for s in range(5):
        cl=inst(n,4.26,s); ws.append(frontier(cl,greedy(cl)))
    res.append({"n":n,"m":int(4.26*n),"greedy_frontier":ws,"mean":sum(ws)/len(ws),"ratio":sum(ws)/len(ws)/n})
    print(res[-1])
json.dump(res,open(sys.argv[1],"w"),indent=1)
