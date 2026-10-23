import sys,time,json
n=int(sys.argv[1]); G=int(sys.argv[2]); T=float(sys.argv[3])
N=1<<n; M=(1<<N)-1
ins=[]
for i in range(n):
    t=0
    for x in range(N):
        if x>>i&1: t|=1<<x
    ins.append(t)
# best[f]=(gates,wires) minimal gates (then wires) found; BFS over states (frozenset of non-input tables w/ cost)
t0=time.time()
best={}
for t in ins+[0,M]: best[t]=(0,0)
start=frozenset()
level={start:0}  # state -> wires
seen={start}
for g in range(1,G+1):
    new={}
    for st,w in level.items():
        avail=list(ins)+sorted(st)
        cands=set()
        for a in avail: cands.add((M^a,1))
        for i,a in enumerate(avail):
            for b in avail[i+1:]:
                cands.add((a&b,2)); cands.add((a|b,2))
        for f,c in cands:
            if f in avail or f in (0,M): continue
            s2=st|{f}
            if s2 in new and new[s2]<=w+c: continue
            new[s2]=w+c if s2 not in new else min(new[s2],w+c)
        if time.time()-t0>T: print("timeout at gate",g);break
    for s,w in new.items():
        for f in s:
            if f not in best or (g,w)<best[f]: best[f]=(g,w)
    level=new
    print(g,len(level),len(best),round(time.time()-t0,1),flush=True)
    if time.time()-t0>T: break
json.dump({str(k):v for k,v in best.items()},open(f"lad{n}.json","w"))
print("covered",len(best),"of",1<<N)
if n==2:
  for k,v in sorted(best.items()): print(format(k,'04b'),v)
