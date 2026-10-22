#!/usr/bin/env python3
"""AFFINE-PIN-CNF28: d+b exponent of the AFFINE-PIN27 pinning algorithm on
XAG encodings of random 3-CNF (and a structured control). Stdlib only.
Each AND gate may pin either input (AND commutes); we pick the cheaper side.
Affine forms are GF(2) vectors over primaries as int bitmasks, or None if the
cone contains an AND (nonlinear)."""
import json, random, sys

def build(n, clauses, shape):
    """gates: list of ('in',i)|('not',a)|('xor',a,b)|('and',a,b); returns gates, out."""
    g=[('in',i) for i in range(n)]
    def add(*t): g.append(t); return len(g)-1
    outs=[]
    for cl in clauses:
        # clause = NOT(AND of negated literals)
        negs=[]
        for v in cl:
            x=v-1 if v>0 else -v-1
            lit=x if v>0 else add('not',x)      # literal
            negs.append(add('not',lit))
        acc=negs[0]
        for t in negs[1:]: acc=add('and',acc,t)
        outs.append(add('not',acc))
    if shape=='chain':
        acc=outs[0]
        for o in outs[1:]: acc=add('and',acc,o)
    else:  # balanced tree
        layer=outs
        while len(layer)>1:
            nxt=[add('and',layer[i],layer[i+1]) for i in range(0,len(layer)-1,2)]
            if len(layer)%2: nxt.append(layer[-1])
            layer=nxt
        acc=layer[0]
    return g,acc

def analyze(g):
    aff=[]  # (mask,const) or None
    for t in g:
        if t[0]=='in': aff.append((1<<t[1],0))
        elif t[0]=='not': a=aff[t[1]]; aff.append(None if a is None else (a[0],a[1]^1))
        elif t[0]=='xor':
            a,b=aff[t[1]],aff[t[2]]; aff.append(None if a is None or b is None else (a[0]^b[0],a[1]^b[1]))
        else: aff.append(None)   # AND output nonlinear
    basis={}
    def insert(m):
        while m:
            h=m.bit_length()-1
            if h in basis: m^=basis[h]
            else: basis[h]=m; return True
        return False
    k=b=0
    ands=[i for i,t in enumerate(g) if t[0]=='and']
    # first pass: gates with a source-affine input; prefer an input already in span
    pending=[]
    for i in ands:
        k+=1
        a,c=aff[g[i][1]],aff[g[i][2]]
        cands=[x for x in (a,c) if x is not None]
        if not cands: b+=1; continue
        pending.append(cands)
    for cands in pending:
        for x in cands:   # free if in span (constant-only or dependent form)
            m=x[0]; 
            for h in sorted(basis,reverse=True):
                if m>>h&1: m^=basis[h]
            if m==0: break
        else:
            insert(cands[0][0])
    d=len(basis)
    return k,d,b

def cnf(n,m,rng):
    out=[]
    for _ in range(m):
        vs=rng.sample(range(1,n+1),3)
        out.append([v if rng.random()<.5 else -v for v in vs])
    return out

def main():
    rng=random.Random(2810)
    rows=[]
    for n in (8,12,16,24,32,48,64,96,128):
        for ratio in (2.0,4.26):
            m=int(ratio*n)
            cl=cnf(n,m,rng)
            for shape in ('chain','tree'):
                g,_=build(n,cl,shape)
                k,d,b=analyze(g)
                rows.append(dict(n=n,m=m,ratio=ratio,shape=shape,gates=len(g),k=k,d=d,b=b,exponent=d+b,trivial=n,gain=n-(d+b)))
    # structured control: conjunction of m clauses over ONLY 3 vars (heavily reused sources)
    for m in (16,64,256):
        cl=[[rng.choice((1,-1))*1,rng.choice((1,-1))*2,rng.choice((1,-1))*3] for _ in range(m)]
        g,_=build(3,cl,'chain'); k,d,b=analyze(g)
        rows.append(dict(n=3,m=m,ratio=None,shape='chain-3var',gates=len(g),k=k,d=d,b=b,exponent=d+b,trivial=3,gain=3-(d+b)))
    json.dump(rows,open('2026-10-22_affine_pin_cnf_exponent28_results.json','w'),indent=1)
    for r in rows: print(r)
    print('min gain over CNF rows:',min(r['gain'] for r in rows if r['shape'] in('chain','tree')))
main()
