#!/usr/bin/env python3
"""TMR-4/069 reproducible compact five-symbol source-to-diagram check."""
from itertools import product
from random import Random

OUT=[sum(1<<b for b in range(5) if (b-a)%5 in (1,3)) for a in range(5)]
IN=[sum(1<<b for b in range(5) if (a-b)%5 in (1,3)) for a in range(5)]

def encode(n, arcs):
    arcs=sorted(set(arcs))
    return ('p t5 %d %d\n'%(n,len(arcs))+
            ''.join('v %d\n'%i for i in range(n))+
            ''.join('e %d %d\n'%(u,v) for u,v in arcs)).encode('ascii')

def parse(data):
    try: text=data.decode('ascii')
    except UnicodeDecodeError: raise ValueError('non-ASCII')
    if not text.endswith('\n') or '\r' in text:raise ValueError('bad newline')
    lines=text.splitlines();head=lines[0].split(' ')
    if len(head)!=4 or head[:2]!=['p','t5']:raise ValueError('header')
    def num(s):
        if not s.isascii() or not s.isdecimal() or (len(s)>1 and s[0]=='0'):
            raise ValueError('number')
        if len(s)>len(str(len(lines))):raise ValueError('huge number')
        return int(s)
    n,m=num(head[2]),num(head[3])
    if len(lines)!=1+n+m:raise ValueError('missing declarations')
    if any(lines[i+1]!='v %d'%i for i in range(n)):
        raise ValueError('vertex list')
    arcs=[]
    for row in lines[n+1:]:
        z=row.split(' ')
        if len(z)!=3 or z[0]!='e':raise ValueError('arc syntax')
        u,v=num(z[1]),num(z[2])
        if u>=n or v>=n:raise ValueError('arc range')
        arcs.append((u,v))
    if arcs!=sorted(set(arcs)) or encode(n,arcs)!=data:
        raise ValueError('not canonical')
    return n,arcs

def compile_graph(data):
    n,arcs=parse(data);e=set(arcs)
    stages=[{(31,)*n}];trans=[];weights={(31,)*n:1}
    for t in range(n):
        nextstates=set();nextweights={};T={}
        for key in stages[-1]:
            children=[]
            for c in range(5):
                if (t,t) in e or not (key[0]>>c)&1:
                    children.append(None);continue
                z=list(key[1:])
                for j in range(t+1,n):
                    if (t,j) in e:z[j-t-1]&=OUT[c]
                    if (j,t) in e:z[j-t-1]&=IN[c]
                if 0 in z:children.append(None);continue
                z=tuple(z);nextstates.add(z);children.append(z)
                nextweights[z]=nextweights.get(z,0)+weights[key]
            T[key]=tuple(children)
        trans.append(T);stages.append(nextstates);weights=nextweights
    # Explicit five-way edges (including sink) at every original-variable layer.
    M={}; B={};
    for t in range(n):
        for key in list(stages[t])+['reject']:
            name=(t,key)
            if key=='reject':
                successors=[(t+1,'reject') if t<n-1 else 'zero']*5
            else:
                successors=[]
                for child in trans[t][key]:
                    if child is None:successors.append((t+1,'reject') if t<n-1 else 'zero')
                    else:successors.append((t+1,child) if t<n-1 else 'one')
            M[name]=tuple(successors)
            for depth in range(3):
                for prefix in range(1<<depth):
                    bname=(t,key,depth,prefix)
                    if depth<2:
                        B[bname]=tuple((t,key,depth+1,2*prefix+b) for b in (0,1))
                    else:
                        endpoints=[]
                        for bit in (0,1):
                            c=2*prefix+bit
                            dst=successors[c] if c<5 else ((t+1,'reject') if t<n-1 else 'zero')
                            endpoints.append((dst[0],dst[1],0,0) if isinstance(dst,tuple) else dst)
                        B[bname]=tuple(endpoints)
    return n,arcs,trans,(('one' if n==0 else (0,(31,)*n)),M),(('one' if n==0 else (0,(31,)*n,0,0)),B),sum(weights.values())

def count_paths(root, graph, base, steps):
    if steps==0:return int(root=='one')
    states={root:1}
    for _ in range(steps):
        nxt={}
        for key,w in states.items():
            for dest in graph[key]:nxt[dest]=nxt.get(dest,0)+w
        states=nxt
    assert sum(states.values())==base**steps
    return states.get('one',0)

def audit():
    rng=Random(20261117069);cases=0
    for n in range(8):
        for _ in range(12):
            arcs=[(u,v) for u in range(n) for v in range(n)
                  if u!=v and rng.randrange(4)==0]
            N,E,T,m,b,c=compile_graph(encode(n,arcs));cases+=1
            exact=sum(all((a[v]-a[u])%5 in (1,3) for u,v in E)
                      for a in product(range(5),repeat=n))
            assert c==exact==count_paths(*m,5,n)==count_paths(*b,2,3*n)
            assert len(b[1])==7*len(m[1])
    print('PASS',cases,'canonical sources, original brute force, explicit 5-MDD/3-bit OBDD counts')

if __name__=='__main__':audit()
