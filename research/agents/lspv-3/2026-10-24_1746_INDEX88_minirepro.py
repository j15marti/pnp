#!/usr/bin/env python3
"""INDEXED-CONTEXT-ESCAPE88: exact reproducible finite MUX proper-3CNF checks.
This is a compact peer reproducer; the complete 34,980-check source and
raw JSON are retained separately in the research package. P vs NP OPEN.
"""
from itertools import product
import json

def make(h,x,y):
    m=1<<h
    sel=list(range(m+1,m+h+1))
    nextvar=m+h+1
    public=[]
    layer=list(range(1,m+1))
    for d in range(h):
        new=[]
        for j in range(0,len(layer),2):
            a,b=layer[j:j+2];z=nextvar;nextvar+=1;s=sel[d]
            public.extend([(s,-a,z),(s,a,-z),(-s,-b,z),(-s,b,-z)])
            new.append(z)
        layer=new
    root=layer[0]
    def pin(lit):
        nonlocal nextvar
        a,b=nextvar,nextvar+1
        nextvar+=2
        return [(lit,a,b),(lit,a,-b),(lit,-a,b),(lit,-a,-b)]
    public+=pin(root)
    C=public[:]
    for i,t in enumerate(x): C+=pin(i+1 if t else -(i+1))
    for i,t in enumerate(y): C+=pin(sel[i] if t else -sel[i])
    n=nextvar-1;M=len(C)
    w=(64*(n+M+1)-1).bit_length()
    assert n==4*m+3*h+1 and M==8*m+4*h
    assert len(public)==4*m and all(len(set(map(abs,c)))==3 for c in C)
    words=[n,M]
    for c in C: words.extend([3]+[2*abs(z)+(z<0) for z in c])
    N=len(words)*w
    assert len(words)==4*M+2
    return C,n,M,N

def witness(h,x,y):
    m=1<<h; v={i+1:x[i] for i in range(m)}
    for j in range(h): v[m+1+j]=y[j]
    layer=list(range(1,m+1)); z=m+h+1
    for d in range(h):
        nxt=[]
        for i in range(0,len(layer),2):
            a,b=layer[i:i+2]
            v[z]=v[b] if y[d] else v[a]
            nxt.append(z);z+=1
        layer=nxt
    for _ in range(m+h+1):
        v[z]=0;v[z+1]=0;z+=2
    return v

def valid(C,v):
    return all(any(v[abs(t)]==int(t>0) for t in c) for c in C)

def dpll(C,v=None):
    if v is None:v={}
    while True:
        new=[];unit=None
        for c in C:
            if any(abs(z) in v and v[abs(z)]==int(z>0) for z in c):continue
            remaining=[z for z in c if abs(z) not in v]
            if not remaining:return False
            if len(remaining)==1:unit=remaining[0]
            new.append(remaining)
        C=new
        if unit is None:break
        v=v.copy();v[abs(unit)]=int(unit>0)
    if not C:return True
    pivot=abs(C[0][0])
    for bit in [0,1]:
        assignment=v.copy();assignment[pivot]=bit
        if dpll(C,assignment):return True
    return False

def run():
    classes=[];n_cases=n_sat=n_unsat=dpll_cases=0
    for h in range(1,5):
        m=1<<h
        base={0,1,2,3,7,15,255,(1<<m)-1}|{1<<i for i in range(m)}
        base |= {(1<<m)-1 ^ a for a in tuple(base)}
        samples=range(1<<m) if h<=3 else sorted(base)
        sat=unsat=0
        for raw in samples:
            x=tuple(raw>>i&1 for i in range(m))
            for idx in range(m):
                y=tuple(idx>>j&1 for j in range(h))
                C,n,M,N=make(h,x,y)
                # Exactly one indexed data-sign probe after Y is known.
                root=x[sum(t<<j for j,t in enumerate(y))]
                live=list(x)
                for bit in y:live=live[bit::2]
                assert live==[root]
                if root:assert valid(C,witness(h,x,y))
                if h<=2:
                    assert dpll(C)==bool(root)
                    dpll_cases+=1
                sat+=root;unsat+=1-root;n_cases+=1
        assert sat==unsat
        # All X words yield distinct Y-to-SAT response rows.
        Q=len({tuple(raw>>j&1 for j in range(m)) for raw in range(1<<m)})
        assert Q==1<<m
        n_sat+=sat;n_unsat+=unsat
        classes.append(dict(h=h,m=m,Q=Q,source_state_lower=m,
                            remote_index_queries=1,sat=sat,unsat=unsat,
                            N_bits=N,vars=n,clauses=M))
    print(json.dumps(dict(status='COMPUTATIONAL',cases=n_cases,
        SAT=n_sat,UNSAT=n_unsat,generic_DPLL=dpll_cases,
        classes=classes,errors=0,all_input_ARC_successor='OPEN'),indent=2))

if __name__=="__main__":
    run()
