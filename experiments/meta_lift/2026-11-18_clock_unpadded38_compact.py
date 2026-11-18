#!/usr/bin/env python3
"""CLOCKUNPADDED38 compact independently runnable finite control; not an asymptotic proof."""
from functools import lru_cache
from itertools import product

CHECKS = 0

def test(ok):
    global CHECKS
    assert ok
    CHECKS += 1

def run(n, address, transition, emit):
    N = 1 << n
    K = len(transition[0])
    A = len(address)
    def schedule(a, bits):
        for b in bits:
            a = address[a][b]
        return a
    def forward(f):
        s, out = 0, ''
        for i,b in enumerate(f):
            a = schedule(0, tuple((i >> j)&1 for j in range(n-1,-1,-1)))
            out += emit[a][s][b]
            s = transition[a][s][b]
        return out,s
    for f in product((0,1), repeat=N):
        y,end = forward(f)
        @lru_cache(None)
        def R(d,a,p,q,l,r):
            if not d:
                return any(transition[a][p][b] == q and emit[a][p][b] == y[l:r] for b in (0,1))
            al,ar = address[a]
            return any(R(d-1,al,p,v,l,t) and R(d-1,ar,v,q,t,r)
                       for v in range(K) for t in range(l,r+1))
        def bit(x):
            d,a,p,q,l,r = n,0,0,end,0,len(y)
            test(R(d,a,p,q,l,r))
            while d:
                al,ar = address[a]
                v,t = next((v,t) for v in range(K) for t in range(l,r+1)
                           if R(d-1,al,p,v,l,t) and R(d-1,ar,v,q,t,r))
                d -= 1
                if (x >> d)&1: a,p,l = ar,v,t
                else: a,q,r = al,v,t
            return next(b for b in (0,1)
                        if transition[a][p][b] == q and emit[a][p][b] == y[l:r])
        g = tuple(bit(i) for i in range(N))
        test(forward(g) == (y,end))
        test(all(bit(i) == g[i] for i in range(N)))
    return N

if __name__ == '__main__':
    # Stationary output-delaying transducer.
    run(3, ((0,0),), (((0,1),(1,0)),),
        ((('', '1'), ('0','')),))
    # Two-address-state Thue-Morse control with source/state-dependent emissions.
    run(3, ((0,1),(1,0)), (((0,1),(1,0)),((1,0),(0,1))),
        ((('', '1'),('0','')), (('1',''),('','0'))))
    print({'assertions':CHECKS,'failures':0,'sources':512})
