#!/usr/bin/env python3
"""Independent referee for exact22 two-swap transport223.

Produces source-indexed Resolution traces for all four fixed-guard forbidden
branches and finite three-port fanout controls. Standard library only.
"""
import collections, hashlib, itertools, json

W1=((-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))

def clause(c): return tuple(sorted(set(c),key=lambda z:(abs(z),z<0)))
def canon(C): return tuple(sorted(map(clause,C)))
def guard():
    C=[list(c) for c in W1]
    for j in (6,11):C[j][0]*=-1
    return canon(C)

def affine(p):
    def v(g,i):return g*p+(i%p)+1
    C=[]
    for s in range(4):
        for i in range(p):
            a,b,c=v(0,i),v(1,i+s),v(2,i+2*s)
            C.append((-a if s<2 else a,-b if s>=2 else b,-c if s in (0,2) else c))
    return canon(C)

def exact_connected(C,n):
    if 3*len(C)!=4*n or len(C)!=len(set(C)):return False
    count=collections.Counter(x for c in C for x in c)
    if any(count[v]!=2 or count[-v]!=2 for v in range(1,n+1)):return False
    g=[set() for _ in range(n+len(C))]
    for j,c in enumerate(C):
        if len(c)!=3 or len({abs(x) for x in c})!=3:return False
        for x in c:g[abs(x)-1].add(n+j);g[n+j].add(abs(x)-1)
    seen={0};todo=[0]
    while todo:
        for y in g[todo.pop()]:
            if y not in seen:seen.add(y);todo.append(y)
    return len(seen)==len(g)

def dimacs(C,n):
    return ('p cnf %d %d\n'%(n,len(C))+''.join(' '.join(map(str,c))+' 0\n' for c in C)).encode()

def dpll(C,pins=None):
    calls=[0]
    def rec(A,cls):
        calls[0]+=1
        while True:
            rem=[];units=[]
            for c in cls:
                if any(abs(x) in A and A[abs(x)]==(x>0) for x in c):continue
                live=[x for x in c if abs(x) not in A]
                if not live:return None
                rem.append(live)
                if len(live)==1:units.append(live[0])
            if not rem:return A
            if not units:break
            for x in units:
                v,b=abs(x),x>0
                if v in A and A[v]!=b:return None
                A[v]=b
        freq=collections.Counter(abs(x) for c in rem for x in c)
        v=max(freq,key=lambda q:(freq[q],-q))
        for b in (False,True):
            z=rec({**A,v:b},rem)
            if z is not None:return z
        return None
    return rec(dict(pins or {}),C),calls[0]

def splice2(H,n,x):
    assert exact_connected(H,n)
    hp=next(j for j,c in enumerate(H) if x in c)
    hn=next(j for j,c in enumerate(H) if -x in c)
    p=n+4; A=[list(c) for c in H]
    A[hp][A[hp].index(x)]=p;A[hn][A[hn].index(-x)]=-p
    B=[[z+n if z>0 else z-n for z in c] for c in guard()]
    assert p in B[15] and -p in B[2]
    B[15][B[15].index(p)]=x;B[2][B[2].index(-p)]=-x
    F=canon(A+B);assert exact_connected(F,n+15)
    return F,n+15,p

def resolution_trace(source):
    clauses=[];parents=[];origin=[];cmap={}
    def add(c,src=None,par=None):
        c=clause(c)
        if any(-x in c for x in c):return None
        if c in cmap:return cmap[c]
        i=len(clauses);clauses.append(c);parents.append(par);origin.append(src);cmap[c]=i;return i
    active=set(add(c,src=i) for i,c in enumerate(source))
    while () not in (clauses[i] for i in active):
        vs=sorted({abs(x) for i in active for x in clauses[i]})
        assert vs
        opts=[]
        for v in vs:
            P=[i for i in active if v in clauses[i]];N=[i for i in active if -v in clauses[i]]
            opts.append((len(P)*len(N),len(P)+len(N),v,P,N))
        _,_,v,P,N=min(opts);new=set()
        for a in P:
            for b in N:
                rid=add((set(clauses[a])-{v})|(set(clauses[b])-{-v}),par=(a,b,v))
                if rid is not None:new.add(rid)
        active={i for i in active if v not in clauses[i] and -v not in clauses[i]}|new
    empty=next(i for i in active if clauses[i]==())
    need=set()
    def mark(i):
        if i in need:return
        need.add(i)
        if parents[i]:mark(parents[i][0]);mark(parents[i][1])
    mark(empty);order=sorted(need);remap={x:i for i,x in enumerate(order)};trace=[]
    for old in order:
        row={'id':remap[old],'clause':clauses[old]}
        if parents[old]:
            a,b,v=parents[old];row.update(parents=[remap[a],remap[b]],pivot=v)
        else:row['source']=origin[old]
        trace.append(row)
    return trace,remap[empty]

