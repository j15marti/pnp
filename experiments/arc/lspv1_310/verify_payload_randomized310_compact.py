#!/usr/bin/env python3
"""Independent NO-IMPORT checker for LSPV-1 randomized payload310 compact raw output."""
import json,sys
from itertools import product,combinations
A=[(1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9)]
B=[(4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9)]
F=tuple(A+[tuple(-v for v in c) for c in B])
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
def check(n,cs):
    counter={}
    for c in cs:
        if len(c)!=3 or len(set(map(abs,c)))!=3:return False
        if not (all(x>0 for x in c) or all(x<0 for x in c)):return False
        if any(abs(x)<1 or abs(x)>n for x in c):return False
        for x in c:
            k=(abs(x),x>0);counter[k]=counter.get(k,0)+1
    return len(cs)*3==4*n and all(counter.get((v,s),0)==2 for v in range(1,n+1) for s in (False,True))
def word(n,cs):
    g=lambda u:'0'*(u.bit_length()-1)+format(u,'b')
    w=n.bit_length()
    return g(n)+g(len(cs))+''.join(str(int(c[0]>0))+''.join(format(abs(x),'0%db'%w) for x in c) for c in cs)
def parse(s):
    at=0;h=[]
    for _ in range(2):
        z=0
        while at+z<len(s) and s[at+z]=='0':z+=1
        k=at+z
        if k+z>=len(s):return False
        h.append(int(s[k:k+z+1],2));at=k+z+1
    n,m=h
    if n<1:return False
    w=n.bit_length()
    if len(s)!=at+m*(1+3*w):return False
    cs=[]
    for i in range(m):
        q=at+i*(1+3*w);sig=2*int(s[q])-1
        cs.append(tuple(sig*int(s[q+1+j*w:q+1+(j+1)*w],2) for j in range(3)))
    return check(n,cs)
def models(n,cs,p):
    return sum(all(a[i-1]==v for i,v in p.items()) and
               all(any(a[abs(x)-1]==int(x>0) for x in c) for c in cs)
               for a in product((0,1),repeat=n))
def checkall(raw):
    assert raw['status']=='PASS'
    for rec,(n,cs) in zip(raw['controls'],[(6,Y),(9,F)]):
        assert check(n,cs)
        s=word(n,cs);M=rec['payload_bits']
        assert rec['encoded_bits']==len(s) and M+rec['header_bits']==len(s) and parse(s)
        for i in range(len(s)-M,len(s)):
            b=s[:i]+str(1-int(s[i]))+s[i+1:]
            assert not parse(b)
        assert rec['invalid_one_bit_mutants']==M
        assert models(n,cs,{})==rec['models']
        assert rec['expected_read_floor']==str(__import__('fractions').Fraction(M,3))
        assert rec['pair_modes']==4*(len(cs)*(len(cs)-1)//2)
    assert models(9,F,{1:1,2:0,3:1,4:0,8:0})==1
    assert models(9,F,{1:1,2:1,3:0,4:0,8:0})==0
    assert raw['same_original_F9']=={'SAT_completions':1,'UNSAT_completions':0}
    return True
if __name__=='__main__':
    with open(sys.argv[1]) as f:raw=json.load(f)
    assert checkall(raw)
    print('PASS: independent source grammar, malformed flips and both-label original controls')
