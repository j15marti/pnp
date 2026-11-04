#!/usr/bin/env python3
"""LSPV-4/385 independently runnable, deterministic finite verifier. No deps."""
from itertools import product
def src(bits,unsat):
    m=len(bits); p=m+1;z=m+2
    f=[tuple((i+1 if v else -(i+1)) for i,v in enumerate(bits))+(p,),(-p,)]
    if unsat:f.extend([(z,),(-z,)])
    return f
def sat(f,n):
    return any(all(any(bool(a&(1<<(abs(l)-1)))==(l>0) for l in c) for c in f) for a in range(1<<n))
def valid(b,y,unsat=False):
    f=src(b,unsat);p=len(b)+1
    target=tuple(i+1 if v else -(i+1) for i,v in enumerate(y))
    return p in f[0] and f[1]==(-p,) and tuple(t for t in f[0] if t!=p)==target
def chunk(b,y,r):
    n=len(b)
    return all(b[(n*i)//r:(n*(i+1))//r]==y[(n*i)//r:(n*(i+1))//r] for i in range(r))
def main():
    nrec=good=bad=pair=multi=checks=0
    for m in range(1,7):
        ss=list(product((0,1),repeat=m))
        for b in ss:
            assert sat(src(b,False),m+2) and not sat(src(b,True),m+2); checks+=2
            for y in ss:
                for unsat in (False,True):
                    ans=valid(b,y,unsat);assert ans==(b==y)
                    nrec+=1; good+=ans;bad+=(not ans);checks+=1
                for r in (1,2,3,4,8):
                    assert chunk(b,y,r)==(b==y);multi+=1;checks+=1
                if b!=y:
                    assert valid(b,b) and not valid(y,b)
                    pair+=1;checks+=2
    assert nrec==10920 and good==252 and bad==10668 and pair==5334
    assert multi==27300
    print(dict(records=nrec,legal=good,illegal=bad,distinguishing_pairs=pair,
               multipass=multi,assertions=checks))
if __name__=="__main__":main()
