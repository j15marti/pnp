#!/usr/bin/env python3
"""Validate repeated-root Hasse jets for synchronous exterior kernels.

Status: COMPUTATIONAL.  This is a toy repeated-root validation for N=2^nu.
It is not the exact source-transcribed SU/vMS label word.
"""
import json, math, random

def bp(n,k): return (math.comb(n,k)&1) if 0<=k<=n else 0
def rank(rows,n):
    rows=rows[:]; r=0
    for c in range(n):
        p=next((i for i in range(r,len(rows)) if (rows[i]>>c)&1),None)
        if p is None: continue
        rows[r],rows[p]=rows[p],rows[r]
        for i in range(len(rows)):
            if i!=r and ((rows[i]>>c)&1): rows[i]^=rows[r]
        r+=1
    return r
def conv(a,b,N):
    y=0
    for i in range(N):
        if (a>>i)&1:
            for j in range(N):
                if (b>>j)&1: y^=1<<((i+j)%N)
    return y
def jet(a,N):
    return sum(((sum(((a>>i)&1)*bp(i,r) for i in range(N))&1)<<r) for r in range(N))
def jmul(a,b,N):
    y=0
    for r in range(N):
        if (a>>r)&1:
            for s in range(N-r):
                if (b>>s)&1:y^=1<<(r+s)
    return y
def hwords(N,m,k,b):
    h={}; ch=0
    for r in range(k):
      for t in range(r+1,k):
        for d in range(1,m):
          w=0
          for s in range(N):
            v=b[s][r]*b[(s+d)%N][t]^b[s][t]*b[(s+d)%N][r]
            w|=v<<s
          h[ch,d]=w
        ch+=1
    return h
def op_rank(N,m,k,h,use_jets):
    dom=[(d,i) for d in range(1,m) for i in range(m-d)]
    C=k*(k-1)//2; rows=[0]*(C*N)
    H={(c,d):jet(h[c,d],N) for c in range(C) for d in range(1,m)} if use_jets else h
    for col,(d,i) in enumerate(dom):
      q=1<<((-i)%N) # DIAGCONV correlation reversal
      if use_jets:q=jet(q,N)
      for c in range(C):
        y=jmul(q,H[c,d],N) if use_jets else conv(q,H[c,d],N)
        for s in range(N):
          if (y>>s)&1: rows[c*N+s]|=1<<col
    return rank(rows,len(dom))
def wedge_rank(N,m,k,b):
    P=[(i,j) for i in range(m) for j in range(i+1,m)]; rows=[]
    for s in range(N):
      C=[[b[(s+i)%N][r] for i in range(m)] for r in range(k)]
      for r in range(k):
       for t in range(r+1,k):
        w=0
        for a,(i,j) in enumerate(P):
          w|=((C[r][i]*C[t][j]^C[r][j]*C[t][i])<<a)
        rows.append(w)
    return rank(rows,len(P))
def check_case(N,m,k,exhaustive=False,trials=100,seed=271828):
    rng=random.Random(seed+100*N+10*m+k)
    masks=range(1<<(N*k)) if exhaustive else [rng.randrange(1<<(N*k)) for _ in range(trials)]
    dist={}; count=0
    for mask in masks:
      b=[[(mask>>(s*k+r))&1 for r in range(k)] for s in range(N)]
      h=hwords(N,m,k,b); a=wedge_rank(N,m,k,b)
      x=op_rank(N,m,k,h,False); y=op_rank(N,m,k,h,True)
      assert a==x==y,(N,m,k,mask,a,x,y)
      dist[str(a)]=dist.get(str(a),0)+1; count+=1
    return {"N":N,"m":m,"k":k,"mode":"exhaustive" if exhaustive else "random",
            "samples":count,"rank_distribution":dist,"all_three_ranks_equal":True}
def main():
    for N in (2,4,8):
      assert rank([sum(bp(i,r)<<i for i in range(N)) for r in range(N)],N)==N
      for a in range(1<<N):
        for b in range(1<<N):
          assert jet(conv(a,b,N),N)==jmul(jet(a,N),jet(b,N),N)
    out={"status":"COMPUTATIONAL","seed":271828,
         "model":"binary repeated-root cyclic toy validation; N=2^nu, unique root 1",
         "identity":"Hasse jet conjugates cyclic convolution to multiplication in F2[epsilon]/(epsilon^N)",
         "convolution_exhaustive_N":[2,4,8],
         "cases":[check_case(4,3,2,True),check_case(4,4,2,True),check_case(4,4,3,True),
                  check_case(8,4,2),check_case(8,5,3),check_case(8,6,4)],
         "limitations":["Not the source-transcribed reconstruction-compatible SU/vMS word.",
                        "N0=1 only; extension-field roots for N0>1 are not implemented.",
                        "Finite computation does not prove asymptotic exterior rank."]}
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
