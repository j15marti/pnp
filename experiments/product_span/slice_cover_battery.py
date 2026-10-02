#!/usr/bin/env python3
"""Exact legal-slice cover battery for declared SU05/Hadamard LDE controls.

COMPUTATIONAL only. Extends vms_lde_hadamard_leaf.py from (R,d) to exact
minimum slice cover tau, greedy cover, and innovation sequence.
"""
import itertools,json,math
from pathlib import Path
ns={}
exec(Path("experiments/product_span/vms_lde_hadamard_leaf.py").read_text().replace('if __name__=="__main__":main()',''),ns)
lagrange_eval,primitive_root,bits=ns["lagrange_eval"],ns["primitive_root"],ns["bits"]

def add(B,x):
    y=x
    for p in sorted(B,reverse=True):
        if (y>>p)&1:y^=B[p]
    if not y:return False
    p=y.bit_length()-1
    for q in list(B):
        if (B[q]>>p)&1:B[q]^=y
    B[p]=y; return True
def basis(rows):
    B={}
    for x in rows:add(B,x)
    return B
def analyze(word,p,m):
    k=math.ceil(math.log2(p)); a=primitive_root(p); N=p-1
    labels=[bits(lagrange_eval(word,pow(a,t,p),p),k) for t in range(N)]
    slices=[]
    for s in range(N):
        cols=[sum(labels[(s+i)%N][j]<<i for i in range(m)) for j in range(k)]
        slices.append(list(basis(cols).values()))
    R=len(basis(x for S in slices for x in S))
    pairs=[(i,j) for i in range(m) for j in range(i+1,m)]
    wedges=[]
    for S in slices:
        for u in range(len(S)):
            for v in range(u+1,len(S)):
                x,y=S[u],S[v]; z=0
                for q,(i,j) in enumerate(pairs):
                    z|=((((x>>i)&1)*((y>>j)&1)^((x>>j)&1)*((y>>i)&1))<<q)
                wedges.append(z)
    d=len(basis(wedges))
    B={}; greedy=[]; innov=[]
    while len(B)<R:
        best=None
        for s,S in enumerate(slices):
            C=dict(B)
            for x in S:add(C,x)
            gain=len(C)-len(B)
            if best is None or gain>best[0]:best=(gain,s,C)
        if best[0]<=0:break
        innov.append(best[0]);greedy.append(best[1]);B=best[2]
    tau=None;cert=None
    for t in range(1,len(greedy)+1):
        for Q in itertools.combinations(range(N),t):
            B={}
            for s in Q:
                for x in slices[s]:add(B,x)
            if len(B)==R:tau=t;cert=Q;break
        if tau is not None:break
    return {"R":R,"d":d,"tau":tau,"greedy_tau":len(greedy),"innovation":innov,
            "cover_certificate":list(cert),"slice_rank_min":min(map(len,slices)),
            "slice_rank_max":max(map(len,slices))}
out=[]
for p,h,m in [(17,4,4),(29,5,5),(37,6,6),(43,7,7)]:
    dist={}
    for w in itertools.product([0,1],repeat=h):
        if len(set(w))==1:continue
        z=analyze(w,p,m)
        key=json.dumps({k:z[k] for k in ["R","d","tau","greedy_tau","innovation"]},sort_keys=True)
        if key not in dist:dist[key]={"count":0,"example":"".join(map(str,w)),"data":z}
        dist[key]["count"]+=1
    out.append({"p":p,"h":h,"m":m,"nonconstant":2**h-2,"patterns":list(dist.values())})
print(json.dumps({"status":"COMPUTATIONAL",
"realization":"axis-parallel canonical Boolean-grid LDE leaf + SU05 multiplicative orbit + standard binary label/Hadamard",
"cases":out,
"limitations":["finite controls","declared source-sanctioned realization, not author-unique vMS binary sampler","parameters do not satisfy vMS asymptotic p>=Delta^100"]},indent=2))
