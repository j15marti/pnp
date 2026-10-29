#!/usr/bin/env python3
"""Exact finite controls for repeated negative-occurrence G splices.

Research control only: standard library, deterministic, no oracle table.
"""
import collections, hashlib, itertools, json

W1 = (
(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))

def canon(cs):
    return tuple(sorted(tuple(sorted(c,key=lambda z:(abs(z),z<0))) for c in cs))

def gbase():
    cs=[list(c) for c in W1]
    for j in (6,11): cs[j][0]=-cs[j][0]
    return canon(cs)

def affine(r):
    def v(g,i): return g*r+(i%r)+1
    out=[]
    for s in range(4):
        for i in range(r):
            a,b,c=v(0,i),v(1,i+s),v(2,i+2*s)
            out.append(((-a if s<2 else a),(-b if s>=2 else b),
                        (-c if s in (0,2) else c)))
    return canon(out)

def exact22(cs,n):
    if len(cs)*3!=4*n or len(cs)!=len(set(cs)): return False
    cnt=collections.Counter(z for c in cs for z in c)
    if any(cnt[v]!=2 or cnt[-v]!=2 for v in range(1,n+1)): return False
    adj={v:set() for v in range(1,n+1)}
    for c in cs:
        if len({abs(z) for z in c})!=3:return False
        for u in map(abs,c): adj[u].update(map(abs,c))
    seen={1}; todo=[1]
    while todo:
        u=todo.pop()
        for v in adj[u]:
            if v not in seen: seen.add(v); todo.append(v)
    return len(seen)==n

def solve(cs,pins=None):
    def rec(a,clauses):
        while True:
            residual=[]; units=[]
            for c in clauses:
                if any(abs(z) in a and a[abs(z)]==(z>0) for z in c):continue
                live=[z for z in c if abs(z) not in a]
                if not live:return None
                residual.append(live)
                if len(live)==1:units.append(live[0])
            if not residual:return a
            if not units:break
            for z in units:
                v,b=abs(z),z>0
                if v in a and a[v]!=b:return None
                a[v]=b
        freq=collections.Counter(abs(z) for c in residual for z in c)
        v=max(freq,key=lambda q:(freq[q],-q))
        for b in (False,True):
            r=rec({**a,v:b},residual)
            if r is not None:return r
        return None
    return rec(dict(pins or {}),cs)

def source_profile(h,x,slot):
    foot=tuple(z for z in h[slot] if abs(z)!=x)
    stripped=h[:slot]+h[slot+1:]
    h0=solve(h,{x:False}) is not None
    h1=solve(h,{x:True}) is not None
    q0=solve(stripped+(foot,),{x:False}) is not None
    assert not q0 or h0
    return {'H0':h0,'H1':h1,'Q0':q0},foot

def attach(cs,n,port,slot):
    old=list(map(list,cs)); foot=tuple(z for z in old[slot] if abs(z)!=port)
    assert -port in old[slot] and len(foot)==2
    newg=[[z+n if z>0 else z-n for z in c] for c in gbase()]
    newp=n+4
    assert -newp in newg[2]
    old[slot][old[slot].index(-port)]=-newp
    newg[2][newg[2].index(-newp)]=-port
    out=canon(old+newg)
    target=tuple(sorted((-newp,*foot),key=lambda z:(abs(z),z<0)))
    newslot=out.index(target)
    assert exact22(out,n+15)
    return out,n+15,newp,newslot

def relation(cs,x,p):
    return {f'{a}{b}': solve(cs,{x:bool(a),p:bool(b)}) is not None
            for a,b in itertools.product((0,1),repeat=2)}

def dimacs(cs,n):
    return ('p cnf %d %d\n'%(n,len(cs))+''.join(' '.join(map(str,c))+' 0\n' for c in cs)).encode()

def matrix_product(a,b):
    return [[any(a[i][k] and b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]

def run_case(name,h,n,x,slot,levels):
    assert exact22(h,n)
    prof,_=source_profile(h,x,slot)
    expected={'00':prof['H0'],'01':prof['Q0'],'10':False,'11':prof['H1']}
    rows=[]; cs=h; nn=n; port=x; current_slot=slot; last_bits=len(dimacs(cs,nn))*8
    for level in range(1,levels+1):
        cs,nn,port,current_slot=attach(cs,nn,port,current_slot)
        got=relation(cs,x,port)
        assert got==expected,(name,level,got,expected)
        bits=len(dimacs(cs,nn))*8
        assert bits>last_bits
        rows.append({'level':level,'variables':nn,'clauses':len(cs),'bits':bits,
                     'growth_bits':bits-last_bits,'relation':got})
        last_bits=bits
    return {'name':name,'source_profile':prof,'expected_relation':expected,
            'levels':rows,'final_sha256':hashlib.sha256(dimacs(cs,nn)).hexdigest()}

def small_sources():
    clauses=tuple(itertools.product((1,-1),repeat=3))
    signed=tuple(tuple((i+1)*s[i] for i in range(3)) for s in clauses)
    out=[]
    for subset in itertools.combinations(signed,4):
        c=canon(subset)
        if exact22(c,3):out.append(c)
    assert len(out)==8
    return out

cases=[]
G=gbase(); cases.append(run_case('G equality',G,15,4,next(i for i,c in enumerate(G) if -4 in c),3))
A=affine(5); cases.append(run_case('affine implication',A,15,1,next(i for i,c in enumerate(A) if -1 in c),3))
for i,h in enumerate(small_sources()):
    cases.append(run_case('small-%d'%i,h,3,1,next(j for j,c in enumerate(h) if -1 in c),2))

matrix_controls=[]
for h0,h1,q0 in itertools.product((False,True),repeat=3):
    if q0 and not h0:continue
    m=[[h0,q0],[False,h1]]
    sq=matrix_product(m,m)
    assert sq==m
    matrix_controls.append({'H0':h0,'H1':h1,'Q0':q0,'idempotent':True})

print(json.dumps({'status':'PASS','run':'TRIANGULAR-SPLICE-IDEMPOTENCE197',
 'cases':cases,'matrix_controls':matrix_controls,
 'claims':['Repeated transported-foot splicing preserves the same triangular endpoint relation.',
           'The Boolean relation matrix is idempotent whenever Q0 implies H0.',
           'Every tested physical level grows and remains connected strict exact-(2,2).'],
 'limitations':['Finite DPLL controls are not kernel verification.',
                'Other occurrences, positive splices, and multi-gadget regulators remain open.',
                'No arbitrary-SAT shrinker or lower bound follows.']},indent=2,sort_keys=True))
