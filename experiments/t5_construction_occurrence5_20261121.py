"""T5-FULL-EQUALITY-SPLIT1. Exact compiler and finite checks, not a lower bound."""
from itertools import product, combinations
from collections import Counter
import hashlib
import json
from pathlib import Path

ALLOWED = {frozenset((i, (i+1)%5, (i+2)%5)) for i in range(5)}
def C(*t):
    return len(set(t)) == 3 and frozenset(t) in ALLOWED

def validate(n, cs):
    if type(n) is not int or n < 0: raise ValueError('n')
    for t in cs:
        if len(t) != 3 or len(set(t)) != 3: raise ValueError('scope')
        if any(type(x) is not int or not 0 <= x < n for x in t): raise ValueError('id')

def encode(n, cs):
    validate(n, cs)
    g = bin(len(cs)+1)[2:]
    w = n.bit_length()
    return '1'*n+'0'+'0'*(len(g)-1)+g+''.join(format(x+1, f'0{w}b') for t in cs for x in t)

def decode(s):
    if any(x not in '01' for x in s): raise ValueError('alphabet')
    p = 0
    while p < len(s) and s[p] == '1': p += 1
    if p == len(s): raise ValueError('unary')
    n = p; p += 1; z = 0
    while p < len(s) and s[p] == '0': p += 1; z += 1
    if p+z >= len(s): raise ValueError('gamma')
    m = int(s[p:p+z+1], 2)-1; p += z+1
    w = n.bit_length()
    if len(s)-p != 3*m*w or (m and not w): raise ValueError('length')
    cs=[]
    for _ in range(m):
        t=[]
        for _ in range(3): t.append(int(s[p:p+w],2)-1); p += w
        cs.append(tuple(t))
    validate(n,cs)
    return n,cs

def bitlength(n,m):
    return n+1+2*((m+1).bit_length()-1)+1+3*m*n.bit_length()

def equality(u,v,aux):
    a=[u]+list(aux)
    assert len(set(a+[v])) == 6
    return [tuple(a[(i+j)%5] for j in range(3)) for i in range(5)]+[(a[4],v,a[1])]

def split(n,cs):
    validate(n,cs)
    copies=[[] for _ in range(n)]; out=[]; nxt=0
    for t in cs:
        nt=[]
        for x in t: copies[x].append(nxt); nt.append(nxt); nxt+=1
        out.append(tuple(nt))
    for xs in copies:
        if not xs: xs.append(nxt); nxt+=1
    links=[]
    for xs in copies:
        for u,v in zip(xs,xs[1:]):
            aux=list(range(nxt,nxt+4)); nxt+=4
            links.append(dict(u=u,v=v,aux=aux,start=len(out)))
            out.extend(equality(u,v,aux))
    return nxt,out,copies,links

def compile_bits(s):
    n,cs=decode(s); nn,out,_,_=split(n,cs)
    return encode(nn,out)

def interface(cs,u,v,aux):
    table=[[0]*5 for _ in range(5)]
    for x,y in product(range(5),repeat=2):
        for av in product(range(5),repeat=4):
            a=dict(zip(aux,av)); a[u]=x; a[v]=y
            table[x][y]+=all(C(*(a[i] for i in t)) for t in cs)
    return table

def count(n,cs):
    return sum(all(C(*(a[x] for x in t)) for t in cs) for a in product(range(5),repeat=n))

def contract(nn,out,m,links):
    # Read the ACTUAL six-clause blocks; normalize labels, evaluate each new
    # interface exhaustively, and only contract a scalar identity matrix.
    parent=list(range(nn)); eliminated=set(); factor=1; cache={}
    def root(x):
        while parent[x]!=x: x=parent[x]
        return x
    for b in links:
        ids=[b['u'],b['v']]+b['aux']; loc={v:k for k,v in enumerate(ids)}
        block=out[b['start']:b['start']+6]
        key=tuple(tuple(loc[x] for x in t) for t in block)
        if key not in cache: cache[key]=interface(key,0,1,[2,3,4,5])
        table=cache[key]; k=table[0][0]
        assert table==[[k if x==y else 0 for y in range(5)] for x in range(5)] and k>0
        assert not eliminated.intersection(b['aux'])
        assert all(sum(a in t for t in out)==sum(a in t for t in block) for a in b['aux'])
        eliminated.update(b['aux']); factor*=k
        parent[root(b['v'])]=root(b['u'])
    roots=sorted({root(x) for x in range(nn) if x not in eliminated})
    ids={x:i for i,x in enumerate(roots)}
    quotient=[tuple(ids[root(x)] for x in t) for t in out[:m]]
    assert len(out)==m+6*len(links)
    return len(roots),quotient,factor

def graph(v,edges):
    cs=[(i,(i+1)%5,(i+2)%5) for i in range(5)]
    for j in range(v): cs += [(0,5+j,5+v+2*j),(1,5+j,5+v+2*j+1)]
    cs += [(5+u,5+w,5+3*v+j) for j,(u,w) in enumerate(edges)]
    return 5+3*v+len(edges),cs

