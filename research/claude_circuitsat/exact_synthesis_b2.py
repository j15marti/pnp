import sys,itertools,json,time
n=int(sys.argv[1]); N=1<<n; M=(1<<N)-1
ins=[sum(((x>>i)&1)<<x for x in range(N)) for i in range(n)]
# 16 binary ops as 4-bit tables; apply bitwise on truth tables
def ap(op,a,b):
    r=0
    if op&1: r|=~a&~b
    if op&2: r|=~a&b
    if op&4: r|=a&~b
    if op&8: r|=a&b
    return r&M
ops=range(1,15) # nonconstant; ops 0,15 const; 
best={0:0,M:0}
for t in ins: best[t]=0
def exp(state):
    s=list(state)
    for i in range(len(s)):
        for j in range(i+1,len(s)):
            for op in ops:
                yield ap(op,s[i],s[j])
states={tuple(sorted(ins))}
t0=time.time()
for g in range(1,6):
    new=set(); 
    last = (g==int(sys.argv[2]))
    for st in states:
        ss=set(st)
        for v in exp(st):
            if v not in best: best[v]=g
            if not last and v not in ss: new.add(tuple(sorted(ss|{v})))
    print(g,len(best),len(new),time.time()-t0,flush=True)
    if last: break
    states=new
from collections import Counter
print(sorted(Counter(best.values()).items()), 2**N)
json.dump({"n":n,"hist":sorted(Counter(best.values()).items()),"covered":len(best)},open(f"syn{n}.json","w"))
