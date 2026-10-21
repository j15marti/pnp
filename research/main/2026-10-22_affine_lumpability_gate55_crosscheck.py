"""Independent brute-force cross-check of Lemma 55A (affine lumpability over GF(2)).
Checks: [H x = H y => H A x = H A y for all x,y] <=> rank([H;HA]) == rank(H) <=> exists Q: HA = QH.
Runs in a few seconds (s<=6)."""
import itertools, random
random.seed(1)
def rank(rows):
    rows=[r for r in rows]; rk=0
    for bit in range(64):
        p=next((i for i in range(rk,len(rows)) if rows[i]>>bit&1),None)
        if p is None: continue
        rows[rk],rows[p]=rows[p],rows[rk]
        for i in range(len(rows)):
            if i!=rk and rows[i]>>bit&1: rows[i]^=rows[rk]
        rk+=1
    return rk
def par(x): return bin(x).count("1")&1
def apply(M,x,n): return sum(par(M[i]&x)<<i for i in range(n))  # M: list of row bitmasks
def trials(s,k,N):
    agree=0; lump=0
    for _ in range(N):
        A=[random.getrandbits(s) for _ in range(s)]
        H=[random.getrandbits(s) for _ in range(k)]
        brute=all(apply(H,apply(A,x,s),k)==apply(H,apply(A,y,s),k)
                  for x in range(1<<s) for y in range(x) if apply(H,x,k)==apply(H,y,k))
        # HA rows: row i of H times A = xor of A rows selected by H[i]
        HA=[]
        for h in H:
            r=0
            for j in range(s):
                if h>>j&1: r^=A[j]
            HA.append(r)
        crit = rank(H+HA)==rank(H)
        assert brute==crit,(A,H)
        agree+=1; lump+=brute
    return agree,lump
for s,k in [(3,1),(4,2),(5,2),(5,3),(6,3),(6,4)]:
    print(s,k,trials(s,k,150))
print("LEMMA55A_CROSSCHECK_OK")
