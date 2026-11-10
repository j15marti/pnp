#!/usr/bin/env python3
"""LSPV-2/534: exact finite pyramid pebbling and XOR/Lucas controls."""
import hashlib, itertools, json
from collections import deque

def pyramid(h):
    V=[(r,i) for r in range(h+1) for i in range(h-r+1)]
    D={v:k for k,v in enumerate(V)}
    P=[tuple(D[r-1,j] for j in (i,i+1)) if r else () for r,i in V]
    return V,P,D[h,0]

def reach(h,bound):
    V,P,z=pyramid(h)
    q=deque([0]); seen={0}; count=0
    while q:
        s=q.popleft();count+=1
        if s&(1<<z):return True,count
        for v,parents in enumerate(P):
            b=1<<v
            if s&b:t=s^b
            elif all(s&(1<<j) for j in parents):t=s|b
            else:continue
            if t.bit_count()<=bound and t not in seen:
                seen.add(t);q.append(t)
    return False,count

def slow(x):
    a=list(x)
    while len(a)>1:a=[a[i]^a[i+1] for i in range(len(a)-1)]
    return a[0]

def fast(x):
    h=len(x)-1
    return sum(x[i] for i in range(h+1) if (i&h)==i)&1

def k4(charges):
    edges=list(itertools.combinations(range(4),2));src=bytearray(b'S3C'+bytes((6,16)))
    for vertex in range(4):
        ids=[i+1 for i,e in enumerate(edges) if vertex in e]
        for a in range(8):
            if a.bit_count()%2!=charges[vertex]:
                src.extend(((-v if a&(1<<j) else v)%256) for j,v in enumerate(ids))
    return bytes(src)

def parse(src):
    if len(src)<5 or src[:3]!=b'S3C':raise ValueError('header')
    v,m=src[3:5]
    if len(src)!=5+3*m:raise ValueError('length')
    cls=[]
    for i in range(m):
        row=[b if b<128 else b-256 for b in src[5+3*i:8+3*i]]
        if any(abs(l)<1 or abs(l)>v for l in row):raise ValueError('literal')
        if len(set(map(abs,row)))!=3:raise ValueError('duplicate')
        cls.append(row)
    return v,cls

def models(src):
    n,cls=parse(src)
    return sum(all(any(((a>>(abs(l)-1))&1)==int(l>0) for l in C) for C in cls) for a in range(1<<n))

def main():
    assertions=0;pebble=[];xor=[]
    for h in range(1,5):
        no,n=reach(h,h+1);yes,m=reach(h,h+2)
        assert not no and yes;assertions+=2
        pebble.append(dict(height=h,vertices=len(pyramid(h)[0]),min_pebbles=h+2,no_goal_states=n,yes_goal_states=m))
    for h in range(16):
        count=0
        gen=(itertools.product((0,1),repeat=h+1) if h<=9 else
             ([((i*37+j*j+17*j+i*j)//3)&1 for j in range(h+1)] for i in range(80)))
        for a in gen:assert slow(a)==fast(a);count+=1;assertions+=1
        coeff=sum((i&h)==i for i in range(h+1))
        assert coeff==2**h.bit_count();assertions+=1
        xor.append(dict(height=h,inputs=count,nonzero_coeffs=coeff))
    for h in (2,4,8):assert xor[h]['nonzero_coeffs']==2;assertions+=1
    assert slow([1,1,1])==0;assertions+=1
    controls={};odd=k4((1,0,0,0))
    for name,charge in [('k4_odd',(1,0,0,0)),('k4_even',(0,0,0,0))]:
        data=k4(charge);ms=models(data);assert (ms==0)==(name=='k4_odd')
        controls[name]=dict(binary_bits=len(data)*8,clauses=16,models=ms,sha256=hashlib.sha256(data).hexdigest(),vars=6)
        assertions+=1
    bad=[b'X'+odd[1:],odd[:-1],odd[:3]+bytes((6,15))+odd[5:],
         odd[:5]+b'\x00'+odd[6:],odd[:6]+odd[5:6]+odd[7:],odd[:5]+b'\x07'+odd[6:]]
    for data in bad:
        try:parse(data)
        except ValueError:assertions+=1
        else:raise AssertionError('malformed accepted')
    result=dict(id='LSPV2-534',checks=assertions,pebble=pebble,xor=xor,controls=controls,
                malformed_rejected=len(bad),status='COMPUTATIONAL, plus known Cook/Nordstrom theorem',
                warning='No native FLMV interpreter or SAT-decider lower bound')
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
