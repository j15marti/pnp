"""Strict-C graph-coloring reduction: exact semantics, not a runtime lower bound."""
from itertools import product, combinations
from math import prod
import hashlib
import json

ALLOWED = {frozenset((i, (i+1)%5, (i+2)%5)) for i in range(5)}

def C(a,b,c):
    return len({a,b,c}) == 3 and frozenset((a,b,c)) in ALLOWED

def gamma(k):
    assert k >= 1
    s = bin(k)[2:]
    return '0'*(len(s)-1)+s

def header(v,e):
    return '1'*v+'0'+gamma(e+1)

def read_header(s):
    if any(c not in '01' for c in s): raise ValueError('nonbinary')
    pos = 0
    while pos < len(s) and s[pos] == '1': pos += 1
    if pos == len(s): raise ValueError('missing unary terminator')
    v = pos; pos += 1; z = 0
    while pos < len(s) and s[pos] == '0': z += 1; pos += 1
    if pos+z >= len(s): raise ValueError('truncated gamma')
    k = int(s[pos:pos+z+1],2); pos += z+1
    return v,k-1,pos

def graph_encode(v,edges):
    edges = sorted(tuple(sorted(e)) for e in edges)
    assert len(set(edges)) == len(edges)
    assert all(0 <= a < b < v for a,b in edges)
    w = v.bit_length()
    return header(v,len(edges))+''.join(format(x+1,f'0{w}b') for e in edges for x in e)

def graph_decode(s):
    v,e,p = read_header(s); w = v.bit_length()
    if e > v*(v-1)//2 or len(s)-p != 2*e*w: raise ValueError('bad length/count')
    edges=[]
    for _ in range(e):
        a=int(s[p:p+w],2)-1; p+=w
        b=int(s[p:p+w],2)-1; p+=w
        if not 0 <= a < b < v: raise ValueError('bad edge')
        if edges and edges[-1] >= (a,b): raise ValueError('noncanonical edge list')
        edges.append((a,b))
    return v,edges

def construct(v,edges):
    # Graph vertices X_i=5+i. Private domain leaves follow, then edge leaves.
    anchors=tuple(range(5)); xs=tuple(range(5,5+v))
    clauses=[(i,(i+1)%5,(i+2)%5) for i in range(5)]
    for i,x in enumerate(xs):
        clauses += [(0,x,5+v+2*i),(1,x,5+v+2*i+1)]
    for j,(u,w) in enumerate(edges): clauses.append((xs[u],xs[w],5+3*v+j))
    n=5+3*v+len(edges)
    assert all(len(set(t))==3 and all(0 <= x < n for x in t) for t in clauses)
    return n,clauses,anchors,xs

def t5_encode(n,clauses):
    w=n.bit_length()
    return header(n,len(clauses))+''.join(format(x+1,f'0{w}b') for t in clauses for x in t)

def t5_decode(s):
    n,m,p=read_header(s); w=n.bit_length()
    if len(s)-p != 3*m*w: raise ValueError('bad T5 length')
    clauses=[]
    for _ in range(m):
        t=[]
        for _ in range(3):
            t.append(int(s[p:p+w],2)-1); p+=w
        if len(set(t))!=3 or any(x<0 or x>=n for x in t): raise ValueError('bad T5 clause')
        clauses.append(tuple(t))
    return n,clauses

def compile_bits(source):
    v,e=graph_decode(source)
    n,cs,_,_=construct(v,e)
    return t5_encode(n,cs)

FRAME_VALUES=[a for a in product(range(5),repeat=5)
              if all(C(a[i],a[(i+1)%5],a[(i+2)%5]) for i in range(5))]

def clause_count(n,clauses,anchors,xs,frames=FRAME_VALUES):
    # Generic sum-out of ACTUAL degree-one private variables, using only C.
    # This is an exact small-instance verifier, not an arbitrary fast solver.
    shared=set(anchors)|set(xs)
    private=set(range(n))-shared
    assert all(sum(p in t for t in clauses)==1 for p in private)
    core=[]; factors=[]
    for t in clauses:
        ps=[p for p in t if p in private]
        if not ps: core.append(t); continue
        assert len(ps)==1
        others=tuple(x for x in t if x!=ps[0])
        table={(a,b):sum(C(a,b,c) for c in range(5)) for a,b in product(range(5),repeat=2)}
        factors.append((others,table))
    total=0; extensions={}
    for av in frames:
        base=dict(zip(anchors,av))
        for xv in product(range(5),repeat=len(xs)):
            vals=base|dict(zip(xs,xv))
            if not all(C(*(vals[x] for x in t)) for t in core):continue
            z=1
            for (a,b),table in factors:
                z*=table[vals[a],vals[b]]
                if not z:break
            total+=z
            extensions[av,xv]=z
    return total,extensions

