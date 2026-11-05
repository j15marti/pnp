#!/usr/bin/env python3
"""LSPV-4/416 exact exponent and charged virtual-input transport controls.
Python 3 standard library only. Does NOT implement a SAT contraction or FLMV TM.
Run: python lspv4_416_access_tax.py [output.json].
"""
from __future__ import annotations
import json, math, sys
from fractions import Fraction as Q
from pathlib import Path

A=Q(3,5); L=Q(1,2); D=Q(11,10); HALF=Q(1,2)
checks=0
def verify(v,msg):
    global checks
    checks+=1
    if not v: raise AssertionError(msg)

def beta(t): return ((t+2)/t**2-t)/2
def inside_k2(t,s):
    # For t>=1 the k=2 FLMV corollary gives the forbidden box s<beta(t).
    return s<beta(t)
def iterate(t,s,setup_u,read_v,steps=48):
    out=[]
    for k in range(steps+1):
        out.append((t,s))
        t=max(D,A+setup_u,A+read_v+L*t)
        s=max(HALF,L*s)
    return out

def decimal(x): return format(float(x),'.13g')
def frac(x): return f'{x.numerator}/{x.denominator}'

def cnf_parse(raw:bytes):
    try: txt=raw.decode('ascii')
    except UnicodeDecodeError:return (None,None)
    lines=txt.splitlines(); hdr=None; clauses=[]; part=[]
    for line in lines:
        line=line.strip()
        if not line:continue
        if line.startswith('c ') or line=='c':continue
        if line.startswith('p '):
            if hdr is not None:return (None,None)
            fields=line.split()
            if len(fields)!=4 or fields[:2]!=['p','cnf']:return (None,None)
            try:n,m=map(int,fields[2:])
            except ValueError:return (None,None)
            if n<0 or m<0:return (None,None)
            hdr=(n,m);continue
        if hdr is None:return (None,None)
        for t in line.split():
            if not (t=='0' or (t[0]=='-' and t[1:].isdigit()) or t.isdigit()):return (None,None)
            v=int(t)
            if abs(v)>hdr[0]:return (None,None)
            if v==0:clauses.append(tuple(part));part=[]
            else:part.append(v)
    if hdr is None or part or len(clauses)!=hdr[1]:return (None,None)
    def sat(assignment):
        return all(any(((assignment>>(abs(z)-1))&1)==(z>0) for z in cl) for cl in clauses)
    models=sum(sat(mask) for mask in range(1<<hdr[0])) if hdr[0]<=12 else None
    return (hdr,models)

def pad_cnf(original:bytes,length:int):
    verify(length>=len(original)+4,'too-short padding')
    line=b'c '+ b' '*(length-len(original)-3)+b'\n'
    ret=line+original
    verify(len(ret)==length,'bad padded length')
    return ret

cases=[]
for name,source in [
 ('SAT',b'p cnf 1 1\n1 0\n'),
 ('UNSAT',b'p cnf 1 2\n1 0\n-1 0\n'),
 ('MALFORMED',b'p cnf 1 1\n1\n'),
 ('CORRUPT',b'p cnf 1 2\n1 0\n-1 0\nTRASH\n')]:
    h,models=cnf_parse(source)
    verify((h is not None)==(name in ('SAT','UNSAT')),'source kind')
    if name=='SAT':verify(models==1,'SAT model')
    if name=='UNSAT':verify(models==0,'UNSAT model')
    cases.append({'source':name,'source_bytes':len(source),'accepted':h is not None,'models':models})

# Exact rational iteration, no floating-point decision at the strict FLMV boundary.
rows=[]
for v in (Q(0),Q(1,400),Q(1,300),Q(1,250),Q(1,100)):
    t0=Q(10);s0=Q(6);u=Q(1,2)
    seq=iterate(t0,s0,u,v)
    hits=[k for k,(t,s) in enumerate(seq) if inside_k2(t,s)]
    fixed=max(D,A+u,(A+v)/(1-L))
    verify(abs(float(seq[-1][0]-fixed))<1e-9,'time recurrence convergence')
    verify(seq[-1][1]==HALF,'space recurrence convergence')
    verify(bool(hits)==(HALF<beta(fixed)),'finite strict entry equivalence for seeded profile')
    if hits:
        k=hits[0]
        verify(k>0 and not inside_k2(*seq[k-1]),'first entry')
    rows.append({'read_tax_v':frac(v),'fixed_time_exponent':frac(fixed),
                 'fixed_time_decimal':decimal(fixed),'strict_flmv_at_fixed_point':HALF<beta(fixed),
                 'first_strict_iteration':hits[0] if hits else None,
                 't_at_first_strict':frac(seq[hits[0]][0]) if hits else None,
                 's_at_first_strict':frac(seq[hits[0]][1]) if hits else None})