def graph_count(v,edges):
    # Sum actual private-clause extensions in the normalized anchor frame;
    # ten frames are justified symbolically, also exhaustively checked below.
    total=0
    for xs in product(range(5),repeat=v):
        z=1
        for x in xs: z*=sum(C(0,x,p) for p in range(5))*sum(C(1,x,q) for q in range(5))
        for u,w in edges: z*=sum(C(xs[u],xs[w],l) for l in range(5))
        total+=z
    return 10*total

def check(name,n,cs,z=None,detail=True):
    bits=encode(n,cs); assert decode(bits)==(n,cs)
    nn,out,copies,links=split(n,cs); target=compile_bits(bits)
    assert decode(target)==(nn,out)
    u=len(set(x for t in cs for x in t)); E=3*len(cs)-u
    assert nn==n+15*len(cs)-5*u and len(out)==19*len(cs)-6*u and E==len(links)
    degrees=Counter(x for t in out for x in t)
    assert max(degrees.values(),default=0)<=5
    assert len(bits)==bitlength(n,len(cs)) and len(target)==bitlength(nn,len(out))
    qn,qcs,factor=contract(nn,out,len(cs),links)
    # Exact source syntax after the computed contraction, including unused vars.
    mapback={copies[x][0]:x for x in range(n)}
    roots=sorted(mapback); qmap={j:mapback[r] for j,r in enumerate(roots)}
    assert qn==n and [tuple(qmap[x] for x in t) for t in qcs]==cs
    if z is None: z=count(n,cs)
    zz=count(qn,qcs) if n<=5 else z
    assert zz==z and factor==2**E
    row=dict(name=name,n=n,m=len(cs),N=len(bits),used=u,E=E,n_out=nn,m_out=len(out),N_out=len(target),max_occurrence=max(degrees.values(),default=0),source_count=z,target_count=zz*factor,status='SAT' if z else 'UNSAT',method='exhaustive local interfaces + exact contraction; no full target enumeration',source_bits_sha256=hashlib.sha256(bits.encode()).hexdigest(),target_bits_sha256=hashlib.sha256(target.encode()).hexdigest())
    if detail: row.update(source_clauses=cs,target_clauses=out,target_encoding=target,links=links)
    return row

def main():
    eq=equality(0,1,[2,3,4,5]); table=interface(eq,0,1,[2,3,4,5])
    assert table==[[2 if x==y else 0 for y in range(5)] for x in range(5)]
    frames=[list(a) for a in product(range(5),repeat=5) if all(C(a[i],a[(i+1)%5],a[(i+2)%5]) for i in range(5))]
    assert len(frames)==10
    rows=[]; clauses=list(combinations(range(4),3))
    for mask in range(16): rows.append(check('four_variable_mask_'+str(mask),4,[t for i,t in enumerate(clauses) if mask>>i&1]))
    for name,n,cs in [('zero_variables',0,[]),('unused',5,[(0,1,2)]),('duplicate',3,[(0,1,2)]*2),('degree_five',3,[(0,1,2)]*3)]: rows.append(check(name,n,cs))
    graphs=[('empty',0,[]),('edge',2,[(0,1)]),('triangle',3,[(0,1),(0,2),(1,2)]),('K4',4,list(combinations(range(4),2))),('path4',4,[(0,1),(1,2),(2,3)]),('star4',4,[(0,1),(0,2),(0,3)])]
    for name,v,es in graphs:
        n,cs=graph(v,es); row=check(name,n,cs,graph_count(v,es)); rows.append(row)
        assert (row['n_out'],row['m_out'],row['E'])==(55+18*v+11*len(es),65+20*v+13*len(es),10+3*v+2*len(es))
    # Name/argument/list permutation has identical count, factor and lengths.
    base=[(0,1,2),(0,1,3),(1,2,3)]
    renamed=[tuple(3-x for x in reversed(t)) for t in reversed(base)]
    r1=check('rename_base',4,base); r2=check('renamed_reordered',4,renamed)
    assert [r1[k] for k in ['source_count','target_count','N','N_out']]==[r2[k] for k in ['source_count','target_count','N','N_out']]
    rows += [r1,r2]
    malformed=['','1','0','02',encode(3,[(0,1,2)])+'0']; rejected=0
    for s in malformed:
        try: compile_bits(s)
        except ValueError: rejected+=1
    assert rejected==len(malformed)
    reflection_checks=sum(C(*t)==C(*tuple((-x)%5 for x in t)) for t in product(range(5),repeat=3))
    assert reflection_checks==125
    result=dict(lemma='T5-FULL-EQUALITY-SPLIT1',code_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),seed=None,mode='deterministic exhaustive finite local checks plus certified contraction',equality_clauses=eq,equality_matrix=table,equality_assignments_enumerated=5**6,frames=frames,reflection_checks=reflection_checks,malformed_rejected=rejected,cases=rows,limitations='No unrestricted lower bound, no SAT solver benchmark, no full target enumeration, no independent reviewer or proof assistant.')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__': main()
