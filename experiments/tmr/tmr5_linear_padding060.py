#!/usr/bin/env python3
"""TMR-5/060 independent executable gate-DAG and padded-language tests.
Nonuniform table values supplied explicitly; they are not uniformly computed.
"""
import argparse, hashlib, itertools, json, random
from collections import Counter

REV = 'TMR5_PAD_LINEAR060_PY_v1'
SEED = 20261116

def build(n, c, table):
    assert n>=1 and c>=1 and len(table)==2**n and all(x in (0,1) for x in table)
    m=2**(c*n)
    gates=[]
    # Inputs are 0..m-1; constants -1 (zero) and -2 (one).
    def add(op,a,b=-1):
        gates.append((op,a,b))
        return m+len(gates)-1
    neg=[add('NOT',i) for i in range(n)]
    def mux(pos,vals):
        if len(vals)==1: return -2 if vals[0] else -1
        half=len(vals)//2
        a=mux(pos+1,vals[:half]); b=mux(pos+1,vals[half:])
        l=add('AND',neg[pos],a); r=add('AND',pos,b)
        return add('OR',l,r)
    root=mux(0,table)
    tail=list(range(n+1,m))
    if tail:
        def balanced_or(items):
            if len(items)==1: return items[0]
            mid=len(items)//2
            return add('OR',balanced_or(items[:mid]),balanced_or(items[mid:]))
        rem=balanced_or(tail)
        rem=add('NOT',rem)
        good=add('AND',n,rem)
    else: good=n
    out=add('AND',root,good)
    # A gate is counted even when a constant fan-in might simplify it.
    assert len(gates)<=4*m
    return m,gates,out

def evaluate(m,gates,out,input_word):
    state=list(input_word)
    for op,a,b in gates:
        u=state[a] if a>=0 else -a-1
        v=state[b] if b>=0 else -b-1
        state.append({'AND':u&v,'OR':u|v,'NOT':1-u}[op])
    return state[out]

def expected(n,c,table,bits):
    m=len(bits)
    if m!=2**(c*n): return 0
    if bits[n]!=1 or any(bits[n+1:]): return 0
    idx=0
    for b in bits[:n]:idx=2*idx+b
    return table[idx]

def run(n,c,samples):
    m=2**(c*n)
    rng=random.Random(SEED+100*n+c)
    truthset=[]
    if n<=3: truthset=[[(mask>>j)&1 for j in range(2**n)] for mask in range(2**(2**n))]
    else:
        truthset=[[0]*(2**n),[1]*(2**n),[j%2 for j in range(2**n)]]
        truthset += [[rng.getrandbits(1) for _ in range(2**n)] for _ in range(samples)]
    tests=0; maximum=0; maxdepth=0
    for table in truthset:
        _,gates,output=build(n,c,table)
        maximum=max(maximum,len(gates))
        depth=[0]*m
        for op,a,b in gates:
            da=depth[a] if a>=0 else 0; db=depth[b] if b>=0 else 0
            depth.append(1+max(da,db))
        maxdepth=max(maxdepth,depth[output])
        assert maxdepth<=2*n+m.bit_length()+4 # balanced suffix and mux depth
        for mask in range(2**m):
            bits=[(mask>>i)&1 for i in range(m)]
            got=evaluate(m,gates,output,bits)
            want=expected(n,c,table,bits)
            if got!=want:raise AssertionError((n,c,table,mask,got,want))
            tests+=1
    return dict(n=n,c=c,M=m,tables=len(truthset),tested_inputs=tests,maximum_gates=maximum,gate_budget=4*m,max_depth=maxdepth,zero_failures=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,required=True);p.add_argument('--c',type=int,required=True);p.add_argument('--samples',type=int,default=5);a=p.parse_args()
    res=run(a.n,a.c,a.samples)
    print(json.dumps(dict(revision=REV,seed=SEED,**res),sort_keys=True))
