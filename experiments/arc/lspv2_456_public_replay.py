#!/usr/bin/env python3
"""Independent minimal fixed-width SAT-frontier check. No general P-vs-NP claim."""
from itertools import product

def force(x, v, a, b):
    p=x if v else -x
    return [(p,a,b),(p,a,-b),(p,-a,b),(p,-a,-b)]

def equality(x, y, d):
    return [(-x,y,d),(-x,y,-d),(x,-y,d),(x,-y,-d)]

def k4(ids, odd):
    edges=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
    clauses=[]
    for v in range(4):
        a,b,c=[ids[j] for j,e in enumerate(edges) if v in e]
        for p,q in product((0,1),repeat=2):
            r=p^q^1^(int(odd and v==0))
            clauses.append(((-a if p else a),(-b if q else b),(-c if r else c)))
    return clauses

def source(h, first, last, core):
    z=tuple(range(1,h)); nxt=h; blocks=[]
    for i in range(h):
        if i==0:
            block=force(z[0],first,nxt,nxt+1);nxt+=2
        elif i==h-1:
            block=force(z[-1],last,nxt,nxt+1);nxt+=2
        else:
            block=equality(z[i-1],z[i],nxt);nxt+=1
        if i==h//2 and core!='none':
            block+=k4(list(range(nxt,nxt+6)),core=='odd');nxt+=6
        blocks.append(block)
    return z,blocks

def sat(clauses):
    # Exact standalone DPLL, no PySAT, external solver or semantic oracle.
    def go(f):
        if not f:return True
        if any(len(c)==0 for c in f):return False
        unit=next((c[0] for c in f if len(c)==1),None)
        var=unit if unit is not None else f[0][0]
        def simplify(lit):
            return [tuple(v for v in c if v!=-lit) for c in f if lit not in c]
        return go(simplify(var)) or (unit is None and go(simplify(-var)))
    return bool(go([tuple(c) for c in clauses]))

def restrict(block, pins):
    out=[]
    for c in block:
        if any((v>0)==pins[abs(v)] for v in c if abs(v) in pins):continue
        out.append(tuple(v for v in c if abs(v) not in pins))
    return out

def frontier(z, blocks):
    prev={():True}; calls=0
    for i,block in enumerate(blocks):
        incoming=(z[i-1],) if i else ()
        outgoing=(z[i],) if i<len(blocks)-1 else ()
        nxt={p:False for p in product((0,1),repeat=len(outgoing))}
        for a in product((0,1),repeat=len(incoming)):
            if not prev[a]:continue
            for b in product((0,1),repeat=len(outgoing)):
                pins=dict(zip(incoming,a));pins.update(zip(outgoing,b))
                calls+=1
                nxt[b]|=sat(restrict(block,pins))
        prev=nxt
    return prev[()],calls

def main():
    inputs=0; sat_count=0; calls=0; assertions=0
    for h in range(2,8):
        for a,b in product((0,1),repeat=2):
            for core in ('none','even','odd'):
                z,blocks=source(h,a,b,core)
                result,n=frontier(z,blocks)
                reference=sat([c for block in blocks for c in block])
                assert result==reference==(a==b and core!='odd')
                assertions+=1;inputs+=1;sat_count+=result;calls+=n
    assert (inputs,sat_count,calls)==(72,24,524)
    print({'status':'PASS','checks':assertions+1,'original_3cnf_sources':inputs,
           'SAT':sat_count,'UNSAT':inputs-sat_count,'guest_calls':calls})
if __name__=='__main__':main()
