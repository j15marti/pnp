# Schur-square dimension control: random binary [n,k] code vs RM(1,m)-like and shortened/punctured variants.
import numpy as np, itertools, random
def rank2(M):
    M=M.copy()%2; r=0
    for c in range(M.shape[1]):
        p=[i for i in range(r,M.shape[0]) if M[i,c]]
        if not p: continue
        M[[r,p[0]]]=M[[p[0],r]]
        for i in range(M.shape[0]):
            if i!=r and M[i,c]: M[i]^=M[r]
        r+=1
        if r==M.shape[0]: break
    return r
def sq(G):
    k=G.shape[0]
    rows=[G[i]*G[j] for i in range(k) for j in range(i,k)]
    return rank2(np.array(rows,dtype=np.uint8))
rng=np.random.default_rng(1)
m=7;n=2**m
pts=np.array(list(itertools.product([0,1],repeat=m)),dtype=np.uint8)
def rm(r):
    mons=[c for d in range(r+1) for c in itertools.combinations(range(m),d)]
    return np.array([[int(all(p[i] for i in mn)) for p in pts] for mn in mons],dtype=np.uint8)
for r in (1,2):
    G=rm(r); k=G.shape[0]
    R=rng.integers(0,2,(k,n),dtype=np.uint8)
    print(f"RM({r},{m}) k={k} sq={sq(G)} | random [{n},{k}] sq={sq(R)} min(n,k(k+1)/2)={min(n,k*(k+1)//2)}")
    # puncture 20% coords
    keep=rng.permutation(n)[:int(.8*n)]
    print("  punctured 80%: RM",sq(G[:,keep]),"random",sq(R[:,keep]))
