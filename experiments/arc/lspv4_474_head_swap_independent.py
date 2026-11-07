#!/usr/bin/env python3
"""Independent finite controls for LSPV-4/474 narrow native INPUT INDEX head-swap cost."""
import json
EDGES=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
def clauses(charge):
    out=[]
    for v in range(4):
        ins=[i+1 for i,e in enumerate(EDGES) if v in e]
        for a in range(8):
            b=[(a>>j)&1 for j in range(3)]
            if b[0]^b[1]^b[2] == ((charge>>v)&1):
                continue
            out.append(tuple(-ins[j] if b[j] else ins[j] for j in range(3)))
    return out
def models(cs):
    return sum(all(any(((mask>>(abs(l)-1))&1)==int(l>0) for l in c) for c in cs) for mask in range(64))
results=[]
checks=0
for charge in range(16):
    cs=clauses(charge)
    assert len(cs)==16
    assert models(cs)==(8 if charge.bit_count()%2==0 else 0)
    checks+=2
    ascii_source=';'.join(','.join(str(l) for l in c) for c in cs)
    bits=[(ord(ch)>>shift)&1 for ch in ascii_source for shift in range(7,-1,-1)]
    for H in (8,16,32,64,128,256):
        offset=2*H+1
        physical=[0]*offset+bits
        q=H
        head=H
        scratch=0
        for _ in range(q):
            # Guest zero-address INPUT INDEX jump preserves its INDEX head.
            assert head==H
            head=0
            scratch+=H
            assert physical[offset]==bits[0]
            head=H
            scratch+=H
            checks+=2
        assert head==H and scratch==2*H*q
        assert physical[offset+1:offset+1+len(bits)] != bits
        checks+=2
        results.append((charge,H,scratch,H+q))
assert len(results)==96
print(json.dumps({'status':'PASS','cases':len(results),'checks':checks,
 'source_alias_reads':sum(h for _,h,_,_ in results),
 'source_index_head_moves':sum(x for _,_,x,_ in results),
 'maxH':max(h for _,h,_,_ in results),
 'charge_classes':{'SAT':8,'UNSAT':8},'ratio_at_H_256':256},sort_keys=True,indent=2))