def verify_resolution(source,trace,empty):
    got=[]
    for row in trace:
        c=tuple(row['clause'])
        if 'source' in row:assert c==clause(source[row['source']])
        else:
            a,b=row['parents'];v=row['pivot'];A=set(got[a]);B=set(got[b])
            if -v in A and v in B:A,B=B,A
            assert v in A and -v in B
            R=(A-{v})|(B-{-v});assert not any(-x in R for x in R);assert c==clause(R)
        got.append(c)
    assert got[empty]==()

def small_sources():
    L=[tuple((i+1) if b else -(i+1) for i,b in enumerate(bits)) for bits in itertools.product((0,1),repeat=3)]
    return [canon(Q) for Q in itertools.combinations(L,4) if exact_connected(canon(Q),3)]

def fanout_case(name,H,n,x,depth=3):
    F=H;nn=n;ports=[];sizes=[len(dimacs(F,nn))*8]
    for _ in range(depth):
        F,nn,p=splice2(F,nn,x);ports.append(p);sizes.append(len(dimacs(F,nn))*8)
    tests=0;calls=0
    for bits in itertools.product((0,1),repeat=depth+1):
        xv=bits[0];src,c=dpll(H,{x:bool(xv)});calls+=c
        pins={x:bool(xv),**{p:bool(b) for p,b in zip(ports,bits[1:])}}
        got,c=dpll(F,pins);calls+=c;tests+=1
        assert (got is not None)==((src is not None) and all(b==xv for b in bits[1:]))
    return {'name':name,'source_variables':n,'final_variables':nn,'ports':ports,'depth':depth,
            'bits_by_level':sizes,'strict_growth':all(a<b for a,b in zip(sizes,sizes[1:])),
            'joint_tests':tests,'dpll_calls':calls,'final_sha256':hashlib.sha256(dimacs(F,nn)).hexdigest()}

G=guard();remaining=[c for j,c in enumerate(G) if j not in (15,2)]
branches=[{4:1,8:1},{4:1,10:0},{4:0,9:0},{4:0,11:0}]
proofs=[]
for pins in branches:
    src=list(remaining)+[(v if b else -v,) for v,b in sorted(pins.items())]
    trace,empty=resolution_trace(src);verify_resolution(src,trace,empty)
    proofs.append({'pins':pins,'source_clauses':len(src),'proof_rows':len(trace),
                   'derived_rows':sum('parents' in r for r in trace),'empty':empty,'trace':trace})

models={}
for pv in (0,1):
    w,_=dpll(G,{4:bool(pv)});assert w is not None
    for v in range(1,16):w.setdefault(v,False)
    assert all(any(w[abs(z)]==(z>0) for z in c) for c in G)
    models[str(pv)]=[v for v in range(1,16) if w[v]]

sources=small_sources();assert len(sources)==8
fan=[fanout_case('n3-%d'%i,H,3,1) for i,H in enumerate(sources)]
fan.append(fanout_case('guard-SAT',G,15,4))
fan.append(fanout_case('affine-R5',affine(5),15,1))

print(json.dumps({'run':'TWO-SWAP-FANOUT-REFEREE198','status':'PASS','seed':None,
 'guard':{'exact_connected':exact_connected(G,15),'pinned_models':models,
          'resolution_proofs':proofs},
 'fanout_cases':fan,
 'claims':['Four source-indexed Resolution traces prove the guard forbidden branches.',
           'Repeated transport from the same source variable yields exact finite fanout.',
           'Every tested physical level grows.'],
 'limitations':['Resolution checker is project code, not a kernel-verified proof assistant.',
                'The theorem applies only to already connected strict exact-(2,2) sources.',
                'No arbitrary-SAT conversion, power-short child, or runtime lower bound follows.']},sort_keys=True,indent=2))