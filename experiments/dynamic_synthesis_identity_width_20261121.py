"""Exact syntactic UNSAT-frontier audit; no solver timing claim."""
from itertools import product
from math import comb
from collections import Counter
from dynamic_redteam_cut_cache_20261121 import memoized
import json

def family(k, sat=False):
    rows=[(i,k+i,2*k+i) for i in range(1,k+1)]
    core=[tuple(s*(3*k+j) for j,s in enumerate(signs,1))
          for signs in product((1,-1),repeat=3)]
    return tuple(rows+(core[:-1] if sat else core))

def restrict(rows,v,b):
    lit=v if b else -v
    return tuple(tuple(x for x in row if x!=-lit) for row in rows if lit not in row)

def audit(k):
    frontier={family(k)}
    widths=[1]
    for v in range(1,k+1):
        frontier={restrict(f,v,b) for f in frontier for b in (0,1)}
        widths.append(len(frontier))
        assert len(frontier)==2**v
        assert all(len(row)>=2 for f in frontier for row in f)
    hist=Counter(sum(len(row)==2 for row in f) for f in frontier)
    assert all(hist[j]==comb(k,j) for j in range(k+1))
    core=family(k)[-8:]
    assert all(f[-8:]==core for f in frontier)
    assert all(not all(any((s>0)==bool(a[abs(s)-3*k-1]) for s in row)
                       for row in core) for a in product((0,1),repeat=3))
    assert all(any(l>0 for l in row) for row in family(k,True))
    c=k+8;d=3*k+3;r=c+1 if c%2==0 else c+2
    n0=d+(10*c+1)*r+2;m0=(20*c+4)*r;n=n0+m0+3;m=2*m0+4
    w=n.bit_length()
    N=3*n+2+2*((m+1).bit_length()-1)+3*m*(w+1)+w
    cached=memoized(family(k))
    assert not cached["sat"] and cached["distinct"]==2**(k+1)-1
    assert cached["calls"]==cached["distinct"] and cached["hits"]==0
    return dict(k=k,widths=widths,central_same_length=hist[k//2],N=N,cached=cached)

if __name__=="__main__":
    print(json.dumps(dict(status="COMPUTATIONAL",rows=[audit(k) for k in range(1,11)],
                         scope="Exact frontier and pinned cut/cache algorithm; no component decomposition or TM timing"),indent=2))

