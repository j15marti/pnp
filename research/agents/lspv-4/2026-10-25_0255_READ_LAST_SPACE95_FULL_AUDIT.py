#!/usr/bin/env python3
"""Cofactor-space95: finite logical audit, NOT a physical TM meter.
Read-only source plus one virtual last-bit override. Stdlib only.
"""
from itertools import product
import random, json, hashlib

SEED=202610250336
rng=random.Random(SEED)
checks=0

def verify(ok, msg):
    global checks
    checks += 1
    if not ok: raise AssertionError(f"check {checks}: {msg}")

def encode(n, clauses):
    assert 1 <= n <= 127 and len(clauses) < 256
    out=f'{n:08b}{len(clauses):08b}'
    for clause in clauses:
        assert 1<=len(clause)<=3
        out+=f'{len(clause):02b}'
        for lit in list(clause)+[0]*(3-len(clause)):
            if lit:
                assert abs(lit)<=n
                out+=f'{abs(lit):07b}'+('1' if lit<0 else '0')
            else: out+='00000000'
    return tuple(int(x) for x in out)

def from_reader(nbits, get):
    if nbits<16 or (nbits-16)%26: return None
    bits=lambda start,size:sum(get(start+i) << (size-1-i) for i in range(size))
    nv=bits(0,8); mc=bits(8,8)
    if nv<1 or nv>127 or mc != (nbits-16)//26: return None
    clauses=[]
    for j in range(mc):
        p=16+26*j; length=bits(p,2)
        if length<1 or length>3:return None
        row=[]
        for i in range(3):
            a=bits(p+2+8*i,7); neg=get(p+2+8*i+7)
            if i<length:
                if not 1<=a<=nv:return None
                row.append(-a if neg else a)
            elif a!=0 or neg:return None
        clauses.append(tuple(row))
    return nv,tuple(clauses)

def brute(n,clauses):
    for mask in range(1<<n):
        if all(any((((mask >> (abs(l)-1)) & 1) != (l<0)) for l in c) for c in clauses):
            return 1
    return 0

def solve_from_bits(nbits, getter):
    item=from_reader(nbits, getter)
    if item is None:return 0,'REJECT'
    n,clauses=item
    # Rule selection uses only decoded syntax, not the true SAT/UNSAT label.
    if all(len(c)<=2 for c in clauses): policy='2CNF'
    elif all(sum(l>0 for l in c)<=1 for c in clauses):policy='HORN'
    else:policy='GENERAL_OR_AFFINE'
    return brute(n,clauses),policy

class Tape:
    def __init__(self, data):
        self.data=data;self.N=len(data);self.read_count=0;self.seen=set();self.last_seen=False;self.last_first_at=None
    def read(self,i):
        assert 0<=i<self.N
        self.read_count+=1
        if i==self.N-1 and not self.last_seen:
            self.last_seen=True
            self.last_first_at=self.read_count
        self.seen.add(i)
        return self.data[i]

def compiler(tape):
    N=tape.N
    assert N>=1
    # All N-1 bits acquired with no persistent source-dependent array.
    for i in range(N-1): tape.read(i)
    verify((N-1) not in tape.seen and len(tape.seen)==N-1,'withheld until final read')
    pre=[];policies=[]
    for b in (0,1):
        def virtual_get(i, override=b):
            return override if i==N-1 else tape.read(i)
        ans,policy=solve_from_bits(N,virtual_get)
        pre.append(ans);policies.append(policy)
        verify(not tape.last_seen,'no withheld source read while computing cofactors')
    before=tape.read_count
    last=tape.read(N-1)
    verify(tape.last_first_at==before+1 and len(tape.seen)==N,'complete coverage on final source read')
    result=pre[last]
    # Post-coverage logical actions are: cached selector, output bit, halt.
    return result,tuple(pre),policies,3, before+1


