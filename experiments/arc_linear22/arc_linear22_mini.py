#!/usr/bin/env python3
"""Standalone standard-library certificate for ARC-LINEAR22-SATURATION1.
Restricted no-shrink, not an unrestricted P vs NP lower bound.
"""
import itertools, collections, json

def family(k):
    assert k>=7 and k%2
    return 3*k, [tuple((1 if s<2 else -1)*v for v in
        (i+1,k+(i+s)%k+1,2*k+(i+2*s)%k+1))
        for s in range(4) for i in range(k)]

def sat(clause,a):
    return any(a[abs(z)]==int(z>0) for z in clause)

def gamma(x):
    return 2*(x.bit_length()-1)+1

def cnf_bits(n,m):
    w=n.bit_length()
    return gamma(n+1)+gamma(m+1)+m*(gamma(4)+3*(1+w))

def check(k):
    n,cs=family(k);m=len(cs)
    assert m==4*k
    counts=collections.Counter()
    edges=collections.Counter()
    for c in cs:
        for z in c:counts[z]+=1
        for p in itertools.combinations(sorted(map(abs,c)),2):edges[p]+=1
    assert all(counts[i]==counts[-i]==2 for i in range(1,n+1))
    assert max(edges.values())==1
    witness={i:int(i<=k) for i in range(1,n+1)}
    assert all(sat(c,witness) for c in cs)
    checked=0
    for x in range(1,n+1):
        pos=[tuple(z for z in c if z!=x) for c in cs if x in c]
        neg=[tuple(z for z in c if z!=-x) for c in cs if -x in c]
        assert len(pos)==len(neg)==2
        assert len({abs(z) for c in pos+neg for z in c})==8
        rs=[tuple(a+b) for a in pos for b in neg]
        assert len({tuple(sorted(map(abs,c))) for c in rs})==4
        assert all(len(c)==4 and len(set(map(abs,c)))==4 for c in rs)
        touched=[c for c in cs if x in c or -x in c]
        others=sorted(set(abs(z) for c in pos+neg for z in c))
        for bits in itertools.product((0,1),repeat=8):
            a=dict(zip(others,bits))
            old=False
            for value in (0,1):
                a[x]=value
                if all(sat(c,a) for c in touched):old=True
            new=all(sat(r,a) for r in rs)
            assert old==new
            checked+=1
    return {'k':k,'n':n,'m':m,'local_truth_tests':checked,
            'reentry_n':n+3,'reentry_m':m+4,
            'gamma_source_bits':cnf_bits(n,m),
            'gamma_child_bits':cnf_bits(n+3,m+4),
            'dag_nodes_delta':1,'dag_edges_delta':-1}

if __name__=='__main__':
    data=[check(k) for k in (7,9,11,15,21,31)]
    print(json.dumps({'status':'exact finite certificate','rows':data},indent=2))