def coloring_reference(v,edges):
    weights=(2,1,2); pair=((0,2,1),(2,0,2),(1,2,0))
    plain=weighted=0
    for a in product(range(3),repeat=v):
        if any(a[u]==a[w] for u,w in edges):continue
        plain+=1
        weighted+=prod(weights[x] for x in a)*prod(pair[a[u]][a[w]] for u,w in edges)
    return plain,10*weighted

def brute(n,clauses):
    return sum(all(C(*(a[x] for x in t)) for t in clauses)
               for a in product(range(5),repeat=n))

def main():
    assert set(FRAME_VALUES)=={tuple((s+d*i)%5 for i in range(5)) for s in range(5) for d in (-1,1)}
    rows=[]; cases=interface_checks=0; all_counts=[]
    # Canonical frame suffices here; all ten are checked separately below.
    for v in range(6):
        possible=list(combinations(range(v),2)); sat=unsat=0
        for mask in range(1<<len(possible)):
            edges=[e for j,e in enumerate(possible) if mask>>j&1]
            source=graph_encode(v,edges); output=compile_bits(source)
            n,cs=t5_decode(output); _,_,aa,xx=construct(v,edges)
            assert n==5+3*v+len(edges) and len(cs)==5+2*v+len(edges)
            assert len(output)==n+1+len(gamma(len(cs)+1))+3*len(cs)*n.bit_length()
            z,ext=clause_count(n,cs,aa,xx,[tuple(range(5))])
            plain,expected=coloring_reference(v,edges)
            assert 10*z==expected and (z>0)==(plain>0)
            for (_,xv),count in ext.items():
                truth=all(x in (2,3,4) for x in xv) and all(xv[a]!=xv[b] for a,b in edges)
                assert (count>0)==truth
                interface_checks+=1
            sat+=int(z>0); unsat+=int(z==0); cases+=1
            all_counts.append((v,mask,plain,10*z))
        rows.append({'vertices':v,'graphs':sat+unsat,'SAT':sat,'UNSAT':unsat})
    controls={}
    graphs={'empty':(0,[]),'isolated_vertex':(1,[]),'edge':(2,[(0,1)]),
            'triangle':(3,[(0,1),(0,2),(1,2)]),'K4':(4,list(combinations(range(4),2))),
            'path4':(4,[(0,1),(1,2),(2,3)]),'star4':(4,[(0,1),(0,2),(0,3)])}
    for name,(v,edges) in graphs.items():
        n,cs,aa,xx=construct(v,edges); z,_=clause_count(n,cs,aa,xx)
        plain,expected=coloring_reference(v,edges); assert z==expected
        rename={i:n-1-i for i in range(n)}
        renamed=[tuple(rename[x] for x in reversed(t)) for t in reversed(cs)]
        rz,_=clause_count(n,renamed,tuple(rename[x] for x in aa),tuple(rename[x] for x in xx))
        assert rz==z
        bits=t5_encode(n,cs)
        controls[name]={'v':v,'edges':edges,'n':n,'m':len(cs),'N':len(bits),
                        'three_colorings':plain,'T5_count':z,'renamed_reordered_count':rz,
                        'decision':'SAT' if z else 'UNSAT','encoded_bits':bits}
    for name in ('empty','isolated_vertex'):
        v,es=graphs[name]; n,cs,_,_=construct(v,es)
        assert brute(n,cs)==controls[name]['T5_count']
    assert controls['path4']['three_colorings']==controls['star4']['three_colorings']==24
    assert controls['path4']['T5_count']==6400 and controls['star4']['T5_count']==7680
    malformed=['','1','010','x','001','110001']
    rejected=0
    for s in malformed:
        try:compile_bits(s)
        except ValueError:rejected+=1
        else:raise AssertionError(('accepted malformed',s))
    raw={'status':'PASS','scope':'finite semantic evidence, no asymptotic resource inference',
         'graph_cases':cases,'by_vertex_count':rows,'interface_rows':interface_checks,
         'anchor_frames':FRAME_VALUES,'controls':controls,'malformed_graph_sources_rejected':rejected,
         'full_assignment_controls':{'empty':5**5,'isolated_vertex':5**8},
         'all_graph_results':all_counts,'seed':None}
    print(json.dumps(raw,indent=2))

if __name__=='__main__':main()
