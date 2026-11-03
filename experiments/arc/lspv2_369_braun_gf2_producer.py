#!/usr/bin/env python3
"""LSPV2-369: source-labelled Res(+) certificates for odd Tseitin controls.
No SAT oracle, no proof minimum claim. Python 3 standard library.
"""
import json, hashlib, itertools, sys
from pathlib import Path

def eq(mask, rhs):
    return [mask, rhs]

def eq_clause(pattern, vs):
    return [eq(1 << v, 1 - bit) for v, bit in zip(vs, pattern)]

def graph(name):
    if name == 'K4':
        return 4, [(i,j) for i in range(4) for j in range(i+1,4)]
    if name == 'K33':
        return 6, [(i,j) for i in range(3) for j in range(3,6)]
    raise ValueError('unknown graph')

def build(name):
    h, edges = graph(name)
    n = len(edges)
    incidence = [[] for _ in range(h)]
    for j,(u,v) in enumerate(edges):
        incidence[u].append(j)
        incidence[v].append(j)
    assert all(len(v)==3 for v in incidence)
    charge = [1]+[0]*(h-1)
    lines, orig = [], []
    def add_src(c):
        idx=len(lines)
        lines.append({'op':'src','clause':c})
        orig.append(c)
        return idx
    def emit(op, clause, **kwargs):
        idx=len(lines)
        lines.append(dict(op=op, clause=clause, **kwargs))
        return idx
    def local_row(v):
        vs=incidence[v]
        rhs=charge[v]
        sources={}
        for bits in itertools.product((0,1), repeat=3):
            if sum(bits)%2 !=rhs:
                sources[bits]=add_src(eq_clause(bits,vs))
        E=eq(sum(1<<x for x in vs),rhs)
        leaves=[]
        for bits in itertools.product((0,1),repeat=3):
            src=sources.get(tuple(bits),next(iter(sources.values())))
            clause=[E]+eq_clause(bits,vs)
            leaves.append((emit('weak',clause,parent=src),bits))
        for axis in (2,1,0):
            nxt=[]
            for j in range(0,len(leaves),2):
                a,ba=leaves[j]; b,bb=leaves[j+1]
                assert ba[:axis]==bb[:axis]
                assert ba[axis]==0 and bb[axis]==1
                clause=[E]+eq_clause(ba[:axis],vs[:axis])
                nxt.append((emit('cut',clause,parents=[a,b],pivot=eq(1<<vs[axis],1)),ba[:axis]))
            leaves=nxt
        return leaves[0][0], E
    rows=[local_row(v) for v in range(h)]
    while len(rows)>1:
        (a,E1),(b,E2)=rows[:2]
        E3=eq(E1[0]^E2[0],E1[1]^E2[1])
        w=emit('weak',[E3,eq(E2[0],1-E2[1])],parent=a)
        z=emit('cut',[E3],parents=[w,b],pivot=eq(E2[0],1-E2[1]))
        rows=[(z,E3)]+rows[2:]
    assert rows[0][1]==[0,1]
    emit('weak',[],parent=rows[0][0])
    return {'name':name,'vertices':h,'edges':edges,'charge':charge,'nvars':n,
            'source_clauses':orig,'proof':lines,
            'nodes':sum(s['op']!='src' for s in lines),
            'source_count':len(orig)}

def bphp(n):
    ell=(n-1).bit_length()
    pigeons=n+1
    clauses=[]
    for i in range(pigeons):
        for j in range(i+1,pigeons):
            for hole in range(n):
                clauses.append([(i*ell+t+1,1-((hole>>t)&1)) for t in range(ell)]
                             +[(j*ell+t+1,1-((hole>>t)&1)) for t in range(ell)])
    return clauses,ell,pigeons

def sat_count(clauses, nv):
    count=0
    for a in range(1<<nv):
        if all(any(((a>>(v-1))&1)==b for v,b in c) for c in clauses):
            count+=1
    return count

def main():
    controls=[]
    for n in (2,4):
        c,ell,p=bphp(n)
        assert sat_count(c,ell*p)==0
        controls.append({'type':'BPHP','holes':n,'variables':ell*p,'clauses':len(c),'models':0})
    cases=[build('K4'),build('K33')]
    out={'model':'ResPlus_Gaussian_SemanticWeakening_And_ParityCut',
         'scope':'proof upper certificates, unrestricted DAG Res(XOR) local controls; not mixed minima',
         'cases':cases,'controls':controls,'deterministic':True}
    path=Path(sys.argv[1] if len(sys.argv)>1 else 'certificates.json')
    path.write_text(json.dumps(out,separators=(',',':'),sort_keys=True)+'\n')
    print(json.dumps({'cases':[(c['name'],c['source_count'],c['nodes']) for c in cases],
       'controls':controls,'bytes':path.stat().st_size,
       'sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2))

if __name__=='__main__':
    main()
