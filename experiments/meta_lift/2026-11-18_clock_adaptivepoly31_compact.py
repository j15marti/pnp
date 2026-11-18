"""CLOCKADAPTIVEPOLY31 compact finite reproducer, stdlib Python 3.9+."""
from itertools import combinations

def transcript(x):
    p=x&1
    j=1 if p else 2
    return ((0,p),(j,(x>>j)&1))

def features(x,t):
    # Distinct selected source-bit polynomials on four or more truth-table entries.
    if t[0][1]:
        return ((x>>3)&1, int((x&48)==48))  # degree 1 and 2
    return (((x>>4)&1)^((x>>5)&1), (x>>6)&1) # degree 1 and 1

def label(x):
    t=transcript(x)
    u,v=features(x,t)
    return (t, (u & v)^u^t[0][1])

def check():
    N=8; passed=0; max_sparse=0
    for f in range(1<<N):
        t=transcript(f); v=features(f,t)
        pins={i:a for i,a in t}
        unp=[i for i in range(N) if i not in pins]
        base=sum(a<<i for i,a in pins.items())
        D=3 if t[0][1] else 2
        witness=None
        for w in range(D+1):
            for pos in combinations(unp,w):
                g=base|sum(1<<i for i in pos)
                if features(g,t)==v:
                    witness=g;break
            if witness is not None:break
        assert witness is not None
        assert transcript(witness)==t
        assert label(witness)==label(f)
        assert witness.bit_count()<=len(pins)+D
        max_sparse=max(max_sparse,witness.bit_count())
        passed+=4
    print({'inputs':256,'assertions':passed,'failures':0,'max_sparse_weight':max_sparse})

if __name__=='__main__': check()
