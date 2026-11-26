from ring import *
out=[]
for k in [5,7,9,17]:
 T,ps,colors=ring(k);r,s,w=solve(T,weighted=True,cap=0);assert r=='YES' and s['pins']==0 and s['maxbag']==k
 out.append(dict(k=k,tuples=len(T),result=r,**s));print(out[-1],flush=True)
json.dump(out,open('weighted_ring_results.json','w'),indent=2)
