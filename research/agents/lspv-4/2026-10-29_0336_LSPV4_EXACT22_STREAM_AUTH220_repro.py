#!/usr/bin/env python3
"""Independent model-level logspace grammar validator for LSPV2 exact22 chains.
Template literals are retyped from published W1. The *reference* producer is
imported from the preserved LSPV2 source archive for comparison only.
The validator stores O(log k) integer counters and O(1) candidate clauses;
Python overhead is not a Turing-machine workspace measurement.
"""
import importlib.util, json, hashlib
from pathlib import Path
P=Path(__file__).parent
W1=(
(-1,3,-14),(2,-8,9),(10,-13,14),(3,7,-13),(-4,-9,-11),
(5,8,-14),(4,-8,-11),(1,7,13),(1,-7,10),(-5,-6,-15),
(-2,-6,12),(-4,9,-10),(-2,5,-12),(-3,6,-15),(6,-7,11),
(2,-9,11),(4,8,-10),(-3,12,15),(-5,-12,15),(-1,13,14))

def cla_sort(c):return tuple(sorted(c,key=lambda a:(abs(a),a<0)))
base=list(W1)
for idx in (6,11):base[idx]=(-base[idx][0],)+base[idx][1:]
BASE=tuple(sorted((cla_sort(c) for c in base)))

def candidate(k,block,slot):
    clause=[(abs(v)+15*block)*(1 if v>0 else -1) for v in BASE[slot]]
    if slot==3 and block<k-1:clause[0]=-(15*(block+1)+4)
    if slot==2 and block>0:clause[0]=-(15*(block-1)+4)
    return cla_sort(clause)

def expected_rank(k,rank):
    size=20*k
    for row in range(size):
        cl=candidate(k,row//20,row%20)
        smaller=0
        for other in range(size):
            if candidate(k,other//20,other%20)<cl:smaller+=1
        if smaller==rank:return cl
    raise ValueError('out of range or duplicate')

def reference(k):
    spec=importlib.util.spec_from_file_location('w221',P/'lspv2'/'exact22_port_wires221.py')
    mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod.make_eq_path(k),mod.dimacs

def validate_text(k,raw):
    try:
        lines=raw.decode('ascii').splitlines()
    except UnicodeDecodeError:
        return False
    if len(lines)!=20*k+1 or lines[0] != f'p cnf {15*k} {20*k}':return False
    for i,row in enumerate(lines[1:]):
        expected=' '.join(map(str, expected_rank(k,i)))+' 0'
        if row!=expected:return False
    return raw.endswith(b'\n')

results={'status':'PASS','cases':[],'verified_clauses':0,'violations':0,'mutation_rejections':0}
for k in (2,3,4,5):
    correct,printer=reference(k)
    mismatches=[]
    for rank,cl in enumerate(correct):
        predicted=expected_rank(k,rank)
        if predicted!=cl:mismatches.append((rank,predicted,cl))
    assert not mismatches, mismatches[:2]
    assert len(correct)==20*k
    # Physical source is read once; output is the fixed 4-clause relation.
    src_bytes=printer(correct,15*k)
    assert validate_text(k,src_bytes)
    bad_header=src_bytes.replace(f'p cnf {15*k} '.encode(), f'p cnf {15*k+1} '.encode(),1)
    bad_char=src_bytes[:len(src_bytes)//2]+b'!' + src_bytes[len(src_bytes)//2+1:]
    bad_eof=src_bytes[:-1]
    for damaged in (bad_header,bad_char,bad_eof):
        assert not validate_text(k,damaged)
        results['mutation_rejections']+=1
    results['cases'].append({'k':k,'clauses':len(correct),'bytes':len(src_bytes),
                             'bit_length':8*len(src_bytes),
                             'conceptual_work_bits':(5*(k*20+1).bit_length()+96),
                             'max_nested_candidate_comparisons':(20*k)**3})
    results['verified_clauses']+=len(correct)
results['reference_raw_sha256']=hashlib.sha256((P/'lspv2'/'raw221.json').read_bytes()).hexdigest()
print(json.dumps(results,indent=2,sort_keys=True))
