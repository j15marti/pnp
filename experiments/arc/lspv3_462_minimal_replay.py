#!/usr/bin/env python3
"""LSPV-3/462 minimal replay. SAT representational control, not UNSAT hardness."""
from itertools import product
import json

CASES = [(1,3),(1,4),(1,5),(1,7),(1,9),(2,3),(2,4),(2,5),(2,7),(3,3),(3,4),(3,5)]

def parity(bits):
    return sum(bits) % 2

def ban(ids, bits):
    return tuple(-i if b else i for i, b in zip(ids, bits))

def clauses(ids, b):
    return [ban(ids, bits) for bits in product((0,1), repeat=len(ids)) if parity(bits) != b]

def xor_def(x, y, z):
    return [ban((x,y,z), bits) for bits in product((0,1), repeat=3) if bits[2] != (bits[0]^bits[1])]

def sat(c, bits):
    return any(bits[abs(l)-1] == (1 if l>0 else 0) for l in c)

def check(r,d):
    rhs=[(j+1)%2 for j in range(r)]
    flat=[]; compact=[]; gates=[]; nxt=r*d+1
    for j in range(r):
        xs=list(range(j*d+1,(j+1)*d+1))
        flat += clauses(xs,rhs[j])
        for _ in range(d-3):
            x,y=xs[:2]; z=nxt; nxt+=1
            compact += xor_def(x,y,z)
            gates.append((x,y,z)); xs=[z]+xs[2:]
        compact += clauses(xs,rhs[j])
    tested=0; good=0
    for b in product((0,1),repeat=r*d):
        truth=all(parity(b[j*d:(j+1)*d])==rhs[j] for j in range(r))
        ext=list(b)
        for x,y,z in gates:
            assert z==len(ext)+1
            ext.append(ext[x-1]^ext[y-1])
        assert truth==all(sat(c,b) for c in flat)
        assert truth==all(sat(c,ext) for c in compact)
        tested+=1; good+=truth
    assert len(flat)==r*2**(d-1) and len(compact)==4*r*(d-2)
    assert len(gates)==r*(d-3) and good==2**(r*(d-1))
    assert all(len(c)==3 and len({abs(x) for x in c})==3 for c in compact)
    return dict(r=r,d=d,flat=len(flat),proper3=len(compact),gates=len(gates),tested=tested,sat=good)

if __name__=='__main__':
    records=[check(r,d) for r,d in CASES]
    print(json.dumps({'classification':'COMPUTATIONAL finite controls; full result proved on paper',
                      'assignments':sum(c['tested'] for c in records),'cases':records},indent=2))
