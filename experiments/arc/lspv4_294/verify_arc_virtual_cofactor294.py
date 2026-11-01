#!/usr/bin/env python3
"""Independent verifier for ARC294. Never imports the producer.
Requires archive's original-source fixtures and arc_virtual_cofactor294_raw.json
in same folder; run in unpacked COMPLETE_REPRO ZIP.
"""
from __future__ import annotations
import hashlib,itertools,json
from collections import Counter
from fractions import Fraction
from pathlib import Path
P=Path(__file__).resolve().parent
U=json.loads((P/'U_source.json').read_text())
Y=json.loads((P/'Y6_source.json').read_text())
V=[row[:] for row in U]
V[1][0],V[7][0]=V[7][0],V[1][0]
F={'U198':U,'V198':V,'Y6':Y}
RAW=json.loads((P/'arc_virtual_cofactor294_raw.json').read_text())
checks=Counter()

def check(cond,why):
    if not cond:raise AssertionError(why)
    checks[why]+=1

def gamma(u):
    z=bin(u)[2:]
    return ('0'*(len(z)-1))+z

def direct(F,p):
    mx=max(abs(t) for clause in F for t in clause)
    width=mx.bit_length()
    rows=[];indices=[]
    for j,source in enumerate(F):
        literals=[]
        satisfied=False
        for t in source:
            if abs(t) in p:
                if p[abs(t)]==int(t>0):satisfied=True
            else:literals.append(t)
        if not satisfied:
            rows.append(literals);indices.append(j)
    header=gamma(mx)+gamma(len(rows))
    bits=list(header)
    for j,cl in enumerate(rows):
        sign=int(F[indices[j]][0]>0)
        bits.append(str(sign));bits.extend(format(len(cl),'02b'))
        for t in cl:bits.extend(format(abs(t),f'0{width}b'))
        bits.extend('0'*(width*(3-len(cl))))
    return ''.join(bits),indices,rows

def source_bits(F):
    n=max(abs(z) for c in F for z in c);w=n.bit_length()
    return gamma(n)+gamma(len(F))+''.join(str(int(c[0]>0))+''.join(format(abs(z),f'0{w}b') for z in c) for c in F)

def truth(cl,a):return sum(a[abs(z)]==int(z>0) for z in cl)

def flmv(c):
    f=Fraction(1);best=Fraction(-1);winner=None
    for k in range(1,100):
        f=c*f/(1+f)
        d=min((1/f-c)/k,c**(-k))
        if d>best:best=d;winner=k
        if k>=4 and c**(-(k+1))<best:return winner,best,k
    raise AssertionError('infinite tail')

for row in RAW['cases']:
    name=row['source'];form=F[name];p=dict(row['pins']);n=max(abs(z) for cl in form for z in cl)
    data,ids,clauses=direct(form,p)
    original=source_bits(form)
    check(hashlib.sha256(data.encode()).hexdigest()==row['emitted_sha256'],'emitted_exact_sha')
    check(len(data)==row['child_bits'],'child_bits')
    check(len(original)==row['source_bits'],'source_bits')
    check(len(clauses)==row['child_m'],'child_clauses')
    check(len(form)==row['parent_m'],'parent_clauses')
    active={abs(z) for cl in clauses for z in cl}
    e=len(set(range(1,n+1))-set(p)-active)
    s=len(form)-len(clauses)
    rhs=3*s-4*(len(p)+e)
    check(len(active)==row['active_unpinned_variables'],'surviving_variables')
    check(e==row['extra_eliminated_variables'],'extra_eliminated')
    check(rhs==row['canonical_completion_balance_rhs'],'cofactor_balance_rhs')
    check(rhs==4*len(active)-3*len(clauses),'general_quota_conservation')
    check(len(p)<=len(form),'pins_valid')
    check(row['setup_reads']==len(original),'setup_one_scan')
    check(sorted(set(range(len(form)))-set(ids))==row['deleted_source_ids'],'deleted_original_ids')
    affected=[j for j,cl in enumerate(form) if any(abs(z) in p for z in cl)]
    check(affected==row['affected_source_ids'],'affected_original_ids')
    check(len(affected)<=4*len(p),'bounded_incidence')
    check(len(row['deleted_source_ids'])<=2*len(p),'bounded_deleted')
    check(row['output_queries']==len(data),'exact_queries')
    check(row['index_subtape_adjacent_xor']==2*row['index_one_writes'],'physical_index_xor')
    check(row['index_subtape_endpoint_xor']==0,'index_erasure')
    sw=n.bit_length()
    start_header=len(gamma(n))+len(gamma(len(form)))
    src_stride=1+3*sw
    acquired=[]
    for src_id,cl in zip(ids,clauses):
        acquired.append(start_header+src_id*src_stride)
        positions=[i for i,z in enumerate(form[src_id]) if abs(z) not in p]
        for original_pos in positions:
            for bit in range(sw):
                acquired.append(start_header+src_id*src_stride+1+original_pos*sw+bit)
    check(len(acquired)==row['output_source_reads'],'source_address_sequence_length')
    ones=sum(addr.bit_count() for addr in acquired)
    check(ones==row['index_one_writes'],'independent_index_writes')
    heads=[max(1,addr.bit_length())-1 for addr in acquired]
    moves=sum(heads)+sum(heads[:-1])
    check(moves==row['index_head_moves'],'independent_head_moves')
    check(len(acquired)==row['index_jumps'],'independent_index_jumps')
    check(moves+ones+len(acquired)==row['declared_index_primitives'],'independent_primitive_sum')
    for q,j,t,addr,bit in row['query_trace_prefix']:
        check(q<len(data) and addr<len(original),'indexed_bounds')
        check(original[addr]==bit==data[q],'indexed_value')
        check(j in ids and 0<=j<len(form),'source_record_index')
    if name=='Y6':
        for bits in itertools.product((0,1),repeat=6):
            a={i+1:bits[i] for i in range(6)}
            if any(a[x]!=v for x,v in p.items()):continue
            check(all(truth(cl,a)>0 for cl in form)==all(truth(cl,a)>0 for cl in clauses),'semantic_restriction_Y6')

models=sum(all(truth(c,{i+1:b for i,b in enumerate(bits)})>0 for c in Y) for bits in itertools.product((0,1),repeat=6))
check(models==20,'Y6_model_count')
for c,wanted in [(Fraction(6,5),Fraction(23,45)),(Fraction(241,200),Fraction(11642479,23232400))]:
    win,best,tail=flmv(c)
    check(win==2 and best==wanted,'FLMV_exact')
    check(c**(-4)<best,'FLMV_tail')

check(RAW['summary']['tested']==len(RAW['cases']),'summary_count')
for key,field in [('total_output_queries','output_queries'),('total_setup_reads','setup_reads'),('total_source_bit_reads','output_source_reads'),('total_index_one_writes','index_one_writes'),('total_directory_checks','directory_sequential_entry_checks'),('total_index_head_moves','index_head_moves'),('total_index_primitives','declared_index_primitives')]:
    check(RAW['summary'][key]==sum(row[field] for row in RAW['cases']),f'summary_{key}')
out={'run':'ARC294','result':'PASS','independent':True,'certified_source_replay':'SAT/UNSAT certificate separately replayed as ARC293','assertions':sum(checks.values()),'counts':dict(checks)}
(P/'arc_virtual_cofactor294_independent.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='counts'},indent=2))