def core_pair():
    allclauses=[]
    for signs in product((-1,1),repeat=3):
        if signs==(1,1,1):continue
        allclauses.append(tuple(signs[i]*(i+1) for i in range(3)))
    allclauses.append((1,2,3))
    u=encode(3,allclauses)
    v=u[:-1]+(1,) # Last sign only (z negative) creates duplicate -> SAT
    assert u[-1]==0
    return u,v

cases=[]
def add(tag,n,clauses):cases.append((tag,encode(n,clauses)))
add('2CNF_SAT',2,[(1,2),(-1,2)])
add('2CNF_UNSAT',2,[(1,2),(-1,2),(1,-2),(-1,-2)])
add('HORN_SAT',3,[(-1,2),(-2,3)])
add('HORN_UNSAT',2,[(1,),(-1,)])
add('HORN_3_SAT',3,[(-1,-2,3)])
add('HORN_3_UNSAT',3,[(-1,-2,3),(1,),(2,),(-3,)])
add('CONNECTED_EASY',6,[(1,2,3),(-1,4,5),(1,-4,6)])
add('DISCONNECTED_EASY',6,[(1,2,3),(4,5,6)])
add('PADDED_SAT',6,[(1,2,3),(4,5,6),(4,5,6)])
add('AFFINE_XOR_SAT',3,[(1,2,3),(1,-2,-3),(-1,2,-3),(-1,-2,3)])
u,v=core_pair()
cases.extend([('MATCHED_UNSAT',u),('MATCHED_SAT',v)])
for index in range(160):
    n=rng.randint(3,7);m=rng.randint(1,11)
    clauses=[]
    for _ in range(m):
        arity=rng.randint(1,3)
        inds=rng.sample(range(1,n+1),arity)
        clauses.append(tuple(a * rng.choice((-1,1)) for a in inds))
    cases.append(('RANDOM_'+str(index),encode(n,clauses)))

stats={'total':0,'sat':0,'unsat':0,'reject':0,'max_real_input_reads':0,'max_nbits':0,'max_cofactor_real_reads':0,'policies':{},'controls':{},'source_copy_bits':0}
for tag,x in cases:
    N=len(x)
    a,policy=solve_from_bits(N,lambda i:x[i]);verify(a in (0,1),'reference decider total')
    tape=Tape(x)
    got,pair,policies,post,reads_to_coverage=compiler(tape)
    verify(got==a,f'final label {tag}')
    verify(tape.read_count==reads_to_coverage,f'no additional reads after coverage {tag}')
    verify(tape.read_count <= N + 2*N, f'basic two-simulation read ceiling {tag}')
    verify(post<=3,f'constant post-coverage logical work {tag}')
    # The last-bit pair is a different *ordinary* bitstring of the same length.
    flipped=x[:-1]+(1-x[-1],)
    a_flipped,_=solve_from_bits(N,lambda i:flipped[i]);verify(pair[1-x[-1]]==a_flipped,'other cofactor')
    stats['total']+=1;stats['sat']+=a;stats['unsat']+=1-a
    if policy=='REJECT':stats['reject']+=1
    stats['max_nbits']=max(stats['max_nbits'],N)
    stats['max_real_input_reads']=max(stats['max_real_input_reads'],tape.read_count)
    stats['max_cofactor_real_reads']=max(stats['max_cofactor_real_reads'],tape.read_count-N)
    stats['policies'][policy]=stats['policies'].get(policy,0)+1
    if not tag.startswith('RANDOM'):stats['controls'][tag]={'label':'SAT' if a else 'UNSAT','other_cofactor':'SAT' if a_flipped else 'UNSAT','N':N,'physical_reads':tape.read_count,'cofactors':pair,'policy':policy}
verify(solve_from_bits(len(u),lambda i:u[i])[0]==0,'matched UNSAT')
verify(solve_from_bits(len(v),lambda i:v[i])[0]==1,'matched SAT')
verify(u[:-1]==v[:-1] and len(u)==len(v),'one-bit matched pair')
stats['assertions']=checks
stats['seed']=SEED
stats['status']='PASS'
stats['scope']='finite Python bit-query traces, not FLMV physical machine instructions'
print(json.dumps(stats,indent=2,sort_keys=True))
