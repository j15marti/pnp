#!/usr/bin/env python3
"""LSPV2-328 compact exact complement-pair M22 SAT terminal.
Only valid proper duplicate-free Doecker monotone 3-SAT-(2,2) originals.
This familiar satisfiable special case does not settle P versus NP.
Usage: python lspv2_328_compact.py original.json
"""
import sys,json,collections

def parse(blob):
    def unique(pairs):
        d={}
        for k,v in pairs:
            if k in d:raise ValueError("duplicate JSON header")
            d[k]=v
        return d
    o=json.loads(blob,object_pairs_hook=unique)
    if type(o)!=dict or set(o)!={'n','clauses'}:raise ValueError('header')
    n,F=o['n'],o['clauses']
    if type(n)!=int or n<3 or n%3 or type(F)!=list or 3*len(F)!=4*n:raise ValueError('size')
    quota=collections.Counter();seen=set()
    for c in F:
        if type(c)!=list or len(c)!=3 or any(type(v)!=int or not 1<=abs(v)<=n for v in c):raise ValueError('triple')
        if len({abs(v) for v in c})!=3 or not (all(x>0 for x in c) or all(x<0 for x in c)):raise ValueError('proper monotone')
        key=tuple(sorted(c))
        if key in seen:raise ValueError('duplicate clause')
        seen.add(key);quota.update(c)
    if any(quota[i]!=2 or quota[-i]!=2 for i in range(1,n+1)):raise ValueError('(2,2)')
    return n,F

def solve_pair(n,F):
    pos={};neg={};ends={i:[] for i in range(1,n+1)}
    for j,c in enumerate(F,1):
        key=tuple(sorted(map(abs,c)))
        if c[0]>0:
            pos[key]=j
            for v in c:ends[v].append(j)
        else:neg[key]=j
    if set(pos)!=set(neg):return None
    vertices=sorted(pos.values());graph={v:[] for v in vertices}
    original={('x',i):tuple(ends[i]) for i in range(1,n+1)}
    for e,(a,b) in original.items():
        if len(ends[e[1]])!=2 or a==b:raise ValueError('bad dual')
        graph[a].append(b);graph[b].append(a)
    components=[];seen=set()
    for start in vertices:
        if start in seen:continue
        todo=[start];seen.add(start);component=[]
        while todo:
            v=todo.pop();component.append(v)
            for w in graph[v]:
                if w not in seen:seen.add(w);todo.append(w)
        components.append(sorted(component))
    colors={}
    for component in components:
        if len(component)%2:raise AssertionError('cubic order parity')
        E={e:uv for e,uv in original.items() if uv[0] in component}
        for k,(a,b) in enumerate(zip(component[::2],component[1::2])):
            E[('aux',k)]=(a,b)
        A={v:[] for v in component}
        for e,(a,b) in E.items():
            A[a].append((e,b));A[b].append((e,a))
        assert all(len(A[v])==4 for v in component)
        stack=[component[0]];incoming=[];used=set();reversed_tour=[]
        while stack:
            v=stack[-1]
            while A[v] and A[v][-1][0] in used:A[v].pop()
            if not A[v]:
                stack.pop()
                if incoming:reversed_tour.append(incoming.pop())
                continue
            e,w=A[v].pop()
            if e in used:continue
            used.add(e);stack.append(w);incoming.append(e)
        tour=reversed_tour[::-1]
        assert len(tour)==len(E)==2*len(component)
        for j,e in enumerate(tour):
            if e[0]=='x':colors[e[1]]=j%2
    bits=[colors[i] for i in range(1,n+1)]
    assert all(any(bits[abs(x)-1]==int(x>0) for x in c) for c in F)
    return bits

def matrix():
    states=((0,0),(0,1),(1,0),(1,1))
    return [[sum(len({s[0],t[0],r})>1 and len({s[1],t[1],r})>1 for r in (0,1))
             for t in states] for s in states]

def trace_power(M,k):
    X=[[int(i==j) for j in range(4)] for i in range(4)]
    for _ in range(k):
        X=[[sum(X[i][a]*M[a][j] for a in range(4)) for j in range(4)] for i in range(4)]
    return sum(X[i][i] for i in range(4))

if __name__=='__main__':
    n,F=parse(open(sys.argv[1]).read()) if len(sys.argv)>1 else parse(json.dumps({
       'n':6,'clauses':[[1,2,3],[1,4,5],[2,4,6],[3,5,6],
                        [-1,-2,-3],[-1,-4,-5],[-2,-4,-6],[-3,-5,-6]]}))
    witness=solve_pair(n,F)
    print(json.dumps({'canonical':True,'recognized_paired':witness is not None,
       'SAT_witness_if_recognized':witness,'UNRESOLVED_if_unpaired':witness is None,
       'prism_transfer_matrix':matrix(),'prism_k3_models':trace_power(matrix(),3),
       'P_vs_NP':'OPEN'},indent=2))
