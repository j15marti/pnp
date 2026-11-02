#!/usr/bin/env python3
"""Self-delimiting source binary grammar and hostile malformed controls, LSPV-1 318."""
import json
from collections import Counter
P9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9))
N9=((4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
P15=((1,2,7),(1,3,8),(4,5,9),(4,6,10),(2,3,5),(6,11,12),(7,11,13),(8,12,14),(9,13,15),(10,14,15))
N15=((1,2,11),(2,3,11),(1,3,12),(4,5,13),(5,6,14),(4,6,15),(7,8,12),(8,9,13),(9,10,14),(10,7,15))
F9=P9+tuple(tuple(-x for x in c) for c in N9)
F15=P15+tuple(tuple(-x for x in c) for c in N15)

def gamma(v):
    b=format(v,'b');return '0'*(len(b)-1)+b

def encode(n,clauses):
    # ceil(log2(n+1)) is n.bit_length() for all positive integer n.
    w=n.bit_length()
    return gamma(n)+gamma(len(clauses))+''.join(str(int(c[0]>0))+''.join(format(abs(x),'0%db'%w) for x in c) for c in clauses)

def parse(src):
    if not src or any(c not in '01' for c in src):return None
    at=0
    def readgamma():
        nonlocal at
        zeros=0
        while at<len(src) and src[at]=='0':zeros+=1;at+=1
        if at+zeros>=len(src):return None
        end=at+zeros+1
        v=int(src[at:end],2);at=end
        return v
    n=readgamma()
    if n is None or n<3 or n%3:return None
    m=readgamma()
    if m is None or m*3!=4*n:return None
    w=n.bit_length()
    if len(src)-at!=m*(1+3*w):return None
    quotas=Counter();seen=set();clauses=[]
    for j in range(m):
        sign=1 if src[at]=='1' else -1;at+=1
        cl=[]
        for i in range(3):
            v=int(src[at:at+w],2);at+=w
            if v<1 or v>n:return None
            cl.append(v*sign);quotas[(v,sign)]+=1
        if len({abs(v) for v in cl})!=3:return None
        key=tuple(sorted(cl))
        if key in seen:return None
        seen.add(key);clauses.append(tuple(cl))
    if not all(quotas[(v,1)]==quotas[(v,-1)]==2 for v in range(1,n+1)):return None
    return (n,tuple(clauses))

def run():
    data={};total=0
    for name,n,formula in (('Y6',6,Y6),('F9',9,F9),('F15',15,F15)):
        encoding=encode(n,formula)
        assert parse(encoding)==(n,formula)
        payload_start=len(gamma(n))+len(gamma(len(formula)))
        mutations=0
        for i in range(payload_start,len(encoding)):
            flipped=encoding[:i]+str(1-int(encoding[i]))+encoding[i+1:]
            assert parse(flipped) is None,(name,i)
            mutations+=1
        for bad in (encoding[:-1],encoding+'0',encoding+'2','',encoding[:payload_start-1]):
            assert parse(bad) is None
        data[name]={'input_bits':len(encoding),'payload_single_bit_rejections':mutations,
                    'five_extra_malformed_rejections':5,'roundtrip':'PASS'}
        total+=mutations+5
    print(json.dumps({'encoding':'gamma(n)||gamma(m)||[clause_sign,three_fixed_width_identifiers]^m',
                      'source_validated':['Y6','F9','F15'],'controls':data,
                      'malformed_rejections':total,'status':'PASS','P_vs_NP':'OPEN'},indent=2,sort_keys=True))
if __name__=='__main__':run()