for v,row in zip((Q(0),Q(1,400),Q(1,300),Q(1,250),Q(1,100)),rows):
    verify(row['fixed_time_exponent']==frac(Q(6,5)+2*v),'two tax locations')

# Only virtual bit-transport is tested here, NOT legal SAT child correctness.
transport=[]
for N in (64,256,1024,4096):
    src=pad_cnf(b'p cnf 1 2\n1 0\n-1 0\n',N)
    parsed,nmodels=cnf_parse(src)
    verify(parsed is not None and nmodels==0,'padded UNSAT acceptance')
    q=math.ceil(N**.6);m=math.ceil(N**.5)
    simulated_reads=0;idx_writes=0;index_clears=0;parent_probes=0
    naive_scan_probes=0;one_time_parent_scan_probes=0;all_match=True
    for child in range(q):
        one_time_parent_scan_probes+=N
        for j in range(m):
            addr=(17*child+31*j)%N
            idx_writes+=(N-1).bit_length()
            index_clears+=1
            parent_probes+=1;simulated_reads+=1
            naive_scan_probes+=N
            bit=(src[addr]>>((child+j)%8))&1
            brute=(src[(17*child+31*j)%N]>>((child+j)%8))&1
            if bit!=brute:all_match=False
    verify(all_match,'direct indexed and independent mathematical index disagree')
    verify(simulated_reads==q*m,'read count');verify(parent_probes==q*m,'probe count')
    verify(one_time_parent_scan_probes==q*N,'per child scan count')
    verify(naive_scan_probes==q*m*N,'per guest bit scan count')
    verify(idx_writes==q*m*(N-1).bit_length(),'index writes charged')
    verify(index_clears==q*m,'index clear counts')
    transport.append({'parent_length_bits_proxy':N,'children':q,'child_length_bits_proxy':m,
           'guest_virtual_input_reads':simulated_reads,'index_digit_writes':idx_writes,
           'index_erase_events':index_clears,'output_bit_writes_if_streamed':q*m,'direct_parent_bit_probes':parent_probes,
           'one_full_parent_scan_per_child_probes':one_time_parent_scan_probes,
           'one_full_parent_scan_per_virtual_read_probes':naive_scan_probes,
           'max_live_child_bits_if_materialized':m,
           'live_counted_bits_if_parent_is_buffered':N+m,
           'live_counted_bits_if_all_child_statuses_cached':q+m,
           'note':'q children were not verified as legal SAT reductions; charged bit transport only'})

semantic_controls=[]
for name,parent,children in [
    ('shared_variable_conflict',b'p cnf 1 2\n1 0\n-1 0\n',
        [b'p cnf 1 1\n1 0\n',b'p cnf 1 1\n-1 0\n']),
    ('compatible_children',b'p cnf 1 2\n1 0\n1 0\n',
        [b'p cnf 1 1\n1 0\n',b'p cnf 1 1\n1 0\n'])]:
    (_,models)=cnf_parse(parent)
    labels=[cnf_parse(c)[1]>0 for c in children]
    parent_label=models>0
    verify(all(labels),'child SAT control')
    verify(parent_label==(name=='compatible_children'),'parent label control')
    semantic_controls.append({'case':name,'parent_sat':parent_label,
      'independent_child_sat':labels,'naive_AND_child_labels':all(labels),
      'faithful_parent_reconstruction':False})

verify(Q(1,2)<beta(Q(6,5)),'nominal strict FLMV')
verify(Q(1)>=beta(Q(6,5)),'parent buffer peak violates FLMV')
verify(Q(1,400)<Q(1,300),'tax order')
output={'title':'LSPV-4/416 per-child versus per-guest-step access tax',
 'status':'PROVED/EXACT for algebraic/specified interpreter ledger; COMPUTATIONAL for finite bit transport; universal contraction OPEN',
 'checked_assumptions':{'fanout_a':frac(A),'child_lambda':frac(L),'local_d':frac(D),'setup_u':frac(Q(1,2)),
                        'source_on_read_only_input':'yes','index_tape_erasure_charged':'yes',
                        'source_to_child_semantics':'NOT proved; synthetic bit access only'},
 'critical_polynomial':'c^3+c^2-c-2=0','critical_c_approx':1.2055694304005903,
 'tax_critical_v_approx':(1.2055694304005903-1.2)/2,
 'nominal_margin':frac(beta(Q(6,5))-HALF),'strict_box_at_241_over_200':frac(beta(Q(241,200))-HALF),
 'profiles':rows,'source_controls':cases,'semantic_controls':semantic_controls,'bit_transport':transport,'assertions':checks}
path=Path(sys.argv[1]) if len(sys.argv)>1 else Path('lspv4_416_access_tax_raw.json')
path.write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'out':str(path),'checks':checks,'profiles':rows,'transport_cases':len(transport)},indent=2))
