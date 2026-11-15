#!/usr/bin/env python3
"""XORSER064: explicit binary-proof serialization audit for Q-XOR3.

This is an authenticated, source-bound proof laboratory, NOT a physical
Turing-machine emulator or a lower bound for unrestricted SAT algorithms.
"""
import itertools
import json
import math
from collections import Counter
from fractions import Fraction

CHECKS = 0

def check(cond, name):
    global CHECKS
    CHECKS += 1
    if not cond:
        raise AssertionError(name)

def widths(h):
    return h.bit_length(), (2*h).bit_length()  # ceil(log2(h+1)), ceil(log2(2h+1))

def sizes(h):
    b, a = widths(h)
    return {"source":2+b, "add":2+2*a, "halt":2+a,
            "total":h*(2+b)+(h-1)*(2+2*a)+(2+a)}

def prism(h):
    if h < 6 or h % 2:
        raise ValueError("requires even h>=6")
    m=h//2
    edges=[]
    for layer in (0,1):
        for j in range(m):
            edges.append((layer*m+j,layer*m+(j+1)%m))
    for j in range(m):
        edges.append((j,m+j))
    inc=[[] for _ in range(h)]
    for i,(u,v) in enumerate(edges):
        inc[u].append(i+1); inc[v].append(i+1)
    check(len(edges)==3*h//2 and all(len(t)==3 for t in inc),"3-regular")
    return [tuple(sorted(t)) for t in inc]

def block(t,parity):
    return tuple(sorted(tuple((-v if bit else v) for v,bit in zip(t,bits))
                        for bits in itertools.product((0,1), repeat=3)
                        if (bits[0]^bits[1]^bits[2]) != parity))

def auth(group):
    if len(group)!=4 or len(set(group))!=4:
        return None
    if not all(len(c)==3 for c in group):
        return None
    t=tuple(sorted(abs(z) for z in group[0]))
    if len(set(t))!=3 or any(tuple(sorted(abs(z) for z in c))!=t for c in group):
        return None
    ordered=tuple(sorted(group))
    for rhs in (0,1):
        if ordered==block(t,rhs):
            return (t,rhs)
    return None

def build_source(h,odd=True):
    inc=prism(h)
    return [block(t, 1 if odd and i==0 else 0) for i,t in enumerate(inc)]

def enc(op, args, h):
    b,a=widths(h)
    if op=='S':
        (v,)=args
        if not 1<=v<=h: raise ValueError("source index")
        return '00'+format(v,f'0{b}b')
    if op=='A':
        j,k=args
        if not 1<=j<2*h or not 1<=k<2*h: raise ValueError("add index")
        return '01'+format(j,f'0{a}b')+format(k,f'0{a}b')
    if op=='H':
        (j,)=args
        if not 1<=j<2*h: raise ValueError("halt index")
        return '10'+format(j,f'0{a}b')
    raise ValueError("opcode")

def records(h):
    result=[('S',(v,)) for v in range(1,h+1)]
    current=1
    for v in range(2,h+1):
        result.append(('A',(current,v)))
        current=h+v-1
    result.append(('H',(current,)))
    return result

def serialized(h):
    return ''.join(enc(op,args,h) for op,args in records(h))

def verify(binary,groups,h):
    if any(c not in '01' for c in binary):
        return False
    b,a=widths(h)
    rows=[]; i=0; halted=False
    while i<len(binary):
        if i+2>len(binary) or halted:
            return False
        op=binary[i:i+2]; i+=2
        if op=='00':
            w=b
        elif op=='01':
            w=2*a
        elif op=='10':
            w=a
        else:
            return False
        if i+w>len(binary):
            return False
        part=binary[i:i+w];i+=w
        if op=='00':
            v=int(part,2)
            if v<1 or v>h or len(groups)!=h:
                return False
            row=auth(groups[v-1])
            if row is None: return False
            ts,rhs=row
            mask=0
            for t in ts: mask^=1<<(t-1)
            rows.append((mask,rhs))
        elif op=='01':
            u,v=int(part[:a],2),int(part[a:],2)
            if u<1 or v<1 or u>len(rows) or v>len(rows):
                return False
            x,y=rows[u-1],rows[v-1]
            rows.append((x[0]^y[0],x[1]^y[1]))
        else:
            j=int(part,2)
            if j<1 or j>len(rows) or rows[j-1]!=(0,1):
                return False
            halted=True
    return halted

def audit_output_tariff(h):
    """Realizable append-only one-output-tape write path.

    A source-dependent bit generator is GRANTED for free. This relaxes, rather
    than models, a full uniform program, and the test measures only writes.
    """
    bits=serialized(h)
    untouched=len(bits)
    pending_halt=1
    charges=0
    for pos,bit in enumerate(bits):
        check(bit in '01', 'binary output')
        old=(untouched,pending_halt)
        untouched-=1
        if pos==len(bits)-1:
            pending_halt=0
        delta=(old[0]-untouched,old[1]-pending_halt)
        check(delta == (1, 1 if pos==len(bits)-1 else 0), 'physical discharge')
        check(Fraction(1)*delta[0]+Fraction(0)*delta[1]<=1, 'unit-bit tariff')
        check(Fraction(1,2)*delta[0]+Fraction(1,2)*delta[1]<=1, 'joint tariff')
        if pos==len(bits)-1:
            check(delta[0]+delta[1]>1, 'naive double-count falsifier')
        charges+=1
    check((untouched,pending_halt)==(0,0), 'goal potential')
    check(charges==len(bits), 'sharp output floor')
    return charges

def main():
    observed=[]
    for h in range(6,100,2):
        groups=build_source(h,True)
        proof=serialized(h)
        info=sizes(h)
        events=records(h)
        check(len(proof)==info['total'],"bit formula")
        check(len(events)==2*h,"2h events")
        check(Counter(op for op,_ in events)=={'S':h,'A':h-1,'H':1},"event counts")
        check(verify(proof,groups,h),"proof must verify")
        even=build_source(h,False)
        check(not verify(proof,even,h),"even-charge refutes falsely")
        broken=list(groups);broken[0]=broken[0][:-1]
        check(not verify(proof,broken,h),"incomplete XOR source rejected")
        check(not verify(proof+'1',groups,h),"trailing half record")
        if h<=16: audit_output_tariff(h)
        check(not verify('11'+proof,groups,h),"unknown opcode")
        tamper='01'+'0'*(2*widths(h)[1])+proof
        check(not verify(tamper,groups,h),"premature ADD")
        check(not verify('10'+format(1,f'0{widths(h)[1]}b'),groups,h),"premature HALT")
        if h in (6,8,16,32,64,98):
            observed.append({'H':h,'source_index_bits':widths(h)[0],
               'proof_index_bits':widths(h)[1], 'native_events':2*h,
               'serialized_bits':len(proof),'bits_per_native_event':len(proof)/(2*h),
               'original_clauses':4*h,'edge_variables':3*h//2})
    # Width and ratio growth on an arbitrary even-H canonical certificate family.
    for h in (128,256,1024,4096,65536,1048576):
        z=sizes(h)
        check(z['total']>=h*widths(h)[0],"source address information")
        check(z['total']>2*h,"not one output bit per abstract event")
        observed.append({'H':h,'source_index_bits':widths(h)[0],
           'proof_index_bits':widths(h)[1], 'native_events':2*h,
           'serialized_bits':z['total'], 'bits_per_native_event':z['total']/(2*h),
           'formula_only':True})
    # Genuine cheap alternative: a changed protocol interprets one macro SUM_ALL.
    h=64; macro='11'+format(h,f'0{widths(h)[0]}b')
    check(len(macro)<sizes(h)['total'],"macro compactness")
    check(not verify(macro,build_source(h),h),"macro not legal native proof")
    print(json.dumps({'id':'XORSER064','scoped_claim':'fixed-width binary explicit proof record serialization',
      'checks':CHECKS,'failures':0,'graph_instances':47,
      'models':['source-bound XOR proof event price','single binary output-tape write model'],
      'opcode_bits':2,'one_output_cell_written_per_paid_TM_transition':True,
      'tariff_weights_accepted':{'interface':'1','machine':'0'},
      'joint_tariff_accepted':{'interface':'1/2','machine':'1/2'},
      'naive_fused_last_write_weights_rejected':{'interface':'1','machine':'1'},
      'witnesses':observed,'macro_h64_bits':len(macro),
      'no_unrestricted_SAT_lower_bound':True},indent=2))

if __name__=='__main__': main()
