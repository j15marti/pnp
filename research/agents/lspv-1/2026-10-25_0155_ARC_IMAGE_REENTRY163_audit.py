#!/usr/bin/env python3
"""Finite exact two-level guarded-image re-entry audit.

Toy wrapper only. This does NOT implement FLMV's Cook reduction and is NOT
an ARC resource-contraction algorithm. Designed to falsify inheritance and
verify semantic repair by explicit near-linear bit-local re-normalization.
"""
from __future__ import annotations
import itertools, json
from pathlib import Path

CANDIDATE_CLAUSES = ((1,),(-1,),(2,),(-2,),(3,),(-3,),(1,2),(-1,2),(2,3),(-2,3))

def width(n): return max(1,n.bit_length())
def bits(v,w): return [(v>>i)&1 for i in range(w-1,-1,-1)]
def val(b):
    y=0
    for t in b:y=2*y+t
    return y

def encode(n,clauses):
    assert 1<=n<65000 and len(clauses)<65000
    w=width(n)
    out=bits(n,16)+bits(len(clauses),16)
    for c in clauses:
        assert len(c)<=3
        for slot in list(c)+[0]*(3-len(c)):
            out.append(1 if slot<0 else 0)
            out.extend(bits(abs(slot),w))
    return tuple(out)

def decode(data):
    assert len(data)>=32
    n=val(data[:16]);m=val(data[16:32]);w=width(n)
    assert len(data)==32+m*3*(1+w)
    clauses=[]
    for j in range(m):
        c=[]
        for k in range(3):
            pos=32+(j*3+k)*(w+1)
            sign=data[pos];v=val(data[pos+1:pos+1+w])
            if v: c.append(-v if sign else v)
        clauses.append(tuple(c))
    return n,tuple(clauses)

def wrapped_len(data):
    n,clauses=decode(data)
    return 32+(len(clauses)+2)*3*(1+width(n+2))

def wrap_bit(data,address):
    # Every access uses only the fixed header and <= one source clause record.
    n=val(data[:16]);m=val(data[16:32]);w=width(n);wp=width(n+2)
    total=32+(m+2)*3*(1+wp)
    assert 0<=address<total
    if address<16:return bits(n+2,16)[address]
    if address<32:return bits(m+2,16)[address-16]
    offset=address-32;reclen=3*(wp+1)
    j=offset//reclen;slot=(offset%reclen)//(wp+1);b=(offset%reclen)%(wp+1)
    if j>=m:
        sign=1 if j==m+1 else 0
        variable=(n+2 if j==m+1 else n+1) if slot==0 else 0
    else:
        source_pos=32+(j*3+slot)*(w+1)
        sign=data[source_pos]
        variable=val(data[source_pos+1:source_pos+1+w])
    return sign if b==0 else bits(variable,wp)[b-1]

def wrap(data):
    return tuple(wrap_bit(data,i) for i in range(wrapped_len(data)))

def is_guard_image(data):
    n,c=decode(data)
    return len(c)>=2 and c[-2:]==((n-1,),(-n,))

def exact_sat(data):
    n,clauses=decode(data)
    for row in itertools.product((False,True),repeat=n):
        if all(any((row[abs(l)-1] if l>0 else not row[abs(l)-1]) for l in clause) for clause in clauses):
            return True
    return False

def promise_solver(data):
    # This intentionally returns an incorrect SAT label on some off-image inputs.
    return exact_sat(data) if is_guard_image(data) else True

def restrict_variable(data, variable, truth):
    n,clauses=decode(data)
    assert 1<=variable<=n
    kept=[]
    for clause in clauses:
        if any((l>0)==truth for l in clause if abs(l)==variable):continue
        kept.append(tuple(l for l in clause if abs(l)!=variable))
    return encode(n,kept)

def run():
    counts=dict(cases=0,SAT=0,UNSAT=0,root_bits=0,wrapped_bits=0,
                first_off_image=0,second_off_image=0,wrong_off_image=0,
                repaired_calls=0,indexed_bit_probes=0,assertions=0,
                double_level_checks=0)
    witness=None
    for mask in range(1<<len(CANDIDATE_CLAUSES)):
        clauses=tuple(c for k,c in enumerate(CANDIDATE_CLAUSES) if mask>>k&1)
        source=encode(3,clauses)
        root=wrap(source)
        n,c=decode(root)
        assert n==5 and c[-2:]==((4,),(-5,));counts['assertions']+=1
        assert is_guard_image(root);counts['assertions']+=1
        label=exact_sat(source)
        assert label==exact_sat(root)==promise_solver(root);counts['assertions']+=1
        counts['cases']+=1;counts['SAT' if label else 'UNSAT']+=1
        counts['root_bits']+=len(source);counts['wrapped_bits']+=len(root)
        for addr in range(len(root)):
            assert wrap_bit(source,addr)==root[addr]
            counts['indexed_bit_probes']+=1
        # First real pinning: delete first forced-true fresh guard variable.
        first=restrict_variable(root,4,True)
        assert exact_sat(first)==label;counts['assertions']+=1
        assert not is_guard_image(first);counts['assertions']+=1
        counts['first_off_image']+=1
        if promise_solver(first)!=label:
            counts['wrong_off_image']+=1
        repair1=wrap(first)
        assert is_guard_image(repair1) and promise_solver(repair1)==label
        counts['assertions']+=1;counts['repaired_calls']+=1
        # Second true recursive level: pin the new fresh guard of the REPAIRED child.
        n1,_=decode(repair1)
        second=restrict_variable(repair1,n1-1,True)
        assert exact_sat(second)==label;counts['assertions']+=1
        assert not is_guard_image(second);counts['assertions']+=1
        counts['second_off_image']+=1
        repair2=wrap(second)
        assert is_guard_image(repair2) and promise_solver(repair2)==label
        counts['assertions']+=1;counts['repaired_calls']+=1
        counts['double_level_checks']+=1
        if not label and witness is None:
            witness={'clauses':clauses,'SAT':label,
                     'bit_lengths':[len(source),len(root),len(first),len(repair1),len(second),len(repair2)],
                     'off_image_solver_wrong':promise_solver(first)!=label,
                     'repaired_labels':[promise_solver(repair1),promise_solver(repair2)]}
    assert counts['cases']==1024 and counts['wrong_off_image']==counts['UNSAT']
    counts['assertions']+=1
    return dict(report='ARC-IMAGE-REENTRY163',counts=counts,witness=witness,
       labels=['PROVED/EXACT toy bit-local embedding (symbolic proof separately)',
               'COMPUTATIONAL finite exhaustive 1024-core audit',
               'OPEN true solver-dependent ARC-EDGE-90'],
       caveat='Toy 16-bit fixed header only; not the actual FLMV Cook reduction, not an asymptotic runtime trace. Child lengths remain linear-scale; no favorable contraction established.')

if __name__=='__main__':
    result=run()
    out=Path(__file__).with_name('2026-10-25_0155_ARC_IMAGE_REENTRY163_results.json')
    out.write_text(json.dumps(result,indent=2,default=list)+'\n')
    print(json.dumps(result,indent=2,default=list))