#!/usr/bin/env python3
"""Reproducible two-level bitstream access and exact FLMV rational margins.
Finite controls only, not an SAT-to-M22 reduction or physical TM counts.
"""
from fractions import Fraction as F
import json,math,itertools
C=F(241,200)
B=F(11642479,23232400)
def case(name,a1,a2,t,s,g1=F(0),g2=F(0),d1=F(0),d2=F(0)):
    a=a1*a2
    time=a*t+g1+a1*g2
    space=max(a*s,d1,a1*d2)
    return dict(name=name,a=str(a),time=str(time),time_decimal=float(time),space=str(space),space_decimal=float(space),inside_strict_box=(time<C and space<B),time_margin=str(C-time),space_margin=str(B-space))
class Source:
    def __init__(self,bits):self.bits=bits;self.calls=0
    def __len__(self):return len(self.bits)
    def get(self,j):
        assert 0<=j<len(self.bits)
        self.calls+=1
        return self.bits[j]
class Twice:
    def __init__(self,p):self.p=p
    def __len__(self):return 2*len(self.p)
    def get(self,j):
        assert 0<=j<len(self)
        return self.p.get(j%len(self.p))
class PaddedReverse:
    def __init__(self,p):self.p=p
    def __len__(self):return 2+2*len(self.p)
    def get(self,j):
        assert 0<=j<len(self)
        if j<2:return '0'
        m=len(self.p)
        if j<2+m:return self.p.get(j-2)
        return self.p.get(m-1-(j-2-m))
def materialized(s):return '00'+s+s[::-1]
checks=0
queries=0
source_reads=0
sizes=[]
for n in range(1,9):
    for bits_tuple in itertools.product('01',repeat=n):
        inp=''.join(bits_tuple)
        x=Source(inp);one=Twice(x);two=PaddedReverse(one)
        target=materialized(inp+inp)
        assert len(two)==4*n+2
        for j in range(len(two)):
            assert two.get(j)==target[j]
            checks+=1
        assert ''.join(two.get(2+j) for j in range(n))==inp
        checks+=n
        assert x.calls==(len(two)-2)+n
        checks+=1
        queries+=len(two)+n
        source_reads+=x.calls
    sizes.append(dict(n=n,sources=2**n,output_bits=4*n+2))
y_pos=['123','145','246','356'];y_neg=['124','136','235','456']
y_clauses=[tuple(int(c) for c in x) for x in y_pos]+[tuple(-int(c) for c in x) for x in y_neg]
def sat(clauses,n):
    return any(all(any((a[v-1] if lit>0 else not a[v-1]) for lit in cl for v in [abs(lit)]) for cl in clauses) for a in itertools.product((False,True),repeat=n))
assert sat(y_clauses,6)
u_clauses=[(1,),(-1,)]
assert not sat(u_clauses,1)
for clauses,label in [(y_clauses,True),(u_clauses,False)]:
    as_bits=''.join(format(b,'08b') for b in str(clauses).encode('utf-8'))
    x=Source(as_bits);two=PaddedReverse(Twice(x))
    assert ''.join(two.get(2+j) for j in range(len(x)))==as_bits
    assert sat(clauses,max(abs(v) for cl in clauses for v in cl))==label
    checks+=len(x)+1
f_cases=[
  case('ideal_local_layers',F(1),F(1),F(6,5),F(1,2)),
  case('size_power_1003_per_1000',F(1003,1000),F(1),F(6,5),F(1,2)),
  case('two_size_power_101_per_100',F(101,100),F(101,100),F(6,5),F(1,2)),
  case('one_percent_accessor_work',F(1),F(1),F(6,5),F(1,2),g1=F(1,100)),
  case('two_0_001_accessor_costs',F(1),F(1),F(6,5),F(1,2),g1=F(1,1000),g2=F(1,1000))]
assert [i['inside_strict_box'] for i in f_cases]==[True,False,False,False,True]
assert B>F(1,2)
assert F(1)>B
out=dict(status='COMPUTATIONAL exact fraction and finite bitstream checks; not an SAT-to-M22 reduction',
 flmv_time=str(C),flmv_space=str(B),flmv_space_decimal=float(B),
 admissible_size_multiplier_if_target_is_1p2_halfspace=dict(
 time=str(C/F(6,5)),space=str(B/F(1,2)),limiting='space'),
 sparse_sat_time_upper_base=1.1199**2,
 sparse_sat_log2_time_coefficient=math.log2(1.1199**2),
 sparse_sat_guaranteed_exhaustive_saving_coeff=1-math.log2(1.1199**2),
 scenarios=f_cases,queries_checked=queries,source_reads=source_reads,assertions=checks,sizes=sizes,
 controls=['Y in canonical Cstar SAT', 'ordinary unit-clause pair UNSAT (outside Cstar)'],
 caveats=['Toy bitstream adapters are not SAT-preserving grammar reductions',
 'Python counters are not counted FLMV machine steps or flips',
 'Space exponent bridge requires an actual uniform indexed random-access implementation'])
print(json.dumps(out,sort_keys=True,indent=2))
