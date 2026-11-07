#!/usr/bin/env python3
"""LSPV-3/469. Compact original-source sparse PC_GF2 proof generator.
Proves only the stated cubic odd-Tseitin family in binary-addition PC over GF2.
The full independently replayed eight-case artifacts are in the LSPV-3/469 ZIP.
"""
from itertools import product
from hashlib import sha256
import json

def xor(a,b): return sorted(set(a)^set(b))
def mul(a,b):
    s=set()
    for u in a:
        for v in b:
            z=u|v
            if z in s:s.remove(z)
            else:s.add(z)
    return sorted(s)
def indicator(bits,edgeids):
    r=[0]
    for b,e in zip(bits,edgeids):
        r=mul(r,[1<<e] if b else [0,1<<e])
    return r
def construct(h,edges,odd=True):
    edges=sorted(set(tuple(sorted(e)) for e in edges))
    assert len(edges)==3*h//2
    inc=[[i for i,(a,b) in enumerate(edges) if v in (a,b)] for v in range(h)]
    assert all(len(e)==3 for e in inc)
    charges=[int(odd)]+[0]*(h-1)
    src=[];nodes=[];poly={};depth={}
    for v,ids in enumerate(inc):
        for bits in product((0,1),repeat=3):
            if sum(bits)%2==charges[v]: continue
            sid=f"s{len(src)+1}"
            lits=[(1 if b==0 else -1)*(e+1) for b,e in zip(bits,ids)]
            src.append(lits)
            poly[sid]=indicator(bits,ids);depth[sid]=0
    def add(a,b):
        key=f"p{len(nodes)+1}"
        val=xor(poly[a],poly[b])
        nodes.append(dict(id=key,parents=[a,b],poly=val))
        poly[key]=val;depth[key]=1+max(depth[a],depth[b])
        return key
    def balanced(keys):
        while len(keys)>1:
            out=[]
            for i in range(0,len(keys),2):
                out.append(add(keys[i],keys[i+1]) if i+1<len(keys) else keys[i])
            keys=out
        return keys[0]
    vertex_rows=[]
    for v in range(h):
        ids=[f"s{i+1}" for i in range(4*v,4*(v+1))]
        row=balanced(ids)
        expected=sorted(([0] if charges[v] else [])+[1<<i for i in inc[v]])
        assert poly[row]==expected
        vertex_rows.append(row)
    root=balanced(vertex_rows)
    assert poly[root]==([0] if odd else [])
    dimacs=f"p cnf {len(edges)} {4*h}\n"+''.join(" ".join(map(str,c))+" 0\n" for c in src)
    assert len(nodes)==4*h-1 and depth[root]==(4*h-1).bit_length()
    return dict(source_sha256=sha256(dimacs.encode()).hexdigest(),
                clauses=len(src),paid_binary_additions=len(nodes),span=depth[root],
                odd=odd,final_polynomial=poly[root],
                sparse_monomial_occurrences=sum(len(poly[s]) for s in poly))
if __name__=="__main__":
    G=[("K4",4,[(a,b) for a in range(4) for b in range(a+1,4)]),
       ("K33",6,[(a,b) for a in range(3) for b in range(3,6)]),
       ("cube",8,[(a,a^(1<<k)) for a in range(8) for k in range(3) if a<a^(1<<k)])]
    for name,h,edges in G:
        for odd in (True,False):
            print(json.dumps(dict(name=name,**construct(h,edges,odd)),sort_keys=True))
