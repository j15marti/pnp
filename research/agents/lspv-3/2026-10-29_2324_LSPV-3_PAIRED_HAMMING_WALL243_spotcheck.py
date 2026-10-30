"""Independent source-clause spotchecker for PAIRED-HAMMING-WALL243. stdlib only."""
import itertools
from math import comb

def family(k,bad):
    F=[]
    for i in range(k):
        a,b,c=3*i+1,3*i+2,3*i+3
        F.extend([(a,b,c),(-a,-b,-c)])
    F += [(3*i+1,3*i+4,3*i+5) for i in range(k-1)]
    if bad:
        for bits in itertools.product((0,1),repeat=3):
            c=tuple((j+1 if bit else -(j+1)) for j,bit in enumerate(bits))
            if c not in F:F.append(c)
    return F

def t(C,a):
    return sum(bool(a&(1<<(abs(l)-1)))==(l>0) for l in C)

def demands(C,mode):
    return {abs(l):(int(l>0) if mode=="S" else int(l<0)) for l in C}

def pair_ok(A,B,p,q):
    x=demands(A,p);y=demands(B,q)
    return all(x[v]==y[v] for v in x.keys()&y.keys())

def check(k,bad):
    F=family(k,bad);n=3*k;allbits=(1<<n)-1
    assert len(F)==3*k-1+(6 if bad else 0)
    for A,B in itertools.combinations(F,2):
        for p,q in itertools.product("SU",repeat=2):
            support=sorted(set(map(abs,A+B)))
            brute=any((t(A,a)==(3 if p=="S" else 0) and t(B,a)==(3 if q=="S" else 0))
                for values in itertools.product((0,1),repeat=len(support))
                for a in [sum(bit<<(v-1) for v,bit in zip(support,values))])
            assert pair_ok(A,B,p,q)==brute
    models=[]
    for a in range(1<<n):
        assert all(t(C,a)+t(C,allbits^a)==3 for C in F)
        good=all(t(C,a)>0 for C in F)
        if a.bit_count()<k or n-a.bit_count()<k:assert not good
        if good:models.append(a)
    assert bool(models)==(not bad)
    if not bad:
        model=sum(1<<(3*i) for i in range(k))
        assert model in models and (allbits^model) in models
    else:
        for bits in itertools.product((0,1),repeat=3):
            a=sum(bit<<j for j,bit in enumerate(bits))
            assert any(t(C,a)==0 and set(map(abs,C))=={1,2,3} for C in F)
    return (k,bad,len(models),sum(comb(n,h) for h in range(k)))

if __name__=="__main__":
    for k in (2,3,4):
        for bad in (False,True):print(check(k,bad))
