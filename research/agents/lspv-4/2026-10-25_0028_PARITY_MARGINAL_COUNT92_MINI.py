#!/usr/bin/env python3
"""PARITY-MARGINAL-COUNT92 peer mini: independent complete x/z enumeration.
The comprehensive 680-assertion audit is shipped separately in the user ZIP.
"""
import itertools, json

def pin(x,v,u,w):
    a=x if v else -x
    return ((a,u,w),(a,u,-w),(a,-u,w),(a,-u,-w))

def xor3(a,b,c,e):
    rows=[]
    for X,Y,Z in itertools.product((0,1),repeat=3):
        if X^Y^Z != e:
            rows.append(tuple(-z if bit else z for z,bit in zip((a,b,c),(X,Y,Z))))
    return rows

def build(q,e):
    x=range(1,q+1)
    z=range(q+1,2*q+1)
    z=list(z); t=1^(q&1)
    B=[(-z[0],1),(z[0],-1)] if not e[0] else [(z[0],1),(-z[0],-1)]
    for i in range(1,q):
        B+=xor3(z[i-1],i+1,z[i],e[i])
    B+=pin(z[-1],t,2*q+1,2*q+2)
    blocks=[pin(i,1,2*q+1+2*i,2*q+2+2*i) for i in x]
    n=4*q+2
    assert len(B)==4*q+2 and len(B)+sum(map(len,blocks))==8*q+2
    return B,blocks,n

def sat(clauses,mask):
    return all(any(((mask>>(abs(v)-1))&1)==int(v>0) for v in c) for c in clauses)

def check():
    cnt=0
    for q in range(1,4):
        for e in itertools.product((0,1), repeat=q):
            B,blocks,n=build(q,e)
            dist=[0]*(1<<q)
            for mask in range(1<<n):
                if sat(B,mask): dist[mask&((1<<q)-1)]+=1
            for choices in itertools.product((-1,0,1),repeat=q):
                S=[i for i,v in enumerate(choices) if v>=0]
                observed=sum(number for x,number in enumerate(dist) if all((x>>i)&1==choices[i] for i in S))
                if len(S)<q:
                    expected=4**(q+1)*2**(q-len(S)-1)
                else:
                    expected=4**(q+1) if sum(choices)%2==(1^(q&1)^(sum(e)&1)) else 0
                assert observed==expected,(q,e,choices,observed,expected)
                cnt+=1
            full=B+[c for cl in blocks for c in cl]
            assert (any(sat(full,m) for m in range(1<<n)))==(sum(e)%2==1)
            cnt+=1
    return {'claim':'PARITY-MARGINAL-COUNT92','controls':'all orientations q<=3 and all partial pinned count profiles','checks':cnt,'failures':0,'status':'COMPUTATIONAL','not':'full 680-check source or physical FLMV machine trace'}
if __name__=='__main__':
    print(json.dumps(check(),indent=2,sort_keys=True))
