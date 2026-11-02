#!/usr/bin/env python3
"""LSPV-3 GATE321 compact independent source-key census.
Full separate no-import verifier and raw per-subset output are in the run archive.
NO semantic SAT-label oracle is granted to a decision algorithm: enumeration below
is OFFLINE measurement, not the runtime of a proposed polynomial SAT solver.
"""
import itertools, collections, json
F9=((1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9),
    (-4,-6,-8),(-1,-6,-7),(-2,-3,-4),(-3,-5,-8),(-1,-2,-9),(-5,-7,-9))
Y6=((1,2,3),(1,4,5),(2,4,6),(3,5,6),
    (-1,-2,-4),(-1,-3,-6),(-2,-3,-5),(-4,-5,-6))
def grammar(F,n):
    if n%3 or len(F)*3!=4*n:return False
    d=collections.Counter(); seen=set()
    for c in F:
        if len(c)!=3 or len({abs(z) for z in c})!=3:return False
        if not(all(z>0 for z in c) or all(z<0 for z in c)):return False
        if any(type(z)!=int or not 1<=abs(z)<=n for z in c):return False
        if tuple(sorted(c)) in seen:return False
        seen.add(tuple(sorted(c)));d.update(c)
    return all(d[v]==d[-v]==2 for v in range(1,n+1))
def original(F,mask):
    return int(all(any(int(bool(mask & (1<<(abs(z)-1))))==int(z>0)
                   for z in c) for c in F))
def frontier(F,S):
    cross=[];inside=[]
    for j,c in enumerate(F):
        v=sum(1<<(abs(z)-1) for z in c)
        if v&S and v&~S:cross.append(j)
        elif v&~S==0:inside.append(j)
    return cross,inside
def key(F,S,A,front,internal):
    for j in internal:
        if not any(int(bool(A&(1<<(abs(z)-1))))==int(z>0) for z in F[j]):
            return ('DEAD',)
    b=0
    for pos,j in enumerate(front):
        if any((S>>(abs(z)-1)&1) and
               int(bool(A&(1<<(abs(z)-1))))==int(z>0) for z in F[j]):
            b|=1<<pos
    return (S,b)
def table(T,n,S,A):
    free=[v for v in range(n) if not(S>>v&1)]
    result=0
    for k in range(1<<len(free)):
        mask=A|sum(((k>>i)&1)<<v for i,v in enumerate(free))
        result|=T[mask]<<k
    return result
def compile_circuit(F):
    nodes=[];outs=[]
    for j,c in enumerate(F):
        a=('lit',c[0]);b=('lit',c[1]);d=('lit',c[2])
        h=('gate',len(nodes));nodes.append(('OR',a,b))
        q=('gate',len(nodes));nodes.append(('OR',h,d));outs.append(q)
    root=outs[0]
    for q in outs[1:]:
        new=('gate',len(nodes));nodes.append(('AND',root,q));root=new
    return nodes,root
def circuit(nodes,root,x):
    vals=[]
    def get(w):
        return int(bool(x&(1<<(abs(w[1])-1)))==bool(w[1]>0)) if w[0]=='lit' else vals[w[1]]
    for op,u,v in nodes:
        vals.append(int(bool(get(u)) or bool(get(v))) if op=='OR' else int(bool(get(u)) and bool(get(v))))
    return get(root)
def census(F,n):
    assert grammar(F,n)
    T=[original(F,x) for x in range(1<<n)]
    nodes,root=compile_circuit(F)
    assert len(nodes)==3*len(F)-1
    assert all(T[x]==circuit(nodes,root,x) for x in range(1<<n))
    summed=collections.Counter();forward=[];reverse=[]
    for S in range(1<<n):
        pinned=[v for v in range(n) if S>>v&1]
        cross,internal=frontier(F,S)
        groups=collections.defaultdict(set)
        for a in range(1<<len(pinned)):
            A=sum(((a>>i)&1)<<v for i,v in enumerate(pinned))
            groups[key(F,S,A,cross,internal)].add(table(T,n,S,A))
            summed['partial_assignments']+=1
            summed['offline_semantic_truth_bits']+=1<<(n-len(pinned))
        assert all(len(g)==1 for g in groups.values())
        q={'S':S,'key_count':len(groups),
           'exact_count':len({next(iter(g)) for g in groups.values()}),
           'crossing':len(cross)}
        summed['source_keys']+=q['key_count'];summed['exact_cofactors']+=q['exact_count']
        if S in [(1<<k)-1 for k in range(n+1)]:forward.append(q)
        if S in [((1<<n)-1)^((1<<(n-k))-1) for k in range(n+1)]:reverse.append(q)
    forward.sort(key=lambda r:r['S'].bit_count())
    reverse.sort(key=lambda r:r['S'].bit_count())
    return {'n':n,'m':len(F),'models':sum(T),'gates':len(nodes),
            'summary':dict(summed),'forward':forward,'reverse':reverse}
def main():
    a=census(F9,9);b=census(Y6,6)
    assert (a['models'],b['models'])==(70,20)
    assert (a['summary']['source_keys'],a['summary']['exact_cofactors'])==(10325,7026)
    assert (b['summary']['source_keys'],b['summary']['exact_cofactors'])==(483,400)
    common={3:0,5:1,6:0,7:0,8:0}
    pinresults={}
    for bit in (0,1):
        a0=common|{1:bit};free=[v for v in range(1,10) if v not in a0]
        rows=[]
        for vals in itertools.product((0,1),repeat=len(free)):
            assign=a0|dict(zip(free,vals))
            mask=sum(assign[v]<<(v-1) for v in range(1,10))
            rows.append(original(F9,mask))
        pinresults[str(bit)]=sum(rows)
    assert pinresults=={'0':2,'1':0}
    malformed=(F9[:-1],F9+((1,2,3),),F9[:-1]+((1,1,2),),F9[:-1]+((1,2,-3),))
    assert all(not grammar(F,9) for F in malformed)
    out={'F9':a,'Y6':b,'F9_same_source_pins':pinresults,'malformed':len(malformed),
         'note':'This is offline enumeration, not free semantic quotient acquisition.'}
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':main()
