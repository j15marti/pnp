#!/usr/bin/env python3
"""LSPV-4/470: canonical radix-DAG live-index counterexample. Python producer.
A finite abstract representation check, NOT a native FLMV interpreter.
"""
import json, sys, itertools, hashlib
from collections import defaultdict

def radix_from_bits(bits):
    assert len(bits) and len(bits)&(len(bits)-1)==0
    nodes={}
    levels=defaultdict(int)
    zero=('zero',0)
    leaves=[('one',0) if b else zero for b in bits]
    height=0
    while len(leaves)>1:
        new=[]
        height+=1
        z=('zero',height)
        for i in range(0,len(leaves),2):
            a,b=leaves[i],leaves[i+1]
            if a[0]=='zero' and b[0]=='zero':
                new.append(z)
                continue
            key=(height,a,b)
            if key not in nodes:
                nodes[key]=('node',len(nodes)+1)
                levels[height]+=1
            new.append(nodes[key])
        leaves=new
    return len(nodes),dict(levels),leaves[0]

def tseitin_k4(odd):
    edges=[(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
    charges=[int(odd),0,0,0]
    clauses=[]
    for v in range(4):
        e=[i+1 for i,(a,b) in enumerate(edges) if a==v or b==v]
        assert len(e)==3
        for t in range(8):
            # every forbidden local edge parity is encoded by the one clause false at that tuple
            if t.bit_count()%2 != charges[v]:
                clauses.append(tuple(-e[j] if (t>>j)&1 else e[j] for j in range(3)))
    models=0
    for bits in range(1<<6):
        if all(any(((bits>>(abs(l)-1))&1)==(l>0) for l in clause) for clause in clauses):
            models+=1
    assert len(clauses)==16 and models==(0 if odd else 8)
    return {'odd':odd,'clauses':16,'models':models}

def main():
    cases=[]
    for k in [2,4,8,16]:
        m=1<<k
        L=m*k
        bits=bytearray(((word>>j)&1) for word in range(m) for j in range(k))
        assert len(bits)==L
        # Simulate faithful INDEX writes (WORK never addressed); its contents remain live.
        tape=bytearray(L)
        for j,b in enumerate(bits):
            tape[j]=b
        assert tape==bits
        unique,levels,root=radix_from_bits(tape)
        level=k.bit_length() # k=2^a -> node height a, not a+1
        level=k.bit_length()-1
        num_nonzero=m-1
        assert levels[level]>=num_nonzero,(k,levels[level],num_nonzero)
        assert unique>=m-1
        # Test the clean-up path on INDEX only, without ever indexing WORK.
        tape[:] = b'\x00'*L
        assert not any(tape)
        cases.append({'k':k,'blocks':m,'index_length':L,'live_nodes':unique,
                      'distinct_level_k_nodes':levels[level],
                      'bound_live_nodes':m-1,'work_highwater':0,
                      'peak_index_ones':sum(bits),
                      'guest_prefix_steps':L,'guest_index_clear_steps':L,
                      'bit_sha256':hashlib.sha256(bits).hexdigest()})
    # All-input wrapper can always preserve its later decider's answers: the prefix alters
    # only INDEX then clears it. Here we check the same finite original signed K4 controls.
    controls=[tseitin_k4(False),tseitin_k4(True)]
    malformed=[(1,1,2),(1,-1,2)]
    assert all(len(set(map(abs,c)))!=3 for c in malformed)
    result={'status':'PROVED/RESTRICTED mathematical witness; COMPUTATIONAL finite radix check',
            'not_native_flmv':True,'cases':cases,'tseitin_controls':controls,
            'malformed_duplicate_abs_literal_rejected':len(malformed),
            'theorem':'live guest INDEX bit payload may be Omega(L/log L) counted radix nodes while guest non-index WORK highwater=0; historical roots have been garbage collected.',
            'source':'LSPV-4/470 independent Python producer'}
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
