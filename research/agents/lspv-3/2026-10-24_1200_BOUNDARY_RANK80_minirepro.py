#!/usr/bin/env python3
"""BOUNDARY-RANK-SWITCH80 compact independent canonical-family reproducer."""
from itertools import product

def xor3(a,b,c,r):
    return [tuple(v if bit==0 else -v for v,bit in zip((a,b,c),bits))
            for bits in product((0,1),repeat=3)
            if bits[0]^bits[1]^bits[2] != r]

def build(q,h,orient=(),endbit=0):
    assert q>=2 and h>=2
    orient=orient or (0,)*(q-1)
    assert len(orient)==q-1
    at=lambda i,j:i*(2*h-1)+j+1
    end=lambda i:at(i,2*h-2)
    E=[]; B=[]; T=[]
    for i in range(q):
        for j in range(h-1):
            vs=(at(i,0),at(i,1),at(i,h)) if j==0 else (at(i,h+j-1),at(i,j+1),at(i,h+j))
            E.append(vs);T+=xor3(*vs,0)
    for i,b in enumerate(orient):
        x,y=end(i),end(i+1)
        B += [(x,y),(-x,-y)] if b else [(-x,y),(x,-y)]
    B += [(end(0),),((end(q-1) if endbit else -end(q-1)),)]
    return q*(2*h-1),E,B,T

def good(cl,x):
    return any((((x>>(abs(v)-1))&1)==int(v>0)) for v in cl)

def valid(n,E,B,x):
    return all((sum((x>>(v-1))&1 for v in row)&1)==0 for row in E) and all(good(c,x) for c in B)

def main():
    tests=0
    for q,h in ((2,2),(2,3),(3,2),(3,3),(4,2)):
        for b in (0,1):
            n,E,B,T=build(q,h,endbit=b)
            models=sum(valid(n,E,B,x) for x in range(1<<n))
            expect=(1<<(q*(h-1))) if b==1 else 0
            assert models==expect,(q,h,b,models,expect)
            assert len(T)==4*q*(h-1) and len(B)==2*q
            tests+=3
    for q in (2,3,4):
        for orient in product((0,1),repeat=q-1):
            n,E,B,T=build(q,2,orient=orient,endbit=0)
            sat=any(valid(n,E,B,x) for x in range(1<<n))
            assert sat==(sum(orient)%2==1),(q,orient)
            tests+=1
    # For E-only block i, free inputs a_1..a_h determine all p's:
    # dimension d=h; binary clauses access only p_(h-1)=XOR_j a_j;
    # nonzero projection has rank t=1, hence two rather than 2^h states.
    for h in (2,4,16,128):
        q=4
        n,E,B,T=build(q,h,endbit=1)
        assert n==q*(2*h-1) and len(E)==q*(h-1)
        assert len(B)==2*q and len(T)==4*q*(h-1)
        tests+=3
    print({'run_id':'BOUNDARY-RANK-SWITCH80-MINI',
           'tests':tests,'failures':0,
           'scope':'canonical algebra and brute-force small instances only',
           'full_137_check_audit':'separate attached full script and raw JSON'})
if __name__=='__main__':main()
