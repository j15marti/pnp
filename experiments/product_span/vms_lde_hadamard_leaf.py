#!/usr/bin/env python3
"""Source-typed LDE-line battery for the declared SU05/Hadamard realization.

Build canonical tensor-grid low-degree extensions over F_p, restrict to an
axis-parallel RMV leaf, and evaluate the SU05 multiplicative orbit with a
standard binary integer label + Hadamard masks.

COMPUTATIONAL only. This is a declared source-sanctioned realization, not a
claim that vMS uniquely fixes the SU05 internal encoder/matrix.
"""
import argparse,json,itertools,math,random

def inv(a,p): return pow(a,p-2,p)
def lagrange_eval(vals,x,p):
    h=len(vals); out=0
    for i,yi in enumerate(vals):
        num=den=1
        for j in range(h):
            if i!=j: num=num*(x-j)%p; den=den*(i-j)%p
        out=(out+yi*num*inv(den,p))%p
    return out
def bits(x,k): return [(x>>j)&1 for j in range(k)]
def primitive_root(p):
    phi=p-1; fac=[]; n=phi; q=2
    while q*q<=n:
        if n%q==0:
            fac.append(q)
            while n%q==0:n//=q
        q+=1
    if n>1:fac.append(n)
    for g in range(2,p):
        if all(pow(g,phi//q,p)!=1 for q in fac): return g
def rank(rows,n):
    rows=rows[:]; r=0
    for c in range(n):
        q=next((i for i in range(r,len(rows)) if (rows[i]>>c)&1),None)
        if q is None:continue
        rows[r],rows[q]=rows[q],rows[r]
        for i in range(len(rows)):
            if i!=r and ((rows[i]>>c)&1):rows[i]^=rows[r]
        r+=1
    return r
def ranks(word,p,m):
    k=math.ceil(math.log2(p)); a=primitive_root(p); N=p-1
    labels=[bits(lagrange_eval(word,pow(a,t,p),p),k) for t in range(N)]
    lin=[]; wed=[]; pairs=[(i,j) for i in range(m) for j in range(i+1,m)]
    for s in range(N):
        cols=[[labels[(s+i)%N][j] for i in range(m)] for j in range(k)]
        for c in cols: lin.append(sum(v<<i for i,v in enumerate(c)))
        for u in range(k):
          for v in range(u+1,k):
            row=0
            for q,(i,j) in enumerate(pairs):
                row|=((cols[u][i]*cols[v][j]^cols[u][j]*cols[v][i])<<q)
            wed.append(row)
    return {"linear_rank":rank(lin,m),"exterior_rank":rank(wed,len(pairs)),
            "linear_max":m,"exterior_max":len(pairs),"orbit_N":N,"label_bits":k,"primitive_root":a}
def main():
    ap=argparse.ArgumentParser();ap.add_argument("--seed",type=int,default=314159);args=ap.parse_args()
    rng=random.Random(args.seed); cases=[]
    for p,h,m in [(17,4,4),(29,5,5),(37,6,6),(43,7,7)]:
        words=[]
        if h<=6:
            words=list(itertools.product([0,1],repeat=h))
        else:
            words=[tuple([0]*h),tuple([1]*h),tuple([1]+[0]*(h-1)),
                   tuple(i%2 for i in range(h))]+[tuple(rng.randrange(2) for _ in range(h)) for _ in range(60)]
        dist={}; bad=[]; nonconst=0
        for w in words:
            z=ranks(w,p,m); key=f"{z['linear_rank']},{z['exterior_rank']}"
            dist[key]=dist.get(key,0)+1
            if len(set(w))>1:
                nonconst+=1
                if z["exterior_rank"]<z["exterior_max"]:bad.append({"word":"".join(map(str,w)),**z})
        cases.append({"p":p,"h":h,"m":m,"samples":len(words),"nonconstant":nonconst,
                      "rank_distribution":dist,"nonconstant_exterior_deficient":bad})
    print(json.dumps({"status":"COMPUTATIONAL","seed":args.seed,
      "realization":"axis-parallel canonical Boolean-grid LDE leaf + SU05 multiplicative orbit + standard binary label/Hadamard",
      "cases":cases,
      "limitations":["Finite leaf-level controls, not full higher-dimensional vMS PCPP instance.",
       "Uses a declared SU05/Hadamard realization; vMS Lemma 4.2 does not uniquely spell out the internal bit-level implementation.",
       "Small p,h are parameter-scaled controls and do not satisfy vMS asymptotic p >= Delta^100." ]},indent=2,sort_keys=True))
if __name__=="__main__":main()
