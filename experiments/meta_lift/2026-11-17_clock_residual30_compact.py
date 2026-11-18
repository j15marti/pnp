"""Compact independent CLOCKRESIDUAL30 reproducer. Python >=3.9."""
from math import ceil, log2

def words_upto(k):
    return ''.join(format(j, '0%db'%r) for r in range(1, k+1) for j in range(1<<r))

def schedule(N):
    k=1
    while (k-1)*(1<<(k+1))+2<N: k+=1
    return words_upto(k)[:N]

def grammar_factor_lower(N):
    n=N.bit_length()-1
    k=n-ceil(log2(n))-3
    if k<2: return None
    s=schedule(N)
    F={s[i:i+k] for i in range(N-k+1)}
    assert (k-1)*(1<<(k+1))+2<=N
    assert len(F)>=1<<k
    return (k, len(F), ceil(len(F)/(k-1)))

def H(f,s):
    t=(''.join(str(1-int(c)) for c in s))
    u=''.join(('1' if c=='0' else '0') if j<2 else c for j,c in enumerate(s))
    return int(f in {s,t,u})

def run():
    tests=0
    for n in (2,3,4):
        N=1<<n;s=schedule(N);a={s,''.join(str(1-int(c)) for c in s),''.join(('1' if c=='0' else '0') if j<2 else c for j,c in enumerate(s))}
        assert len(a)==3; tests+=1
        for x in range(1<<N):
            f=''.join(str((x>>i)&1) for i in range(N))
            assert H(f,s)==int(f in a);tests+=1
        for i in range(N):
            assert all((v[:i]+str(1-int(v[i]))+v[i+1:]) not in a for v in a); tests+=1
        assert sum(H(''.join(str((x>>i)&1) for i in range(N)),s) for x in range(1<<N))%2==1;tests+=1
    for n in range(8,17):
        t=grammar_factor_lower(1<<n)
        assert t[1]>=1<<t[0] and t[2]>=(1<<t[0])/(t[0]-1);tests+=1
    print({'tests':tests,'failures':0,'status':'independent compact finite control'})
if __name__=='__main__':run()
