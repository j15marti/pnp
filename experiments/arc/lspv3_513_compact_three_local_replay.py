#!/usr/bin/env python3
"""LSPV-3/513. Compact independent source-excess reproduction.
Validates the original source, source-essentiality, proof dependency topology,
and arity counts. NOT a complete historical R_mix341 typed certificate checker.
"""
import itertools, hashlib, json
edges=[]
for j in range(3):
    u,a,b,c,d=[5*j+k+1 for k in range(5)]
    edges.extend([(0,u),(a,u),(u,b),(a,c),(a,d),(b,c),(b,d),(c,d)])
inc=[[] for _ in range(16)]
for i,(u,v) in enumerate(edges,1): inc[u].append(i);inc[v].append(i)
assert len(edges)==24 and all(len(s)==3 for s in inc)
charge=[1]+[0]*15
source=[];indices={};per=[[] for _ in range(16)]
for v in range(16):
    for bits in itertools.product((0,1),repeat=3):
        if (sum(bits)&1)==charge[v]:continue
        ix=len(source);source.append(tuple(-e if b else e for e,b in zip(inc[v],bits)))
        indices[v,bits]=ix;per[v].append(ix)
dimacs='p cnf 24 64\n'+''.join(' '.join(map(str,c))+' 0\n' for c in source)
sha=hashlib.sha256(dimacs.encode()).hexdigest()
assert sha=='dc62a4995250bb6922d31e711562fa7408e67968e097289fe8a5cb8c9c55dc20'
def compatible(rows):
    piv={}
    for var,rhs in rows:
        mask=0
        for e in var:mask^=1<<(e-1)
        while mask:
            k=mask.bit_length()-1
            if k not in piv:piv[k]=(mask,rhs);break
            mm,bb=piv[k];mask^=mm;rhs^=bb
        if not mask and rhs:return False
    return True
essential=set()
for (v,bits),ix in indices.items():
    rows=[(inc[u],charge[u]) for u in range(16) if u!=v]
    rows +=[([e],b) for e,b in zip(inc[v],bits)]
    if compatible(rows):essential.add(ix)
assert len(essential)==55
nodes=[]
def add(rule,parents):
    ident='N'+str(len(nodes));nodes.append((ident,rule,parents));return ident
units=[]
for j in range(3):
    root=1+5*j;rows=[]
    for v in range(root+1,root+5):
        ids=['S'+str(i) for i in per[v]]
        rows.append(add('AND3',[add('AND3',ids[:2]),add('AND3',ids[2:])]))
    xor=add('XOR',[add('XOR',rows[:2]),add('XOR',rows[2:])])
    bridge=inc[0][j];pos=inc[root].index(bridge)
    two=['S'+str(indices[b]) for b in indices if b[0]==root and b[1][pos]==1]
    assert len(two)==2
    forced=add('AND3',[add('AND3',two),xor]);units.append(add('LOCAL',[forced]))
root='S'+str(indices[0,(0,0,0)])
for u in units:root=add('RES',[root,u])
assert len(nodes)==57
by={i:p for i,_,p in nodes};anc=set()
def traverse(i):
    if i in anc:return
    anc.add(i)
    for p in by.get(i,[]):traverse(p)
traverse(root)
assert len(anc)==len(nodes)+55
assert {int(i[1:]) for i in anc if i.startswith('S')}==essential
n1=sum(len(p)==1 for _,_,p in nodes)
n2=sum(len(p)==2 for _,_,p in nodes)
E=n1+2*n2
beta=E-(len(anc)-1)
assert (n1,n2,E,beta)==(3,54,111,0)
mu=len(essential);q=len(nodes);r=55;d0=0
assert q-(mu-1)==(r-mu)+beta+n1+2*d0==3
print(json.dumps({'source_sha256':sha,'clauses':len(source),'essential':mu,
 'nonessential':len(source)-mu,'used_source_indices':sorted(essential),
 'nodes':q,'unary':n1,'binary':n2,'edges':E,'cycle_excess':beta,
 'minimum_for_three_unaries':mu-1+3,'historical_parser':'OPEN'},sort_keys=True,indent=2))
