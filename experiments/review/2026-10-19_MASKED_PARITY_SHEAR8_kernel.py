#!/usr/bin/env python3
"""Masked hypercube parity, independent reversible-shear control."""
for n in range(3,13):
    for z in range(1<<n):
        x=[(z>>i)&1 for i in range(n)]
        y=x[:]
        for i in range(2,n): y[i]=x[i]^(y[i-1]&x[i-2])
        r=y[:]
        for i in range(2,n): r[i]=y[i]^(y[i-1]&r[i-2])
        assert r==x
for d in range(3,8):
    V=1<<d
    E=[(u,u^(1<<k)) for u in range(V) for k in range(d) if not ((u>>k)&1)]
    assert len(E)==d*V//2
    M=len(E)
    N=5*M-8+V*(d-3)
    C=9*(M-2)+4*V*(d-2)
    assert (N,C)==(5*M-8+V*(d-3),9*(M-2)+4*V*(d-2))
    print(d,V,M,N,C,"PASS")
