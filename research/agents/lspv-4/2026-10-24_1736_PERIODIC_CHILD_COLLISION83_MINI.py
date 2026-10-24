#!/usr/bin/env python3
"""PERIODIC-CHILD-COLLISION83 compact independent stdlib reproducer.
Deterministic full assignment counts; no FLMV machine simulation.
"""
import math, json
from collections import Counter

FILL=(4,5,6)

def core(a):
    return tuple(-i if (a>>(i-1))&1 else i for i in (1,2,3))

def width(n,m):
    return (64*(n+m+1)-1).bit_length()

def size(n,m):
    return (4*m+2)*width(n,m)

def odd_k(N):
    k=int(math.sqrt(N)/math.log2(N))
    return k if k%2 else k-1

def parent(M,p,change):
    g=p//8
    clauses=[]
    for j in range(M):
        z=j%p
        if z%g: clauses.append(FILL)
        else:
            a=z//g
            clauses.append(core(6 if change and a==7 else a))
    return tuple(clauses)

def encode(clauses,n=6):
    m=len(clauses)
    w=width(n,m)
    words=[n,m]
    for c in clauses:
        assert len(c)==3 and len(set(map(abs,c)))==3
        words.extend([3]+[2*abs(l)+int(l<0) for l in c])
    return ''.join(format(v,'0%db'%w) for v in words)

def count(clauses,n=6):
    ct=0
    for assignment in range(1<<n):
        if all(any(bool(assignment & (1<<(abs(l)-1)))==(l>0) for l in c) for c in clauses):
            ct+=1
    return ct

def test(M):
    N=size(6,M)
    K=odd_k(N)
    p=1 << (8*K-1).bit_length()
    g=p//8
    Q=min(M,int(N**.6))
    assert p<=M and p%8==0 and 3<=K<g and Q>=p and K%2==1
    U,V=parent(M,p,False),parent(M,p,True)
    assert count(U)==0 and count(V)==7
    enc=[set(),set()]
    selectors=set()
    last=None
    changed=0
    hist=Counter()
    for j in range(Q):
        indices=tuple((j*K+i)%M for i in range(K))
        assert indices not in selectors
        selectors.add(indices)
        cs=[tuple(F[i] for i in indices) for F in (U,V)]
        marker=sum((i%g)==0 for i in indices)
        assert marker<=1
        predicted=49 if marker else 56
        hist[marker]+=1
        for typ,c in enumerate(cs):
            assert count(c)==predicted
            bits=encode(c)
            assert len(bits)==size(6,K)
            enc[typ].add(bits)
        if last is not None:
            changed += sum(a!=b for C,D in zip(last,cs[0]) for a,b in zip(C,D))
        last=cs[0]
    assert len(selectors)==Q
    assert len(enc[0])==1+8*K and len(enc[1])==1+7*K
    assert changed<=6*(Q-1)
    return {'M':M,'N':N,'K':K,'p':p,'Q':Q,'child_bits':size(6,K),
            'parent_counts':[0,7],'unique_indices':len(selectors),
            'unique_children':[len(s) for s in enc],
            'flat_changed_literal_fields':changed,'child_marker_histogram':dict(hist)}

def main():
    M=16;K=3
    identical=tuple(FILL for _ in range(M))
    index_sets={tuple((j*K+i)%M for i in range(K)) for j in range(M)}
    encodings={encode(tuple(identical[(j*K+i)%M] for i in range(K))) for j in range(M)}
    assert len(index_sets)==16 and len(encodings)==1
    rows=[test(M) for M in (256,512,1024,4096)]
    print(json.dumps({'status':'PASS','seed':None,
        'all_identical_control':{'distinct_index_selections':16,'distinct_child_encodings':1},
        'rows':rows,'scope':'finite exhaustive 64-assignment child checks; not all-decider lower bound'},indent=2,sort_keys=True))

if __name__=='__main__': main()
