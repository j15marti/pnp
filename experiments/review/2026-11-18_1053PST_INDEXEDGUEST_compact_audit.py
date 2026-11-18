#!/usr/bin/env python3
"""Compact independent finite audit of INDEXEDGUEST exact quantifier identity.
For full serialized AND/OR/NOT guest and 30MB source tests, use run bundle.
No third party modules needed.
"""
import itertools
def B(n): return itertools.product((0,1),repeat=n)
def audit():
    total=0; win=0; badcount=0
    for mask in range(1<<16):
        def G(i,x,y,c):
            return (mask>>((i<<3)|(x<<2)|(y<<1)|c))&1
        some_x=False
        for x in range(2):
            good=all(any(all(G(i,x,y,c) for i in range(2))
                         for c in range(2)) for y in range(2))
            bad=any(all(any(not G(i,x,y,c) for i in range(2))
                        for c in range(2)) for y in range(2))
            assert good == (not bad)
            total+=1;badcount+=bool(bad);some_x|=good
        win+=some_x
    assert total==131072 and win==22687 and badcount==105984
    # Adaptive shared c=y and uniquely determined u=c works only
    # when c is after y. Shared c cannot be guessed independently by factor.
    assert all(any(c==y for c in (0,1)) for y in (0,1))
    assert not any(all(c==y for y in (0,1)) for c in (0,1))
    assert not any(all(c==i for i in (0,1)) for c in (0,1))
    print("PASS",total,"per-x equivalences,",
          win,"Sigma3-true truth tables; zero discrepancies")
if __name__=="__main__": audit()