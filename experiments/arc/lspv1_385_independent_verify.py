#!/usr/bin/env python3
"""Independent finite audit of LSPV-1/385; toy language, NOT halting oracle."""
from itertools import product
import json

def build(bits):
    assert len(bits)%2==0 and set(bits)<={'0','1'}
    return [[1],[-1]]+[[(j+2)*(1 if b=='1' else -1)] for j,b in enumerate(bits)]

def read_source(c):
    if not isinstance(c,list) or len(c)<2 or c[:2]!=[[1],[-1]]:return None
    out=[]
    for i,cl in enumerate(c[2:],2):
        if not isinstance(cl,list) or len(cl)!=1 or type(cl[0]) is not int or abs(cl[0])!=i:return None
        out.append('1' if cl[0]>0 else '0')
    return ''.join(out) if len(out)%2==0 else None

def check(c,trace):
    bits=read_source(c)
    if bits is None or not isinstance(trace,list) or not trace:return False
    pc=0;val=0
    for t,pair in enumerate(trace):
        if pair!=[pc,val]:return False
        op=bits[2*pc:2*pc+2]
        if op=='10':return t==len(trace)-1
        if op=='00':pc+=1;val=1-val
        elif op!='01':return False
    return False

def toy_trace(bits):
    pc=0;val=0;seen=set();out=[]
    while (pc,val) not in seen:
        seen.add((pc,val))
        op=bits[2*pc:2*pc+2]
        if op not in ('00','01','10'):return None
        out.append([pc,val])
        if op=='10':return out
        if op=='00':pc+=1;val=1-val
    return None

halt=nonhalt=assertions=0
for words in range(4):
    for pair in product(('00','01','10','11'),repeat=words):
        bits=''.join(pair);f=build(bits);tr=toy_trace(bits)
        assert read_source(f)==bits;assertions+=1
        assert check(f,tr if tr is not None else [])==(tr is not None);assertions+=1
        assert not check(f,[[0,0],[0,0]]);assertions+=1
        assert not check(f,[[0,0],[0,1]]);assertions+=1
        if tr is None:nonhalt+=1
        else:halt+=1

for bad in [[],[[1]],[[1],[-1],[3]],[[1],[-1],[2],[2]],[[1],[-1],[-2],[3],[4]]]:
    assert read_source(bad) is None;assertions+=1
    assert not check(bad,[[0,0]]);assertions+=1
    assert not check(bad,[]);assertions+=1

print(json.dumps({'programs':85,'halt':halt,'nonhalt':nonhalt,'assertions':assertions,'seed':None,'note':'independent finite checker only'},indent=2))
