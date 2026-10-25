#!/usr/bin/env python3
"""Independent minimal exact audit for ARC-SCOPE-TOLL160; finite checks only."""
from itertools import product

def truth(F):
    vs=sorted({abs(v) for c in F for v in c})
    for bits in product([0,1],repeat=len(vs)):
        a=dict(zip(vs,bits))
        if all(any(a[abs(v)]==int(v>0) for v in c) for c in F):return True
    return False

def scoped(F):
    first={};last={}
    for j,c in enumerate(F):
        for z in c:first.setdefault(abs(z),j);last[abs(z)]=j
    ev=[];live=set();w=0
    for j,c in enumerate(F):
        for v in sorted(x for x in first if first[x]==j):
            live.add(v);ev.append(('open',v));w=max(w,len(live))
        assert all(abs(z) in live for z in c)
        ev.append(('clause',c))
        for v in sorted(x for x in last if last[x]==j):
            live.remove(v);ev.append(('close',v))
    assert not live
    a=[];rows={()};peak=1
    for op,arg in ev:
        if op=='open':
            a.append(arg);rows={t+(b,) for t in rows for b in (0,1)}
        elif op=='clause':
            pos={v:i for i,v in enumerate(a)}
            rows={t for t in rows if any(t[pos[abs(z)]]==int(z>0) for z in arg)}
        else:
            i=a.index(arg);rows={t[:i]+t[i+1:] for t in rows};a.pop(i)
        peak=max(peak,len(rows))
    assert not a and peak<=2**w
    return bool(rows),w,peak

def encode(F):
    n=max((abs(x) for c in F for x in c),default=0)
    b=(f'p cnf {n} {len(F)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in F)).encode()
    rows=b.decode().splitlines();h=rows.pop(0).split()
    assert int(h[3])==len(rows)
    G=tuple(tuple(map(int,r.split()[:-1])) for r in rows)
    assert G==F
    return G,len(b)*8

def two_level(F,depth,c):
    F,bits=encode(F);s,w,p=scoped(F)
    assert s==truth(F)
    c['checked']+=1;c['emitted_bits']+=bits;c['max_width']=max(c['max_width'],w)
    if depth==0 or len(F)<2:
        c['actual_leaf_calls']+=1;return truth(F)
    j=len(F)//2
    V=sorted({abs(x) for z in F[:j] for x in z}&{abs(x) for z in F[j:] for x in z})
    for z in product((0,1),repeat=len(V)):
        pins=tuple((v if b else -v,) for v,b in zip(V,z))
        if two_level(F[:j]+pins,depth-1,c) and two_level(F[j:]+pins,depth-1,c):return True
    return False

def parity(bits):
    F=[(-1,)];n=len(bits)
    for i,b in enumerate(bits):
        u=i+1;v=i+2
        F.extend(((u,v),(-u,-v)) if b else ((-u,v),(u,-v)))
    F.append((-(n+1),))
    return tuple(F)

F8=tuple(tuple(i+1 if z[i]==0 else -(i+1) for i in range(3)) for z in product((0,1),repeat=3))
Y=((1,2,3),(1,4,5),(2,4,6),(3,5,6),(-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
controls=[('F8',F8,False),('F8-1',F8[:-1],True),('Y6',Y,True),
          ('even',parity((0,0,0,0)),True),('odd',parity((1,0,0,0)),False),
          ('Horn',((1,),(-1,2),(-2,3),(-3,)),False)]
count={'checked':0,'actual_leaf_calls':0,'emitted_bits':0,'max_width':0}
for name,F,expected in controls:
    assert truth(F)==expected and two_level(F,2,count)==expected,name
print({'status':'PASS','tests':len(controls),'sat':sum(x[2] for x in controls),
       'unsat':sum(not x[2] for x in controls),**count,
       'scope':'ordinary CNF serialized and parsed at both actual recursive levels'})
