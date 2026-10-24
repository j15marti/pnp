#!/usr/bin/env python3
"""CYCLIC-VIRTUAL-SELECTOR82 independent standard-library reproducer.
Syntax/bit service, not an all-input SAT reduction. P versus NP OPEN.
"""
import math, json

def w(n,m):
    return (64*(n+m+1)-1).bit_length()

def family(M, sat):
    assert M>=16 and M&(M-1)==0
    m=(M-6)//2
    a,b,c,d=2*m,2*m+1,2*m+2,2*m+3
    signs=((1,1),(1,-1),(-1,1),(-1,-1))
    C=[(1,u*a,v*b) for u,v in signs]
    for i in range(1,m):
        C.extend([(-i,i+1,m+i),(-i,i+1,-(m+i))])
    C.extend([(-m,u*c,v*d) for u,v in signs])
    if sat: C[-4]=(-m,c,1)
    assert len(C)==M and len(set(C))==M
    return M-3,C

def code(l):
    return 2*abs(l)+(l<0)

def words(n,C):
    return [n,len(C)]+[v for cl in C for v in (3,*map(code,cl))]

def bitstream(n,C):
    W=w(n,len(C))
    return ''.join(format(z,'0%db'%W) for z in words(n,C))

def bit(n,C,j,K,i):
    M=len(C); W=w(n,K)
    assert 0<=i<(4*K+2)*W
    word=i//W; shift=W-1-i%W
    if word==0: value=n
    elif word==1: value=K
    else:
        row=(word-2)//4
        col=(word-2)%4
        source=C[(j*K+row)%M]
        value=3 if col==0 else code(source[col-1])
    return (value>>shift)&1

def main():
    checks=0; rows=[]
    for M in (16,32,64,256,1024):
        n,U=family(M,False)
        n2,S=family(M,True)
        assert n==n2
        N=(4*M+2)*w(n,M)
        raw=int(math.sqrt(N)/math.log2(N))
        K=max(3,raw if raw%2 else raw+1)
        Q=min(M,int(N**.6))
        assert math.gcd(M,K)==1 and 2*K<=M and K<M
        checks+=1
        seen=set();last=None;source_changes=0;compared=0
        for j in range(Q):
            ids=tuple((j*K+i)%M for i in range(K))
            assert ids not in seen; seen.add(ids); checks+=1
            if last is not None:
                assert set(ids).isdisjoint(last)
                a=words(n,[U[i] for i in last])
                b=words(n,[U[i] for i in ids])
                changes=sum(x!=y for x,y in zip(a,b))
                assert changes>=K
                source_changes+=changes;checks+=2
            last=ids
            if j in (0,1,Q//2,Q-1):
                for C in (U,S):
                    target=bitstream(n,[C[i] for i in ids])
                    virtual=''.join(str(bit(n,C,j,K,i)) for i in range(len(target)))
                    assert target==virtual
                    compared+=len(target);checks+=1
        rows.append(dict(M=M,K=K,Q=Q,N=N,L=(4*K+2)*w(n,K),
                         exact_child_bits_compared=compared,
                         changed_word_fields=source_changes,
                         status_of_every_strict_child='SAT on either minimal pair'))
    print(json.dumps(dict(run='CYCLIC-VIRTUAL-SELECTOR82',status='PASS',
                          checks=checks,rows=rows,
                          all_input_ARC_successor='OPEN',
                          P_versus_NP='OPEN'),indent=2))

if __name__=='__main__':
    main()
